
import time
import pandas as pd
import random

def load_memory():
    try:
        candles = pd.read_csv("memory_candles.csv")
        trades = pd.read_csv("memory_trades.csv")
        print(f"Loaded {len(candles)} candles and {len(trades)} trades.")
        return candles, trades
    except Exception as e:
        print("Error loading memory files:", e)
        return None, None

def simulate_confidence_and_decision():
    confidence = round(random.uniform(0.4, 0.9), 4)
    if confidence >= 0.58:
        print(f"[OK] Ставка дозволена. Confidence: {confidence}")
    else:
        print(f"[SKIP] Пропуск ставки. Confidence: {confidence}")

def run_bot():
    candles, trades = load_memory()
    if candles is not None and trades is not None:
        while True:
            print("Elios AI bot is running...")
            simulate_confidence_and_decision()
            time.sleep(60)
    else:
        print("Bot stopped due to memory loading error.")

if __name__ == "__main__":
    run_bot()
