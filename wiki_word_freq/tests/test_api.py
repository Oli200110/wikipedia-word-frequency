"""
Tests for the API endpoints.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

from wiki_word_freq.main import app
from wiki_word_freq.wikipedia import WikipediaClient
from wiki_word_freq.word_frequency import WordFrequencyAnalyzer


class TestAPI(unittest.TestCase):
    """Test cases for the API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)

        # Sample data for mocking
        self.sample_words_by_article = {
            "Python": ["python", "programming", "language", "code", "python"],
            "Programming": ["code", "programming", "software", "development"],
        }

        self.sample_word_frequencies = {
            "word_count": {
                "python": 2,
                "programming": 2,
                "language": 1,
                "code": 2,
                "software": 1,
                "development": 1,
            },
            "word_frequency": {
                "python": 22.22,
                "programming": 22.22,
                "language": 11.11,
                "code": 22.22,
                "software": 11.11,
                "development": 11.11,
            },
        }

    @patch.object(WikipediaClient, "traverse_articles")
    @patch.object(WordFrequencyAnalyzer, "calculate_word_frequencies")
    def test_get_word_frequency(self, mock_calculate, mock_traverse):
        """Test the GET /word-frequency endpoint."""
        # Mock the dependencies
        mock_traverse.return_value = self.sample_words_by_article
        mock_calculate.return_value = self.sample_word_frequencies

        # Make the request
        response = self.client.get("/word-frequency?article=Python&depth=1")

        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["word_count"], self.sample_word_frequencies["word_count"])
        self.assertEqual(
            data["word_frequency"], self.sample_word_frequencies["word_frequency"]
        )

        # Verify the dependencies were called with the correct arguments
        mock_traverse.assert_called_once_with("Python", 1)
        mock_calculate.assert_called_once_with(self.sample_words_by_article)

    @patch.object(WikipediaClient, "traverse_articles")
    def test_get_word_frequency_article_not_found(self, mock_traverse):
        """Test the GET /word-frequency endpoint with a non-existent article."""
        # Mock the traverse_articles method to return an empty dictionary
        mock_traverse.return_value = {}

        # Make the request
        response = self.client.get("/word-frequency?article=NonExistentArticle&depth=1")

        # Verify the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("404", response.json()['detail'])
        self.assertIn("not found", response.json()["detail"])

    @patch.object(WikipediaClient, "traverse_articles")
    @patch.object(WordFrequencyAnalyzer, "calculate_word_frequencies")
    def test_post_keywords(self, mock_calculate, mock_traverse):
        """Test the POST /keywords endpoint."""
        # Mock the dependencies
        mock_traverse.return_value = self.sample_words_by_article
        mock_calculate.return_value = self.sample_word_frequencies

        # Request data
        request_data = {
            "article": "Python",
            "depth": 1,
            "ignore_list": ["code"],
            "percentile": 50,
        }

        # Make the request
        response = self.client.post("/keywords", json=request_data)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["word_count"], self.sample_word_frequencies["word_count"])
        self.assertEqual(
            data["word_frequency"], self.sample_word_frequencies["word_frequency"]
        )

        # Verify the dependencies were called with the correct arguments
        mock_traverse.assert_called_once_with("Python", 1)
        mock_calculate.assert_called_once_with(
            self.sample_words_by_article, ignore_list=["code"], percentile=50
        )

    @patch.object(WikipediaClient, "traverse_articles")
    def test_post_keywords_article_not_found(self, mock_traverse):
        """Test the POST /keywords endpoint with a non-existent article."""
        # Mock the traverse_articles method to return an empty dictionary
        mock_traverse.return_value = {}

        # Request data
        request_data = {"article": "NonExistentArticle", "depth": 1}

        # Make the request
        response = self.client.post("/keywords", json=request_data)

        # Verify the response
        self.assertEqual(response.status_code, 500)
        self.assertIn("404", response.json()['detail'])
        self.assertIn("not found", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
