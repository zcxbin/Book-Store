import os

import openai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get('OPENAI_API_KEY')

def get_chatbot_service():
    try:
        yield ChatbotService()
    finally:
        pass

class ChatbotService:
    def gpt_response(self, message: str, db, book_service):
        # Lấy danh sách sách từ cơ sở dữ liệu
        books = book_service.get_all_books(db)
        if books:
            books_list = [f"{book.to_dict()}" for book in books]
            # Chuẩn bị ngữ cảnh dữ liệu cho chatbot
        else:
            books_list = "No books"
        # Thêm thông tin khuyến mãi
        promotions_info = """
        Hello
        Hello, hãy cho tôi 1 quyển sách -> bạn muốn đọc thể loại hay tác giả nào
        Khi nào hỏi 
                
        """

        context = f"""
        Danh sách sách hiện có trong cửa hàng: {books_list}.
        
        {promotions_info}
    
        # Yêu cầu: Khi khách hàng hỏi về danh sách sách, chỉ liệt kê tên sách và tên tác giả, không xuống dòng và không dùng ký tự đặc biệt. Nếu khách hàng yêu cầu thêm, cung cấp thông tin chi tiết hơn.
        Nếu chưa có gì trong ưu đãi thì trả lời là hiện tại chúng tôi không có chương trình khuyến mãi nào.
        khi nào hỏi đến đưa sách ra mới show list_book còn không thì cứ đối thoại bình thường 
        """

        # Gọi API OpenAI để chatbot trả lời
        openai.api_key = API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": message}
            ]
        )

        return response.choices[0].message["content"]
