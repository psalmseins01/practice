import csv
from bs4 import BeautifulSoup
import requests

def scrape_quotes():
    url = "http://quotes.toscrape.com/"
    headers = {"User-Agent": "SE-Intro-Class/1.0"}

    # 1. Fetch the page using a Session for connection reuse
    with requests.Session() as session:
        session.headers.update(headers)
        response = session.get(url, timeout=10)
        response.raise_for_status()

    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, "lxml")

    # 3. Extract the data
    scraped_data = []
    for item in soup.find_all("div", class_="quote"):
        text = item.find("span", class_="text").get_text(strip=True)
        author = item.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in item.select(".tags a.tag")]

        scraped_data.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })

    # 4. Save to CSV
    with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
        writer.writeheader()
        writer.writerows(scraped_data)

    print(f"Saved {len(scraped_data)} quotes to quotes.csv!")

if __name__ == "__main__":
    scrape_quotes()