def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = 5
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            if n < H + 25: continue
            r1 = pd.Series(c).pct_change().values
            s = pd.Series(c)
            ret5p = (s / s.shift(5) - 1).values
            ret20p = (s / s.shift(20) - 1).values
            vol20 = pd.Series(r1).rolling(20, min_periods=10).std().values
            hi = s.rolling(60, min_periods=20).max().values
            lo = s.rolling(60, min_periods=20).min().values
            rng = (df["high"] - df["low"]).astype(float).values / c
            ts = pd.to_datetime(df["timestamp"])
            fc = df["forecast"].astype(float).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, fwd=c[i+H]/c[i]-1, r1=r1[i], r5=ret5p[i],
                                 r20=ret20p[i], vol=vol20[i], nhi=c[i]/hi[i]-1 if hi[i]==hi[i] else np.nan,
                                 nlo=c[i]/lo[i]-1 if lo[i]==lo[i] else np.nan, rng=rng[i],
                                 wd=ts.iloc[i].dayofweek, fc=fc[i], year=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean(); usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["ex"] / g["coin"].map(usual)
    # vol rank within coin
    g["volr"] = g.groupby("coin")["vol"].rank(pct=True)
    def slope(col, sub=None):
        d = (g if sub is None else sub).dropna(subset=[col, "z"])
        x = d.groupby("coin")[col].transform(lambda v: (v - v.mean())/v.std())
        res = stats.linregress(x, d["z"])
        return pd.Series(dict(slope=res.slope, t=res.slope/res.stderr, n=len(d)))
    out = {}
    out["slopes_z_on_std_signal"] = pd.DataFrame({c: slope(c) for c in ["fc","r1","r5","r20","vol","nhi","nlo","rng"]}).T
    def bins(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda v: pd.qcut(v.rank(method="first"), q, labels=False))
        a = d.groupby("b")["ex"].agg(["mean","std","count"])
        a["t"] = a["mean"]/(a["std"]/np.sqrt(a["count"]))
        return a
    out["fc_quint"] = bins("fc"); out["r1_quint"] = bins("r1"); out["r20_quint"] = bins("r20")
    out["vol_quint"] = bins("vol"); out["nlo_quint"] = bins("nlo")
    # r20 slope by vol tercile
    g["volt"] = pd.cut(g["volr"], [0, 1/3, 2/3, 1], labels=False, include_lowest=True)
    out["r20_by_vol"] = pd.DataFrame({k: slope("r20", g[g.volt==k]) for k in [0,1,2]}).T
    out["nhi_by_vol"] = pd.DataFrame({k: slope("nhi", g[g.volt==k]) for k in [0,1,2]}).T
    out["r1_by_vol"] = pd.DataFrame({k: slope("r1", g[g.volt==k]) for k in [0,1,2]}).T
    a = g.groupby("wd")["ex"].agg(["mean","std","count"]); a["t"]=a["mean"]/(a["std"]/np.sqrt(a["count"]))
    out["weekday_start"] = a
    out["fc_slope_by_coin"] = pd.DataFrame({c: slope("fc", g[g.coin==c]) for c in g.coin.unique()}).T
    out["fc_slope_by_year"] = pd.DataFrame({y: slope("fc", g[g.year==y]) for y in sorted(g.year.unique())}).T
    out["r20_slope_by_coin"] = pd.DataFrame({c: slope("r20", g[g.coin==c]) for c in g.coin.unique()}).T
    # book: daily returns, largest days
    D = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_vs_hold_by_window_count"] = pd.Series(dict(
        book_mean=bk.book_return.mean(), hold_mean=bk.coin_return.mean(),
        corr=bk.book_return.corr(bk.coin_return), ndays=len(bk),
        share_win_book_beats=(bk.groupby(level=0).book_return.sum() > bk.groupby(level=0).coin_return.sum()).mean()))
    # position vs forecast
    allb = pd.concat([df.assign(coin=c) for c, ws in bars.items() for df in ws.values()])
    allb["fcb"] = pd.cut(allb["forecast"], [-21,-5,-2,0,2,5,21])
    out["alloc_by_fc"] = allb.groupby("fcb")["postRebalance_current_allocation"].agg(["mean","count"])
    out["share_short"] = (allb["postRebalance_current_allocation"] < 0).mean()
    return out
