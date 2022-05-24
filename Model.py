import openai
import os
import re

from model.message_preparation import MessageBuilder
from history_scanner.GitHistoryDataSetParser import GitHistoryDataSetParser


class Model:
    def __init__(self):
        self.line_regex = r"line (\d+)"
        self.prompt = None
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def create_test(self, prompt):
        self.prompt = prompt
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt=f"{prompt}",
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            echo=True,
            stop=["#"]
        )
        completion_text = response.choices[0]["text"]
        return self.__compile_code(completion_text)

    def __compile_code(self, code, depth=150):
        if depth == 0:
            print("WARN: couldn't make compilable for code")
            return ""
        try:
            exec(code)
            return self.__get_only_generated_code(code)
        except SyntaxError as e:
            lines = code.split("\n")
            line_number = re.findall(self.line_regex, e.__str__())[0]
            lines.pop(int(line_number) - 1)
            return self.__compile_code("\n".join(lines), depth-1)
        except NameError as e:
            print("Name error: ", e)
            print(code)

    def __get_only_generated_code(self, code):
        return code[len(self.prompt):]


def main():
    parser = GitHistoryDataSetParser("./")
    data = parser.load_data("history_scanner/test_save.dat")
    messages = MessageBuilder(data)
    model = Model()
    for message in messages.create_prompt():
        test = model.create_test(message)
        print(f"""
        =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        Generated test for: {message}
        The test is:{test}
        """)


if __name__ == "__main__":
    main()
