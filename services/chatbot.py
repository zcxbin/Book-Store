import os

import openai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('OPENAI_API_KEY')


def gpt_response(message: str, db, book_service):
    # Lấy danh sách sách từ cơ sở dữ liệu
    books = book_service.get_all_books(db)
    if books:
        books_list = [f"{book.title} by {book.authors.author_name}" for book in books]
        # Chuẩn bị ngữ cảnh dữ liệu cho chatbot
        books_data = ", ".join(books_list)
    else:
        books_data = "No books"
    # Thêm thông tin khuyến mãi
    promotions_info = """
    Các ưu đãi hiện có:
    - 
    - 
    - 
    """

    context = f"""
    Danh sách sách hiện có trong cửa hàng:
    {books_data}

    {promotions_info}
    trong câu trả lời nếu có \n thay \n bằng \", \"
    Nếu không có sách nào trong cửa hàng thì trả lời là hiện tại không có cuốn sách nào được bày bán tại cửa hàng!
    '.
    """

    # Gọi API OpenAI để chatbot trả lời
    openai.api_key = API_KEY
    response = openai.ChatCompletion.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": context},
            {"role": "user", "content": message}
            ]
        )

    return response.choices[0].message["content"]
