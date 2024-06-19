from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Function to extract names from the current page
        def extract_names():
            names_elements = page.locator('//h2[@class="entry-title"]/a').all()
            names = [element.text_content() for element in names_elements]
            return names

        # Open the file in append mode
        with open("result.txt", "a") as result_file:

            # Go to the initial page
            page.goto("https://www.nationalparalegals.co.uk/searchable-members/")
            page.click("button:has-text('Accept')")

            # Loop through the pages
            while True:
                # Wait for the names to appear on the page
                page.wait_for_selector('//h2[@class="entry-title"]/a')

                # Extract names from the current page and append to the file
                names_on_page = extract_names()
                for name in names_on_page:
                    result_file.write(name + "\n")

                # Flush the file to ensure data is saved
                result_file.flush()

                # Click on the "← older" link to navigate to the next page
                older_link = page.locator('//div[@class="nav-previous"]/a')
                if not older_link.is_disabled():
                    older_link.click()
                else:
                    # No more pages, break out of the loop
                    break

        context.close()
        browser.close()

if __name__ == "__main__":
    main()
