from playwright.sync_api import sync_playwright
import sys

def extract_product_info(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Wait for the accordion to load
        page.wait_for_selector("#accordion")

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <product_url>")
        sys.exit(1)

    url = sys.argv[1]
    product_info = extract_product_info(url)

    print("Product Information:")
    for key, value in product_info.items():
        print(f"\n{key}:")
        print(value)