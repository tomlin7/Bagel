from CodeAnalysis.parser import Parser


class SyntaxTree:
    def __init__(self, diagnostics, root, end_of_file_token):
        self._diagnostics = diagnostics
        self._root = root
        self._end_of_file_token = end_of_file_token

    @property
    def diagnostics(self):
        return self._diagnostics

    @property
    def root(self):
        return self._root

    @property
    def end_of_file_token(self):
        return self._end_of_file_token

    @staticmethod
    def parse(text):
        parser = Parser(text)
        return parser.parse()
