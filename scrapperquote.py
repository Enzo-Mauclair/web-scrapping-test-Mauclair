import requests
from bs4 import BeautifulSoup

# URL de base du site de citations
BASE_URL = "https://quotes.toscrape.com"
# Liste des tags à récupérer
TARGET_TAGS = ["love", "inspirational", "life", "humor"]

def get_quotes_from_page(page_num):
    """
    Récupère les citations de la page spécifiée
    """
    url = f"{BASE_URL}/page/{page_num}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all("div", class_="quote")

    filtered_quotes = []
    for quote in quotes:
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        if any(tag in TARGET_TAGS for tag in tags):
            text = quote.find("span", class_="text").text
            filtered_quotes.append({"text": text, "tags": tags})

    return filtered_quotes

def scrape_quotes(pages=5):
    """
    Scrape les citations des premières pages spécifiées et les filtre selon les tags
    """
    all_quotes = []
    for page_num in range(1, pages + 1):
        quotes = get_quotes_from_page(page_num)
        all_quotes.extend(quotes)

    return all_quotes

if __name__ == "__main__":
    quotes = scrape_quotes()
    for quote in quotes:
        print(f"Citation: {quote['text']}\nTags: {', '.join(quote['tags'])}\n")



