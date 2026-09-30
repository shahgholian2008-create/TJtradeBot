TJtrade Bot 🤖
A Telegram bot that delivers TJtrade MAP indicator content.
Each username can access exactly one product, and after receiving the content, the username is permanently disabled.

Features
Username/password authentication from a multi-sheet Excel file.

Each sheet corresponds to one product (Word file).

One-time access per username (tracked in used_users.json).

Rate-limited password attempts (max 3 per session).

Fully English user interface.

Clean FSM-based conversation flow using aiogram v3.

Optional HTTP proxy support via config.json.

Project Structure
TJtradeBot/
├── bot.py # Entry point
├── config.json # Bot token + optional proxy (NOT in git)
├── config.example.json # Template for config.json
├── requirements.txt
├── README.md
├── .gitignore
├── users.xlsx # User credentials (NOT in git)
├── used_users.json # Tracks used usernames (auto-generated)
├── create_excel.py # Script to generate users.xlsx
├── contents/ # Product Word files (NOT in git)
│ ├── map_src.docx
│ ├── map_upd1.docx
│ ├── map_upd2.docx
│ ├── map_upd3.docx
│ └── map_upd4.docx
├── handlers/
│ ├── init.py
│ ├── auth.py # Authentication handlers
│ └── menu.py # Product display + confirmation
├── states.py # FSM states
└── utils/
├── init.py
├── constants.py # Shared constants
├── user_utils.py # Excel reader + credential check
├── used_tracker.py # JSON-based usage tracker
└── word_utils.py # Word file reader

Setup
1. Install dependencies
pip install -r requirements.txt

2. Configure the bot
Copy the template and fill in your bot token:

cp config.example.json config.json

Then edit config.json:

{
"telegram_token": "YOUR_BOT_TOKEN_HERE",
"proxy_url": null
}

Notes:

Set proxy_url to "http://127.0.0.1:8080" if you need a proxy.

Set it to null if you do not need a proxy.

3. Prepare user credentials
Create users.xlsx in the project root. It must contain 5 sheets named exactly:

MAP_SRC, MAP_UPD1, MAP_UPD2, MAP_UPD3, MAP_UPD4

Each sheet must have the following columns:

username | password | used

Where used is either "no" or "yes".
You can generate a sample file using:

python create_excel.py

4. Prepare product content
Create a contents/ folder in the project root and place the 5 Word files inside:

contents/
├── map_src.docx
├── map_upd1.docx
├── map_upd2.docx
├── map_upd3.docx
└── map_upd4.docx

Important: These files are NOT included in the repository for security reasons. You must provide them manually on the server (e.g., via SFTP or direct copy).

5. Run the bot
python bot.py

How It Works
User sends /start.

Bot asks for username, then password.

Bot checks credentials against the Excel file:

Username not found → invalid username.

Password wrong → up to 3 attempts allowed.

Username already used → access expired.

Valid → proceeds to product confirmation.

Bot shows the product tied to that username.

User taps the confirmation button.

Bot:

Marks the username as used in used_users.json.

Sends the Word content as text.

Removes the keyboard and clears the session.

Security Notes
config.json, users.xlsx, used_users.json, and contents/ are excluded from git via .gitignore.

Used usernames are tracked in a separate JSON file so the original Excel file stays untouched (and can be regenerated safely).

mark_used() is called before sending content, so even if the bot crashes mid-send, the username cannot be reused.

Password attempts are limited to 3 per session.

The bot token in config.json should be kept secret. If it ever leaks, revoke it immediately via BotFather.

Dependencies
aiogram (v3.x)

pandas

openpyxl

python-docx

See requirements.txt for exact versions.

License
Private project. All rights reserved.