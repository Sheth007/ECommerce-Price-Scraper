from flask import Flask, render_template, request,jsonify
import amazon, flipkart, jiomart, croma ,bigbasket
import time, os

app = Flask(__name__)

txt_file = "price.json"  # File where prices are stored

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product = request.form["product"]  # Get input from HTML form

        # Clear the file before writing new data
        #,encoding="utf-8"
        with open(txt_file, "r+") as f:
            f.write("")

        # Fetch prices from different websites and store them in the file
        # amazon.amazon_price(product)
        # time.sleep(2)
        # flipkart.flipkart_price(product)
        # time.sleep(2)
        # bigbasket.BigBasket_price(product)
        # time.sleep(2)
        # jiomart.JioMart_price(product)
        # time.sleep(2)
        croma.croma_price(product)

        return render_template("status.html",product_name=product)  # Redirect to status page

    return render_template("index.html")

@app.route("/fetch_prices", methods=["GET"])
def fetch_prices():
    """Reads the stored prices from Price.txt and returns them in a structured format."""
    prices_list = []
    
    if os.path.exists(txt_file):
        with open(txt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if line:
                parts = line.split(" : ")  # Split by " : "
                if len(parts) == 2:
                    platform, price = parts
                    prices_list.append({"platform": platform.strip(), "price": price.strip()})
    
    return jsonify({"prices": prices_list})


if __name__ == "__main__":
    app.run(debug=True)


