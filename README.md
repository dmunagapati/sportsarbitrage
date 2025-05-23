# Sports Arbitrage Bot

A multithreaded Python bot that scrapes real-time sports betting odds from multiple sportsbooks and identifies arbitrage opportunities with 2–4% profit margins. When an opportunity is found, it sends immediate email alerts to notify the user. The project is Dockerized and deployable on AWS EC2 for continuous uptime.

---

## Features

- Real-time scraping of 7+ sportsbooks (DraftKings, Caesars, Bovada, BetMGM, etc.)
- Multithreaded scraping with a 70% latency reduction
- Automated arbitrage alert system via email
- Identifies arbitrage edges using proprietary calculations
- Docker support for deployment on AWS EC2
- Tracks and logs potential arbitrage cases with timestamped records

---

## Tech Stack

- **Language**: Python  
- **Concurrency**: `threading`, `queue`  
- **Web Scraping**: `requests`, `BeautifulSoup`, `Selenium`  
- **Email Alerts**: `smtplib`, `email.mime`  
- **Deployment**: Docker, AWS EC2  
- **Others**: Custom date parsing, betting line analysis, JSON formatting

---

## Project Structure

```
├── main.py                      # Entry point for running the arbitrage system
├── scrape.py                    # Web scraping logic
├── thread_manager.py            # Manages scraper threads and concurrency
├── accumulator_thread.py        # Accumulates and processes odds
├── arb_tracker_thread.py        # Tracks arbitrage opportunities
├── sportbook_thread_manager.py  # Orchestrates scraping across sportsbooks
├── email_alert.py               # Sends email alerts
├── /possible_arbs               # Logs and data storage
├── Dockerfile                   # For containerized deployment
└── requirements.txt             # Python dependencies
```

---

## How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/dmunagapati/sportsarbitrage.git
cd sportsarbitrage
```

### 2. Set up Environment

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file with:

```
EMAIL_ADDRESS=youremail@example.com
EMAIL_PASSWORD=yourpassword
```

### 4. Run the Bot

```bash
python main.py
```

### 5. (Optional) Run via Docker

```bash
docker build -t sportsarbitrage .
docker run sportsarbitrage
```

---

## Sample Output

```
[+] Arbitrage Opportunity Found!
Team A: +150 on Caesars
Team B: -130 on BetMGM
Expected Profit Margin: 2.3%
Alert sent to user@example.com
```

---

## What I Learned

This project taught me how to:

- Optimize scraping latency with multithreading
- Design and orchestrate a multi-component backend system
- Work with asynchronous data pipelines and real-time notifications
- Deploy production-ready code using Docker and EC2
- Apply mathematical models to detect arbitrage in live financial data

---

## My Role

I developed this entire project from scratch — from designing the threading model and scraping architecture to alert logic and deployment. It reflects my ability to independently build and maintain scalable, user-facing backend systems.

---

## License

MIT
