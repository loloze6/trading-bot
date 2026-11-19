def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    hrs = []; grid = []; grid3 = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            n = len(c)
            r1 = np.r_[c[1:]/c[:-1]-1, np.nan]
            hrs.append(pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year.values, "hour": ts.dt.hour.values, "r": r1}))
            for h, lst in ((24, grid), (72, grid3)):
                past = np.full(n, np.nan); past[h:] = c[h:]/c[:-h]-1
                fut = np.full(n, np.nan); fut[:-h] = c[h:]/c[:-h]-1
                vol = pd.Series(np.r_[np.nan, c[1:]/c[:-1]-1]).rolling(168).std().values
                idx = np.arange(0, n, h)
                lst.append(pd.DataFrame({"coin": coin, "win": w, "year": ts.dt.year.values[idx],
                                         "past": past[idx], "fut": fut[idx], "vol": vol[idx]}))
    H = pd.concat(hrs).dropna()
    def tt(s):
        return pd.Series({"mean_bp": s.mean()*1e4, "t": s.mean()/(s.std()/np.sqrt(len(s))), "n": len(s)})
    H2021 = H[H.hour.isin([20, 21])]
    out["h20_21_by_year"] = H2021.groupby("year")["r"].apply(tt).unstack()
    out["h20_21_by_coin"] = H2021.groupby("coin")["r"].apply(tt).unstack()
    H13 = H[H.hour == 13]
    out["h13_by_year"] = H13.groupby("year")["r"].apply(tt).unstack()
    out["h13_by_coin"] = H13.groupby("coin")["r"].apply(tt).unstack()
    H02 = H[H.hour.isin([0, 1, 2])]
    out["h00_02_by_year"] = H02.groupby("year")["r"].apply(tt).unstack()
    for name, L in (("d1", grid), ("d3", grid3)):
        G = pd.concat(L).dropna()
        G["z"] = G["past"]/G["vol"]
        def slope(df):
            res = stats.linregress(df["z"], df["fut"]/df["vol"])
            return pd.Series({"slope": res.slope, "t": res.slope/res.stderr, "n": len(df)})
        out[name+"_reversal_slope_all"] = slope(G)
        out[name+"_reversal_by_year"] = G.groupby("year").apply(slope)
        out[name+"_reversal_by_coin"] = G.groupby("coin").apply(slope)
        G["zq"] = G.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
        out[name+"_fut_by_zquint"] = G.groupby("zq")["fut"].apply(tt).unstack()
    return out
