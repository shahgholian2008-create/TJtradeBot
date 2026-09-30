from aiogram.fsm.state import State, StatesGroup


class AuthStates(StatesGroup):
    waiting_for_username = State()
    waiting_for_password = State()
    waiting_for_confirmation = State()  # ← تغییر: تأیید مستقیم، نه انتخاب