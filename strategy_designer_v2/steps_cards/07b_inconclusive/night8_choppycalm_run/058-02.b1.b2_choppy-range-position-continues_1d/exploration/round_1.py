def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    P = "debug_info.components.range_pos.post_pipeline_value"
    R = "debug_info.components.range_pos.last_history_value"
    rows = []
    # coin mean h-day returns over all windows (grid)
    def gridret(c, h):
        out = []
        for w, df in bars[c].items():
            cl = df["close"].values
            for i in range(0, len(cl) - h, h):
                out.append(cl[i + h] / cl[i] - 1)
        return np.mean(out) if out else np.nan
    for c in bars:
        means = {h: gridret(c, h) for h in (1, 3, 5, 10, 20)}
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            hi = df["high"].rolling(20).max(); lo = df["low"].rolling(20).min()
            rp = 2 * (cl - lo) / (hi - lo) - 1
            r1 = cl.pct_change()
            vol30 = r1.rolling(30).std()
            for h in (1, 3, 5, 10, 20):
                idx = np.arange(0, len(df) - h, h)
                fr = (cl.shift(-h) / cl - 1).values
                for i in idx:
                    if pd.isna(df.loc[i, P]) if P in df else True:
                        continue
                    rows.append(dict(coin=c, w=w, h=h, f=df.loc[i, P], raw=df.loc[i, R],
                                     rp=rp[i], ex=fr[i] - means[h], vol=vol30[i]))
    d = pd.DataFrame(rows)
    # agitation proxy: vol vs coin median of vol
    med = d.groupby("coin")["vol"].median()
    d["agit"] = d["vol"] > d["coin"].map(med)
    def slope(g, x="f"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope / r.stderr))
    out = {}
    out["by_horizon"] = d.groupby("h").apply(slope)
    d5 = d[d.h == 5]
    out["h5_by_coin"] = d5.groupby("coin").apply(slope)
    out["h5_by_window"] = d5.groupby("w").apply(slope)
    out["h5_by_agit"] = d5.groupby("agit").apply(slope)
    out["by_h_agit"] = d.groupby(["h", "agit"]).apply(slope)
    out["by_h_rawpos"] = d.groupby("h").apply(lambda g: slope(g, "raw"))
    d5 = d5.copy()
    d5["q"] = pd.qcut(d5["raw"], 5, labels=False, duplicates="drop")
    out["h5_raw_quintile"] = d5.groupby("q")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    d10 = d[d.h == 10].copy()
    d10["q"] = pd.qcut(d10["raw"], 5, labels=False, duplicates="drop")
    out["h10_raw_quintile"] = d10.groupby("q")["ex"].agg(["count", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    out["raw_range"] = d5["raw"].describe()
    return out
