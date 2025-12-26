import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


def parse_date(date_text):
    """
    Convert G2 date text to datetime.
    Example: 'Feb 12, 2023'
    """
    try:
        return datetime.strptime(date_text.strip(), "%b %d, %Y")
    except:
        return None


def scrape_g2_reviews(company):
    """
    Scrapes reviews from G2 without strict date filtering
    (date filtering is done later in main.py)
    """
    reviews = []
    page = 1

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept-Language": "en-US,en;q=0.9",
    }

    while page <= 3:  # limit pages to avoid blocking
        url = f"https://www.g2.com/products/{company}/reviews?page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch page", page)
            break

        soup = BeautifulSoup(response.text, "html.parser")

        # More reliable selector
        review_cards = soup.find_all("div", attrs={"data-testid": "review-card"})
        print(f"Page {page}: Found {len(review_cards)} reviews")

        if not review_cards:
            break

        for card in review_cards:
            title = card.find("h3")
            review = card.find("p")
            date_tag = card.find("time")
            rating = card.find("span")

            review_date = (
                parse_date(date_tag.text) if date_tag else None
            )

            reviews.append({
                "title": title.text.strip() if title else "",
                "review": review.text.strip() if review else "",
                "date": review_date.strftime("%Y-%m-%d") if review_date else "",
                "rating": rating.text.strip() if rating else "",
                "source": "G2"
            })

        page += 1
        time.sleep(1)

    return reviews
