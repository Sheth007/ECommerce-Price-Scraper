from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Path to your extracted Edge WebDriver
EDGE_DRIVER_PATH = "msedgedriver.exe"  # Update this to the actual path

def get_amazon_price(product_name, driver):
    try:
        search_url = f"https://www.amazon.in/s?k={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price .a-offscreen"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = soup.find("span", class_="a-offscreen")
        if price:
            return {"company": "Amazon", "price": price.text.strip()}
        return {"company": "Amazon", "price": "N/A"}
    except Exception as e:
        return {"company": "Amazon", "price": f"Error: {e}"}

def get_flipkart_price(product_name, driver):
    try:
        search_url = f"https://www.flipkart.com/search?q={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".hl05eU .Nx9bqj"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = soup.find("div", class_="Nx9bqj")
        if price:
            return {"company": "Flipkart", "price": price.text.strip()}
        return {"company": "Flipkart", "price": "N/A"}
    except Exception as e:
        return {"company": "Flipkart", "price": f"Error: {e}"}

def get_zepto_price(product_name, driver):
    try:
        search_url = f"https://www.zeptonow.com/search?query={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h4[data-testid='product-card-price']"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = soup.find("h4", class_="font-heading text-lg tracking-wide line-clamp-1 !font-semibold !text-md !leading-4 !m-0",
                          attrs={"data-testid": "product-card-price"})
        if price:
            return {"company": "Zepto", "price": price.text.strip()}
        return {"company": "Zepto", "price": "N/A"}
    except Exception as e:
        return {"company": "Zepto", "price": f"Error: {e}"}
    
def get_tata_neu_price(product_name, driver):
    try:
        # Format the search URL for Tata Neu
        search_url = f"https://www.bigbasket.com/ps/?q={'+'.join(product_name.split())}"
        driver.get(search_url)

        # Wait for the price element to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Label-sc-15v1nk5-0"))
        )

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Locate the price using the correct CSS selector
        price = soup.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")

        # Extract the price
        if price:
            return {
                "company": "Tata Neu",
                "price": price.text.strip()
            }
        else:
            return {"company": "Tata Neu", "price": "N/A"}
    except Exception as e:
        return {"company": "Tata Neu", "price": f"Error: {e}"}
    
def get_jiomart_price(product_name, driver):
    try:
        # Replace spaces with '%20' for the correct URL format
        product_name = product_name.replace(" ", "%20")
        
        # Format search URL for JioMart with the correctly encoded product name
        search_url = f"https://www.jiomart.com/search/{product_name}"
        driver.get(search_url)

        # Wait for the price element to appear
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.plp-card-details-price"))
        )

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Locate the price using the correct CSS selector
        price = soup.find("span", class_="jm-heading-xxs jm-mb-xxs")

        # Extract the price
        if price:
            return {
                "company": "JioMart",
                "price": price.text.strip()
            }
        else:
            return {"company": "JioMart", "price": "N/A"}
    except Exception as e:
        return {"company": "JioMart", "price": f"Error: {e}"}


def fetch_prices(product_name):
    # Initialize WebDriver
    service = Service(EDGE_DRIVER_PATH)
    options = Options()
    #options.add_argument("--headless")  # Optional: Run in headless mode
    
    results = []
    with webdriver.Edge(service=service, options=options) as driver:
        results.append(get_amazon_price(product_name, driver))
        results.append(get_flipkart_price(product_name, driver))
        results.append(get_zepto_price(product_name, driver))
        results.append(get_tata_neu_price(product_name, driver))
        results.append(get_jiomart_price(product_name, driver))
    
    return results

if __name__ == "__main__":
    product_name = input("Enter Product Name : ").strip()
    results = fetch_prices(product_name)
    df = pd.DataFrame(results)
    print(df)
