# 🏆 Python Job Monitor - GUI + Telegram job parser

Developed a GUI application for monitoring job openings with web parsing, Telegram notifications, and automatic data updates. Used Python, BeautifulSoup, Tkinter, and a REST API.

**What it can do:**

- 🔍 Parses programming job openings from website

- 🧠 Filters by keywords and salary

- 🖥️ GUI application (Tkinter, dark theme)

- 📩 Telegram notifications about new openings

- 💾 Save as CSV

- 🕒 Automatic check every N minutes

- 🚫 Duplicate protection

- 📂 Neat project structure

# 📁 1️⃣ Project structure

~~~bash
job_monitor/
│
├── app.py                # GUI
├── parser.py             # Job Parser
├── telegram_bot.py       # Telegram Notifications
├── storage.py            # File Management
├── config.py             # Settings
├── requirements.txt
├── README.md
└── data/
    ├── sent_links.txt
    └── vacancies.csv
~~~

# ⚙️ 2️⃣ config.py —Settings

~~~bash
BASE_URL = "https://www.ss.com"
START_URL = "https://www.ss.com/ru/work/are-required/programmer/"

HEADERS = {"User-Agent": "Mozilla/5.0"}

TELEGRAM_TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

CHECK_INTERVAL = 1800  # 30 минут
~~~

# 🧠 3️⃣ parser.py — parsing logic

# 💾 4️⃣ storage.py - protection against duplicates + CSV

# 📩 5️⃣ telegram_bot.py

# 🖥️ 6️⃣ app.py — GUI + automatic verification

## Features

- Parsing all pages
  
- Job filtering
  
- GUI (Tkinter)
  
- Telegram notifications
  
- Duplicate protection
  
- Saving to CSV

## Stack

- Python
  
- Requests
  
-BeautifulSoup

- Tkinter

- Telegram Bot API

## Launch

~~~bash
pip install -r requirements.txt
python app.py
~~~

## 🏗️ 5️⃣ Build into a single EXE

# License

This project is licensed under the MIT License.
 
