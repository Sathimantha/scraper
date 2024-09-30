import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

def extract_product_info(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Extract description
        description = page.eval_on_selector('#ui-id-2 .product-single__description', 'el => el.innerText')

        # Extract additional information
        additional_info = page.eval_on_selector('#ui-id-4 .product-single__description', 'el => el.innerText')

        # Extract ingredients
        ingredients = page.eval_on_selector('#ui-id-6 .product-single__description', 'el => el.innerText')

        browser.close()

        return {
            "Description": description,
            "Additional Information": additional_info,
            "Ingredients": ingredients
        }

def extract_image_urls(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        image_urls = page.evaluate("""
            () => {
                const imageElements = document.querySelectorAll('.product-single__media img');
                return Array.from(imageElements).map(img => img.src);
            }
        """)

        browser.close()
        return image_urls

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <product_url>")
        sys.exit(1)

    product_url = sys.argv[1]

    # Extract product info
    product_info = extract_product_info(product_url)

    # Extract image URLs
    image_urls = extract_image_urls(product_url)

    # Create output directory with product name
    product_name = product_url.split("/")[-1].split(".")[0]
    product_dir = Path(f"{product_name}")
    product_dir.mkdir(parents=True, exist_ok=True)

    # Save product info to a file
    product_info_file = product_dir / "info.txt"
    with open(product_info_file, "w") as f:
        f.write(f"Description:\n{product_info['Description']}\n\nAdditional Information:\n{product_info['Additional Information']}\n\nIngredients:\n{product_info['Ingredients']}\n")

    # Save image URLs to a file
    image_urls_file = product_dir / "image_urls.txt