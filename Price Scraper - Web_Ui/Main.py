import amazon
import flipkart
import jiomart
import bigbasket
import croma
import user_input as ui
import time
import sys
import os
import webbrowser

user_product = ui.user_enters_product_name()

print("1. Amazon")
amazon.amazon_price(user_product)
# time.sleep(2)

print("2. Flipkart")
flipkart.flipkart_price(user_product)
# time.sleep(2)

print("3. Jio Mart")
jiomart.JioMart_price(user_product)
# time.sleep(2)

print("4. Big Basket")
bigbasket.BigBasket_price(user_product)
# time.sleep(2)

print("5. Croma")
croma.croma_price(user_product)
# time.sleep(2)

print("Opening File")
txt_file = "Price.txt"
if os.path.exists(txt_file):
    webbrowser.open(txt_file)
else:
    print("File not found:", txt_file)

print("Exiting..........")
sys.exit()
print("Job Done 👍")