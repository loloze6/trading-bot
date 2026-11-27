import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 5: continue
            c = b["close"]; r = c.pct_change()
            s30 = r.rolling(30, min_periods=15).std()
            mid = (b["high"] + b["low"]) / 2
            rng = (b["high"] - b["low"]) / c
            clv = 2 * (c - mid) / (b["high"] - b["low"]).replace(0, np.nan)  # -1 low .. +1 high
            width = rng / s30
            tr60 = c / c.shift(60) - 1
            d = pd.DataFrame({
                "coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r0": r, "r0z": r / s30, "clv": clv, "width": width,
                "nxt": c.shift(-1) / c - 1, "nxt2": c.shift(-2) / c.shift(-1) - 1,
                "s30": s30, "tr60": tr60,
                "inprof": (b["regime"] == "unknown"),
                "alloc": b["postRebalance_current_allocation"],
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["nxt"].mean()
    D["ex"] = D["nxt"] - D["coin"].map(drift)
    D["exz"] = D["ex"] / D["s30"]
    D = D.dropna(subset=["ex", "clv", "width", "s30"])

    def ct(sub, col="ex"):
        g = sub.groupby("day")[col].sum()
        n = len(sub)
        if len(g) < 5: return pd.Series({"n": n, "days": len(g), "mean": sub[col].mean(), "t": np.nan})
        return pd.Series({"n": n, "days": len(g), "mean": sub[col].mean(),
                          "t": g.mean() / (g.std() / np.sqrt(len(g)))})

    out = {}
    # fade signal: -clv*width, graded, in profile vs out
    D["fade"] = -D["clv"] * D["width"]
    D["fadeq"] = pd.qcut(D["fade"], 5, labels=False, duplicates="drop")
    D["trb"] = pd.cut(D["tr60"], [-9, -0.1, 0.1, 9], labels=["fall", "chop", "rise"])
    out["ex_by_fadeQ_inprof"] = D.groupby(["inprof", "fadeq"]).apply(ct).round(4)
    out["ex_by_fadeQ_trend"] = D.dropna(subset=["trb"]).groupby(["trb", "fadeq"]).apply(ct).round(4)
    # clv x width quintile, all bars
    D["wq"] = pd.qcut(D["width"], 3, labels=["narrow", "mid", "wide"])
    D["cq"] = pd.cut(D["clv"], [-1.01, -0.5, 0.5, 1.01], labels=["low", "middle", "high"])
    out["ex_by_close_width_all"] = D.groupby(["wq", "cq"]).apply(ct).round(4)
    # after large moves (r0z)
    D["mq"] = pd.qcut(D["r0z"], 5, labels=False)
    out["ex_by_todaymoveQ"] = D.groupby("mq").apply(ct).round(4)
    out["ex_by_todaymoveQ_trend"] = D.dropna(subset=["trb"]).groupby(["trb", "mq"]).apply(ct).round(4)
    # weekday
    out["ex_by_weekday"] = D.groupby("wd").apply(ct).round(4)
    # vol level
    D["sq"] = D.groupby("coin")["s30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["ex_fade_signed_by_volQ"] = D.assign(fx=np.sign(D["fade"]) * D["ex"] * (D["fade"].abs() > 1)).groupby("sq").apply(lambda s: ct(s, "fx")).round(4)

    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            dd.append(t.assign(coin=coin, win=w))
    DD = pd.concat(dd, ignore_index=True)
    bk = DD.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "std", "sum"]).round(5)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            T.append(t.assign(coin=coin, win=w))
    T = pd.concat(T, ignore_index=True)
    out["trades_by_side"] = T.groupby("side")[["net_profit_loss_percent", "profit_loss_percent", "duration_minutes"]].agg(["count", "mean"]).round(3)
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "sum"]).round(3)
    return out
