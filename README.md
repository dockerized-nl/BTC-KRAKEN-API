# 🚀 Kraken Crypto Trading Analyzer

A powerful Python script for analyzing cryptocurrency price movements using Kraken API with advanced technical analysis including Fibonacci retracement levels, volume analysis, and professional candlestick charts.

## ✨ Features

- 📊 **Real-time price data** from Kraken API
- 🕯️ **Professional candlestick charts** with OHLC data
- 📐 **Fibonacci retracement analysis** with automatic buy/sell signals
- 📈 **Volume analysis** with trend indicators
- 🎨 **Dual-panel charts** (Price + Volume) like professional trading platforms
- 🔄 **Multiple cryptocurrencies** support (BTC, ETH, SOL, XRP, ADA, DOGE, and more)
- ⏱️ **Customizable timeframes** (1min to 1week intervals)
- 🔒 **Secure API key management** with .env files

## 🎯 What You'll Learn

This project teaches you:
- How to interact with cryptocurrency APIs
- Technical analysis fundamentals (Fibonacci, volume, candlestick patterns)
- Data visualization with matplotlib
- Secure credential management
- Professional trading chart creation

## 📋 Prerequisites

- Python 3.8 or higher
- Basic understanding of Python
- (Optional) Kraken API keys for private endpoints

## 🛠️ Installation

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <your-repo-url>
cd kraken-crypto-tracker

# Or simply download the kraken_btc_tracker.py file
```

### Step 2: Create a Virtual Environment

**Why use venv?** A virtual environment keeps your project dependencies isolated and prevents conflicts with other Python projects.

**On Linux/Mac:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt when activated.

### Step 3: Install Required Packages

```bash
pip install --upgrade pip
pip install requests matplotlib python-dotenv
```

**Required packages:**
- `requests` - For making API calls to Kraken
- `matplotlib` - For creating charts and visualizations
- `python-dotenv` - For secure API key management

**Optional: Create requirements.txt**

For easy installation in the future:
```bash
# Create requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt later
pip install -r requirements.txt
```

## 🔐 Setup (API Keys - Optional)

API keys are **NOT required** for fetching public market data (prices, charts). They're only needed for private operations like trading or checking account balances.

### If You Need API Keys:

1. **Get your Kraken API keys:**
   - Log in to [Kraken.com](https://www.kraken.com)
   - Go to Settings → API
   - Create new API key
   - Note: For this script, you only need "Query Funds" permission

2. **Create a .env file** in the same directory as the script:

```bash
# On Linux/Mac
touch .env

# On Windows
type nul > .env
```

3. **Add your keys to .env:**

```env
KRAKEN_API_KEY=your_api_key_here
KRAKEN_API_SECRET=your_api_secret_here
```

4. **Add .env to .gitignore** (CRITICAL for security):

```bash
echo ".env" >> .gitignore
```

## 🚀 Usage

### Basic Usage (Default: BTC, 1-hour candles, 24 hours)

```bash
# Make sure your virtual environment is activated!
python kraken_btc_tracker.py
```

### Customize Parameters

Edit the main section in `kraken_btc_tracker.py`:

```python
# Choose your cryptocurrency
trading_pair = TRADING_PAIRS['BTC/USD']  # Change this!

# Choose your time interval
interval = INTERVALS['1hour']             # Change this!

# Choose number of candles
num_candles = 24                          # Change this!
```

### Available Trading Pairs

```python
'BTC/USD'   # Bitcoin
'ETH/USD'   # Ethereum
'XRP/USD'   # Ripple
'SOL/USD'   # Solana
'ADA/USD'   # Cardano
'DOGE/USD'  # Dogecoin
'DOT/USD'   # Polkadot
'LTC/USD'   # Litecoin
```

### Available Time Intervals

```python
'1min'    # 1-minute candles
'5min'    # 5-minute candles
'15min'   # 15-minute candles
'30min'   # 30-minute candles
'1hour'   # 1-hour candles (default)
'4hour'   # 4-hour candles
'1day'    # Daily candles
'1week'   # Weekly candles
```

## 📊 Example Configurations

### Example 1: Ethereum with 4-hour candles (4 days of data)
```python
trading_pair = TRADING_PAIRS['ETH/USD']
interval = INTERVALS['4hour']
num_candles = 24
```

### Example 2: Bitcoin with 15-minute candles (6 hours of data)
```python
trading_pair = TRADING_PAIRS['BTC/USD']
interval = INTERVALS['15min']
num_candles = 24
```

### Example 3: Solana with 5-minute candles (2 hours of data)
```python
trading_pair = TRADING_PAIRS['SOL/USD']
interval = INTERVALS['5min']
num_candles = 24
```

### Example 4: Daily Bitcoin analysis (30 days of data)
```python
trading_pair = TRADING_PAIRS['BTC/USD']
interval = INTERVALS['1day']
num_candles = 30
```

## 📈 Understanding the Output

### Console Output

The script provides detailed analysis in the terminal:

1. **24-Hour Price Analysis**
   - Current price, high, low, average
   - 24h price change and percentage
   - Volatility measurement

2. **Fibonacci Retracement Analysis**
   - Trend direction (UPTREND/DOWNTREND)
   - Key Fibonacci levels (23.6%, 38.2%, 50%, 61.8%, 78.6%)
   - **Trading signals** (BUY/SELL/HOLD/WAIT)
   - Current price zone

3. **Volume Analysis**
   - Total 24h trading volume
   - Average volume per candle
   - Volume trend (increasing/decreasing)
   - **Volume-price divergence signals**

### Chart Output

You'll see **two professional trading charts**:

#### Chart 1: Candlestick + Volume (Dual Panel)
- **Top Panel:** Candlestick chart with Fibonacci levels
  - 🟢 Green candles = Price went up
  - 🔴 Red candles = Price went down
  - Colored lines = Fibonacci retracement levels
  - 🟡 Gold line = 61.8% (Golden Ratio - most important!)
  
- **Bottom Panel:** Volume bars
  - 🟢 Green bars = Bullish (price up)
  - 🔴 Red bars = Bearish (price down)
  - Blue dashed line = Average volume

#### Chart 2: Detailed Fibonacci Chart
- Candlestick chart with all Fibonacci levels
- Trend direction in title
- Good for detailed analysis

## 🎓 Understanding Technical Indicators

### Fibonacci Retracement Levels

Fibonacci levels help identify potential support/resistance areas:

- **61.8%** - "Golden Ratio" - Most important level
- **50.0%** - Psychological midpoint
- **38.2%** - Common retracement level
- **23.6%** - Minor retracement

**Trading Strategy:**
- **In UPTREND:** Look to BUY near 38.2%, 50%, or 61.8% levels
- **In DOWNTREND:** Look to SELL near these resistance levels

### Volume Analysis

Volume confirms price movements:

- **High volume + Price up** = Strong bullish signal ✅
- **High volume + Price down** = Strong bearish signal ✅
- **Low volume + Price up** = Weak rally (be cautious) ⚠️
- **Low volume + Price down** = Weak sell-off ⚠️

### Candlestick Patterns

Each candlestick shows 4 prices:
- **Open:** Starting price
- **High:** Highest price (top wick)
- **Low:** Lowest price (bottom wick)
- **Close:** Ending price

**Pattern Recognition:**
- Long green body = Strong buying
- Long red body = Strong selling
- Small body = Indecision (Doji)
- Long wicks = Price rejection

## 🔧 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"

Make sure you activated your virtual environment and installed packages:
```bash
source venv/bin/activate  # On Linux/Mac
pip install requests matplotlib python-dotenv
```

### "Glyph ... missing from font"

This warning is harmless and has been fixed in the latest version. If you still see it, update matplotlib:
```bash
pip install --upgrade matplotlib
```

### "API Error: ..."

- Check your internet connection
- Verify the trading pair name is correct
- Try a different interval
- If using API keys, verify they're correct in .env

### No Data Returned

- Kraken may have rate limits
- Try increasing the interval (use '1hour' instead of '1min')
- Check if the trading pair exists on Kraken

### Chart Not Displaying

- On Linux, you may need: `sudo apt-get install python3-tk`
- On Mac: Tkinter should be included
- On Windows: Tkinter is included with Python

## 📁 Project Structure

```
kraken-crypto-tracker/
├── kraken_btc_tracker.py    # Main script
├── .env                      # API keys (create this, don't commit!)
├── .gitignore               # Protects sensitive files
├── README.md                # This file
├── requirements.txt         # Python dependencies (optional)
└── venv/                    # Virtual environment (don't commit!)
```

## 🔒 Security Best Practices

- ✅ Always use virtual environments
- ✅ Store API keys in .env file
- ✅ Add .env to .gitignore
- ✅ Never commit API keys to Git
- ✅ Never share your .env file
- ✅ Use read-only API permissions when possible
- ✅ Regenerate API keys if exposed

## 🎯 Next Steps & Improvements

Want to enhance the script? Here are some ideas:

- [ ] Add RSI (Relative Strength Index) indicator
- [ ] Add Moving Averages (SMA/EMA)
- [ ] Add MACD (Moving Average Convergence Divergence)
- [ ] Add Support/Resistance level detection
- [ ] Add email/SMS alerts for trading signals
- [ ] Create a web dashboard with Flask/Django
- [ ] Add backtesting capabilities
- [ ] Implement automated trading (use with caution!)

## 📚 Learning Resources

- [Kraken API Documentation](https://docs.kraken.com/rest/)
- [Fibonacci Retracement Guide](https://www.investopedia.com/terms/f/fibonacciretracement.asp)
- [Candlestick Patterns](https://www.investopedia.com/trading/candlestick-charting-what-is-it/)
- [Volume Analysis](https://www.investopedia.com/articles/technical/02/091002.asp)

## ⚠️ Disclaimer

This script is for **educational purposes only**. It is NOT financial advice. 

- Cryptocurrency trading involves substantial risk
- Past performance does not guarantee future results
- Always do your own research (DYOR)
- Never invest more than you can afford to lose
- The author is not responsible for any financial losses

## 🤝 Contributing

Feel free to fork this project and submit pull requests with improvements!

## 📝 License

This project is open source and available for educational purposes.

## 💬 Support

If you encounter issues or have questions:
1. Check the Troubleshooting section
2. Review the Kraken API documentation
3. Make sure all dependencies are installed correctly

---

**Happy Trading! 🚀📈**

Remember: The best investment is in your education. Use this tool to learn, not to gamble!
