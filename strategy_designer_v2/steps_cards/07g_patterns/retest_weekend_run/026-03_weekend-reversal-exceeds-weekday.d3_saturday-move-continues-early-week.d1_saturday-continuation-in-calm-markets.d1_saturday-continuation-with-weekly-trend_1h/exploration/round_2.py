def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","close"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.set_index("timestamp")
            c = d["close"]
            vol = c.pct_change().rolling(720, min_periods=300).std()
            idx = d.index
            for i in np.where(idx.hour == 0)[0]:
                if i - 169 < 0 or i + 48 >= len(d): continue
                t = idx[i]
                p = c.iloc[i-1]
                rows.append(dict(coin=coin, w=w, wd=t.weekday(), year=t.year,
                    prev=p/c.iloc[i-25]-1, prev2=c.iloc[i-25]/c.iloc[i-49]-1,
                    wk=p/c.iloc[i-169]-1, fwd=c.iloc[i+47]/p-1, fwd24=c.iloc[i+23]/p-1,
                    vol=vol.iloc[i-1]))
    X = pd.DataFrame(rows).dropna()
    X["prevs"] = X.prev/(X.vol*np.sqrt(24)); X["prev2s"] = X.prev2/(X.vol*np.sqrt(24))
    X["fwds"] = X.fwd/(X.vol*np.sqrt(48)); X["fwd24s"] = X.fwd24/(X.vol*np.sqrt(24))
    X["wks"] = X.wk/(X.vol*np.sqrt(168))
    X["vt"] = X.groupby("coin").vol.transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=["lo","mid","hi"]))
    X["era"] = np.where(X.year <= 2021, "y2018_2021", "y2022_2025")
    def slope(g, xc, yc):
        g = g[[xc,yc]].dropna()
        if len(g) < 30: return pd.Series(dict(n=len(g), slope=np.nan, t=np.nan))
        r = stats.linregress(g[xc], g[yc]); return pd.Series(dict(n=len(g), slope=r.slope, t=r.slope/r.stderr))
    out = {}
    M = X[X.wd==0].copy()
    M["agree"] = np.sign(M.prev2)==np.sign(M.wk)
    out["sat_to_monTue_by_era"] = M.groupby("era").apply(lambda g: slope(g,"prev2s","fwds"))
    out["sat_to_monTue_by_vt_era"] = M.groupby(["vt","era"]).apply(lambda g: slope(g,"prev2s","fwds"))
    out["sat_to_monTue_lo_disagree_by_era"] = M[(M.vt=="lo")&(~M.agree)].groupby("era").apply(lambda g: slope(g,"prev2s","fwds"))
    # multivariate: sat and week together on Mon-Tue
    import numpy.linalg as la
    Z = M[["prev2s","wks","prevs","fwds"]].dropna()
    A = np.column_stack([np.ones(len(Z)), Z.prev2s, Z.wks, Z.prevs]); y = Z.fwds.values
    b, *_ = la.lstsq(A, y, rcond=None); res = y - A@b
    s2 = res@res/(len(y)-4); se = np.sqrt(np.diag(s2*la.inv(A.T@A)))
    out["monTue_on_sat_week_sun"] = pd.DataFrame({"coef":b,"t":b/se}, index=["const","sat","week","sun"])
    # Sunday -> Monday 24h reversal by vol tercile and era
    out["sun_to_mon24_by_vt"] = M.groupby("vt").apply(lambda g: slope(g,"prevs","fwd24s"))
    out["sun_to_mon24_by_era"] = M.groupby("era").apply(lambda g: slope(g,"prevs","fwd24s"))
    # weekly return -> Fri+Sat (start Friday)
    F = X[X.wd==4]
    out["week_to_friSat_by_era"] = F.groupby("era").apply(lambda g: slope(g,"wks","fwds"))
    out["week_to_friSat_by_coin"] = F.groupby("coin").apply(lambda g: slope(g,"wks","fwds"))
    out["week_to_friSat_by_vt"] = F.groupby("vt").apply(lambda g: slope(g,"wks","fwds"))
    # placebo: week -> next 48h on other days pooled
    out["week_to_48h_other_days"] = slope(X[~X.wd.isin([4])],"wks","fwds").to_frame("v")
    # Saturday mean return by era and coin
    S = X[X.wd==5]
    out["sat_mean_by_era"] = S.groupby("era").fwd24s.agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["sat_mean_by_coin"] = S.groupby("coin").fwd24s.agg(["count","mean",lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    out["sat_mean_raw_by_coin"] = S.groupby("coin").fwd24.agg(["mean","median"])
    return out
