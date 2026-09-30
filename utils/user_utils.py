"""خواندن و بررسی کاربران از فایل اکسل"""
import pandas as pd

from utils.constants import SHEET_NAMES
from utils.used_tracker import is_used

USERS_FILE = "users.xlsx"


def load_sheet(sheet_name: str):
    """بارگذاری یک شیت خاص از فایل Excel"""
    try:
        return pd.read_excel(USERS_FILE, sheet_name=sheet_name, dtype=str)
    except Exception as e:
        print(f"❌ Error loading sheet '{sheet_name}': {e}")
        return None


def check_credentials(username: str, password: str):
    """
    بررسی صحت یوزرنیم و پسورد در همه‌ی شیت‌ها.
    
    خروجی: (sheet_name, status)
        status ∈ {"valid", "wrong_password", "used", "invalid_username", "file_error"}
    """
    found_username_sheet = None

    for sheet_name in SHEET_NAMES:
        df = load_sheet(sheet_name)
        if df is None:
            continue

        row = df[df["username"] == username]
        if row.empty:
            continue

        # یوزرنیم در این شیت پیدا شد
        found_username_sheet = sheet_name
        stored_password = str(row.iloc[0]["password"]).strip()

        if stored_password != password:
            return (sheet_name, "wrong_password")

        # پسورد درست — حالا چک کن مصرف نشده باشد
        # هم از JSON، هم از ستون used در اکسل (برای سازگاری)
        if is_used(username):
            return (sheet_name, "used")

        excel_used = str(row.iloc[0].get("used", "no")).strip().lower()
        if excel_used == "yes":
            return (sheet_name, "used")

        return (sheet_name, "valid")

    if found_username_sheet is None:
        return (None, "invalid_username")

    return (None, "file_error")