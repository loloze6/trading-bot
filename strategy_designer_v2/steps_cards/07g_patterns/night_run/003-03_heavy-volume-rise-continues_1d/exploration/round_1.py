import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    n = len(x)
    if n < 3 or x.std() == 0:
        return (np.nan, n)
    return (x.mean() / (x.std() / np.sqrt(n)), n)

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r = c.pct_change()
            sd = r.rolling(20, min_periods=15).std()
            z = r / sd
            rv = v / v.rolling(30, min_periods=20).mean()
            r20 = c / c.shift(20) - 1
            fwd = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            idx = np.arange(0, len(b), 5)
            g = pd.DataFrame({"coin": coin, "win": w, "z": z.iloc[idx].values, "rv": rv.iloc[idx].values,
                              "sd": sd.iloc[idx].values, "r20": r20.iloc[idx].values,
                              "fwd": fwd.iloc[idx].values, "fc": b["forecast"].iloc[idx].values,
                              "wd": pd.to_datetime(b["timestamp"].iloc[idx]).dt.dayofweek.values,
                              "yr": pd.to_datetime(b["timestamp"].iloc[idx]).dt.year.values})
            rows.append(g)
    G = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["sdr"] = G.groupby("coin")["sd"].rank(pct=True)
    out = {}
    H = G.dropna(subset=["z", "rv"]).copy()
    H["zb"] = pd.cut(H["z"], [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    H["rvb"] = pd.cut(H["rv"], [0, 0.8, 1.2, 99], labels=["thin", "mid", "heavy"])
    def agg(df, keys):
        return df.groupby(keys, observed=True)["ex"].agg(
            mean="mean", n="count", t=lambda x: _t(x)[0]).round(4)
    out["z x volume"] = agg(H, ["zb", "rvb"])
    out["z only"] = agg(H, ["zb"])
    out["vol level quintile"] = agg(G.assign(q=pd.cut(G["sdr"], 5, labels=False)), ["q"])
    out["past20 return quintile"] = agg(G.assign(q=G.groupby("coin")["r20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))), ["q"])
    out["weekday"] = agg(G, ["wd"])
    out["year"] = agg(G, ["yr"])
    out["forecast>=5 by coin"] = agg(G[G.fc >= 5], ["coin"])
    out["forecast>=5 by year"] = agg(G[G.fc >= 5], ["yr"])
    # book decomposition
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D, ignore_index=True)
    out["book mean daily, coin mean daily"] = pd.Series({"book": D["book_return"].mean(), "coin": D["coin_return"].mean(),
        "book_sd": D["book_return"].std(), "corr": D[["book_return", "coin_return"]].corr().iloc[0, 1]})
    return out
