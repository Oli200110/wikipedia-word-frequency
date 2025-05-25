"""
Module for interacting with Wikipedia and traversing articles.
"""

import re
import requests
from typing import Dict, List
from bs4 import BeautifulSoup
from urllib.parse import unquote


class WikipediaClient:
    """Client for fetching and processing Wikipedia articles."""

    BASE_URL = "https://en.wikipedia.org/wiki/"
    API_URL = "https://en.wikipedia.org/w/api.php"

    def __init__(self):
        """Initialize the Wikipedia client."""
        self.session = requests.Session()
        self.visited_articles = set()

    def get_article_content(self, article_title: str) -> str:
        """
        Fetch the content of a Wikipedia article.

        Args:
            article_title: The title of the Wikipedia article.

        Returns:
            The HTML content of the article.

        Raises:
            ValueError: If the article cannot be found.
        """
        # Replace spaces with underscores for URL
        article_title = article_title.replace(" ", "_")

        # Use the API to get the page content
        params = {
            "action": "parse",
            "page": article_title,
            "format": "json",
            "prop": "text",
            "redirects": True,
        }

        response = self.session.get(self.API_URL, params=params)
        data = response.json()

        if "error" in data:
            raise ValueError(
                f"Article '{article_title}' not found: {data['error']['info']}"
            )

        # Extract the HTML content
        html_content = data["parse"]["text"]["*"]
        return html_content

    def extract_wiki_links(self, html_content: str) -> List[str]:
        """
        Extract Wikipedia article links from HTML content.

        Args:
            html_content: The HTML content of a Wikipedia article.

        Returns:
            A list of Wikipedia article titles that are linked from the content.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        content_div = soup.find("div", {"class": "mw-parser-output"})

        if not content_div:
            return []

        links = []

        # Find all links in the content
        for link in content_div.find_all("a"):
            href = link.get("href", "")

            # Only consider internal Wikipedia article links
            if (
                    href.startswith("/wiki/")
                    and ":" not in href
                    and not href.startswith("/wiki/File:")
            ):
                # Extract the article title from the URL
                article_title = unquote(href.replace("/wiki/", ""))
                links.append(article_title)

        return links

    def extract_words(self, html_content: str) -> List[str]:
        """
        Extract words from the HTML content of a Wikipedia article.

        Args:
            html_content: The HTML content of a Wikipedia article.

        Returns:
            A list of words from the article content.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        content_div = soup.find("div", {"class": "mw-parser-output"})

        if not content_div:
            return []

        # Remove unwanted elements
        for element in content_div.select(
                "table, .reference, .mw-editsection, .mw-headline, script, style"
        ):
            element.extract()

        # Get the text content
        text = content_div.get_text()

        # Clean and normalize the text
        text = re.sub(r"\[\d+\]", "", text)  # Remove citation numbers
        text = re.sub(r"\s+", " ", text)  # Normalize whitespace

        # Split into words and filter out non-words
        words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

        return words

    def traverse_articles(self, start_article: str, depth: int) -> Dict[str, List[str]]:
        """
        Traverse Wikipedia articles starting from a given article up to a specified depth.

        Args:
            start_article: The title of the Wikipedia article to start from.
            depth: The depth of traversal.

        Returns:
            A dictionary mapping article titles to lists of words from those articles.
        """
        self.visited_articles = set()
        return self._traverse_recursive(start_article, depth)

    def _traverse_recursive(
            self, article: str, depth: int, current_depth: int = 0
    ) -> Dict[str, List[str]]:
        """
        Recursive helper method for traversing Wikipedia articles.

        Args:
            article: The current article title.
            depth: The maximum depth to traverse.
            current_depth: The current traversal depth.

        Returns:
            A dictionary mapping article titles to lists of words from those articles.
        """
        # Check if we've reached the maximum depth or already visited this article
        if current_depth > depth or article in self.visited_articles:
            return {}

        # Mark this article as visited
        self.visited_articles.add(article)

        try:
            # Get the article content
            html_content = self.get_article_content(article)

            # Extract words from the article
            words = self.extract_words(html_content)

            # Initialize the result with the current article
            result = {article: words}

            # If we haven't reached the maximum depth, traverse linked articles
            if current_depth < depth:
                # Extract links from the article
                links = self.extract_wiki_links(html_content)

                # Traverse each linked article
                for link in links:
                    # Skip already visited articles
                    if link in self.visited_articles:
                        continue

                    # Recursively traverse the linked article
                    linked_articles = self._traverse_recursive(
                        link, depth, current_depth + 1
                    )

                    # Add the results to our result dictionary
                    result.update(linked_articles)

            return result

        except ValueError:
            # If the article doesn't exist, return an empty result
            return {}
