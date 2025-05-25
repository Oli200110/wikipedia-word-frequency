"""
Main module for the Wikipedia Word-Frequency Dictionary API.
"""

import uvicorn
from fastapi import FastAPI, HTTPException, Query

from wiki_word_freq.models import WordFrequencyResponse, KeywordsRequest
from wiki_word_freq.wikipedia import WikipediaClient
from wiki_word_freq.word_frequency import WordFrequencyAnalyzer

app = FastAPI(
    title="Wikipedia Word-Frequency Dictionary",
    description="An API for generating word-frequency dictionaries from Wikipedia articles.",
    version="0.1.0",
)

# Initialize the Wikipedia client and word frequency analyzer
wikipedia_client = WikipediaClient()
word_frequency_analyzer = WordFrequencyAnalyzer()


@app.get("/word-frequency", response_model=WordFrequencyResponse)
async def get_word_frequency(
    article: str = Query(
        ..., description="The title of the Wikipedia article to start from"
    ),
    depth: int = Query(
        0, description="The depth of traversal within Wikipedia articles", ge=0
    ),
):
    """
    Generate a word-frequency dictionary for a Wikipedia article and its linked articles.

    Args:
        article: The title of the Wikipedia article to start from.
        depth: The depth of traversal within Wikipedia articles.

    Returns:
        A word-frequency dictionary that includes the count and percentage frequency
        of each word found in the traversed articles.
    """
    try:
        # Traverse Wikipedia articles
        words_by_article = wikipedia_client.traverse_articles(article, depth)

        if not words_by_article:
            raise HTTPException(
                status_code=404,
                detail=f"Article '{article}' not found or no content available",
            )

        # Calculate word frequencies
        result = word_frequency_analyzer.calculate_word_frequencies(words_by_article)

        return WordFrequencyResponse(
            word_count=result["word_count"], word_frequency=result["word_frequency"]
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/keywords", response_model=WordFrequencyResponse)
async def get_keywords(request: KeywordsRequest):
    """
    Generate a filtered word-frequency dictionary for a Wikipedia article and its linked articles.

    Args:
        request: The request body containing article, depth, ignore_list, and percentile.

    Returns:
        A word-frequency dictionary that includes the count and percentage frequency
        of each word found in the traversed articles, excluding words in the ignore list
        and filtered by the specified percentile.
    """
    try:
        # Traverse Wikipedia articles
        words_by_article = wikipedia_client.traverse_articles(
            request.article, request.depth
        )

        if not words_by_article:
            raise HTTPException(
                status_code=404,
                detail=f"Article '{request.article}' not found or no content available",
            )

        # Calculate word frequencies with filtering
        result = word_frequency_analyzer.calculate_word_frequencies(
            words_by_article,
            ignore_list=request.ignore_list,
            percentile=request.percentile,
        )

        return WordFrequencyResponse(
            word_count=result["word_count"], word_frequency=result["word_frequency"]
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == "__main__":
    uvicorn.run("wiki_word_freq.main:app", host="0.0.0.0", port=8000, reload=True)
