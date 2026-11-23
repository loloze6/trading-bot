"""Topic 47, the trade table (operator, 2026-11-23: "how to increase the winning rate; the profile of losing trades;
limit them; increase the winners"). Every trade of every real book of night 5 (step 5 confirmed), from the engine's
trade diagnostics (trade_diagnostics.json.gz: result, MAE, MFE, exit efficiency, what the price did after the exit),
joined with what was known at its entry:
  - the forecast at the entry bar (chart files), its size |forecast|;
  - the coin at the previous day's close (local daily bars): 20-day volatility, 30-day return, distance below its
    90-day high, the day's volume against its 20-day mean;
  - the market (equal-weight of the six default coins) at the previous day's close: 30-day return, 20-day volatility;
  - how many of the book's coins entered on the same day; weekday (and hour on hourly bars); side.
Why this can't leak: every entry feature is computed from closes up to the day before the entry day (the forecast is
the engine's own value at the entry bar, computed from that bar's close and earlier). Fold: windows 1-6, 7-12, 13-18,
19-24 (step 4 numbers windows in the folds' order). Writes trades.csv.gz (57 MB: kept out of git; give a path).  python3 topics/47_review/trade_table.py [OUT]"""
import glob, gzip, json, pathlib, sys, warnings
import numpy as np, pandas as pd

warnings.simplefilter("ignore")
STEPS = pathlib.Path(__file__).resolve().parents[2]
DATA = STEPS.parents[1] / "trading-bot" / "local_data"
DEFAULT = ["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]


def coin_state(coin):
    d = pd.read_csv(DATA / f"kraken_{coin}_1d.csv", usecols=["timestamp", "close", "volume"], parse_dates=["timestamp"]).set_index("timestamp")
    r = d.close.pct_change()
    s = pd.DataFrame({"vol20": r.rolling(20).std(), "ret30": d.close / d.close.shift(30) - 1,
                      "below_high90": d.close / d.close.rolling(90).max() - 1, "volume_ratio": d.volume / d.volume.rolling(20).mean(),
                      "ret1": r})
    return s.shift(1)                                    # the state known at the previous day's close


states = {}
def state(c):
    if c not in states: states[c] = coin_state(c)
    return states[c]


mk = pd.concat({c: state(c).ret1 for c in DEFAULT}, axis=1).mean(axis=1)
market = pd.DataFrame({"market_ret30": (1 + mk).rolling(30).apply(np.prod, raw=True) - 1, "market_vol20": mk.rolling(20).std()})

gate = pd.read_csv(pathlib.Path(__file__).with_name("calmar_gate.csv"))
parts = []
for b in gate.itertuples():
    rec = STEPS / "04_backtest" / b.run / "backtests" / b.backtest
    tr = {}
    for f in glob.glob(str(rec / "*" / "*" / "trade_diagnostics.json.gz")):
        for t in json.load(gzip.open(f))["trades"]:
            tr[t["trade_id"]] = t
    if not tr: continue
    t = pd.DataFrame(tr.values())
    t["entry_time"] = pd.to_datetime(t.entry_time)
    bars = pd.read_csv(rec / "chart_bars.csv.gz", usecols=["coin", "window", "timestamp", "forecast"], parse_dates=["timestamp"])
    t = t.merge(bars.rename(columns={"coin": "symbol", "timestamp": "entry_time"}), on=["symbol", "entry_time"], how="left")
    t["w"] = t.window_y.str[1:].astype(float) if "window_y" in t else t.window.str[1:].astype(float)
    t["fold"] = ((t.w - 1) // 6 + 1)
    t["day"] = t.entry_time.dt.normalize()
    feats = pd.concat({c: state(c) for c in t.symbol.unique()}, names=["symbol", "day"])
    t = t.join(feats, on=["symbol", "day"]).join(market, on="day")
    t["crowd"] = t.groupby("day").symbol.transform("nunique")
    t["weekday"] = t.entry_time.dt.dayofweek; t["hour"] = t.entry_time.dt.hour
    t["net_pct"] = t.realized_return - t.cost_paid / 100
    t["win"] = t.net_pct > 0
    t["abs_forecast"] = t.forecast.abs()
    t["run"], t["book"], t["bar"], t["pays"] = b.run, b.backtest, b.backtest[-2:], b.pays
    keep = ["run", "book", "bar", "pays", "symbol", "fold", "direction", "entry_time", "holding_bars", "net_pct", "win", "mae", "mfe",
            "exit_efficiency", "post_exit_return_5bars", "post_exit_return_20bars", "net_portfolio_return_pct", "abs_forecast",
            "vol20", "ret30", "below_high90", "volume_ratio", "market_ret30", "market_vol20", "crowd", "weekday", "hour"]
    parts.append(t[keep])
d = pd.concat(parts, ignore_index=True)
OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).with_name("trades.csv.gz")
d.to_csv(OUT, index=False, float_format="%.5g")
print(f"trades {len(d)}, books {d.book.nunique()}, with a forecast {d.abs_forecast.notna().mean():.0%}, with coin state {d.vol20.notna().mean():.0%}")
print(d.groupby(["pays", "bar"]).agg(trades=("win", "size"), books=("book", "nunique"), win_rate=("win", "mean"), mean_net=("net_pct", "mean")).round(3))
