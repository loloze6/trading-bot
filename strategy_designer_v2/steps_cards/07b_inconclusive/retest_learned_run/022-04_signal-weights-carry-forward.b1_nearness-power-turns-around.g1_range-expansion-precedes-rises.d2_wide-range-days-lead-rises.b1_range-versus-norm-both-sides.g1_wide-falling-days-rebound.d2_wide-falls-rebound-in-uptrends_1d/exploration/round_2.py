def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    h = 3
    drift = {}
    for c in bars:
        rs = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - h, h):
                rs.append(cl[i + h] / cl[i] - 1)
        drift[c] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            rng = (df["high"] - df["low"]) / df["close"].shift(1)
            rmult = (rng / rng.shift(1).rolling(30, min_periods=20).mean()).values
            down = (df["close"] < df["close"].shift(1)).values
            ret30 = (df["close"] / df["close"].shift(30) - 1).values
            fc = df["forecast"].values
            for i in range(0, len(df) - h, h):
                rows.append(dict(coin=c, w=w, fc=fc[i], rm=rmult[i], down=down[i], r30=ret30[i],
                                 ex=cl[i + h] / cl[i] - 1 - drift[c],
                                 year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    out = {}
    s = d[d.down].dropna(subset=["rm"]).copy()
    q80 = s.rm.quantile(0.8); q90 = s.rm.quantile(0.9); q95 = s.rm.quantile(0.95)
    out["thresholds"] = pd.Series({"q80": q80, "q90": q90, "q95": q95})
    def agg(g):
        return pd.Series({"ex": g.ex.mean(), "n": len(g), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    top = s[s.rm > q80]
    out["top20_by_coin"] = top.groupby("coin").apply(agg)
    out["top20_by_year"] = top.groupby("year").apply(agg)
    s["bin"] = pd.cut(s.rm, [0, q80, q90, q95, np.inf], labels=["<q80", "q80-90", "q90-95", ">q95"])
    out["down_by_bin"] = s.groupby("bin").apply(agg)
    # slope on log rm, down days
    ss = s[s.rm > 0]
    r = stats.linregress(np.log(ss.rm), ss.ex); out["down_logrm_slope"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(ss)})
    r = stats.linregress(ss.rm, ss.ex); out["down_rm_slope"] = pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(ss)})
    # forecast vs rm on down days
    f = s[s.fc > 0]
    out["fc_rm_corr_down_fc>0"] = pd.Series({"corr": f[["fc", "rm"]].corr().iloc[0, 1], "n": len(f)})
    # forecast quintiles
    f = d[d.fc > 0].copy(); f["q"] = pd.qcut(f.fc.rank(method="first"), 5, labels=False)
    out["fc_quintiles"] = f.groupby("q").apply(lambda g: pd.Series({"fc": g.fc.mean(), "rm": g.rm.mean(), "ex": g.ex.mean(), "n": len(g), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g)))}))
    return out
