"""
Tests for the Wikipedia client.
"""

import unittest
from unittest.mock import patch, MagicMock
from wiki_word_freq.wikipedia import WikipediaClient


class TestWikipediaClient(unittest.TestCase):
    """Test cases for the WikipediaClient class."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = WikipediaClient()

        # Sample HTML content for testing
        self.sample_html = """
        <div class="mw-parser-output">
            <p>This is a sample Wikipedia article about <a href="/wiki/Python">Python</a>.</p>
            <p>It contains links to <a href="/wiki/Programming">programming</a> and 
            <a href="/wiki/Computer_science">computer science</a>.</p>
            <p>Some links are not articles: <a href="/wiki/File:Python_logo.png">Python logo</a> or 
            <a href="/wiki/Category:Programming_languages">Category</a>.</p>
            <p>External links like <a href="https://python.org">Python.org</a> should be ignored.</p>
        </div>
        """

    @patch("requests.Session.get")
    def test_get_article_content(self, mock_get):
        """Test fetching article content."""
        # Mock the API response
        mock_response = MagicMock()
        mock_response.json.return_value = {"parse": {"text": {"*": self.sample_html}}}
        mock_get.return_value = mock_response

        # Call the method
        result = self.client.get_article_content("Python")

        # Verify the API was called with the correct parameters
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs["params"]["page"], "Python")

        # Verify the result
        self.assertEqual(result, self.sample_html)

    @patch("requests.Session.get")
    def test_get_article_content_error(self, mock_get):
        """Test handling of errors when fetching article content."""
        # Mock the API response for an error
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "error": {"info": "The article does not exist."}
        }
        mock_get.return_value = mock_response

        # Verify that a ValueError is raised
        with self.assertRaises(ValueError):
            self.client.get_article_content("NonExistentArticle")

    def test_extract_wiki_links(self):
        """Test extracting Wikipedia links from HTML content."""
        links = self.client.extract_wiki_links(self.sample_html)

        # Verify the extracted links
        expected_links = ["Python", "Programming", "Computer_science"]
        self.assertEqual(set(links), set(expected_links))

    def test_extract_words(self):
        """Test extracting words from HTML content."""
        words = self.client.extract_words(self.sample_html)

        # Verify some of the extracted words
        expected_words = [
            "this",
            "is",
            "a",
            "sample",
            "wikipedia",
            "article",
            "about",
            "python",
        ]
        for word in expected_words:
            self.assertIn(word, words)

    @patch.object(WikipediaClient, "get_article_content")
    @patch.object(WikipediaClient, "extract_wiki_links")
    @patch.object(WikipediaClient, "extract_words")
    def test_traverse_articles(
        self, mock_extract_words, mock_extract_links, mock_get_content
    ):
        """Test traversing articles."""
        # Mock the dependencies
        mock_get_content.return_value = self.sample_html
        mock_extract_links.return_value = ["Python", "Programming"]
        mock_extract_words.return_value = ["python", "programming", "language"]

        # Call the method with depth 1
        result = self.client.traverse_articles("Python", 1)

        # Verify the result
        self.assertIn("Python", result)
        self.assertEqual(result["Python"], ["python", "programming", "language"])

        # Verify the dependencies were called
        mock_get_content.assert_called()
        mock_extract_links.assert_called()
        mock_extract_words.assert_called()

    @patch.object(WikipediaClient, "get_article_content")
    def test_traverse_articles_error(self, mock_get_content):
        """Test handling of errors when traversing articles."""
        # Mock the get_article_content method to raise a ValueError
        mock_get_content.side_effect = ValueError("Article not found")

        # Call the method
        result = self.client.traverse_articles("NonExistentArticle", 1)

        # Verify the result is an empty dictionary
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
