
import openai
import os
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import pipeline

from models.book import Book as BookModel
from models.author import Author as AuthorModel

load_dotenv()
hf_api_key = os.getenv("HUGGINGFACE_API_KEY")
login(hf_api_key)

generator = pipeline("text-generation", model="EleutherAI/gpt-neo-2.7B")

def suggest_book_from_description():
    prompt = """
            You are a helpful assistant. Based on the user's input, suggest up to 5 books from the given book list.
            Please return the result **ONLY** in JSON format with the fields "title" and "author". 
            Do not return any text outside the JSON object. If there is an issue, return an error message in this JSON format:
            {{
                "error": "error description"
            }}.

            User's input: "I like books about futuristic societies."

            Available books: [{{"title": "Dune", "author": "Frank Herbert"}}, {{"title": "1984", "author": "George Orwell"}}]
        """

    response = generator(prompt, max_length = 300, num_return_sequences = 1, temperature = 0.7)

    return response[0]["generated_text"].strip()

os.environ['HF_HUB_DISABLE_SYMLINKS_WARNING'] = 'true'
os.environ['HF_HOME'] = 'D:/huggingface_cache'
a = suggest_book_from_description()
print(a)
