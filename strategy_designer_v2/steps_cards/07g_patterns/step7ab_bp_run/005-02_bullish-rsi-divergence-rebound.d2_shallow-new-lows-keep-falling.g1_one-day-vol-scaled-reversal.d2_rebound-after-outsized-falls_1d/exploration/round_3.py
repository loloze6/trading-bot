import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            allr.append(c.pct_change().dropna())
        drift1 = pd.concat(allr).mean()
        sd10 = []
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            f = (c.shift(-10) / c - 1)[::10].dropna()
            sd10.append(f)
        usual10 = pd.concat(sd10).std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(20, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(c)),
                               "z5": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                               "z10": (c / c.shift(10) - 1) / (sd * np.sqrt(10)),
                               "year": ts.dt.year, "wnum": int(w[1:])})
            df["f10"] = c.shift(-10) / c - 1
            df["x10"] = df["f10"] - drift1 * 10
            df["s10"] = df["x10"] / usual10
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    g = d[d["pos"] % 10 == 0].dropna(subset=["z5", "z10", "x10"]).copy()
    for key in ("z5", "z10"):
        g["q"] = g.groupby("coin")[key].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
        m = g.groupby("q").agg(x=("x10", "mean"), sd=("x10", "std"), n=("x10", "count"), s=("s10", "mean"), k=(key, "mean"))
        m["t"] = m["x"] / (m["sd"] / np.sqrt(m["n"]))
        out[f"{key} quintile 10d excess (offset 0)"] = m.round(4)
        out[f"{key} q x coin"] = g.groupby(["coin", "q"])["x10"].mean().unstack().round(4)
        g["half"] = np.where(g["wnum"] <= 12, "w1-12", "w13-24")
        out[f"{key} q x half"] = g.groupby(["half", "q"])["x10"].mean().unstack().round(4)
        out[f"{key} top-q by year"] = g[g["q"] == 4].groupby("year")["x10"].agg(["mean", "count"]).round(4)
        sl = stats.linregress(g[key], g["x10"])
        out[f"{key} slope t"] = round(sl.slope / sl.stderr, 3)
        pos = g[g[key] > 0]
        sl = stats.linregress(pos[key], pos["x10"])
        out[f"{key} slope t rises only"] = round(sl.slope / sl.stderr, 3)
    return out
