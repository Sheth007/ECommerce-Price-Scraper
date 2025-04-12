def flipkart_price(query):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    import time
    import random
    import json
    import os

    print("Initializing Flipkart scraper...")

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

    driver = None 

    try:
        print("Launching Flipkart...")
        driver = uc.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        search_url = f"https://www.flipkart.com/search?q={query}"
        driver.get(search_url)

        while driver.execute_script("return document.readyState") != "complete":
            time.sleep(1)

        print("Fetching price...")

        name = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a/div[2]/div[1]/div[1]')
        p_name = name.text.strip()

        prices = driver.find_element(By.XPATH, '//div[@class="Nx9bqj _4b5DiR"]')
        first_price = prices.text.strip()

        desc = driver.find_element(By.XPATH, '//div[@class="yKfJKb row"]')
        desc_details = desc.text.strip()

        img = driver.find_element(By.XPATH, '//div[contains(@class, "_4WELSP")]//img')
        img_src = img.get_attribute("src")
        p_image_link = img_src

        p_link = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[2]/div/div/div/a')
        href_link = p_link.get_attribute("href")
        p_link_text = href_link

        product_entry = {
            "Platform": "Flipkart",
            "Product Name": p_name,
            "Product Price": first_price,
            "Product Description": desc_details,
            "Product Image": p_image_link,
            "Product Link": p_link_text
        }

        return product_entry

    except Exception as e:
        print(f"⚠️ Error fetching Flipkart price: {str(e)}")

    finally:
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print("⚠️ Error while quitting Chrome:", e)