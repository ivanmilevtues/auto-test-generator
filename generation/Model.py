import openai
import os
import re
import ast
import time


class Model:
    def __init__(self):
        self.line_regex = r"line (\d+)"
        self.original_prompt = None
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_test(self, prompt):
        self.original_prompt = prompt
        completion = self.complete(self.original_prompt)
        code_with_test = self.complete_test(completion)
        code_with_test = self.__compile_code(code_with_test)
        return self.__get_only_generated_code(code_with_test)

    def complete(self, prompt, depth=2):
        try:
            if depth == 0:
                print(f"WARN: Couldn't generate code for {prompt}")
                return ""
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=prompt,
                temperature=0,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                echo=True,
                stop=["#"]
            )
            return response.choices[0]['text']
        except Exception as e:
            print(e)
            print("Sleeping for a minute to reduce rate limiting.")
            time.sleep(60)
            return self.complete(prompt, depth-1)

    def complete_test(self, code):
        generated_code = code[:len(self.original_prompt)]
        if 'assert' in generated_code:
            return code
        if 'test_' in generated_code:
            return self.complete(code + '\n# Generate asserts')
        return self.complete(code + f'\n# Generate test case method\n{4*" "}def test_')

    def __compile_code(self, code, depth=150):
        if depth == 0:
            print("Couldn't make compilable for code")
            return ""
        try:
            ast.parse(code)
            return code
        except SyntaxError as e:
            lines = code.split("\n")
            line_number = re.findall(self.line_regex, e.__str__())[0]
            lines.pop(int(line_number) - 1)
            return self.__compile_code("\n".join(lines), depth-1)
        except NameError as e:
            print("Name error: ", e)
            return code

    def __get_only_generated_code(self, code):
        return code[len(self.original_prompt):]
