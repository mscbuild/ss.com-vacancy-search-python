import os
import sys
import csv

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

DATA_DIR = resource_path("data")
SENT_FILE = os.path.join(DATA_DIR, "sent_links.txt")
CSV_FILE = os.path.join(DATA_DIR, "vacancies.csv")

def ensure_files():
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(SENT_FILE):
        with open(SENT_FILE, "w", encoding="utf-8"):
            pass

def load_sent_links():
    ensure_files()
    with open(SENT_FILE, "r", encoding="utf-8") as f:
        return set(f.read().splitlines())

def save_sent_link(link):
    ensure_files()
    with open(SENT_FILE, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def save_csv(vacancies):
    ensure_files()
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Название", "Зарплата", "Ссылка"])
        writer.writerows(vacancies)
