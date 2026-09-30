"""ثابت‌های مشترک پروژه"""

# نقشه‌ی شیت‌ها به نام نمایشی، فایل Word و متن دکمه
SHEETS = {
    "MAP_SRC": {
        "display": "MAP SRC",
        "word": "map_src.docx",
        "button": "1. MAP SRC",
    },
    "MAP_UPD1": {
        "display": "MAP UPD #1",
        "word": "map_upd1.docx",
        "button": "2. MAP UPD #1",
    },
    "MAP_UPD2": {
        "display": "MAP UPD #2",
        "word": "map_upd2.docx",
        "button": "3. MAP UPD #2",
    },
    "MAP_UPD3": {
        "display": "MAP UPD #3",
        "word": "map_upd3.docx",
        "button": "4. MAP UPD #3",
    },
    "MAP_UPD4": {
        "display": "MAP UPD #4",
        "word": "map_upd4.docx",
        "button": "5. MAP UPD #4",
    },
}

SHEET_NAMES = list(SHEETS.keys())

# متن دکمه‌ی تأیید
CONFIRM_BUTTON = "✅ دریافت محتوا"
CANCEL_BUTTON = "❌ لغو"

# محدودیت تلاش
MAX_ATTEMPTS = 3