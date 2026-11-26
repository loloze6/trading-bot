import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-H) / c - 1,
                "ret28": c / c.shift(28) - 1,
                "ret7": c / c.shift(7) - 1,
                "ret1": r1,
                "dist": 1 - c / c.rolling(28).max(),
                "distlow": c / c.rolling(28).min() - 1,
                "vol20": r1.rolling(20).std(),
                "rng": ((hi - lo) / c).rolling(28).mean() / ((hi - lo) / c).rolling(90, min_periods=40).mean(),
                "vrel": v.rolling(28).mean() / v.rolling(90, min_periods=40).mean(),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": np.arange(len(b)),
            })
            df["grid"] = df["pos"] % H == 0
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A["grid"] & A["fwd"].notna()].copy()
    G["ex"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    out = {}

    def qtab(sub, col, q=5):
        s = sub.dropna(subset=[col, "ex"]).copy()
        s["q"] = pd.qcut(s[col].rank(method="first"), q, labels=False)
        t = s.groupby("q").agg(n=("ex", "size"), xmean=(col, "mean"), ex_mean=("ex", "mean"),
                               ex_t=("ex", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))))
        lr = stats.linregress(s[col], s["ex"])
        t.loc["slope_t"] = [len(s), np.nan, lr.slope, lr.slope / lr.stderr]
        return t

    tr = G[G["ret28"] > 0]
    nt = G[G["ret28"] <= 0]
    out["trend: dist quintiles"] = qtab(tr, "dist")
    out["trend: ret28 quintiles"] = qtab(tr, "ret28")
    out["down: ret28 quintiles"] = qtab(nt, "ret28")
    out["down: distlow quintiles"] = qtab(nt, "distlow")
    out["all: ret28 quintiles"] = qtab(G, "ret28")
    out["all: ret7 quintiles"] = qtab(G, "ret7")
    out["all: ret1 quintiles"] = qtab(G, "ret1")
    out["all: vol20 quintiles"] = qtab(G, "vol20")
    out["trend: vol20 quintiles"] = qtab(tr, "vol20")
    out["trend: vrel quintiles"] = qtab(tr, "vrel")
    calm = nt[(nt["rng"] < 1) & (nt["vrel"] < 1.1)]
    out["calm down: ret28 quintiles"] = qtab(calm, "ret28", 4)
    out["trend: by coin"] = tr.groupby("coin")["ex"].agg(["size", "mean"])
    # book daily
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["wd"] = pd.to_datetime(d["day"]).dt.weekday
            D.append(d)
    D = pd.concat(D, ignore_index=True)
    out["book by weekday"] = D.groupby("wd")[["book_return", "coin_return"]].mean()
    out["book by window"] = D.groupby("win")[["book_return", "coin_return"]].mean()
    tdf = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    tdf["ef"] = pd.qcut(tdf["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry_forecast q"] = tdf.groupby("ef")["net_profit_loss_percent"].agg(["size", "mean", "median"])
    out["trades dur days"] = tdf["duration_minutes"].describe() / 1440
    return out
