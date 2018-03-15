from more_itertools import peekable


class Chunker:
    def __init__(self, iterable, whitespace, special_tokens=(), end_tokens=()):
        self.iterator = peekable(iterable)
        self.end_tokens = tuple(end_tokens)

        self.whitespace = whitespace
        self.special_tokens = special_tokens + self.end_tokens

    def __iter__(self):
        """
        Yields tokens generated from input iterator

        Splits tokens based on whitespace characters, and on special_tokens,
        yielding special_tokens, but not whitespace

        Ends when the iterator is exhausted, or one of the end_tokens are reached
        """
        if "" in self.special_tokens:
            while self.iterator:
                yield ""
            return

        token = ""
        for char in self.iterator:
            if char in self.whitespace:
                if token:
                    yield token
                    token = ""
                continue

            token += char

            special_token = next((special_token for special_token in self.special_tokens if token.endswith(special_token)), None)
            if special_token is not None:
                if token != special_token:
                    yield token[:len(token) - len(special_token)]
                token = ""

                yield special_token

            if special_token in self.end_tokens:
                return

        if token:
            yield token
