import sys
from playwright.sync_api import sync_playwright, TimeoutError

def scrape_product_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        try:
            # Extract size options
            size_options = page.eval_on_selector_all('#SingleOptionSelector-0 option', '''
                (options) => options.map(option => option.textContent.trim())
            ''')

            # Extract prices for each size
            variant_data = []
            for size in size_options:
                # Select the size
                page.select_option('#SingleOptionSelector-0', size)
                page.wait_for_timeout(1000)  # Wait for price update

                # Extract the price
                price_element = page.query_selector('.price-item.price-item--regular')
                price = price_element.inner_text().strip() if price_element else "Price not available"

                variant_data.append({'size': size, 'price': price})

        except TimeoutError:
            print("Timeout error: Unable to load the page or find elements.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        finally:
            browser.close()

        return variant_data

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <product_url>")
        sys.exit(1)

    url = sys.argv[1]
    product_data = scrape_product_data(url)

    if product_data:
        print("Product Data:")
        for variant in product_data:
            print(f"Size: {variant['size']}, Price: {variant['price']}")
    else:
        print("Failed to scrape product data.")

if __name__ == "__main__":
    main()