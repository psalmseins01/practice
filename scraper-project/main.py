import requests
from bs4 import BeautifulSoup


url = "http://quotes.toscrape.com/"
headers = {"User-Agent": "StudentScraperBot/1.0"}

response = requests.get(url, headers=headers, timeout=10)

response.raise_for_status()
html_content = response.text
soup = BeautifulSoup(html_content, "lxml")


# print(f"Successfully fetched {len(html_content)} characters!")
# print("Page Title:", soup.title.string)

quotes = soup.find_all("div", class_="quote")

quotes = soup.find_all("div", class_="quote")

# with open("demo.txt", mode="w", encoding="utf-8") as f:
#     for quote in quotes:
#         text = quote.find("span", class_="text").get_text()
#         f.write(text + "\n")

for quote in quotes:
    text = quote.find("span", class_="text").get_text()
    author = quote.select_one("small.author").get_text()
    author_link = quote.find("a").get("href")

    print(f"{text} - {author} (Bio: {author_link})")