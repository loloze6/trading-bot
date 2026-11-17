import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ret1": r1, "ret3": c / c.shift(3) - 1, "ret7": c / c.shift(7) - 1,
                "vol30": r1.rolling(30).std(),
                "rng": (b["high"] - b["low"]) / c,
                "fwd1": c.shift(-1) / c - 1, "fwd2": c.shift(-2) / c - 1, "fwd3": c.shift(-3) / c - 1,
                "fwd7": c.shift(-7) / c - 1, "fwd14": c.shift(-14) / c - 1,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
                "i": np.arange(len(b)),
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def grid(h, col):
        g = A[A["i"] % h == 0].dropna(subset=[col]).copy()
        g["y"] = g[col] - g.groupby("coin")[col].transform("mean")
        return g
    def sl(g, x):
        g = g.dropna(subset=[x, "y"])
        if len(g) < 10: return pd.Series({"slope": np.nan, "t": np.nan, "rho": np.nan, "n": len(g)})
        res = stats.linregress(g[x], g["y"])
        rho = stats.spearmanr(g[x], g["y"]).correlation
        return pd.Series({"slope": res.slope, "t": res.slope / res.stderr, "rho": rho, "n": len(g)})
    g1 = grid(1, "fwd1"); g2 = grid(2, "fwd2"); g3 = grid(3, "fwd3"); g7 = grid(7, "fwd7"); g14 = grid(14, "fwd14")
    # reversal: by coin, by year, by vol level
    t = {}
    for coin in g1["coin"].unique():
        t["ret1_fwd1_" + coin] = sl(g1[g1.coin == coin], "ret1")
        t["ret7_fwd14_" + coin] = sl(g14[g14.coin == coin], "ret7")
    t["ret1_fwd2"] = sl(g2, "ret1"); t["ret1_fwd3"] = sl(g3, "ret1")
    t["ret3_fwd3"] = sl(g3, "ret3"); t["ret1_fwd7"] = sl(g7, "ret1")
    t["ret7_fwd7"] = sl(g7, "ret7")
    # z-scored ret1 (by own vol)
    g1["z1"] = g1["ret1"] / g1["vol30"]
    t["z1_fwd1"] = sl(g1, "z1")
    # trimmed: exclude top/bottom 1% ret1
    q = g1["ret1"].quantile([0.01, 0.99])
    t["ret1_fwd1_trim1pct"] = sl(g1[(g1.ret1 > q.iloc[0]) & (g1.ret1 < q.iloc[1])], "ret1")
    out["slopes"] = pd.DataFrame(t).T
    out["ret1_fwd1_by_year"] = g1.groupby("yr").apply(lambda g: sl(g, "ret1"))
    g1["vq"] = pd.qcut(g1["vol30"].rank(method="first"), 3, labels=False)
    out["ret1_fwd1_by_volterc"] = g1.dropna(subset=["vq"]).groupby("vq").apply(lambda g: sl(g, "ret1"))
    # windows: share of windows with negative slope
    ws = g1.groupby(["coin", "win"]).apply(lambda g: sl(g, "ret1")["slope"])
    out["window_slopes_neg_share"] = pd.Series({"neg_share": (ws < 0).mean(), "n": ws.notna().sum(),
                                                 "binom_p": stats.binomtest(int((ws < 0).sum()), int(ws.notna().sum())).pvalue})
    # up vs down day asymmetry
    g1["up"] = g1["ret1"] > 0
    out["ret1_fwd1_by_sign"] = g1.dropna(subset=["ret1"]).groupby("up").apply(lambda g: sl(g, "ret1"))
    out["ret7_fwd14_by_year"] = g14.groupby("yr").apply(lambda g: sl(g, "ret7"))
    # range: high range days next-day
    g1["rq"] = pd.qcut(g1["rng"].rank(method="first"), 5, labels=False)
    out["rng_quint_fwd1"] = g1.groupby("rq")["y"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    return out
