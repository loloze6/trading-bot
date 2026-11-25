def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    for c in bars:
        for H in [1,3,5,10]:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl)-H, H):
                    rs.append(cl[i+H]/cl[i]-1)
            drift[(c,H)] = np.mean(rs) if rs else np.nan
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            hi30 = pd.Series(cl).rolling(30, min_periods=1).max().values
            dep = cl/hi30-1
            fc = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            for H in [1,3,5,10]:
                for i in range(0, len(cl)-H, H):
                    if fc[i] != 0 and not np.isnan(fc[i]):
                        r = cl[i+H]/cl[i]-1
                        rows.append(dict(coin=c, win=w, H=H, fc=fc[i], depth=dep[i],
                                         unus=-(r-drift[(c,H)]), tot=-r, day=ts[i].normalize(), yr=ts[i].year))
    d = pd.DataFrame(rows)
    out = {}
    def summ(g):
        n = len(g)
        m = g["unus"].mean(); s = g["unus"].std()
        return pd.Series({"n": n, "unus_mean": m, "t": m/(s/np.sqrt(n)) if n>1 else np.nan, "tot_mean": g["tot"].mean()})
    out["by_horizon"] = d.groupby("H").apply(summ)
    def slope(g):
        if len(g) < 10: return pd.Series({"n": len(g), "slope_depth": np.nan, "t": np.nan})
        r = stats.linregress(g["depth"], -g["unus"])  # return-minus-drift on depth
        return pd.Series({"n": len(g), "slope_depth": r.slope, "t": r.slope/r.stderr})
    out["slope_ret_on_depth_by_H"] = d.groupby("H").apply(slope)
    d3 = d[d.H==3].copy()
    d3["q"] = pd.qcut(d3["depth"], 5, labels=False)
    out["H3_by_depth_quintile"] = d3.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series({"depth_mean": g["depth"].mean()})]))
    out["H3_by_coin"] = d3.groupby("coin").apply(summ)
    out["H3_by_window"] = d3.groupby("win").apply(summ)
    out["H3_by_year"] = d3.groupby("yr").apply(summ)
    d10 = d[d.H==10].copy()
    d10["q"] = pd.qcut(d10["depth"], 4, labels=False)
    out["H10_by_depth_quartile"] = d10.groupby("q").apply(summ)
    d1 = d[d.H==1].copy()
    d1["q"] = pd.qcut(d1["depth"], 5, labels=False)
    out["H1_by_depth_quintile"] = d1.groupby("q").apply(summ)
    return out
