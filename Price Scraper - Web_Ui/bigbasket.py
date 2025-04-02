def BigBasket_price(query):
    import undetected_chromedriver as uc
    from selenium.webdriver.common.by import By
    import time
    import random
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
        print("Launching BigBasket...")
        driver = uc.Chrome(options=options)

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        search_url = f"https://www.bigbasket.com/ps/?q={query}" 
        driver.get(search_url)
        # time.sleep(10)

        while driver.execute_script("return document.readyState") != "complete":
            time.sleep(1)

        def get_bigbasket_price(driver):
            try:
                prices = driver.find_element(By.XPATH, '//div[@class="Pricing___StyledDiv-sc-pldi2d-0 bUnUzR"]/span[@class="Label-sc-15v1nk5-0 Pricing___StyledLabel-sc-pldi2d-1 gJxZPQ AypOi"]')
                with open('Price.txt', 'a', encoding='utf-8') as f:
                    f.write(f"\nBigBasket : {prices.text.strip()}")

                print("Price fetched successfully.")
                return {query, prices.text.strip()}

            except Exception as e:
                with open('Price.txt', 'a', encoding='utf-8') as f:
                    f.write(f"\nError fetching price from BigBasket: {str(e)}")

                print(f"Error fetching price: {str(e)}")
                return {"company": "BB", "price": f"Error: {str(e)}"}

        price_info = get_bigbasket_price(driver)
        print("Price information saved.")

    except Exception as e:
        print(f"Critical error: {str(e)}")

    finally:
        driver.quit()
        print("Browser closed.")

# Run the function
# BigBasket_price()
