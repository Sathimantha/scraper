import sys
from playwright.sync_api import sync_playwright

def extract_image_urls(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        image_urls = page.evaluate("""
            () => {
                const imageElements = document.querySelectorAll('.product-single__media img');
                return Array.from(imageElements).map(img => {
                    if (img.dataset.srcset) {
                        const srcset = img.dataset.srcset.split(',');
                        const largestImage = srcset[srcset.length - 1].trim().split(' ')[0];
                        return largestImage;
                    }
                    return img.src;
                });
            }
        """)

        browser.close()
        return image_urls

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <product_url>")
        sys.exit(1)

    product_url = sys.argv[1]
    try:
        urls = extract_image_urls(product_url)
        print("Extracted image URLs:")
        for url in urls:
            print(url)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()