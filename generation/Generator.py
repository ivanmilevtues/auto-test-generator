from generation.CodeCleanser import CodeCleanser
from generation.Model import Model
from history_scanner.Prompt import Prompt


class Generator:
    def __init__(self, cleanser: CodeCleanser):
        self.model = Model()
        self.cleanser = cleanser

    def generate(self, prompt: Prompt):
        for prompt_str in prompt.to_prompts():
            test_code = self.model.generate_test(prompt_str)
            yield self.cleanser.cleanse_test(test_code)
