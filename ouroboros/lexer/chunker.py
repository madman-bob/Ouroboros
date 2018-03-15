from more_itertools import peekable


class Chunker:
    def __init__(self, iterable, whitespace, special_lexemes=(), end_lexemes=()):
        self.iterator = peekable(iterable)
        self.end_lexemes = tuple(end_lexemes)

        self.whitespace = whitespace
        self.special_lexemes = special_lexemes + self.end_lexemes

    def __iter__(self):
        """
        Yields lexemes generated from input iterator

        Splits lexemes based on whitespace characters, and on special_lexemes,
        yielding special_lexemes, but not whitespace

        Ends when the iterator is exhausted, or one of the end_lexemes are reached
        """
        if "" in self.special_lexemes:
            while self.iterator:
                yield ""
            return

        lexeme = ""
        for char in self.iterator:
            if char in self.whitespace:
                if lexeme:
                    yield lexeme
                    lexeme = ""
                continue

            lexeme += char

            special_lexeme = next((special_lexeme for special_lexeme in self.special_lexemes if lexeme.endswith(special_lexeme)), None)
            if special_lexeme is not None:
                if lexeme != special_lexeme:
                    yield lexeme[:len(lexeme) - len(special_lexeme)]
                lexeme = ""

                yield special_lexeme

            if special_lexeme in self.end_lexemes:
                return

        if lexeme:
            yield lexeme
