from nltk.translate.bleu_score import sentence_bleu
import pandas as pd
import re


class BLEUEvaluator:
    def __init__(self):
        self.df = pd.DataFrame(columns=['commit-hash', 'BleuScore'])

    def evaluate(self, candidate, reference, commit_hash):
        if isinstance(reference, list):
            for ref in reference:
                self.evaluate(candidate, ref, commit_hash)
        reference_words = re.split(r"\s+", reference)
        candidate_words = re.split(r"\s+", candidate)
        score = sentence_bleu(reference_words, candidate_words, weights=(0.25, 0.25, 0.25, 0.25))
        self.df = self.df.append({'commit-hash': commit_hash, 'BleuScore': score}, ignore_index=True)

    def export(self, filename='bleu_score_evaluation.csv'):
        self.df.to_csv(filename)
