import pandas as pd
import numpy as np

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c / c.shift(1) - 1
            vol = r.rolling(30, min_periods=20).std()
            z = r / vol
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            rng = (b["high"] - b["low"]) / c
            body = (c - b["open"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "day": ts.dt.floor("D"),
                              "wd": ts.dt.weekday, "year": ts.dt.year, "r": r, "z": z,
                              "f1": f1, "f3": f3, "pos3": (np.arange(len(b)) % 3 == 0),
                              "agit": b["regime"] != "chop", "alloc": b["postRebalance_current_allocation"],
                              "closepos": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                              "r5": c / c.shift(5) - 1})
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift1 = D.groupby("coin")["f1"].mean()
    drift3 = D[D.pos3].groupby("coin")["f3"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift1)
    D["x3"] = D["f3"] - D["coin"].map(drift3)

    def ct(df, col):
        df = df.dropna(subset=[col])
        if len(df) < 10: return pd.Series({"n": len(df), "mean%": np.nan, "t": np.nan})
        m = df[col].mean()
        s = (df[col] - m).groupby(df["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(df)
        return pd.Series({"n": len(df), "days": G, "mean%": 100 * m, "t": m / se if se > 0 else np.nan})

    bins = [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf]
    D["zb"] = pd.cut(D["z"], bins)
    out = {}
    out["z bucket x agit, next-day excess"] = D.groupby(["agit", "zb"], observed=True).apply(lambda g: ct(g, "x1"))
    D3 = D[D.pos3]
    out["z bucket x agit, 3-day excess"] = D3.groupby(["agit", "zb"], observed=True).apply(lambda g: ct(g, "x3"))
    D["cpb"] = pd.cut(D["closepos"], [0, 0.2, 0.4, 0.6, 0.8, 1.0], include_lowest=True)
    out["close position in range x agit, next-day"] = D.groupby(["agit", "cpb"], observed=True).apply(lambda g: ct(g, "x1"))
    out["weekday, next-day excess (all)"] = D.groupby("wd").apply(lambda g: ct(g, "x1"))
    D["r5b"] = pd.qcut(D["r5"], 5)
    out["5-day return quintile x agit, next-day"] = D.groupby(["agit", "r5b"], observed=True).apply(lambda g: ct(g, "x1"))
    out["coin, ordinary rise agit next-day"] = D[D.agit & (D.z > 0) & (D.z <= 1)].groupby("coin").apply(lambda g: ct(g, "x1"))
    # book
    days = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            days.append(dd.assign(coin=coin, win=w))
    Dy = pd.concat(days, ignore_index=True)
    out["book by window: mean bp, coin mean bp"] = Dy.groupby("win")[["book_return", "coin_return"]].mean() * 1e4
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            tr.append(t.assign(coin=coin))
    T = pd.concat(tr, ignore_index=True)
    out["trades by side"] = T.groupby("side")[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"])
    return out
