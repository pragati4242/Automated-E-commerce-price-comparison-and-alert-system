import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Function to generate URLs
def generate_url(base_url, search_query):
    return base_url + search_query.replace(" ", "+")

search_query = input("Enter the product you want to search: ")

# URLs for Amazon and Flipkart
amazon_base_url = "https://www.amazon.in/s?k="
flipkart_base_url = "https://www.flipkart.com/search?q="

amazon_url = generate_url(amazon_base_url, search_query)
flipkart_url = generate_url(flipkart_base_url, search_query)

# Scraping function for Amazon
def scrape_amazon_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_list = []
    price_list = []
    link_list = []

    # Scraping product info, prices, and links
    for product in soup.find_all("span", attrs={"class": "a-size-medium a-color-base a-text-normal"}):
        product_list.append(product.text.strip())

    for price in soup.find_all("span", attrs={"class": "a-price-whole"}):
        price_list.append(int(''.join(filter(str.isdigit, price.text.strip()))))

    for link in soup.find_all("a", attrs={"class": "a-link-normal s-no-outline"}, href=True):
        link_list.append("https://www.amazon.in" + link["href"])

    return product_list[:5], price_list[:5], link_list[:5]

# Scraping function for Flipkart
def scrape_flipkart_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    product_list = []
    price_list = []
    link_list = []

    # Scraping product info, prices, and links (you need to add Flipkart scraping logic here)

    return product_list[:5], price_list[:5], link_list[:5]

while True:
    # Scraping data from Amazon
    amazon_products, amazon_prices, amazon_links = scrape_amazon_data(amazon_url)

    # Scraping data from Flipkart
    flipkart_products, flipkart_prices, flipkart_links = scrape_flipkart_data(flipkart_url)

    # Finding the cheaper price
    cheapest_amazon_price = min(amazon_prices) if amazon_prices else float('inf')
    cheapest_flipkart_price = min(flipkart_prices) if flipkart_prices else float('inf')

    # Compare prices and notify if cheaper price found
    cheaper_store = None
    cheapest_price = min(cheapest_amazon_price, cheapest_flipkart_price)

    if cheapest_price == cheapest_amazon_price:
        cheaper_store = "Amazon"
        cheapest_url = amazon_links[amazon_prices.index(cheapest_price)] if cheapest_price in amazon_prices else None
    elif cheapest_price == cheapest_flipkart_price:
        cheaper_store = "Flipkart"
        cheapest_url = flipkart_links[flipkart_prices.index(cheapest_price)] if cheapest_price in flipkart_prices else None

    # Notify if cheaper price found
    if cheaper_store and cheapest_url:
        message = f"Product: {search_query}\nCheaper Price: {cheapest_price}\nStore: {cheaper_store}\nBuy Now: {cheapest_url}\n"

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("rautharish909@gmail.com", "mdph jfsu tulg dqny")
        server.sendmail("rautharish909@gmail.com", "rautharish909@gmail.com", f"Subject: Cheaper Price Alert!\n\n{message}")
        server.quit()

        print("Notification sent for cheaper price.")

    # Wait for 1 hour before checking again
    time.sleep(3600)  # 1 hour interval for continuous analysis