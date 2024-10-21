import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class AIService:
    def __init__(self):
        self.api_key = openai.api_key

    def suggest_book_from_description(self, user_message: str, book_list: list):
        prompt = f"""
        You are a helpful assistant. Based on the user's input, suggest up to 5 books from the given book list.
        Please return the result **ONLY** in JSON format with the fields "title" and "author". 
        Do not return any text outside the JSON object. If there is an issue, return an error message in this JSON format:
        {{
            "error": "error description"
        }}.
    
        User's input: "{user_message}"
    
        Available books: {', '.join([f'{{"title": "{book.title}", "author": "{book.authors.author_name}"}}' for book in book_list])}
        """

        response = openai.Completion.create(
            model = "text-davinci-003",
            prompt = prompt,
            max_tokens = 300,
            temperature = 0.7
            )

        return response.choices[0].text.strip()
