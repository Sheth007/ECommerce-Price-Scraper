from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import itertools
import threading
import pandas as pd
import time
import sys

app = Flask(__name__)

EDGE_DRIVER_PATH = "msedgedriver.exe"

def loader_animation(stop_event):
    for frame in itertools.cycle(["|", "/", "-", "\\"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rFetching prices... {frame}")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write("\rFetching prices... Done!    \n")

def get_croma_price(product_name, driver):
    try:
        search_url = f"https://www.croma.com/searchB?q={'+'.join(product_name.split())}"
        driver.get(search_url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.new-price"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        price = soup.find("span", class_="amount plp-srp-new-amount")

        if price:
            return {
                "company": "Croma",
                "price": price.text.strip()
            }
        else:
            return {"company": "Croma", "price": "N/A"}
    except Exception as e:
        return {"company": "Croma", "price": f"Error: {e}"}

def get_tata_neu_price(product_name, driver):
    try:
        search_url = f"https://www.bigbasket.com/ps/?q={'+'.join(product_name.split())}"
        driver.get(search_url)

        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Label-sc-15v1nk5-0"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        price = soup.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")

        if price:
            return {
                "company": "Tata Neu",
                "price": price.text.strip()
            }
        else:
            return {"company": "Tata Neu", "price": "N/A"}
    except Exception as e:
        return {"company": "Tata Neu", "price": f"Error: {e}"}

def get_amazon_price(product_name, driver):
    try:
        search_url = f"https://www.amazon.in/s?k={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price .a-price-whole"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = soup.find("span", class_="a-price-whole")
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
    
def get_jiomart_price(product_name, driver):
    try:
        product_name = product_name.replace(" ", "%20")
        
        search_url = f"https://www.jiomart.com/search/{product_name}"
        driver.get(search_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.plp-card-details-price"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")

        price = soup.find("span", class_="jm-heading-xxs jm-mb-xxs")

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
    service = Service(EDGE_DRIVER_PATH)
    options = Options()
    
    # Uncomment the line to run in headless mode if needed
    # options.add_argument("--headless")
    
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1920x1080")  # Default size for the window
    options.add_argument("window-position=-10000,-10000")  # Move the window off-screen
    
    # Alternatively, you can use `--start-maximized` to start with a minimized window
    # options.add_argument("--start-maximized") 
    
    results = []
    with webdriver.Edge(service=service, options=options) as driver:
        results.append(get_croma_price(product_name, driver))
        results.append(get_tata_neu_price(product_name, driver))
        results.append(get_amazon_price(product_name, driver))
        results.append(get_flipkart_price(product_name, driver))
        results.append(get_jiomart_price(product_name, driver))
    
    return results


@app.route('/fetch_prices', methods=['GET'])
def fetch_prices_api():
    product_name = request.args.get('product_name', '').strip()
    
    if not product_name:
        return jsonify({"error": "Product name is required"}), 400

    stop_event = threading.Event()

    # Start the loader animation in a separate thread
    loader_thread = threading.Thread(target=loader_animation, args=(stop_event,))
    loader_thread.start()

    # Fetch prices
    results = fetch_prices(product_name)

    # Stop the loader animation thread once prices are fetched
    stop_event.set()
    loader_thread.join()

    # Return results in JSON format
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5001)