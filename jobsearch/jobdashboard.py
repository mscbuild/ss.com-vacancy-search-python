import requests
import pandas as pd
from bs4 import BeautifulSoup

import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

# 🔎 URL поиска вакансий «программист»
URL = "https://www.ss.com/ru/work/are-required/programmer/"

def fetch_ss_com_vacancies(url=URL):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        print(f"Ошибка доступа к странице: {response.status_code}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, "html.parser")
    vacancies = []

    for link in soup.select("a[href*='/msg/']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        full_link = "https://www.ss.com" + href
        link_md = f"[Ссылка]({full_link})"  # Markdown ссылка

        vacancies.append({
            "Название вакансии": title,
            "Ссылка": link_md
        })

    return pd.DataFrame(vacancies)

# ───────────────
# Создаём Dash-приложение
# ───────────────
app = dash.Dash(__name__)
app.title = "Вакансии программистов (ss.com)"

# ───────────────
# Layout с интервалом обновления каждые N миллисекунд
# ───────────────
UPDATE_INTERVAL_MS = 5 * 60 * 1000  # 5 минут

app.layout = html.Div(
    style={"width": "80%", "margin": "auto", "fontFamily": "Arial"},
    children=[
        html.H1("💻 Вакансии программистов (SS.COM)", style={"textAlign": "center"}),

        html.P(id="vacancy-count", style={"fontSize": "18px"}),

        dcc.Graph(id="vacancy-graph"),

        html.H3("📋 Список вакансий"),

        dash_table.DataTable(
            id="vacancy-table",
            columns=[
                {"name": "Название вакансии", "id": "Название вакансии"},
                {"name": "Ссылка", "id": "Ссылка", "presentation": "markdown"}  # <-- markdown для кликабельной ссылки
            ],
            page_size=10,
            filter_action="native",
            sort_action="native",
            style_cell={
                "textAlign": "left",
                "padding": "8px",
                "whiteSpace": "normal"
            },
            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f0f0f0"
            }
        ),

        # Интервал для автообновления
        dcc.Interval(
            id="interval-component",
            interval=UPDATE_INTERVAL_MS,
            n_intervals=0
        )
    ]
)

# ───────────────
# Callback для обновления данных
# ───────────────
@app.callback(
    Output("vacancy-table", "data"),
    Output("vacancy-graph", "figure"),
    Output("vacancy-count", "children"),
    Input("interval-component", "n_intervals")
)
def update_vacancies(n):
    df = fetch_ss_com_vacancies()

    count_text = f"Найдено вакансий: {len(df)}" if not df.empty else "Вакансий не найдено"

    fig = px.bar(
        x=["Вакансии"],
        y=[len(df)],
        labels={"x": "", "y": "Количество"},
        title="Общее количество вакансий"
    )

    return df.to_dict("records"), fig, count_text

# ───────────────
# Запуск приложения
# ───────────────
if __name__ == "__main__":
    app.run(debug=True)
