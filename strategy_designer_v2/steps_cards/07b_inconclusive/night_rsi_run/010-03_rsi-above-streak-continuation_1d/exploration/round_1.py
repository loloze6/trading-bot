def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def grid(h):
        rows = []
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                cl = df["close"].values
                f = df["forecast"].values
                raw = df.get("debug_info.components.rsi_age.last_history_value")
                yr = pd.to_datetime(df["timestamp"]).dt.year.values
                for i in range(0, len(df) - h, h):
                    rows.append(dict(coin=c, w=w, year=yr[i], f=f[i],
                                     raw=(raw.values[i] if raw is not None else np.nan),
                                     r=cl[i+h]/cl[i]-1))
        g = pd.DataFrame(rows)
        g["ex"] = g["r"] - g.groupby("coin")["r"].transform("mean")
        return g
    def slope(g):
        g = g.dropna(subset=["f","ex"])
        if len(g) < 5 or g["f"].std() == 0: return (np.nan, np.nan, len(g))
        lr = stats.linregress(g["f"], g["ex"])
        return (lr.slope, lr.slope/lr.stderr, len(g))
    res = {}
    for h in [3,7,14,21,28]:
        g = grid(h)
        s = slope(g)
        on = g[g.f>0]["ex"]; off = g[g.f<=0]["ex"]
        tt = stats.ttest_ind(on, off, equal_var=False)
        res[h] = dict(slope=s[0], t=s[1], n=s[2], n_on=len(on), on_mean=on.mean(), off_mean=off.mean(), welch_t=tt.statistic)
    out["by_horizon"] = pd.DataFrame(res).T
    g = grid(14)
    out["by_coin"] = pd.DataFrame({c: dict(zip(["slope","t","n"], slope(gg))) for c, gg in g.groupby("coin")}).T
    out["by_year"] = pd.DataFrame({y: dict(zip(["slope","t","n"], slope(gg))) for y, gg in g.groupby("year")}).T
    g["fbin"] = pd.cut(g["f"], [-0.1, 0, 2, 5, 10, 20.1])
    out["by_fbin"] = g.groupby("fbin")["ex"].agg(["count","mean","std"])
    if g["raw"].notna().any():
        g["rawbin"] = pd.cut(g["raw"], [-1000, 0, 5, 15, 30, 61])
        out["by_rawbin"] = g.groupby("rawbin")["ex"].agg(["count","mean","std"])
    # regime: coin's past 60-bar return sign at grid
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            cl = df["close"].values; f = df["forecast"].values
            for i in range(60, len(df)-14, 14):
                rows.append(dict(coin=c, up=cl[i]/cl[i-60]-1 > 0, f=f[i], r=cl[i+14]/cl[i]-1))
    q = pd.DataFrame(rows); q["ex"] = q["r"] - q.groupby("coin")["r"].transform("mean")
    out["by_trend60"] = pd.DataFrame({k: dict(zip(["slope","t","n"], slope(gg))) for k, gg in q.groupby("up")}).T
    return out
