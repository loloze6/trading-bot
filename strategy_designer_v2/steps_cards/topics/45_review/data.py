"""Shared loader for the investigation: daily closes of the local Kraken files, fold years only (2018-2025): the
unseen periods (2016-17, 2026) and the sealed one are never read into an analysis."""
import json, pandas as pd, numpy as np
import os
TB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../trading-bot")
CORE = ["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]
ALL = ["AAVEUSD", "ADAUSD", "AVAXUSD", "BTCUSD", "DOGEUSD", "ETHUSD", "INJUSD", "LINKUSD", "LTCUSD", "NEARUSD", "ONDOUSD",
       "SOLUSD", "SUIUSD", "TAOUSD", "TRXUSD", "UNIUSD", "XMRUSD", "XRPUSD", "ZECUSD"]
START, END = "2018-01-01", "2025-12-31"
cm = json.load(open(f"{TB}/config/cost_model.json"))["kraken"]["futures"]
def cost_bps(c): return cm["fee_bps"] + cm["slippage_bps"].get(c, cm["slippage_bps"]["default"])
def closes(coins, start=START, end=END, warm=400):
    """Closes with `warm` days before START for warm-up (still inside fold years' preceding data, 2016-17 excluded:
    warm-up starts no earlier than 2017-01-01... it is cut at 2017-01-01 if earlier would reach 2016)."""
    out = {}
    for c in coins:
        d = pd.read_csv(f"{TB}/local_data/kraken_{c}_1d.csv", usecols=["timestamp", "close", "volume"])
        d["timestamp"] = pd.to_datetime(d["timestamp"]); d = d.set_index("timestamp")
        out[c] = d["close"]
    px = pd.DataFrame(out).sort_index()
    return px.loc[:end]
