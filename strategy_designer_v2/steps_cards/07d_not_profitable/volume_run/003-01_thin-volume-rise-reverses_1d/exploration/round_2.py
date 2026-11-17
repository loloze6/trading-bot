import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        allr = pd.concat([bars[c][w]["close"].pct_change() for w in bars[c]])
        cm = allr.mean()
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True).copy()
            b["nxt1"] = b["close"].shift(-1) / b["close"] - 1
            b["nxt5"] = b["close"].shift(-5) / b["close"] - 1
            b["r1"] = b["close"].pct_change()
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["vr"] = b["volume"] / b["volume"].rolling(30, min_periods=10).mean()
            b["gain"] = b["postRebalance_current_allocation"] * b["nxt1"]
            b["mkt"] = b["postRebalance_current_allocation"] * cm
            b["coin"] = c; b["cm"] = cm; b["pos"] = np.arange(len(b))
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    a = B["postRebalance_current_allocation"]
    act = B[a.abs() > 1e-9].copy()
    act["fc0"] = act["forecast"].abs() < 1e-9
    out["active_split"] = act.groupby(["regime", "fc0"]).agg(
        n=("gain", "size"), gain=("gain", "mean"), mkt=("mkt", "mean"),
        alloc=("postRebalance_current_allocation", "mean"), nxt1=("nxt1", "mean"))
    out["totals"] = pd.Series({"gain_per_bar": B["gain"].sum() / len(B), "mkt_per_bar": B["mkt"].sum() / len(B),
                               "timing_per_bar": (B["gain"].sum() - B["mkt"].sum()) / len(B)})
    # signal bars: forecast<0, by regime and forecast size, next-day excess
    s = B[B["forecast"] < 0].copy()
    s["ex1"] = s["nxt1"] - s["cm"]
    s["fb"] = pd.cut(-s["forecast"], [0, 2, 8, 15, 20.1])
    out["sig_ex1_by_regime_fsize"] = s.groupby(["regime", "fb"])["ex1"].agg(["mean", "count"])
    # 5-day excess on non-overlap grid among signal bars, by trend
    g = s[s["pos"] % 5 == 0].dropna(subset=["nxt5"]).copy()
    g["ex5"] = g["nxt5"] - 5 * g["cm"]
    g["tr"] = pd.cut(g["ret30"], [-9, -0.1, 0, 0.1, 9])
    out["sig_ex5_by_regime_trend"] = g.groupby(["regime", "tr"])["ex5"].agg(["mean", "count"])
    # all signal bars (overlapping ok just for direction) by trend, next-day
    s["tr"] = pd.cut(s["ret30"], [-9, -0.1, 0, 0.1, 9])
    out["sig_ex1_by_trend"] = s.groupby("tr")["ex1"].agg(["mean", "count",
        lambda x: x.mean() / (x.std() / np.sqrt(len(x)))])
    # holding period of trades
    tl = []
    for c in data["trades"]:
        for w in data["trades"][c]:
            tl.append(data["trades"][c][w])
    T = pd.concat(tl)
    T["days"] = T["duration_minutes"] / 1440
    out["trades"] = T.groupby("entry_regime").agg(n=("days", "size"), days=("days", "mean"),
        pl=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"))
    return out
