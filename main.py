
import time
import pandas as pd
import random
from datetime import datetime
from binance.client import Client
import os

# Отримати API ключі з середовища
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

client = Client(API_KEY, API_SECRET)

def get_binance_price(symbol="BTCUSDT"):
    try:
        price = client.get_symbol_ticker(symbol=symbol)
        return float(price['price'])
    except Exception as e:
        print("Binance API Error:", e)
        return None

def load_memory():
    try:
        candles = pd.read_csv("memory_candles.csv")
        trades = pd.read_csv("memory_trades.csv")
        print(f"Loaded {len(candles)} candles and {len(trades)} trades.")
        return candles, trades
    except Exception as e:
        print("Error loading memory files:", e)
        return None, None

def simulate_confidence():
    return round(random.uniform(0.4, 0.9), 4)

def evaluate_trade(entry_price, direction):
    current_price = get_binance_price()
    if current_price is None:
        return 0
    if direction == "up":
        return 1 if current_price > entry_price else 0
    elif direction == "down":
        return 1 if current_price < entry_price else 0
    return 0

def write_trade(confidence, trend, correct):
    try:
        df = pd.read_csv("memory_trades.csv")
    except:
        df = pd.DataFrame(columns=["timestamp", "confidence", "trend", "correct"])

    df.loc[len(df)] = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "confidence": confidence,
        "trend": trend,
        "correct": correct
    }
    df.to_csv("memory_trades.csv", index=False)
    print(f"[WRITE] correct={correct}, confidence={confidence}, trend={trend}")

def run_bot():
    candles, _ = load_memory()
    if candles is not None:
        while True:
            print("ШТ-бот Elios працює...")
            confidence = simulate_confidence()
            trend = random.choice(["up", "down"])

            if confidence >= 0.58:
                print(f"[OK] Ставка дозволена. Достовірність: {confidence}")
                entry_price = get_binance_price()
                if entry_price:
                    print(f"[BINANCE] Поточна ціна: {entry_price}, тренд: {trend}")
                    time.sleep(300)  # 5 хвилин
                    correct = evaluate_trade(entry_price, trend)
                    write_trade(confidence, trend, correct)
            else:
                print(f"[SKIP] Пропуск ставки. Достовірність: {confidence}")

            time.sleep(60)
    else:
        print("Bot stopped due to memory loading error.")

if __name__ == "__main__":
    run_bot()
