from groq import Groq

key = "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"


import openai

from groq import Groq
import pandas as pd

# client = Groq(
#     api_key=key,
# )
# completion = client.chat.completions.create(
#     model="deepseek-r1-distill-llama-70b",
#     messages=[
#         {
#             "role": "user",
#             "content": """
#              You are a helpful assistant, who generates a list of 30 information LLM models

#              output json format:
#                 {
#                 "data":[
#                     {
#                         "model name": "Title of the information",
#                         "description": "Description of the information",
#                         "release date": "",
#                         "context length": "Context length of the information",
#                     },
#                     ...
#                 ]}
# """
#         }
#     ],
#     temperature=0.6,
#     response_format={ "type": "json_object" },
#     max_completion_tokens=4096,
#     top_p=0.95,
#     stream=False,
#     stop=None,
# )

# print(completion.choices[0].message.content)
class ExcelAgent:
    def __init__(self, excel_path, oaiclient):
        self.df = pd.read_excel(excel_path)
        self.oaiclient = oaiclient

    def ask(self, question):
        # Convert the entire DataFrame to JSON (may be large!)
        all_data = self.df.to_dict(orient="records")
        prompt = f"""You are an assistant with access to the following Excel data (all rows shown as JSON):
{all_data}

Answer the following question based on the data above:
Question: {question}
Answer:"""
        response = self.oaiclient.chat.completions.create(
            model="deepseek-r1-distill-llama-70b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=512,
        )
        return response.choices[0].message.content

# Example usage:
# agent = ExcelAgent("/path/to/your/file.xlsx", oaiclient)
# answer = agent.ask("What is the total sales for 2023?")
# print(answer)



if __name__ == "__main__":
    # Example usage:

    oaiclient = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=key
    )
    agent = ExcelAgent("./The Alex Ideas Report.xlsx", oaiclient)
    answer = agent.ask("What is the total sales for 2023?")
    print(answer)