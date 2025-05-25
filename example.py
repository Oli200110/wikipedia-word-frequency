"""
Example script demonstrating how to use the Wikipedia Word-Frequency Dictionary API.
"""

import requests
import json
import time

# Base URL for the API
BASE_URL = "http://localhost:8000"


def print_json(data):
    """Print JSON data in a readable format."""
    print(json.dumps(data, indent=2))


def main():
    # Start the server before running this script
    print(
        "Make sure the server is running (python run.py) before executing this script."
    )
    print("Waiting 2 seconds before making requests...")
    time.sleep(2)

    print("\n=== Example 1: GET /word-frequency ===")
    try:
        # Example 1: GET /word-frequency
        article = "Python_(programming_language)"
        depth = 0
        print(f"Fetching word frequency for article '{article}' with depth {depth}...")

        response = requests.get(
            f"{BASE_URL}/word-frequency", params={"article": article, "depth": depth}
        )
        response.raise_for_status()

        data = response.json()

        # Print the top 10 most frequent words
        print("\nTop 10 most frequent words:")
        sorted_words = sorted(
            data["word_frequency"].items(), key=lambda x: x[1], reverse=True
        )[:10]
        for word, frequency in sorted_words:
            print(f"  {word}: {frequency:.2f}%")

        print(f"\nTotal unique words: {len(data['word_count'])}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    print("\n=== Example 2: POST /keywords ===")
    try:
        # Example 2: POST /keywords
        request_data = {
            "article": "Python_(programming_language)",
            "depth": 0,
            "ignore_list": [
                "the",
                "and",
                "is",
                "in",
                "of",
                "to",
                "a",
                "for",
                "on",
                "with",
            ],
            "percentile": 80,
        }

        print(
            f"Fetching keywords for article '{request_data['article']}' with depth {request_data['depth']}..."
        )
        print(
            f"Ignoring common words and filtering to the top 20% most frequent words..."
        )

        response = requests.post(f"{BASE_URL}/keywords", json=request_data)
        response.raise_for_status()

        data = response.json()

        # Print the top 10 most frequent words
        print("\nTop 10 most frequent words after filtering:")
        sorted_words = sorted(
            data["word_frequency"].items(), key=lambda x: x[1], reverse=True
        )[:10]
        for word, frequency in sorted_words:
            print(f"  {word}: {frequency:.2f}%")

        print(f"\nTotal unique words after filtering: {len(data['word_count'])}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
