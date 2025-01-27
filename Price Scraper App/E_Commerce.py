import itertools
import time
import threading
import tkinter as tk
from tkinter import messagebox, StringVar, ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

EDGE_DRIVER_PATH = "msedgedriver.exe"

#loading animation when the price scrapes
def loader_animation(stop_event, loading_var):
    for frame in itertools.cycle([" ◜", " ◝ ", "◞ ", " ◟"]):
        if stop_event.is_set():
            break
        loading_var.set(f"Fetching prices it takes few seconds... {frame}")
        time.sleep(0.5)
    loading_var.set("✧ദ്ദി ˉ͈̀꒳ˉ͈́ )")

def get_croma_price(product_name, driver):
    try:
        search_url = f"https://www.croma.com/searchB?q={'+'.join(product_name.split())}"
        driver.get(search_url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.new-price"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = soup.find("span", class_="amount plp-srp-new-amount")
        if price:
            return {"company": "Croma", "price": price.text.strip()}
        return {"company": "Croma", "price": "N/A"}
    except Exception as e:
        return {"company": "Croma", "price": f"Error: {e}"}

def get_tata_neu_price(product_name, driver):
    try:
        search_url = f"https://www.bigbasket.com/ps/?q={'+'.join(product_name.split())}"
        driver.get(search_url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.Label-sc-15v1nk5-0"))
        )
        soup = BeautifulSoup(driver.page_source, "html.parser")
        price = soup.find("span", class_="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi")
        if price:
            return {"company": "Tata Neu", "price": price.text.strip()}
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
            return {"company": "JioMart", "price": price.text.strip()}
        return {"company": "JioMart", "price": "N/A"}
    except Exception as e:
        return {"company": "JioMart", "price": f"Error: {e}"}

def fetch_prices(product_name):
    service = Service(EDGE_DRIVER_PATH)
    options = Options()
    options.add_argument("--headless") #if it's not in comment then it will run without gui otherwise it opens the edge browser
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36") #giving the user agent becayse the croma and tata new price are not fetching 
    #DUE TO IT LOADS DYNAMICALLY
    options.add_argument("window-size=1920x1080") #giving the size of the browser if you are runnin in gui mode 
    
    results = [] #storeing all the results in an array and retrun it
    with webdriver.Edge(service=service, options=options) as driver:
        results.append(get_croma_price(product_name, driver))
        results.append(get_tata_neu_price(product_name, driver))
        results.append(get_amazon_price(product_name, driver))
        results.append(get_flipkart_price(product_name, driver))
        results.append(get_jiomart_price(product_name, driver))
    
    return results

#GUI STARTS HERE
def fetch_prices_gui(product_name, result_var, loading_var):
    stop_event = threading.Event()
    
    loading_var.set("Fetching prices... Please wait!")
    
    loader_thread = threading.Thread(target=loader_animation, args=(stop_event, loading_var))
    loader_thread.start()
    
    try:
        results = fetch_prices(product_name)
        stop_event.set()
        loader_thread.join()
        
        df = pd.DataFrame(results)
        result_var.set(df.to_string(index=False))
    except Exception as e:
        result_var.set(f"Error: {e}")
        stop_event.set()
        loader_thread.join()

def start_fetching_prices(entry_var, result_var, loading_var):
    product_name = entry_var.get().strip()
    if not product_name:
        messagebox.showerror("Input Error", "Please enter a product name.")
        return

    threading.Thread(target=fetch_prices_gui, args=(product_name, result_var, loading_var)).start()

def create_gui():
    root = tk.Tk()
    root.title("E Commerce Price Scraper")
    root.geometry("600x500")
    root.config(bg="#f5f5f5")
    
    header = tk.Label(root, text="🛍️ E commerce Price Scraper Tool", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
    header.pack(pady=10)
    
    tk.Label(root, text="Enter Product Name:", font=("Helvetica", 12, "bold"), bg="#f5f5f5").pack(pady=10)
    entry_var = StringVar()
    entry_field = ttk.Entry(root, textvariable=entry_var, width=50)
    entry_field.pack(pady=5)

    result_var = StringVar()
    loading_var = StringVar()
    fetch_button = ttk.Button(root, text="Fetch Prices", command=lambda: start_fetching_prices(entry_var, result_var, loading_var))
    fetch_button.pack(pady=10)

    loading_label = tk.Label(root, textvariable=loading_var, font=("Helvetica", 12, "italic"), bg="#f5f5f5", fg="#555")
    loading_label.pack(pady=10)

    tk.Label(root, text="Results:", font=("Helvetica", 14, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)
    result_label = tk.Label(root, textvariable=result_var, wraplength=500, justify="center", anchor="w", bg="#e8e8e8", relief="solid", font=("Courier", 12))
    result_label.pack(pady=10, fill="both", expand=True, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()

