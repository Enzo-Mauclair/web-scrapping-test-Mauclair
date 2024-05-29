import requests
from bs4 import BeautifulSoup
import csv

# URL de base du site de citations
BASE_URL = "https://quotes.toscrape.com"
# URL de connexion
LOGIN_URL = "https://quotes.toscrape.com/login"
# Liste des tags à récupérer
TARGET_TAGS = ["love", "inspirational", "life", "humor", "books"]
# Informations de connexion
LOGIN_DATA = {
    'username': 'test',
    'password': 'test'
}

def login_and_get_token():
    """
    Effectue la connexion et retourne le token reçu
    """
    session = requests.Session()
    # Obtenir le token CSRF
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    LOGIN_DATA['csrf_token'] = csrf_token

    # Effectuer la connexion
    response = session.post(LOGIN_URL, data=LOGIN_DATA)
    if response.status_code == 200:
        print("Connexion réussie")
    else:
        print("Échec de la connexion")
        return None
    
    # Retourner le token de session ou autre identifiant
    return session.cookies.get_dict().get('session', None), session

def get_quotes_from_page(page_num, session):
    """
    Récupère les citations de la page spécifiée
    """
    url = f"{BASE_URL}/page/{page_num}/"
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all("div", class_="quote")

    filtered_quotes = []
    for quote in quotes:
        tags = [tag.text for tag in quote.find_all("a", class_="tag")]
        if any(tag in TARGET_TAGS for tag in tags):
            text = quote.find("span", class_="text").text
            filtered_quotes.append({"text": text, "tags": tags})

    return filtered_quotes

def scrape_quotes(pages=5, session=None):
    """
    Scrape les citations des premières pages spécifiées et les filtre selon les tags
    """
    all_quotes = []
    for page_num in range(1, pages + 1):
        quotes = get_quotes_from_page(page_num, session)
        all_quotes.extend(quotes)

    # Ajouter spécifiquement les 2 premières pages avec le tag 'books'
    for page_num in range(1, 3):
        quotes = get_quotes_from_page(page_num, session)
        for quote in quotes:
            if "books" in quote['tags']:
                all_quotes.append(quote)

    return all_quotes

def save_quotes_to_csv(quotes, token, filename="results.csv"):
    """
    Sauvegarde les citations et le token dans un fichier CSV
    """
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Token", token])  # Écrire le token
        writer.writerow(["Citation", "Tags"])  # Écrire l'en-tête
        for quote in quotes:
            writer.writerow([quote['text'], ', '.join(quote['tags'])])

if __name__ == "__main__":
    token, session = login_and_get_token()
    if token:
        quotes = scrape_quotes(session=session)
        save_quotes_to_csv(quotes, token)
        print(f"Les citations et le token ont été sauvegardés dans le fichier results.csv")
    else:
        print("Impossible de récupérer le token. Vérifiez les informations de connexion.")


