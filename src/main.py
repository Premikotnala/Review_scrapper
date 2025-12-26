import json
import os
from src.capterra_scraper import scrape_capterra_reviews
from src.g2_scraper import scrape_g2_reviews


def main():
    print("Review Scraper")
    print("1. Capterra (Recommended)")
    print("2. G2 (Limited due to restrictions)")

    choice = input("Choose source (1 or 2): ").strip()

    os.makedirs("output", exist_ok=True)

    if choice == "1":
        product = input("Enter Capterra product ID (example: slack): ").strip()
        reviews = scrape_capterra_reviews(product)

        output_file = f"output/{product}_capterra_reviews.json"

    elif choice == "2":
        product = input("Enter G2 company slug: ").strip()
        reviews = scrape_g2_reviews(product)

        output_file = f"output/{product}_g2_reviews.json"

    else:
        print("Invalid choice")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=4)

    print(f"\nSaved {len(reviews)} reviews to {output_file}")


if __name__ == "__main__":
    main()
