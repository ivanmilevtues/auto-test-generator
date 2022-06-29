import ast


class CommitFile:
    def __init__(self, filename, source):
        self.filename = filename
        self.source = source
        try:
            self.source_ast = ast.parse(source)
        except:
            self.source_ast = None
        self.related_source = []
        self.ranking_score = 0

    def relate_source(self, token, expr):
        self.related_source.append((token, expr))
        self.ranking_score += 1

    def rank_up(self):
        self.ranking_score += 1
