import re

from app.config import settings


class ContentFilter:
    def __init__(self, inappropriate_words):
        self.inappropriate_words = inappropriate_words or settings.inappropriate_words
        self._compile_patterns()

    def _compile_patterns(self):
        patterns = []
        for word in self.inappropriate_words:
            pattern = r"\b" + re.escape(word.lower()) + r"\b"
            patterns.append(pattern)

        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]

    def check_content(self, content):
        """
        Checks if the content contains inappropriate words

        Args:
            content: Content to verify

        Returns:
            Tuple[bool, List[str]]: (is_appropriate, found_words)
        """
        if not content:
            return True, []

        found_words = []
        content_lower = content.lower()

        for pattern in self.patterns:
            if pattern.search(content_lower):
                matches = pattern.findall(content_lower)
                found_words.extend(matches)

        unique_found_words = list(dict.fromkeys(found_words))

        return len(unique_found_words) == 0, unique_found_words

    def filter_content(self, content, replacement):
        """
        Filters content by replacing inappropriate words

        Args:
            content: Content to filter
            replacement: Replacement text for inappropriate words

        Returns:
            str: Filtered content
        """
        if not content:
            return content

        filtered_content = content

        for pattern in self.patterns:
            filtered_content = pattern.sub(replacement, filtered_content)

        return filtered_content

    def get_content_metadata(self, content):
        """
        Gets content metadata

        Args:
            content: Message content

        Returns:
            dict: Content metadata
        """
        if not content:
            return {
                "length": 0,
                "word_count": 0,
                "character_count": 0,
                "has_inappropriate_content": False,
                "inappropriate_words": [],
            }

        words = content.split()
        word_count = len(words)

        character_count = len(content)

        is_appropriate, inappropriate_words = self.check_content(content)

        return {
            "length": len(content),
            "word_count": word_count,
            "character_count": character_count,
            "has_inappropriate_content": not is_appropriate,
            "inappropriate_words": inappropriate_words,
        }


content_filter = ContentFilter(settings.inappropriate_words)
