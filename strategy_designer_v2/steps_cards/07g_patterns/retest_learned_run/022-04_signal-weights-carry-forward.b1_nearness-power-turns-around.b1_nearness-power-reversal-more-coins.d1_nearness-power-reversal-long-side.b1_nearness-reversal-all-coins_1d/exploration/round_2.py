def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # daily coin returns by weekday of the day that the return ends on (UTC day of bar start)
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; ts = pd.to_datetime(df["timestamp"])
            r = c.pct_change()
            r5p = c / c.shift(5) - 1
            vol60 = r.rolling(60).std()
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rows.append(pd.DataFrame(dict(coin=coin, win=w, ts=ts, wd=ts.dt.dayofweek, yr=ts.dt.year,
                                          r=r, r5p=r5p, vol60=vol60, fwd5=fwd5, fwd1=fwd1, f=df["forecast"])))
    B = pd.concat(rows, ignore_index=True)
    # coin drift per day
    B["dr1"] = B.groupby("coin")["r"].transform("mean")
    B["ex1"] = B["fwd1"] - B["dr1"]
    # date-clustered: mean across coins per date, then t across dates
    Dd = B.dropna(subset=["ex1"]).groupby("ts").agg(ex1=("ex1", "mean"), wd=("wd", "first"), yr=("yr", "first"))
    t = Dd.groupby("wd")["ex1"].agg(["count", "mean", "std"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["next-day excess return by weekday of signal bar (date-clustered)"] = t.round(5)
    # weekday x year sign stability: Sunday-bar and Tuesday-bar next day
    piv = Dd.groupby(["yr", "wd"])["ex1"].mean().unstack().round(4)
    out["next-day excess by year x weekday"] = piv
    # per-coin, Sunday-bar next day mean and Monday
    pc = B.dropna(subset=["ex1"]).groupby(["coin", "wd"])["ex1"].mean().unstack().round(4)
    out["next-day excess by coin x weekday"] = pc
    # 5-day reversal: non-overlapping grid, r5p scaled by vol, quintiles within coin; date-clustered by year
    G = []
    for (coin, w), x in B.groupby(["coin", "win"], sort=False):
        x = x.reset_index(drop=True)
        G.append(x.iloc[::5])
    G = pd.concat(G, ignore_index=True)
    G["dr5"] = G.groupby("coin")["fwd5"].transform("mean")
    G["ex5"] = G["fwd5"] - G["dr5"]
    G["s"] = G["r5p"] / (G["vol60"] * np.sqrt(5))
    G = G.dropna(subset=["s", "ex5"])
    G["q"] = G.groupby("coin")["s"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    q = G.groupby("q")["ex5"].agg(["count", "mean", "std"]); q["t"] = q["mean"] / (q["std"] / np.sqrt(q["count"]))
    out["excess5 by vol-scaled 5d return quintile"] = q.round(4)
    G["yrq"] = G["yr"]
    rho_y = G.groupby("yr").apply(lambda x: pd.Series({"rho": stats.spearmanr(x["s"], x["ex5"])[0], "n": len(x)}))
    out["spearman vol-scaled r5p vs ex5 by year"] = rho_y.round(4)
    # date-clustered: per date, slope sign; correlation of cross-sectional? per coin rho
    rho_c = G.groupby("coin").apply(lambda x: pd.Series({"rho": stats.spearmanr(x["s"], x["ex5"])[0], "n": len(x)}))
    out["spearman vol-scaled r5p vs ex5 by coin"] = rho_c.round(4)
    # reversal graded by vol regime
    G["vq"] = G.groupby("coin")["vol60"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["spearman by vol tercile"] = G.groupby("vq").apply(lambda x: pd.Series({"rho": stats.spearmanr(x["s"], x["ex5"])[0], "n": len(x)})).round(4)
    # within forecast>0 vs =0
    out["spearman by forecast>0"] = G.groupby(G["f"] > 0).apply(lambda x: pd.Series({"rho": stats.spearmanr(x["s"], x["ex5"])[0], "n": len(x)})).round(4)
    return out
