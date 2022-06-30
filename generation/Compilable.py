import openai
import os


class Compilable:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    @staticmethod
    def fix_test(code):
        try:
            response = openai.Edit.create(
                model="code-davinci-edit-001",
                input=code,
                instruction="Fix compilation",
                temperature=0,
                top_p=1
            )
            return response['choices'][0]['text']
        except openai.error.InvalidRequestError as e:
            print("Couldn't edit this code")
            return code
