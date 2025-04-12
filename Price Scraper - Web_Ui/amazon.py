def amazon_price(query):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    import time
    import random
    import webbrowser
    import os
    import json

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

        while driver.execute_script("return document.readyState") != "complete":
            time.sleep(1)

        try:
            div = driver.find_element(By.ID, "puisg-col-inner")
            
            driver.execute_script("arguments[0].style.display = 'none';", div)
            
            print("Div blocked/hidden successfully.")

        except Exception as e:
            print("Could not find the element:", e)

        print("Fetching price...")

        p_name = query

        prices = driver.find_element(By.XPATH, '//span[@class="a-price"]')
        first_price = prices.text.strip()

        p_link = driver.find_element(By.XPATH, '//a[contains(@class, "a-link-normal") and contains(@class, "s-line-clamp-2") and contains(@href, "/dp/")]')
        href_link = p_link.get_attribute("href")
        p_link_text = href_link

        product_entry = {
            "Platform": "Amazon",
            "Product Name": p_name,
            "Product Price": first_price,
            "Product Link": p_link_text
         }
      
        return product_entry

    except Exception as e:
        print(f"⚠️ Error fetching Amazon price: {str(e)}")
        return None

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print("⚠️ Error while quitting Chrome:", e)