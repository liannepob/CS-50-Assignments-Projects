# CS50 Finance

A web-based stock trading simulation built with **Python**, **Flask**, and **SQLite**, part of Harvard's CS50 course.

---

## Overview

This application allows users to simulate buying and selling stocks in real time. Users can register, log in, view stock quotes, and manage their portfolio, including cash balance and transaction history.

---

## Features

* User registration and login
* Lookup real-time stock quotes
* Buy and sell stocks with cash balance management
* Portfolio overview with stock values and total assets
* Transaction history with timestamps
* Password change functionality

---

## Technologies Used

* **Python 3**
* **Flask**
* **SQLite**
* **CS50 Library**
* **Bootstrap** for front-end styling

---

## Setup & Installation

1. **Clone the repository:**

```bash
git clone <your-repo-url>
cd finance
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set environment variables (Linux/Mac):**

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export API_KEY=<your_iex_cloud_api_key>
```

Windows (Command Prompt):

```cmd
set FLASK_APP=app.py
set FLASK_ENV=development
set API_KEY=<your_iex_cloud_api_key>
```

4. **Run the app:**

```bash
flask run
```

5. **Open your browser** and go to [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Usage

* Register a new account
* Login with your credentials
* Quote a stock by entering its ticker symbol
* Buy and Sell shares
* View Portfolio for your current holdings and cash balance
* Check History for all previous transactions

---

## Database Schema

**users**

* `id` INTEGER PRIMARY KEY
* `username` TEXT UNIQUE NOT NULL
* `hash` TEXT NOT NULL
* `cash` REAL DEFAULT 10000.00

**user_portfolio**

* `id` INTEGER PRIMARY KEY AUTOINCREMENT
* `user_id` INTEGER NOT NULL
* `symbol` TEXT NOT NULL
* `shares` INTEGER NOT NULL
* `price` REAL NOT NULL
* `time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
* `deal` TEXT NOT NULL

---

## Screenshots

*(Add screenshots of your app here: login, quote, buy, sell, portfolio, history.)*

---

## License

This project is for educational purposes and follows the [CS50 Academic Honesty Policy](https://cs50.harvard.edu/college/2025/academic-honesty/).

---

**Author:** Lianne Poblador
