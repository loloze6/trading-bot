"""Task 5.1 — data availability check. Run from trading-bot/ directory."""
import sys
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import datetime
import numpy as np
import pandas as pd
from data.data_manager import DataManager

SYMBOLS = ["BTCUSDT", "ETHUSDT"]
START = "2023-07-01"
END   = "2024-12-31"
INTERVAL_SECONDS = 3600  # 1h

start_dt = datetime.datetime.strptime(START, "%Y-%m-%d")
end_dt   = datetime.datetime.strptime(END,   "%Y-%m-%d")
expected_bars = int((end_dt - start_dt).total_seconds() / INTERVAL_SECONDS)

print(f"Data availability check: {START} to {END} (1h)")
print(f"Expected bars (per symbol): {expected_bars}")
print()

MAX_GAP_SECONDS = 86400  # 1 day — threshold to STOP

any_large_gap = False

for symbol in SYMBOLS:
    dm = DataManager(symbols=[symbol], interval_seconds=INTERVAL_SECONDS, mode="backtest")
    df = dm.fetch_historical_data(symbol, START, END)

    if df.empty:
        print(f"{symbol}: NO DATA RETURNED — cannot proceed")
        any_large_gap = True
        continue

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    actual_bars = len(df)
    diff = df["timestamp"].diff().dropna()
    expected_delta = pd.Timedelta(seconds=INTERVAL_SECONDS)
    gaps = diff[diff > expected_delta * 1.5]

    print(f"{symbol}:")
    print(f"  actual bars  : {actual_bars:,}")
    print(f"  expected bars: {expected_bars:,}")
    print(f"  gap count    : {len(gaps)}")

    if gaps.empty:
        print("  gaps         : none")
    else:
        for idx in gaps.index:
            gap_start = df.loc[idx - 1, "timestamp"]
            gap_end   = df.loc[idx,     "timestamp"]
            duration  = gap_end - gap_start
            dur_h     = duration.total_seconds() / 3600
            flag = " *** > 1 DAY ***" if duration.total_seconds() > MAX_GAP_SECONDS else ""
            print(f"  gap: {gap_start} → {gap_end}  ({dur_h:.1f}h){flag}")
            if duration.total_seconds() > MAX_GAP_SECONDS:
                any_large_gap = True
    print()

if any_large_gap:
    print("STOP: gap > 1 day detected. Report above. Do not proceed to 5.2 until user decides.")
    sys.exit(2)
else:
    print("OK: no gap > 1 day. Safe to proceed to 5.2.")
