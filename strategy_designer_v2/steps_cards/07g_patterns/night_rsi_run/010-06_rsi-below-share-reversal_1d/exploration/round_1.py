import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fc": b["forecast"].astype(float),
                "raw": b.get("debug_info.components.rsi_below_share.last_history_value", pd.Series(np.nan, index=b.index)).astype(float),
                "pos": b["postRebalance_current_allocation"].astype(float),
                "ret1": r1,
                "ret7": c / c.shift(7) - 1,
                "ret30": c / c.shift(30) - 1,
                "vol30": r1.rolling(30).std(),
                "rng": (b["high"] - b["low"]) / c,
                "fwd14": c.shift(-14) / c - 1,
                "fwd7": c.shift(-7) / c - 1,
                "fwd1": c.shift(-1) / c - 1,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "i": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    # coin-demeaned on grids
    def grid(h, col):
        g = A[A["i"] % h == 0].dropna(subset=[col]).copy()
        g["y"] = g[col] - g.groupby("coin")[col].transform("mean")
        return g
    def slope(g, x):
        g = g.dropna(subset=[x, "y"])
        res = stats.linregress(g[x], g["y"])
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "n": len(g)})
    g14 = grid(14, "fwd14"); g7 = grid(7, "fwd7"); g1 = grid(1, "fwd1")
    tab = {}
    for x in ["fc", "raw", "ret7", "ret30", "vol30"]:
        tab[x + "_h14"] = slope(g14, x)
        tab[x + "_h7"] = slope(g7, x)
    tab["ret1_h1"] = slope(g1, "ret1")
    tab["rng_h1"] = slope(g1, "rng")
    out["slopes"] = pd.DataFrame(tab).T
    # forecast quintiles fwd14
    g14["fq"] = pd.qcut(g14["fc"].rank(method="first"), 5, labels=False)
    out["fc_quint_fwd14"] = g14.groupby("fq")["y"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    g14["r30q"] = pd.qcut(g14["ret30"].rank(method="first"), 5, labels=False)
    out["ret30_quint_fwd14"] = g14.groupby("r30q")["y"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    g7["vq"] = pd.qcut(g7["vol30"].rank(method="first"), 5, labels=False)
    out["vol_quint_fwd7"] = g7.groupby("vq")["y"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # weekday
    out["weekday_ret1"] = A.dropna(subset=["fwd1"]).groupby("wd")["fwd1"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # large moves next day
    g1["abs"] = g1["ret1"].abs()
    g1["mq"] = pd.qcut(g1["ret1"].rank(method="first"), 10, labels=False)
    out["ret1_decile_next1"] = g1.groupby("mq")["y"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # book by coin/year
    D = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["book_by_year"] = D.groupby("yr")[["book_return", "coin_return"]].mean()
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    out["pos_by_fc_sign"] = A.groupby(np.sign(A["fc"]))["pos"].agg(["mean", "count"])
    return out
