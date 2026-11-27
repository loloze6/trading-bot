import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True).copy()
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            b["loc"] = 2 * (b["close"] - b["low"]) / rng - 1
            b["ret"] = b["close"].pct_change()
            b["next"] = b["close"].shift(-1) / b["close"] - 1
            b["next3"] = b["close"].shift(-3) / b["close"] - 1
            b["ret5"] = b["close"] / b["close"].shift(5) - 1
            b["ret20"] = b["close"] / b["close"].shift(20) - 1
            b["vol20"] = b["ret"].rolling(20).std()
            b["rngrel"] = (rng / b["close"]) / (rng / b["close"]).rolling(20).median()
            b["wd"] = pd.to_datetime(b["timestamp"]).dt.dayofweek
            b["coin"] = coin; b["win"] = w
            b["pos"] = np.arange(len(b))
            b["held"] = b["postRebalance_current_allocation"].fillna(0)
            b["gain"] = b["held"] * b["next"]
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["next"].mean()
    d["ex"] = d["next"] - d["coin"].map(mu)
    sd = d.groupby("coin")["next"].std()
    d["z"] = d["ex"] / d["coin"].map(sd)
    out = {}
    def tab(g, col="ex"):
        return d.dropna(subset=[col]).groupby(g, observed=True)[col].agg(
            n="count", mean="mean", t=lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
    d["locq"] = pd.cut(d["loc"], [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out["next excess by close loc (all bars)"] = tab("locq")
    out["next excess by regime"] = tab("regime")
    d["inreg"] = d["regime"] == "mean_reversion"
    out["next excess by loc, in regime"] = d[d.inreg].dropna(subset=["ex"]).groupby("locq", observed=True)["ex"].agg(["count", "mean"])
    d["r1q"] = d.groupby("coin")["ret"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next z by today's return quintile"] = tab("r1q", "z")
    d["r5q"] = d.groupby("coin")["ret5"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next z by 5d return quintile"] = tab("r5q", "z")
    d["r20q"] = d.groupby("coin")["ret20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next z by 20d return quintile"] = tab("r20q", "z")
    d["rngq"] = d.groupby("coin")["rngrel"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next z by relative range quintile"] = tab("rngq", "z")
    d["volq"] = d.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["next z by vol20 quintile"] = tab("volq", "z")
    out["next z by weekday"] = tab("wd", "z")
    # loc x today's return sign
    d["upday"] = d["ret"] > 0
    out["next z by loc x upday"] = d.dropna(subset=["z"]).groupby(["upday", "locq"], observed=True)["z"].agg(["count", "mean"])
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    out["book daily by coin"] = dd.groupby("coin")[["book_return", "coin_return"]].mean()
    out["book daily by window"] = dd.groupby("win")["book_return"].agg(["count", "mean", "sum"])
    t = []
    for coin, wins in data["trades"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; t.append(x)
    t = pd.concat(t)
    out["trades by coin"] = t.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["held bars gain by loc bucket"] = d[d.held != 0].groupby("locq", observed=True)["gain"].agg(["count", "mean"])
    return out
