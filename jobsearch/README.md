## 📌 What the app does

- Download "programmer" jobs from website

- Save them in a DataFrame

**Display:**

- 📊 Job table

- 📈 Number of jobs

- 🔎 Interactive search by job title

## 📦 Installing dependencies

~~~bash
pip install requests beautifulsoup4 pandas dash plotly
~~~

## ▶️ How to launch

~~~bash
python ss_com_dashboard.py
~~~

### Open in browser:

~~~bash
http://127.0.0.1:8050
~~~

## Full data pipeline:

| Stage | Implementation |
| ---------------- | ------------------------ |
| Data Collection | requests + BeautifulSoup |
| Structuring | Pandas |
| Analytics | Plotly |
| Visualization | Dash |
| UI | Interactive Table |

