import csv
from pathlib import Path
from bs4 import BeautifulSoup
import requests

URL = "http://quotes.toscrape.com/"
HEADERS = {"User-Agent": "SE-Intro-Class/1.0"}
HTML_FILE = Path("page.html")
CSV_FILE = Path("quotes.csv")


def fetch_and_save_html(url: str = URL, output_path: Path = HTML_FILE) -> Path:
    """Fetch the page and save the HTML response locally."""
    with requests.Session() as session:
        session.headers.update(HEADERS)
        response = session.get(url, timeout=10)
        response.raise_for_status()

        # Use response.apparent_encoding or response.encoding (defaults to UTF-8/ISO-8859-1)
        encoding = response.encoding or "utf-8"
        output_path.write_text(response.text, encoding=encoding)

    print(f"Saved response HTML to {output_path}")
    return output_path


def extract_from_saved_html(
    html_path: Path = HTML_FILE, csv_path: Path = CSV_FILE
) -> None:
    """Read the locally saved HTML file, extract quotes, and save to CSV."""
    html_content = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html_content, "lxml")

    scraped_data = []
    for item in soup.find_all("div", class_="quote"):
        text_el = item.find("span", class_="text")
        author_el = item.find("small", class_="author")
        tags = [tag.get_text(strip=True) for tag in item.select(".tags a.tag")]

        scraped_data.append({
            "quote": text_el.get_text(strip=True) if text_el else "",
            "author": author_el.get_text(strip=True) if author_el else "",
            "tags": ", ".join(tags),
        })

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["quote", "author", "tags"])
        writer.writeheader()
        writer.writerows(scraped_data)

    print(f"Saved {len(scraped_data)} quotes to {csv_path}!")


if __name__ == "__main__":
    saved_file = fetch_and_save_html()
    extract_from_saved_html(saved_file)