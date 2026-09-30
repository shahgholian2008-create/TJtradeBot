"""هندلرهای احراز هویت"""
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from states import AuthStates
from utils.user_utils import check_credentials
from utils.constants import MAX_ATTEMPTS


async def start_command(message: types.Message, state: FSMContext):
    """شروع فرآیند احراز هویت"""
    await state.clear()

    welcome_message = (
        "╔══════════════════════════════════╗\n"
        "║      🤖   TJtrade BOT   🤖       ║\n"
        "╚══════════════════════════════════╝\n\n"
        "👋 Welcome!\n\n"
        "This bot provides you with the official\n"
        "TJtrade MAP indicator content.\n\n"
        "⚠️ **Important:**\n"
        "• Each username can access ONLY ONE product.\n"
        "• After receiving the content, your access expires.\n"
        "• Choose wisely before confirming.\n\n"
        "🔐 To begin, please enter your username:"
    )

    await message.answer(welcome_message, reply_markup=ReplyKeyboardRemove())
    await state.set_state(AuthStates.waiting_for_username)
    await state.update_data(attempts=0)


async def handle_username(message: types.Message, state: FSMContext):
    """دریافت یوزرنیم"""
    if not message.text:
        await message.answer("⚠️ Please send your username as text.")
        return

    username = message.text.strip()
    if not username:
        await message.answer("⚠️ Username cannot be empty. Please try again:")
        return

    await state.update_data(username=username)
    await message.answer(
        "✅ Username received.\n\n"
        "🔐 Please enter your password:"
    )
    await state.set_state(AuthStates.waiting_for_password)


async def handle_password(message: types.Message, state: FSMContext):
    """دریافت پسورد و بررسی"""
    if not message.text:
        await message.answer("⚠️ Please send your password as text.")
        return

    password = message.text.strip()
    if not password:
        await message.answer("⚠️ Password cannot be empty. Please try again:")
        return

    data = await state.get_data()
    username = data.get("username")
    attempts = data.get("attempts", 0)

    sheet_name, result = check_credentials(username, password)

    # ---------- موفق ----------
    if result == "valid":
        await state.update_data(sheet_name=sheet_name)
        from handlers.menu import show_product
        await show_product(message, state, sheet_name)
        return

    # ---------- خطاها ----------
    if result == "used":
        await message.answer(
            "╔══════════════════════════════════╗\n"
            "║      ❌  ACCESS EXPIRED  ❌      ║\n"
            "╚══════════════════════════════════╝\n\n"
            "🔒 This username has already been used\n"
            "to receive a product's content.\n\n"
            "If you need another product, please\n"
            "contact the administrator.\n\n"
            "👋 Goodbye!"
        )
        await state.clear()
        return

    if result == "wrong_password":
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts

        if attempts >= MAX_ATTEMPTS:
            await message.answer(
                "╔══════════════════════════════════╗\n"
                "║   ⛔  TOO MANY ATTEMPTS  ⛔    ║\n"
                "╚══════════════════════════════════╝\n\n"
                "🚫 Too many failed attempts.\n"
                "Please try again later.\n\n"
                "Type /start to restart."
            )
            await state.clear()
            return

        await state.update_data(attempts=attempts)
        await message.answer(
            "❌ **Wrong password.**\n\n"
            f"🔁 Remaining attempts: **{remaining}**\n\n"
            "Please enter your password again:"
        )
        # state همان waiting_for_password می‌ماند
        return

    if result == "invalid_username":
        await message.answer(
            "╔══════════════════════════════════╗\n"
            "║  ❌  INVALID USERNAME  ❌       ║\n"
            "╚══════════════════════════════════╝\n\n"
            "🔒 This username was not found.\n\n"
            "🔄 Type /start to retry."
        )
        await state.clear()
        return

    # file_error
    await message.answer(
        "❌ Error loading users file.\n\n"
        "Please contact the administrator."
    )
    await state.clear()