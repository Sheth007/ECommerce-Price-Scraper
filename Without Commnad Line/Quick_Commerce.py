import itertools
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import threading
import tkinter as tk
from tkinter import messagebox, StringVar, ttk

EDGE_DRIVER_PATH = "msedgedriver.exe"

# Loading animation
def loader_animation(stop_event, loading_var):
    for frame in itertools.cycle(["─•────", "──•───", "───•──", "─────•"]):
        if stop_event.is_set():
            break
        loading_var.set(f"Fetching prices it takes few seconds... {frame}")
        time.sleep(1)
    loading_var.set("ദ്ദി(ᵔᗜᵔ)")

def get_zepto_price(product_name, driver):
    try:
        search_url = f"https://www.zeptonow.com/search?query={'+'.join(product_name.split())}"
        driver.get(search_url)
        
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

def get_swiggy_instamart_price(product_name, driver):
    try:
        search_url = f"https://www.swiggy.com/instamart/search?custom_back=true&query={'+'.join(product_name.split())}"
        driver.get(search_url)
        
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.sc-aXZVg.ihMJwf.JZGfZ"))
        )
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
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
    options.add_argument("--headless")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("window-size=1920x1080")
    
    results = []
    with webdriver.Edge(service=service, options=options) as driver:
        results.append(get_zepto_price(product_name, driver))
        results.append(get_swiggy_instamart_price(product_name, driver))
    
    return results

#Gui starts from here
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

    #price will be fetched in background via thread
    threading.Thread(target=fetch_prices_gui, args=(product_name, result_var, loading_var)).start()

# Create the GUI
def create_gui():
    root = tk.Tk()
    root.title("Price Scraper")
    root.geometry("600x500")
    root.config(bg="#f5f5f5")
    
    # Header Label
    header = tk.Label(root, text="🛍️ Price Scraper Tool", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
    header.pack(pady=10)
    
    # Input field
    tk.Label(root, text="Enter Product Name:", font=("Helvetica", 12), bg="#f5f5f5").pack(pady=10)
    entry_var = StringVar()
    entry_field = ttk.Entry(root, textvariable=entry_var, width=50)
    entry_field.pack(pady=5)
    
    # Fetch button
    result_var = StringVar()
    loading_var = StringVar()
    fetch_button = ttk.Button(root, text="Fetch Prices", command=lambda: start_fetching_prices(entry_var, result_var, loading_var))
    fetch_button.pack(pady=10)
    
    # Loading animation
    loading_label = tk.Label(root, textvariable=loading_var, font=("Helvetica", 12, "italic"), bg="#f5f5f5", fg="#555")
    loading_label.pack(pady=10)
    
    # Result display
    tk.Label(root, text="Results:", font=("Helvetica", 14, "bold"), bg="#f5f5f5", fg="#333").pack(pady=10)
    result_label = tk.Label(root, textvariable=result_var, wraplength=500, justify="center", anchor="w", bg="#e8e8e8", relief="solid", font=("Courier", 20))
    result_label.pack(pady=10, fill="both", expand=True, padx=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()