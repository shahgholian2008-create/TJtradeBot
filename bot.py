import asyncio
import json
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import auth, menu
from states import AuthStates

# ========== بارگذاری تنظیمات ==========
CONFIG_FILE = "config.json"

if not os.path.exists(CONFIG_FILE):
    raise SystemExit(
        f"❌ {CONFIG_FILE} not found!\n"
        f"Copy 'config.example.json' to '{CONFIG_FILE}' and fill in your token."
    )

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

TOKEN = config.get("telegram_token")
if not TOKEN or TOKEN == "YOUR_BOT_TOKEN_HERE":
    raise SystemExit("❌ Please set a valid 'telegram_token' in config.json")

# ========== لاگ ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ========== Storage ==========
storage = MemoryStorage()

# ========== Session (با پروکسی اختیاری) ==========
proxy_url = config.get("proxy_url")
if proxy_url:
    logger.info(f"Using proxy: {proxy_url}")
    session = AiohttpSession(proxy=proxy_url)
else:
    logger.info("No proxy configured.")
    session = AiohttpSession()

bot = Bot(token=TOKEN, session=session)
dp = Dispatcher(storage=storage)


# ========== ثبت هندلرها ==========
dp.message.register(auth.start_command, Command("start"))
dp.message.register(auth.handle_username, AuthStates.waiting_for_username)
dp.message.register(auth.handle_password, AuthStates.waiting_for_password)
dp.message.register(
    menu.handle_confirmation,
    AuthStates.waiting_for_confirmation,
)


@dp.message()
async def unknown_message(message: types.Message):
    await message.answer("❌ Please use /start to begin.")


async def main():
    logger.info("🤖 TJtrade Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())