import requests
from bs4 import BeautifulSoup
import time


def scrape_capterra_reviews(product_slug, max_pages=3):
    reviews = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }

    for page in range(1, max_pages + 1):
        url = f"https://www.capterra.com/p/{product_slug}/reviews/?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("div", class_="review")

        if not cards:
            break

        for card in cards:
            title = card.find("h3")
            body = card.find("p", class_="review-text")
            date = card.find("span", class_="review-date")
            rating = card.find("span", class_="rating")

            reviews.append({
                "title": title.text.strip() if title else "",
                "review": body.text.strip() if body else "",
                "date": date.text.strip() if date else "",
                "rating": rating.text.strip() if rating else "",
                "source": "Capterra"
            })

        time.sleep(1)

    return reviews
