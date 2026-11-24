import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); o = b["open"].astype(float)
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "r1": r1,
                               "vol20": r1.rolling(20).std(),
                               "r3p": c / c.shift(3) - 1,
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1, "f5": c.shift(-5) / c - 1,
                               "pos": np.arange(len(b)), "year": ts.dt.year,
                               "dkey": ts.dt.floor("D").astype("int64") // 86400_000_000_000,
                               "s20": (c / c.shift(20) - 1) / (r1.rolling(20).std() * np.sqrt(20))})
            df["z"] = df["r1"] / df["vol20"]
            df["z3"] = df["r3p"] / (df["vol20"] * np.sqrt(3))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def clus_t(d, col):
        g = d.groupby("dkey")[col].sum()
        n = d[col].notna().sum()
        m = d[col].mean()
        dev = d[col] - m
        s = dev.groupby(d["dkey"]).sum()
        se = np.sqrt((s ** 2).sum()) / n
        return m / se, g.size
    res = []
    for h, fc, zc in [(1, "f1", "z"), (3, "f3", "z"), (3, "f3", "z3"), (5, "f5", "z3")]:
        G = A[(A["pos"] % h == 0)].dropna(subset=[fc, zc]).copy()
        drift = G.groupby("coin")[fc].mean()
        G["ex"] = G[fc] - G["coin"].map(drift)
        G["q"] = pd.qcut(G[zc], 5, labels=False)
        for q, d in G.groupby("q"):
            t, nd = clus_t(d, "ex")
            res.append([f"h{h}_{zc}", q, len(d), nd, d[zc].mean(), d["ex"].mean(), d[fc].mean(), t])
        # slope with day-clustered: regress per-day? simple OLS t
        sl = stats.linregress(G[zc], G["ex"])
        res.append([f"h{h}_{zc}", "slope", len(G), np.nan, np.nan, sl.slope, np.nan, sl.slope / sl.stderr])
    out["reversal_by_move"] = pd.DataFrame(res, columns=["set", "q", "n", "days", "z", "mean_ex", "mean_fwd", "t_dayclus"])
    # bottom-quintile 3-day after z3, by coin and year
    G = A[(A["pos"] % 3 == 0)].dropna(subset=["f3", "z3"]).copy()
    drift = G.groupby("coin")["f3"].mean()
    G["ex"] = G["f3"] - G["coin"].map(drift)
    G["q"] = pd.qcut(G["z3"], 5, labels=False)
    L = G[G["q"] == 0]
    out["low_z3_by_coin"] = L.groupby("coin")["ex"].agg(["size", "mean"])
    out["low_z3_by_year"] = L.groupby("year")["ex"].agg(["size", "mean"])
    H = G[G["q"] == 4]
    out["high_z3_by_coin"] = H.groupby("coin")["ex"].agg(["size", "mean"])
    # per-coin slope of ex on z3
    r = []
    for coin, d in G.groupby("coin"):
        sl = stats.linregress(d["z3"], d["ex"]); r.append([coin, len(d), sl.slope, sl.slope / sl.stderr])
    out["slope_by_coin_h3"] = pd.DataFrame(r, columns=["coin", "n", "slope", "t"])
    # interaction with 20-day trend: low z3 within s20 up vs down
    G2 = G.dropna(subset=["s20"]).copy()
    G2["trend"] = np.where(G2["s20"] > 0, "up20", "down20")
    t = G2.groupby(["trend", "q"])["ex"].agg(["size", "mean"])
    out["z3q_by_trend"] = t
    # usual 3-day move sd
    out["usual_3d_sd"] = float(G["f3"].std())
    return out
