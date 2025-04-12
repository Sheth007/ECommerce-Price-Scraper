from flask import Flask, render_template, request,jsonify
import amazon, flipkart, jiomart, croma
import time

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        product = request.form["product"]  

        return render_template("status.html",product_name=product)

    return render_template("index.html")

@app.route("/fetch_prices", methods=["GET"])
def fetch_prices():
    """Reads the stored prices from Price.txt and returns them in a structured format."""
    prices_list = []

    query = request.args.get("product")
    if not query:
        return jsonify({"Error":"Missing product name"}),400 
    
    try:
        prices_list.append(amazon.amazon_price(query=query))
    except Exception as e:
        print("Amazon Error---", e)
   
    try:
        prices_list.append(flipkart.flipkart_price(query=query))
    except Exception as e:
        print("Flipkart Error---",e)

    try:
        prices_list.append(jiomart.JioMart_price(query=query))
    except Exception as e:
        print("Jiomart Error---",e)

    try:
        prices_list.append(croma.croma_price(query=query))
    except Exception as e:
        print("Croma Error---",e)
    
    return jsonify({"prices": prices_list})


if __name__ == "__main__":
    app.run(debug=True)