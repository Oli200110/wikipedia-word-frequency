"""
Module for calculating word frequencies from a text.
"""

from collections import Counter
from typing import Dict, List, Optional
import numpy as np


class WordFrequencyAnalyzer:
    """Class for analyzing word frequencies in text."""

    def __init__(self):
        """Initialize the word frequency analyzer."""
        pass

    def calculate_word_frequencies(
        self,
        words_by_article: Dict[str, List[str]],
        ignore_list: Optional[List[str]] = None,
        percentile: int = 0,
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate word frequencies from a collection of words.

        Args:
            words_by_article: A dictionary mapping article titles to lists of words.
            ignore_list: A list of words to ignore in the frequency calculation.
            percentile: The percentile threshold for word frequency (0-100).
                        Words below this percentile will be excluded.

        Returns:
            A dictionary containing word counts and frequency percentages.
        """
        # Flatten the list of words from all articles
        all_words = []
        for words in words_by_article.values():
            all_words.extend(words)

        # Filter out words in the ignore list
        if ignore_list:
            ignore_set = set(word.lower() for word in ignore_list)
            all_words = [word for word in all_words if word.lower() not in ignore_set]

        # Count word occurrences
        word_counter = Counter(all_words)

        # Apply percentile filtering if specified
        if percentile > 0:
            counts = np.array(list(word_counter.values()))
            threshold = np.percentile(counts, percentile)
            word_counter = {
                word: count
                for word, count in word_counter.items()
                if count >= threshold
            }

        # Calculate total word count for frequency calculation
        total_words = sum(word_counter.values())

        # Calculate frequency percentages
        word_frequency = {}
        if total_words > 0:
            word_frequency = {
                word: (count / total_words) * 100
                for word, count in word_counter.items()
            }

        return {"word_count": dict(word_counter), "word_frequency": word_frequency}
