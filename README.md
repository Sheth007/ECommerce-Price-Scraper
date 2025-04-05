# 🛒 ECommerce Price Scraper

A powerful and flexible tool to **track and compare prices** of products from multiple Indian e-commerce platforms. Whether you prefer a graphical UI, a command-line interface, or a web interface — this project has it all!

## 🚀 Features

- 🔍 Search and scrape real-time product prices from popular e-commerce websites.
- 💻 Three modes of usage:
  - **GUI**: Tkinter-based desktop app.
  - **CLI**: Terminal-based for quick and lightweight use.
  - **WebUI**: Flask-powered web interface.
- 🧠 Efficient scraping with Selenium and BeautifulSoup.
- 📦 Modular code structure for easy customization and extension.

## 📁 Project Structure

```
ECommerce-Price-Scraper/
│
├── App/        # Desktop app using Tkinter
├── CLI/        # Command-line interface
├── WebUI/      # Web interface using Flask
├── README.md
└── requirements.txt
```

## 🔧 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Sheth007/ECommerce-Price-Scraper.git
cd ECommerce-Price-Scraper
```

2. **Install dependencies**
```bash
pip install selenium
pip install beautifulsoup4
pip install flask
pip install undetected-chromedriver
```

> 🔐 Note: Some sites may block headless scraping. If issues arise, try running without headless mode or consider using proxies/user-agent rotation.

---

## 💡 How to Use

### 🖥 GUI (Tkinter)
```bash
cd App
python app.py
```

### ⚙️ CLI
```bash
cd CLI
python scraper.py "product name"
```

### 🌐 Web Interface
```bash
cd WebUI
python app.py
```
Then, visit `http://127.0.0.1:5000/` in your browser.

---

## 📌 Tech Stack

- **Python**
- **Selenium**
- **BeautifulSoup**
- **Tkinter**
- **Flask**

---

## 📌 Todo / Improvements

- [ ] Add support for more e-commerce platforms (e.g., Amazon, Flipkart, Reliance Digital)
- [ ] Export results to CSV/Excel
- [ ] Add proxy & headless mode toggles in settings
- [ ] Dockerize for easy deployment

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork this repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes and commit them.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE), meaning you're free to use, modify, and distribute it with attribution.

---

## 🙌 Acknowledgements

Thanks to the open-source community for the tools and libraries that power this project.

---

## ✨ Author

**[Sheth007](https://github.com/Sheth007)** – Building tools to make price comparison easier and smarter.

---

⭐ **Star this repo** if you find it helpful!
