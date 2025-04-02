import config

def user_enters_product_name():  # Corrected function name
    config.query = input("Enter product name: ").strip()  # Corrected input
    print(f"Product set to: {config.query}")  # Confirmation message
    return config.query  # Return the value for use in main.py