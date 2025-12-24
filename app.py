import requests
import webbrowser
import threading
import csv
import time
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

BASE_URL = "https://www.ss.com"
START_URL = "https://www.ss.com/ru/work/are-required/programmer/"

HEADERS = {"User-Agent": "Mozilla/5.0"}

vacancies_data = []

# ---------- Парсинг ----------

def get_soup(url):
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def get_all_pages():
    soup = get_soup(START_URL)
    pages = {START_URL}
    for a in soup.select("a[href*='page']"):
        pages.add(BASE_URL + a["href"])
    return list(pages)

def parse_vacancy(url):
    soup = get_soup(url)

    title = soup.select_one("h2")
    title = title.get_text(strip=True) if title else ""

    description = soup.select_one("#msg_div_msg")
    description = description.get_text(" ", strip=True) if description else ""

    salary = ""
    for tr in soup.select("tr"):
        if "Зарплата" in tr.get_text():
            salary = tr.get_text(" ", strip=True)

    return title, salary, description

def load_vacancies():
    btn_search.config(state="disabled")
    status.set("Загрузка вакансий...")
    listbox.delete(0, tk.END)
    vacancies_data.clear()

    keyword = entry_keyword.get().lower()
    min_salary = entry_salary.get()

    try:
        min_salary = int(min_salary) if min_salary else 0
    except ValueError:
        messagebox.showerror("Ошибка", "Зарплата должна быть числом")
        btn_search.config(state="normal")
        return

    pages = get_all_pages()
    links = set()

    for page in pages:
        soup = get_soup(page)
        for a in soup.select("a[href*='/msg/']"):
            links.add(BASE_URL + a["href"])

    for i, link in enumerate(links, 1):
        status.set(f"Обработка {i}/{len(links)}")
        try:
            title, salary, desc = parse_vacancy(link)

            if keyword and keyword not in title.lower() and keyword not in desc.lower():
                continue

            salary_value = 0
            digits = "".join(filter(str.isdigit, salary))
            if digits:
                salary_value = int(digits)

            if salary_value < min_salary:
                continue

            vacancies_data.append((title, salary, link))
            listbox.insert(tk.END, f"{title} | {salary}")

            time.sleep(0.5)
        except:
            pass

    status.set(f"Найдено вакансий: {len(vacancies_data)}")
    btn_search.config(state="normal")

def start_search():
    threading.Thread(target=load_vacancies, daemon=True).start()

def open_vacancy(event):
    index = listbox.curselection()
    if index:
        webbrowser.open(vacancies_data[index[0]][2])

def save_csv():
    if not vacancies_data:
        messagebox.showwarning("Нет данных", "Сначала выполните поиск")
        return

    with open("vacancies_programmer_ss.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Название", "Зарплата", "Ссылка"])
        writer.writerows(vacancies_data)

    messagebox.showinfo("Готово", "Файл vacancies_programmer_ss.csv сохранён")

# ---------- GUI ----------

root = tk.Tk()
root.title("Вакансии программиста — ss.com")
root.geometry("900x500")

# Тёмная тема
style = ttk.Style()
style.theme_use("default")
style.configure(".", background="#2b2b2b", foreground="white")
style.configure("TButton", background="#3c3f41")
style.configure("TEntry", fieldbackground="#3c3f41")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="both", expand=True)

controls = ttk.Frame(frame)
controls.pack(fill="x", pady=5)

ttk.Label(controls, text="Ключевые слова:").grid(row=0, column=0)
entry_keyword = ttk.Entry(controls, width=20)
entry_keyword.grid(row=0, column=1, padx=5)

ttk.Label(controls, text="Мин. зарплата:").grid(row=0, column=2)
entry_salary = ttk.Entry(controls, width=10)
entry_salary.grid(row=0, column=3, padx=5)

btn_search = ttk.Button(controls, text="🔍 Найти", command=start_search)
btn_search.grid(row=0, column=4, padx=5)

btn_save = ttk.Button(controls, text="💾 CSV", command=save_csv)
btn_save.grid(row=0, column=5)

listbox = tk.Listbox(frame, bg="#1e1e1e", fg="white", font=("Arial", 11))
listbox.pack(fill="both", expand=True, pady=10)
listbox.bind("<Double-Button-1>", open_vacancy)

status = tk.StringVar(value="Готово")
status_bar = ttk.Label(root, textvariable=status, anchor="w")
status_bar.pack(fill="x")

root.mainloop()

