"""
ردیابی یوزرنیم‌های مصرف‌شده در یک فایل JSON جداگانه.
دلیل: فایل اکسل ممکن است قفل شود یا در حین نوشتن خراب شود.
"""
import json
import os
import threading

USED_FILE = "used_users.json"
_lock = threading.Lock()


def _load() -> dict:
    if not os.path.exists(USED_FILE):
        return {}
    try:
        with open(USED_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def _save(data: dict) -> None:
    # نوشتن atomic: اول temp، بعد rename
    tmp = USED_FILE + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, USED_FILE)


def is_used(username: str) -> bool:
    """آیا این یوزرنیم قبلاً مصرف شده؟"""
    with _lock:
        return username in _load()


def mark_used(username: str, sheet_name: str) -> None:
    """ثبت مصرف یوزرنیم. عملیات atomic است."""
    with _lock:
        data = _load()
        data[username] = {"sheet": sheet_name, "status": "used"}
        _save(data)