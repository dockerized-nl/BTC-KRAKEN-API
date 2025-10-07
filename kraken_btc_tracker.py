import requests
import matplotlib.pyplot as plt
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Kraken API Configuration
BASE_URL = "https://api.kraken.com/0/public"

# API Keys - Loaded from .env file for security
# These are only needed for private endpoints (trading, balance checking, etc.)
API_KEY = os.getenv('KRAKEN_API_KEY', '')
API_SECRET = os.getenv('KRAKEN_API_SECRET', '')

# Check if API keys are loaded (optional - only needed for private endpoints)
if API_KEY and API_SECRET:
    print("✓ API Keys loaded successfully")
else:
    print("ℹ️  No API keys found (not needed for public data)")
    print("   To add keys: Create a .env file with KRAKEN_API_KEY and KRAKEN_API_SECRET")

# Trading Pairs (Kraken notation)
TRADING_PAIRS = {
    'BTC/USD': 'XXBTZUSD',
    'ETH/USD': 'XETHZUSD',
    'XRP/USD': 'XXRPZUSD',
    'LTC/USD': 'XLTCZUSD',
    'ADA/USD': 'ADAUSD',
    'SOL/USD': 'SOLUSD',
    'DOT/USD': 'DOTUSD',
    'DOGE/USD': 'XDGUSD'
}

# Time Intervals (in minutes)
INTERVALS = {
    '1min': 1,
    '5min': 5,
    '15min': 15,
    '30min': 30,
    '1hour': 60,
    '4hour': 240,
    '1day': 1440,
    '1week': 10080,
    '15days': 21600
}


def get_24h_btc_prices(trading_pair='XXBTZUSD', interval=60, num_candles=24):
    # OHLC endpoint for getting candlestick data
    endpoint = f"{BASE_URL}/OHLC"
    
    # Parameters for the API request
    params = {
        'pair': trading_pair,
        'interval': interval
    }
    
    try:
        # Make the API request
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Check if the request was successful
        if data['error']:
            print(f"API Error: {data['error']}")
            return []
        
        # Extract the OHLC data
        # The data structure is: [timestamp, open, high, low, close, vwap, volume, count]
        ohlc_data = data['result'][trading_pair]
        
        # Get the last N hours of closing prices and volume
        # Each item in ohlc_data is: [time, open, high, low, close, vwap, volume, count]
        btc_24h_list = []
        
        for candle in ohlc_data[-num_candles:]:  # Get last N candles
            timestamp = candle[0]
            open_price = float(candle[1])   # Opening price
            high_price = float(candle[2])   # High price
            low_price = float(candle[3])    # Low price
            close_price = float(candle[4])  # Closing price
            volume = float(candle[6])       # Volume in BTC
            
            # Convert timestamp to readable format
            time_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
            
            btc_24h_list.append({
                'timestamp': timestamp,
                'time': time_str,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'price': close_price,
                'volume': volume
            })
        
        print(f"✓ Successfully fetched {len(btc_24h_list)} candles of {trading_pair} data")
        return btc_24h_list
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []


def calculate_fibonacci_levels(btc_24h_list):
    if not btc_24h_list:
        print("No data to calculate Fibonacci levels!")
        return None
    
    prices = [item['price'] for item in btc_24h_list]
    current_price = prices[-1]
    
    # Find swing high and swing low (highest and lowest points in 24h)
    swing_high = max(prices)
    swing_low = min(prices)
    
    # Calculate price difference
    diff = swing_high - swing_low
    
    # Determine trend direction
    # If price is closer to high, it's likely an uptrend
    # If price is closer to low, it's likely a downtrend
    price_position = (current_price - swing_low) / diff if diff > 0 else 0.5
    is_uptrend = price_position > 0.5
    
    # Calculate Fibonacci retracement levels
    # In uptrend: levels are calculated from high down
    # In downtrend: levels are calculated from low up
    if is_uptrend:
        fib_levels = {
            '0.0% (High)': swing_high,
            '23.6%': swing_high - (diff * 0.236),
            '38.2%': swing_high - (diff * 0.382),
            '50.0%': swing_high - (diff * 0.500),
            '61.8%': swing_high - (diff * 0.618),
            '78.6%': swing_high - (diff * 0.786),
            '100.0% (Low)': swing_low
        }
    else:
        fib_levels = {
            '0.0% (Low)': swing_low,
            '23.6%': swing_low + (diff * 0.236),
            '38.2%': swing_low + (diff * 0.382),
            '50.0%': swing_low + (diff * 0.500),
            '61.8%': swing_low + (diff * 0.618),
            '78.6%': swing_low + (diff * 0.786),
            '100.0% (High)': swing_high
        }
    
    # Determine current price zone and trading signal
    signal = "HOLD"
    zone = ""
    
    if is_uptrend:
        if current_price > fib_levels['23.6%']:
            zone = "Above 23.6%"
            signal = "STRONG - Consider taking profits"
        elif current_price > fib_levels['38.2%']:
            zone = "Between 23.6% and 38.2%"
            signal = "HOLD - Watch for reversal"
        elif current_price > fib_levels['50.0%']:
            zone = "Between 38.2% and 50%"
            signal = "BUY ZONE - Good entry point"
        elif current_price > fib_levels['61.8%']:
            zone = "Between 50% and 61.8%"
            signal = "STRONG BUY - Golden ratio support"
        else:
            zone = "Below 61.8%"
            signal = "WAIT - Possible trend reversal"
    else:
        if current_price < fib_levels['23.6%']:
            zone = "Below 23.6%"
            signal = "STRONG SELL - Consider exit"
        elif current_price < fib_levels['38.2%']:
            zone = "Between 23.6% and 38.2%"
            signal = "HOLD - Watch for bounce"
        elif current_price < fib_levels['50.0%']:
            zone = "Between 38.2% and 50%"
            signal = "SELL ZONE - Consider reducing position"
        elif current_price < fib_levels['61.8%']:
            zone = "Between 50% and 61.8%"
            signal = "CAUTION - Near golden ratio resistance"
        else:
            zone = "Above 61.8%"
            signal = "WAIT - Possible trend change"
    
    # Print Fibonacci analysis
    print("\n" + "="*50)
    print("📐 FIBONACCI RETRACEMENT ANALYSIS")
    print("="*50)
    print(f"Trend Direction:  {'📈 UPTREND' if is_uptrend else '📉 DOWNTREND'}")
    print(f"Swing High:       ${swing_high:,.2f}")
    print(f"Swing Low:        ${swing_low:,.2f}")
    print(f"Current Price:    ${current_price:,.2f}")
    print(f"Price Zone:       {zone}")
    print("-" * 50)
    print("Fibonacci Levels:")
    for level, price in fib_levels.items():
        marker = "👉" if abs(price - current_price) < diff * 0.05 else "  "
        print(f"{marker} {level:15s} ${price:,.2f}")
    print("-" * 50)
    print(f"💡 SIGNAL: {signal}")
    print("="*50 + "\n")
    
    return {
        'levels': fib_levels,
        'current_price': current_price,
        'signal': signal,
        'zone': zone,
        'is_uptrend': is_uptrend,
        'swing_high': swing_high,
        'swing_low': swing_low
    }


def analyze_volume(btc_24h_list):
    if not btc_24h_list:
        print("No data to analyze volume!")
        return None
    
    volumes = [item['volume'] for item in btc_24h_list]
    prices = [item['price'] for item in btc_24h_list]
    times = [item['time'] for item in btc_24h_list]
    
    # Calculate volume statistics
    total_volume = sum(volumes)
    avg_volume = total_volume / len(volumes)
    max_volume = max(volumes)
    min_volume = min(volumes)
    
    # Find the hour with highest volume
    max_volume_index = volumes.index(max_volume)
    max_volume_time = times[max_volume_index]
    max_volume_price = prices[max_volume_index]
    
    # Calculate price change during high volume periods
    # High volume hours are those above average
    high_volume_hours = [i for i, v in enumerate(volumes) if v > avg_volume]
    
    # Determine if volume is increasing or decreasing (trend)
    recent_volume_avg = sum(volumes[-6:]) / 6  # Last 6 hours
    earlier_volume_avg = sum(volumes[:6]) / 6   # First 6 hours
    volume_trend = "INCREASING 📈" if recent_volume_avg > earlier_volume_avg else "DECREASING 📉"
    
    # Volume-price divergence analysis
    price_change = prices[-1] - prices[0]
    volume_change = volumes[-1] - volumes[0]
    
    # Interpret volume patterns
    if price_change > 0 and recent_volume_avg > earlier_volume_avg:
        volume_signal = "BULLISH - Price up with increasing volume"
    elif price_change > 0 and recent_volume_avg < earlier_volume_avg:
        volume_signal = "CAUTION - Price up but volume decreasing (weak rally)"
    elif price_change < 0 and recent_volume_avg > earlier_volume_avg:
        volume_signal = "BEARISH - Price down with increasing volume"
    elif price_change < 0 and recent_volume_avg < earlier_volume_avg:
        volume_signal = "NEUTRAL - Price down but volume decreasing (weak sell-off)"
    else:
        volume_signal = "NEUTRAL - Price stable"
    
    # Print volume analysis
    print("\n" + "="*50)
    print("📊 VOLUME ANALYSIS")
    print("="*50)
    print(f"Total 24h Volume:     {total_volume:,.2f} BTC")
    print(f"Average Volume/Hour:  {avg_volume:,.2f} BTC")
    print(f"Highest Volume:       {max_volume:,.2f} BTC")
    print(f"  → Time: {max_volume_time}")
    print(f"  → Price: ${max_volume_price:,.2f}")
    print(f"Lowest Volume:        {min_volume:,.2f} BTC")
    print(f"Volume Trend:         {volume_trend}")
    print(f"Recent Volume Avg:    {recent_volume_avg:,.2f} BTC")
    print(f"Earlier Volume Avg:   {earlier_volume_avg:,.2f} BTC")
    print("-" * 50)
    print(f"💡 VOLUME SIGNAL: {volume_signal}")
    print("="*50 + "\n")
    
    return {
        'volumes': volumes,
        'total_volume': total_volume,
        'avg_volume': avg_volume,
        'max_volume': max_volume,
        'volume_signal': volume_signal,
        'volume_trend': volume_trend
    }


def plot_price_and_volume(btc_24h_list, fib_data=None, volume_data=None):
    if not btc_24h_list:
        print("No data to plot!")
        return
    
    prices = [item['price'] for item in btc_24h_list]
    volumes = [item['volume'] for item in btc_24h_list]
    times = [item['time'] for item in btc_24h_list]
    
    # Create figure with two subplots (price on top, volume on bottom)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10), 
                                     gridspec_kw={'height_ratios': [3, 1]},
                                     sharex=True)
    
    # ===== TOP PANEL: CANDLESTICK CHART =====
    for i, candle in enumerate(btc_24h_list):
        open_price = candle['open']
        high_price = candle['high']
        low_price = candle['low']
        close_price = candle['price']
        
        # Determine color (green for bullish, red for bearish)
        if close_price >= open_price:
            color = '#00c853'  # Green for bullish
            body_bottom = open_price
            body_height = close_price - open_price
        else:
            color = '#ff1744'  # Red for bearish
            body_bottom = close_price
            body_height = open_price - close_price
        
        # Draw the wick (high-low line)
        ax1.plot([i, i], [low_price, high_price], color='black', linewidth=1, zorder=1)
        
        # Draw the body (open-close rectangle)
        ax1.add_patch(plt.Rectangle((i - 0.3, body_bottom), 0.6, body_height,
                                     facecolor=color, edgecolor='black', linewidth=1, zorder=2))
    
    # Add Fibonacci levels if provided
    if fib_data:
        fib_colors = {
            '0.0% (High)': '#ff0000',
            '0.0% (Low)': '#00ff00',
            '23.6%': '#ff69b4',
            '38.2%': '#ffa500',
            '50.0%': '#9370db',
            '61.8%': '#ffd700',
            '78.6%': '#87ceeb',
            '100.0% (Low)': '#ff0000',
            '100.0% (High)': '#00ff00'
        }
        
        for level, price in fib_data['levels'].items():
            color = fib_colors.get(level, '#808080')
            linestyle = '-' if '61.8%' in level else '--'
            linewidth = 2 if '61.8%' in level else 1
            ax1.axhline(y=price, color=color, linestyle=linestyle, 
                       alpha=0.6, linewidth=linewidth, 
                       label=f'Fib {level}: ${price:,.0f}', zorder=3)
    
    # Customize price chart
    title = 'Bitcoin (BTC/USD) - Candlestick & Volume Analysis (24 Hours)'
    if fib_data:
        trend = 'UPTREND' if fib_data['is_uptrend'] else 'DOWNTREND'
        title += f' | {trend}'
    
    ax1.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax1.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3, linestyle='--', zorder=0)
    ax1.legend(loc='best', fontsize=8, ncol=2)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    ax1.set_xlim(-0.5, len(times) - 0.5)
    
    # ===== BOTTOM PANEL: VOLUME CHART =====
    # Color bars based on price movement (green for up, red for down)
    colors = []
    for i, candle in enumerate(btc_24h_list):
        if candle['price'] >= candle['open']:
            colors.append('#00c853')  # Green for bullish
        else:
            colors.append('#ff1744')  # Red for bearish
    
    ax2.bar(range(len(volumes)), volumes, color=colors, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Add average volume line
    if volume_data:
        ax2.axhline(y=volume_data['avg_volume'], color='blue', linestyle='--', 
                   linewidth=2, alpha=0.7, label=f"Avg Volume: {volume_data['avg_volume']:.1f} BTC")
    
    # Customize volume chart
    ax2.set_ylabel('Volume (BTC)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Hour', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3, linestyle='--', axis='y')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.set_xlim(-0.5, len(times) - 0.5)
    
    # Format x-axis labels (show every 4 hours)
    tick_positions = range(0, len(times), 4)
    tick_labels = [times[i].split()[1] for i in tick_positions]
    ax2.set_xticks(tick_positions)
    ax2.set_xticklabels(tick_labels, rotation=45)
    
    plt.tight_layout()
    plt.show()


def analyze_and_plot_24h(btc_24h_list, fib_data=None):
    if not btc_24h_list:
        print("No data to analyze!")
        return
    
    # Extract prices and times for analysis
    prices = [item['price'] for item in btc_24h_list]
    times = [item['time'] for item in btc_24h_list]
    
    # Calculate statistics
    current_price = prices[-1]
    min_price = min(prices)
    max_price = max(prices)
    avg_price = sum(prices) / len(prices)
    price_change = prices[-1] - prices[0]
    price_change_pct = (price_change / prices[0]) * 100
    
    # Print analysis
    print("\n" + "="*50)
    print("📊 24-HOUR BTC PRICE ANALYSIS")
    print("="*50)
    print(f"Current Price:    ${current_price:,.2f}")
    print(f"24h High:         ${max_price:,.2f}")
    print(f"24h Low:          ${min_price:,.2f}")
    print(f"24h Average:      ${avg_price:,.2f}")
    print(f"24h Change:       ${price_change:,.2f} ({price_change_pct:+.2f}%)")
    print(f"Volatility:       ${max_price - min_price:,.2f}")
    print("="*50 + "\n")
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(15, 8))
    
    # Plot candlesticks
    for i, candle in enumerate(btc_24h_list):
        open_price = candle['open']
        high_price = candle['high']
        low_price = candle['low']
        close_price = candle['price']
        
        # Determine color (green for bullish, red for bearish)
        if close_price >= open_price:
            color = '#00c853'  # Green for bullish
            body_bottom = open_price
            body_height = close_price - open_price
        else:
            color = '#ff1744'  # Red for bearish
            body_bottom = close_price
            body_height = open_price - close_price
        
        # Draw the wick (high-low line)
        ax.plot([i, i], [low_price, high_price], color='black', linewidth=1, zorder=1)
        
        # Draw the body (open-close rectangle)
        ax.add_patch(plt.Rectangle((i - 0.3, body_bottom), 0.6, body_height,
                                    facecolor=color, edgecolor='black', linewidth=1, zorder=2))
    
    # Add Fibonacci levels if provided
    if fib_data:
        fib_colors = {
            '0.0% (High)': '#ff0000',
            '0.0% (Low)': '#00ff00',
            '23.6%': '#ff69b4',
            '38.2%': '#ffa500',
            '50.0%': '#9370db',
            '61.8%': '#ffd700',
            '78.6%': '#87ceeb',
            '100.0% (Low)': '#ff0000',
            '100.0% (High)': '#00ff00'
        }
        
        for level, price in fib_data['levels'].items():
            color = fib_colors.get(level, '#808080')
            linestyle = '-' if '61.8%' in level else '--'
            linewidth = 2 if '61.8%' in level else 1
            ax.axhline(y=price, color=color, linestyle=linestyle, 
                       alpha=0.6, linewidth=linewidth, 
                       label=f'Fib {level}: ${price:,.0f}', zorder=3)
    else:
        # Add basic horizontal lines if no Fibonacci data
        ax.axhline(y=avg_price, color='green', linestyle='--', 
                    alpha=0.7, label=f'Average: ${avg_price:,.0f}')
        ax.axhline(y=max_price, color='red', linestyle=':', 
                    alpha=0.5, label=f'24h High: ${max_price:,.0f}')
        ax.axhline(y=min_price, color='orange', linestyle=':', 
                    alpha=0.5, label=f'24h Low: ${min_price:,.0f}')
    
    # Customize the plot
    title = 'Bitcoin (BTC/USD) - Last 24 Hours (Candlestick Chart)'
    if fib_data:
        trend = 'UPTREND' if fib_data['is_uptrend'] else 'DOWNTREND'
        title += f' | {trend}'
    
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel('Hour', fontsize=12)
    ax.set_ylabel('Price (USD)', fontsize=12)
    ax.grid(True, alpha=0.3, linestyle='--', zorder=0)
    ax.legend(loc='best', fontsize=8, ncol=2)
    
    # Format x-axis labels (show every 4 hours to avoid crowding)
    tick_positions = range(0, len(times), 4)
    tick_labels = [times[i].split()[1] for i in tick_positions]  # Show only time
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45)
    
    # Format y-axis to show prices with commas
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Set x-axis limits
    ax.set_xlim(-0.5, len(times) - 0.5)
    
    plt.tight_layout()
    plt.show()


# Main execution
if __name__ == "__main__":
    print("🚀 Starting Kraken Crypto Tracker...")
    print("-" * 50)
    
    # ===== CHOOSE YOUR PARAMETERS HERE =====
    
    # Example 1: Default - Bitcoin, 1-hour candles, last 24 hours
    trading_pair = TRADING_PAIRS['BTC/USD']  # Change to 'ETH/USD', 'XRP/USD', etc.
    interval = INTERVALS['1hour']             # Change to '5min', '15min', '4hour', etc.
    num_candles = 24                          # Number of candles to fetch
    
    print(f"📈 Analyzing: {[k for k, v in TRADING_PAIRS.items() if v == trading_pair][0]}")
    print(f"⏱️  Interval: {[k for k, v in INTERVALS.items() if v == interval][0]}")
    print(f"📊 Candles: {num_candles}")
    print("-" * 50)
    
    # Function 1: Get price data with custom parameters
    crypto_data = get_24h_btc_prices(trading_pair, interval, num_candles)
    
    if crypto_data:
        # Function 2: Basic statistics (integrated in plotting)
        
        # Function 3: Calculate Fibonacci levels and get trading signals
        fib_data = calculate_fibonacci_levels(crypto_data)
        
        # Function 4: Analyze trading volume
        volume_data = analyze_volume(crypto_data)
        
        # Create comprehensive plot with price and volume
        plot_price_and_volume(crypto_data, fib_data, volume_data)
        
        # Also show the basic analysis with Fibonacci
        analyze_and_plot_24h(crypto_data, fib_data)
    else:
        print("❌ Failed to fetch data. Please check your connection.")
    
    
# ===== HELPER FUNCTION: Show available options =====
def show_available_options():
    """
    Display all available trading pairs and intervals
    """
    print("\n" + "="*50)
    print("📋 AVAILABLE TRADING PAIRS:")
    print("="*50)
    for name, code in TRADING_PAIRS.items():
        print(f"  {name:15s} → {code}")
    
    print("\n" + "="*50)
    print("⏱️  AVAILABLE INTERVALS:")
    print("="*50)
    for name, minutes in INTERVALS.items():
        print(f"  {name:15s} → {minutes} minutes")
    print("="*50 + "\n")

# Uncomment the line below to see all available options
# show_available_options()


# ===== ADVANCED: Command Line Usage =====
"""
You can also run this script with command-line arguments:

Example 1: Default Bitcoin analysis
    python kraken_btc_tracker.py

Example 2: Analyze Ethereum with 4-hour candles
    python kraken_btc_tracker.py --pair ETH/USD --interval 4hour --candles 24

Example 3: Analyze Solana with 15-minute candles
    python kraken_btc_tracker.py --pair SOL/USD --interval 15min --candles 48

To enable command-line arguments, uncomment the code below:
"""

# import argparse
# 
# parser = argparse.ArgumentParser(description='Kraken Crypto Trading Analyzer')
# parser.add_argument('--pair', type=str, default='BTC/USD', 
#                     help='Trading pair (e.g., BTC/USD, ETH/USD)')
# parser.add_argument('--interval', type=str, default='1hour',
#                     help='Time interval (e.g., 1min, 5min, 1hour, 4hour)')
# parser.add_argument('--candles', type=int, default=24,
#                     help='Number of candles to fetch')
# 
# args = parser.parse_args()
# trading_pair = TRADING_PAIRS.get(args.pair, TRADING_PAIRS['BTC/USD'])
# interval = INTERVALS.get(args.interval, INTERVALS['1hour'])
# num_candles = args.candles