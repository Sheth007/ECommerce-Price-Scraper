def amazon_price(query):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    import time
    import random
    import webbrowser
    import os

    print("Initializing script...")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0"
    ]

    options = uc.ChromeOptions()
    options.add_argument(f"--user-agent={random.choice(user_agents)}")
    options.headless = True
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-renderer-backgrounding")  
    options.add_argument("--disable-background-timer-throttling")  
    options.add_argument("--disable-backgrounding-occluded-windows")

    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 2
    })

    try:
        print("Launching Amazon...")
        driver = uc.Chrome(options=options)

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        search_url = f"https://www.amazon.in/s?k={query}" 
        driver.get(search_url)
        # time.sleep(10)

        while driver.execute_script("return document.readyState") != "complete":
            time.sleep(1)

        def get_amazon_price(driver):
            try:
                prices = driver.find_element(By.XPATH, '//span[@class="a-price-whole"]')
                with open('Price.txt', 'a', encoding='utf-8') as f:
                    f.write(f"Amazon : ₹{prices.text.strip()}\n")

                print("Price fetched successfully.")
                return {query, prices.text.strip()}

            except Exception as e:
                with open('Price.txt', 'a', encoding='utf-8') as f:
                    f.write(f"\n Error fetching price: {str(e)}\n")

                print(f"Error fetching price: {str(e)}")
                return {"company": "Amazon", "price": f"Error: {str(e)}"}

        price_info = get_amazon_price(driver)
        print("Price information saved.")

    except Exception as e:
        print(f"Critical error: {str(e)}")

    finally:
        driver.quit()
        print("Browser closed.")

# Run the function
# amazon_price()