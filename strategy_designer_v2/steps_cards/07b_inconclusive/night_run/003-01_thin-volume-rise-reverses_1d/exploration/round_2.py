def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            z = r1 / r1.rolling(20).std()
            lvr = np.log(v / v.shift(1).rolling(30).mean())
            yr = pd.to_datetime(df["timestamp"]).dt.year
            n = len(df)
            for h in (1, 3, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=int(yr.iloc[i]),
                                     z=z.iloc[i], lvr=lvr.iloc[i],
                                     ret=c.iloc[i + h] / c.iloc[i] - 1))
    d = pd.DataFrame(rows).dropna()
    d["ex"] = d["ret"] - d.groupby(["coin", "h"])["ret"].transform("mean")
    out = {}
    def tt(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})
    def corr(g, col):
        r, p = stats.spearmanr(g[col], g["ex"]); return pd.Series({"n": len(g), "rho": r, "p": p})
    # heavy-volume rises: graded continuation signal = z * lvr (both positive)
    hv = d[(d.z > 0) & (d.lvr > 0)].copy(); hv["s"] = hv.z * hv.lvr
    out["heavy_up_rank_corr_by_h"] = hv.groupby("h").apply(lambda g: corr(g, "s"))
    hv["q"] = hv["s"] / hv.groupby("h")["s"].transform("std") * hv["ex"]
    out["heavy_up_q_by_h"] = hv.groupby("h")["q"].apply(tt).unstack()
    h5 = hv[hv.h == 5].copy()
    h5["sq"] = pd.qcut(h5["s"].rank(method="first"), 5, labels=False)
    out["heavy_up5_ex_by_strength_quintile(4=strongest)"] = h5.groupby("sq")["ex"].apply(tt).unstack()
    out["heavy_up5_q_by_coin"] = h5.groupby("coin")["q"].apply(tt).unstack()
    out["heavy_up5_q_by_year"] = h5.groupby("year")["q"].apply(tt).unstack()
    # thin rises: graded reversal signal = z * (-lvr)
    th = d[(d.z > 0) & (d.lvr < 0)].copy(); th["s"] = th.z * (-th.lvr)
    out["thin_up_rank_corr_by_h"] = th.groupby("h").apply(lambda g: corr(g, "s"))
    # heavy-volume falls: continuation, signal = |z| * lvr, expect ex negative
    hd = d[(d.z < 0) & (d.lvr > 0)].copy(); hd["s"] = -hd.z * hd.lvr
    out["heavy_down_rank_corr_by_h"] = hd.groupby("h").apply(lambda g: corr(g, "s"))
    return out
