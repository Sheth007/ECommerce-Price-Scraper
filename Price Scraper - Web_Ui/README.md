# 🌐 Price Scraper - Web UI

A lightweight **Flask-based web app** for scraping product prices from Indian e-commerce websites. Designed for users who prefer a browser experience.

> ⚠️ **Note:** This project is currently in active development. Output is saved to a `price.json` file and **not yet displayed on the webpage**.

---

## ✨ Features

- 🌍 Web-based interface powered by Flask
- 🔍 Real-time product price scraping
- 📁 Results saved to `price.json`

---

## 📋 TODO List

Here's what's planned:

### ✅ Current Progress
- [x] Scraping backend (Selenium + BeautifulSoup)
- [x] Save results to `price.json`
- [x] UI styling
- [x] Add error handling and loading indicators
- [x] Input form on homepage
- [x] Flask app setup

### 🔜 Upcoming Features
- [ ] Display scraped results on the webpage
- [ ] Option to download results (CSV/JSON)
- [ ] Deploy using Render/Heroku

---

## 📦 Used Libraries

- `flask`
- `selenium`
- `undetected_chromedriver`
- `bs4` (BeautifulSoup)

> Install the required packages:
```bash
pip install flask selenium beautifulsoup4 undetected-chromedriver
```

---

## ⚙️ Setup & Run

1. **Clone the repo**
```bash
git clone https://github.com/Sheth007/ECommerce-Price-Scraper.git
cd "ECommerce-Price-Scraper/Price Scraper - Web_Ui"
```

2. **Ensure you have:**
   - Python 3.7+
   - Google Chrome latest version

3. **Run the Flask app**
```bash
python app.py
```
Visit: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🎥 Demo (Coming Soon)

> A demo video will be added once the frontend is connected to display the results.

---

## 👨‍💻 Author

Built by [Sheth007](https://github.com/Sheth007)  
Explore the full project: [ECommerce-Price-Scraper](https://github.com/Sheth007/ECommerce-Price-Scraper)

---

⭐ **Star this repo** to support the development!
