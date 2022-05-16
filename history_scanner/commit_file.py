import ast


class CommitFile:
    def __init__(self, filename, source):
        self.filename = filename
        self.source = source
        try:
            self.source_ast = ast.parse(source)
        except:
            self.source_ast = None
        self.ranking_score = 0

    def rank_up(self):
        self.ranking_score += 1
