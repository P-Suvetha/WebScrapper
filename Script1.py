from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time

# Set up Selenium WebDriver (assuming Chrome)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
driver = webdriver.Chrome(options=chrome_options)  # Specify driver path if needed

def get_all_links(url):
    """Extract all sub-URLs from the given page."""
    try:
        driver.get(url)
        time.sleep(2)  # Adjust this delay based on page load
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        links = set()
        for a_tag in soup.find_all('a', href=True):
            link = a_tag['href']
            if link.startswith('http') or link.startswith('/'):
                full_url = link if link.startswith('http') else url + link
                links.add(full_url)
        return links
    except Exception as e:
        print(f"Error extracting links from {url}: {e}")
        return set()

def scrape_content(url):
    """Scrape the content from the given URL."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Proper encoding detection
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = soup.get_text(separator=' ').strip()
        cleaned_content = ' '.join(page_content.split())  # Clean extra whitespace
        print(cleaned_content)
        return cleaned_content

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}. Error: {e}")
        return ""

def save_to_file(content, filename="scraped_content.txt"):
    """Save the scraped content to a text file."""
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Scraped content saved to {filename}")
    except Exception as e:
        print(f"Error saving content to file: {e}")

def main():
    # Replace with the actual URL you want to scrape
    start_url = 'https://www.aible.com/'
    all_links = get_all_links(start_url)

    # Collect and concatenate all scraped content
    all_content = ""
    for link in all_links:
        print(f"Scraping: {link}")
        content = scrape_content(link)
        if content:
            all_content += content + "\n\n"  # Separate content from different URLs
        time.sleep(2)  # Avoid overwhelming the server

    # Save all scraped content to a .txt file
    save_to_file(all_content)

    # Close the browser
    driver.quit()

# Run the main function
if __name__ == "__main__":
    main()
