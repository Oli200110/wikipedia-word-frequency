"""
Tests for the word frequency analyzer.
"""

import unittest
from wiki_word_freq.word_frequency import WordFrequencyAnalyzer


class TestWordFrequencyAnalyzer(unittest.TestCase):
    """Test cases for the WordFrequencyAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = WordFrequencyAnalyzer()

        # Sample data for testing
        self.sample_words = {
            "article1": [
                "apple",
                "banana",
                "apple",
                "cherry",
                "date",
                "apple",
                "banana",
            ],
            "article2": ["banana", "cherry", "date", "elderberry", "fig", "grape"],
        }

    def test_calculate_word_frequencies_basic(self):
        """Test basic word frequency calculation."""
        result = self.analyzer.calculate_word_frequencies(self.sample_words)

        # Expected word counts
        expected_counts = {
            "apple": 3,
            "banana": 3,
            "cherry": 2,
            "date": 2,
            "elderberry": 1,
            "fig": 1,
            "grape": 1,
        }

        # Expected word frequencies (percentages)
        total_words = sum(expected_counts.values())
        expected_frequencies = {
            word: (count / total_words) * 100 for word, count in expected_counts.items()
        }

        self.assertEqual(result["word_count"], expected_counts)

        # Check frequencies with a small tolerance for floating-point differences
        for word, freq in result["word_frequency"].items():
            self.assertAlmostEqual(freq, expected_frequencies[word], places=5)

    def test_calculate_word_frequencies_with_ignore_list(self):
        """Test word frequency calculation with an ignore list."""
        ignore_list = ["apple", "banana"]
        result = self.analyzer.calculate_word_frequencies(
            self.sample_words, ignore_list=ignore_list
        )

        # Expected word counts (without ignored words)
        expected_counts = {
            "cherry": 2,
            "date": 2,
            "elderberry": 1,
            "fig": 1,
            "grape": 1,
        }

        # Expected word frequencies (percentages)
        total_words = sum(expected_counts.values())
        expected_frequencies = {
            word: (count / total_words) * 100 for word, count in expected_counts.items()
        }

        self.assertEqual(result["word_count"], expected_counts)

        # Check frequencies with a small tolerance for floating-point differences
        for word, freq in result["word_frequency"].items():
            self.assertAlmostEqual(freq, expected_frequencies[word], places=5)

    def test_calculate_word_frequencies_with_percentile(self):
        """Test word frequency calculation with percentile filtering."""
        # Set a percentile to exclude the least frequent words
        percentile = 50  # This should exclude words with count 1
        result = self.analyzer.calculate_word_frequencies(
            self.sample_words, percentile=percentile
        )

        # Expected word counts (only words with count > 1)
        expected_counts = {"apple": 3, "banana": 3, "cherry": 2, "date": 2}

        # Expected word frequencies (percentages)
        total_words = sum(expected_counts.values())
        expected_frequencies = {
            word: (count / total_words) * 100 for word, count in expected_counts.items()
        }

        self.assertEqual(result["word_count"], expected_counts)

        # Check frequencies with a small tolerance for floating-point differences
        for word, freq in result["word_frequency"].items():
            self.assertAlmostEqual(freq, expected_frequencies[word], places=5)

    def test_calculate_word_frequencies_empty_input(self):
        """Test word frequency calculation with empty input."""
        result = self.analyzer.calculate_word_frequencies({})

        self.assertEqual(result["word_count"], {})
        self.assertEqual(result["word_frequency"], {})


if __name__ == "__main__":
    unittest.main()
