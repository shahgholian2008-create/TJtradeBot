"""خواندن محتوای فایل‌های Word"""
import os
from docx import Document

CONTENTS_FOLDER = "contents"


def read_word_file(file_name: str):
    """
    خواندن محتوای یک فایل Word.
    خروجی: متن یا None اگر فایل نبود.
    """
    file_path = os.path.join(CONTENTS_FOLDER, file_name)

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return None

    try:
        doc = Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        print(f"❌ Error reading Word file '{file_name}': {e}")
        return None