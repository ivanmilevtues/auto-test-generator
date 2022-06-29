import openai
import os
import re
import ast
import time


class Model:
    def __init__(self):
        self.line_regex = re.compile(r"line (\d+)")
        self.original_prompt = None
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_test(self, prompt):
        self.original_prompt = prompt
        completion = self.complete(self.original_prompt)
        completion = self.complete_test(completion)
        generated_code = self.__get_only_generated_code(completion)
        return generated_code

    def complete(self, prompt, depth=2):
        try:
            if depth == 0:
                print(f"WARN: Couldn't generate code for {prompt}")
                return ""
            response = openai.Completion.create(
                engine="code-davinci-002",
                prompt=prompt,
                temperature=0.64,
                max_tokens=256,
                frequency_penalty=0.66,
                presence_penalty=1.25,
                best_of=5,
                echo=True,
                stop=["#"]
            )
            return response.choices[0]['text']
        except Exception as e:
            print(e)
            print("Sleeping for a minute to reduce rate limiting.")
            time.sleep(60)
            return self.complete(prompt, depth - 1)

    def complete_test(self, code):
        generated_code = code[:len(self.original_prompt)]
        if 'assert' in generated_code:
            return code
        if 'test_' in generated_code:
            return self.complete(code + '\n# Generate asserts')
        return self.complete(code + f'\n# Generate test case method\n{4 * " "}def test_')

    def __compile_code(self, code, depth=10):
        if depth == 0:
            print("Couldn't make compilable for code")
            return code
        try:
            ast.parse(code)
            return code
        except SyntaxError as e:
            lines = code.split("\n")
            line_number = re.findall(r"line (\d+)", e.__str__())[0]
            print("Syntax Error:", line_number, e)
            lines.pop(int(line_number) - 1)
            return self.__compile_code("\n".join(lines), depth - 1)
        except NameError as e:
            print("Name error: ", e)
            return code
        except Exception as e:
            print("Code compilation error: ", e)
            return code

    def __get_only_generated_code(self, code):
        return code[len(self.original_prompt):]
