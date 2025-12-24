import requests
from bs4 import BeautifulSoup
from config import BASE_URL, START_URL, HEADERS

def get_soup(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return BeautifulSoup(r.text, "html.parser")

def get_all_links():
    soup = get_soup(START_URL)
    pages = {START_URL}

    for a in soup.select("a[href*='page']"):
        pages.add(BASE_URL + a["href"])

    links = set()
    for page in pages:
        soup = get_soup(page)
        for a in soup.select("a[href*='/msg/']"):
            links.add(BASE_URL + a["href"])

    return links

def parse_vacancy(url):
    soup = get_soup(url)

    title = soup.select_one("h2")
    title = title.get_text(strip=True) if title else ""

    salary = ""
    for tr in soup.select("tr"):
        if "Зарплата" in tr.get_text():
            salary = tr.get_text(" ", strip=True)

    return title, salary, url
