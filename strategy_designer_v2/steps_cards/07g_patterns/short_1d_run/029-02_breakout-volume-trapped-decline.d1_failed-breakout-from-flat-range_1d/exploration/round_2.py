import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "fwd": c.shift(-H) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "r1": r1,
                "z1": r1 / r1.rolling(20).std().shift(1),
                "ret20": c / c.shift(20) - 1,
                "above": c > c.shift(1).rolling(20).max(),
                "dist_hi": c / c.rolling(20).max() - 1,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            df["grid"] = (np.arange(n) % H) == 0
            df["coin"] = coin; df["win"] = w
            df["wnum"] = int(w[1:])
            recs.append(df)
        d = pd.concat(recs, ignore_index=True)
        g = d[d["grid"] & d["fwd"].notna()]
        drift = g["fwd"].mean(); sd = g["fwd"].std()
        d["unus"] = d["fwd"] - drift
        d["str"] = d["unus"] / sd
        d["unus1"] = d["fwd1"] - d["fwd1"].mean()
        rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    G = D[D["grid"] & D["fwd"].notna()].copy()
    res = {}

    def slope(df, x, y="unus"):
        df = df.dropna(subset=[x, y])
        if len(df) < 10:
            return pd.Series({"n": len(df), "slope": np.nan, "t": np.nan})
        r = stats.linregress(df[x], df[y])
        return pd.Series({"n": len(df), "slope": r.slope, "t": r.slope / r.stderr})

    def summ(df, col):
        out = df.groupby(col, observed=True)["unus"].agg(["count", "mean", "std"])
        out["t"] = out["mean"] / (out["std"] / np.sqrt(out["count"]))
        out["strength"] = df.groupby(col, observed=True)["str"].mean()
        return out.drop(columns="std").round(4)

    G["z1c"] = G["z1"].clip(-4, 4)
    res["slope_z1_pooled"] = slope(G, "z1c").round(5)
    res["slope_z1_by_coin"] = G.groupby("coin").apply(lambda x: slope(x, "z1c")).round(5)
    G["half"] = np.where(G["wnum"] <= 12, "w1-w12", "w13-w24")
    res["slope_z1_by_half"] = G.groupby("half").apply(lambda x: slope(x, "z1c")).round(5)
    res["slope_z1_by_year"] = G.groupby("year").apply(lambda x: slope(x, "z1c")).round(5)
    G["upday"] = np.where(G["z1"] > 1, "z>1", np.where(G["z1"] < -1, "z<-1", "mid"))
    res["upday_by_coin"] = summ(G[G["upday"] == "z>1"], "coin")
    res["upday_by_half"] = summ(G[G["upday"] == "z>1"], "half")
    res["slope_ret20_pooled"] = slope(G, "ret20").round(5)
    res["slope_ret20_by_coin"] = G.groupby("coin").apply(lambda x: slope(x, "ret20")).round(5)
    res["slope_disthi_pooled"] = slope(G, "dist_hi").round(5)
    res["slope_disthi_by_half"] = G.groupby("half").apply(lambda x: slope(x, "dist_hi")).round(5)
    res["above20_by_half"] = summ(G[G["above"]], "half")
    # weekday next day (non-overlapping by construction for h=1: all bars)
    A = D.dropna(subset=["fwd1"])
    wd = A.groupby("wd")["unus1"].agg(["count", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    res["weekday_next1d"] = wd.drop(columns="std").round(5)
    return res
