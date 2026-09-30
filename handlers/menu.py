"""هندلر نمایش و ارسال محتوای محصول"""
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from states import AuthStates
from utils.constants import SHEETS, CONFIRM_BUTTON, CANCEL_BUTTON
from utils.word_utils import read_word_file
from utils.used_tracker import mark_used


async def show_product(message: types.Message, state: FSMContext, user_sheet: str):
    """
    چون هر یوزرنیم فقط به یک شیت دسترسی دارد،
    مستقیم همان محصول را با دکمه‌ی تأیید نشان می‌دهیم.
    """
    product_name = SHEETS[user_sheet]["display"]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=CONFIRM_BUTTON)]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await message.answer(
        "╔══════════════════════════════════╗\n"
        "║     ✅  LOGIN SUCCESSFUL  ✅     ║\n"
        "╚══════════════════════════════════╝\n\n"
        f"🎯 Your product: **{product_name}**\n\n"
        "⚠️ **Important:**\n"
        "• After you receive the content, your\n"
        "  username will be permanently disabled.\n"
        "• You cannot undo this action.\n\n"
        f"👇 Tap **{CONFIRM_BUTTON}** below to receive it:",
        reply_markup=keyboard,
    )
    await state.set_state(AuthStates.waiting_for_confirmation)


async def handle_confirmation(message: types.Message, state: FSMContext):
    """پردازش تأیید کاربر و ارسال محتوا"""
    if not message.text:
        return

    text = message.text.strip()
    data = await state.get_data()
    user_sheet = data.get("sheet_name")
    username = data.get("username")

    if text == CANCEL_BUTTON:
        await message.answer(
            "❌ Cancelled. You can use /start again if needed.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
        return

    if text != CONFIRM_BUTTON:
        await message.answer(
            f"⚠️ Please use the button **{CONFIRM_BUTTON}** below."
        )
        return

    if not user_sheet or user_sheet not in SHEETS:
        await message.answer("❌ Session expired. Please /start again.")
        await state.clear()
        return

    # 1) اول علامت‌گذاری کن (قبل از ارسال، برای جلوگیری از سوءاستفاده)
    mark_used(username, user_sheet)

    # 2) محتوا را بخوان
    word_file = SHEETS[user_sheet]["word"]
    content = read_word_file(word_file)
    product_name = SHEETS[user_sheet]["display"]

    if content is None:
        await message.answer(
            f"❌ Content file '{word_file}' not found.\n"
            "Please contact the administrator."
        )
        # چون mark_used قبلاً انجام شده، باید برگردانیم
        # (این حالت نادر است، پس فقط لاگ می‌کنیم)
        print(f"⚠️ WARNING: {username} marked as used but content not found!")
        await state.clear()
        return

    # 3) ارسال محتوا
    await message.answer(
        f"╔══════════════════════════════════╗\n"
        f"║   📄  {product_name}  📄\n"
        f"╚══════════════════════════════════╝\n\n"
        f"{content}\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "🔒 Your access has now expired.\n"
        "This username cannot be used again.\n\n"
        "💡 If you need another product, please\n"
        "contact the administrator.\n\n"
        "👋 Goodbye!"
    )

    await message.answer(
        "✅ Done. You may now close this chat.",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()