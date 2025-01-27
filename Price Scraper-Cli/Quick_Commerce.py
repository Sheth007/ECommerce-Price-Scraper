from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import itertools
import threading
import sys
import pyautogui

EDGE_DRIVER_PATH = "msedgedriver.exe" 

def loader_animation(stop_event):
    for frame in itertools.cycle(["🔎", "🔍"]):
        if stop_event.is_set():
            break
        sys.stdout.write(f"\rFetching prices... {frame}")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write("\rFetching prices... Done!    \n")

def get_zepto_price(product_name, driver):
    try:
        search_url = f"https://www.zeptonow.com/search?query={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        time.sleep(6)

        WebDriverWait(driver, 20).until(
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

#def get_blinkit_price(product_name, driver):
#    try:
#        search_url = f"https://blinkit.com/s/?q={'+'.join(product_name.split())}"
#        driver.get(search_url)
#        
#        print("Removing interfering elements...")
#        driver.execute_script("""
#            const elementToRemove = document.querySelector('.LocationSelectorDesktopV1__LocationBodyContainer-sc-19zschz-3.hQrfMz');
#            if (elementToRemove) elementToRemove.remove();
#        """)
#        
#        driver.execute_script("""
#            const elementToRemove2 = document.querySelector('.LocationDropDown__LocationOverlay-sc-bx29pc-1.bLgtGp');
#            if (elementToRemove2) elementToRemove2.remove();
#        """)
#
#        WebDriverWait(driver, 30).until(
#            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.tw-text-200.tw-font-semibold"))
#        )
#
#        soup = BeautifulSoup(driver.page_source, "html.parser")
#        price_element = soup.find("div", class_="tw-text-200.tw-font-semibold")
#        if price_element:
#            return {"company": "Blinkit", "price": price_element.text.strip()}
#        
#        return {"company": "Blinkit", "price": "N/A"}
#    
#    except Exception as e:
#        print(f"Error fetching Blinkit price: {e}")
#        return {"company": "Blinkit", "price": f"Error: {e}"}

def get_swiggy_instamart_price(product_name, driver):
    try:
        search_url = f"https://www.swiggy.com/instamart/search?custom_back=true&query={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        time.sleep(6)

        # Wait for the price element to be loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-aXZVg.ihMJwf.JZGfZ"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Find the div element with price in the aria-label
        price_element = soup.find("div", class_="sc-aXZVg ihMJwf JZGfZ")
        if price_element and price_element.has_attr("aria-label"):
            price = price_element["aria-label"].strip()
            return {"company": "Swiggy Instamart", "price": price}
        
        return {"company": "Swiggy Instamart", "price": "N/A"}
    
    except Exception as e:
        return {"company": "Swiggy Instamart", "price": f"Error: {e}"}
   
def fetch_prices(product_name):
    service = Service(EDGE_DRIVER_PATH)
    options = Options()
    options.add_argument("--headless")  # Optional: Run in headless mode
    
    results = []
    with webdriver.Edge(service=service, options=options) as driver:
        results.append(get_zepto_price(product_name, driver))        
        results.append(get_swiggy_instamart_price(product_name, driver))        
        #results.append(get_blinkit_price(product_name, driver))
    
    return results

if __name__ == "__main__":
    product_name = input("Enter Product Name : ").strip()
    stop_event = threading.Event()

    loader_thread = threading.Thread(target=loader_animation, args=(stop_event,))
    loader_thread.start()

    results = fetch_prices(product_name)

    stop_event.set()
    loader_thread.join()

    df = pd.DataFrame(results)
    print(df)