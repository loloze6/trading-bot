import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    out = {}
    D = []
    G = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year, "dow": ts.dt.dayofweek,
                              "r_next": r.shift(-1), "r": r, "z": r / vol, "vol": vol,
                              "f3": c.shift(-3) / c - 1})
            D.append(d)
            ph = hi.shift(1).rolling(20).max()
            gap = c / ph - 1
            fwd = c.shift(-5) / c - 1
            idx = np.arange(0, len(b), 5)
            G.append(pd.DataFrame({"coin": coin, "w": w, "year": ts.dt.year.iloc[idx].values,
                                   "fwd": fwd.iloc[idx].values, "gap": gap.iloc[idx].values,
                                   "r20": (c / c.shift(20) - 1).iloc[idx].values}))
    D = pd.concat(D)
    D = D.dropna(subset=["r_next", "z"])
    m = D.groupby("coin")["r_next"].transform("mean")
    D["u"] = D["r_next"] - m
    def summ(x, by, col="u"):
        a = x.groupby(by, observed=True)[col].agg(["count", "mean", "median", "std"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        return a.drop(columns="std")
    out["overall_mean_daily"] = float(D["r_next"].mean())
    D["zq"] = D.groupby("coin")["z"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    out["next_day_by_z_decile"] = summ(D, "zq")
    big = D[D.zq == 0]
    out["lowest_z_decile_by_coin"] = summ(big, "coin")
    out["lowest_z_decile_by_year"] = summ(big, "year")
    trim = big["u"].clip(big["u"].quantile(0.05), big["u"].quantile(0.95))
    out["lowest_z_trimmed_mean_t"] = float(trim.mean() / (trim.std() / np.sqrt(len(trim))))
    # graded within negative z
    neg = D[D.z < 0]
    out["spearman_negz_vs_next"] = float(stats.spearmanr(-neg["z"], neg["u"]).correlation)
    out["n_negz"] = int(len(neg))
    # 3-day after lowest decile, non-overlapping-ish: take every 3rd within each coin
    # weekday
    out["dow_unusual"] = summ(D, "dow")
    sat = D[D.dow == 5]
    out["sat_by_coin"] = summ(sat, "coin")
    out["sat_by_year"] = summ(sat, "year")
    # breakout continuation graded
    G = pd.concat(G).dropna(subset=["fwd", "gap"])
    G["u"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    B = G[G.gap > 0]
    out["breakout_gap_tercile"] = summ(B.assign(q=pd.qcut(B["gap"], 3, labels=False)), "q")
    out["breakout_by_coin"] = summ(B, "coin")
    out["breakout_by_year"] = summ(B, "year")
    G["gq"] = pd.qcut(G["gap"], 10, labels=False)
    out["fwd5_by_gap_decile"] = summ(G, "gq")
    return out
