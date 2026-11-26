def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        g5 = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            n = len(b)
            for i in range(0, n - 5, 5):
                g5.append(c[i+5]/c[i]-1)
            rng = (b["high"]-b["low"])
            rr = rng / rng.rolling(20).mean()
            fl = 1 - (b["close"]-b["open"]).abs()/rng.replace(0, np.nan)
            pe5 = b["close"]/b["close"].shift(5)-1
            pe60 = b["close"]/b["close"].shift(60)-1
            r1 = b["close"].pct_change()
            sd30 = r1.rolling(30).std()
            agit = sd30 > sd30.rolling(365, min_periods=120).median()
            for i in range(n):
                d = dict(coin=coin, w=w, cell=i//5, rr=rr.iat[i], fl=fl.iat[i], pe5=pe5.iat[i],
                         pe60=pe60.iat[i], agit=agit.iat[i], day=str(b["timestamp"].iat[i])[:10])
                for h in (3,5):
                    d[f"r{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(d)
        drift[coin] = np.mean(g5)
    df = pd.DataFrame(rows)
    df["u5"] = df["r5"] - df["coin"].map(drift)
    def summ(sub, col="u5", sign=1):
        sub = sub.dropna(subset=[col]).groupby(["coin","w","cell"]).head(1)
        v = sign*sub[col]
        dd = v.groupby(sub["day"]).sum()
        t = dd.mean()/(dd.std(ddof=1)/np.sqrt(len(dd))) if len(dd)>2 else np.nan
        return pd.Series(dict(n=len(sub), days=len(dd), mean=v.mean(), t=t, share_pos=(v>0).mean()))
    out = {}
    up = df.pe5>0
    sit = up & (df.rr>=1.5) & (df.fl>=0.9)
    loose = up & (df.rr>=1.2) & (df.fl>=0.7)
    upwide = up & (df.rr>=1.5)
    g = {}
    for nm, m in [("sit", sit), ("loose", loose), ("upwide_any", upwide)]:
        s = df[m].dropna(subset=["u5"]).groupby(["coin","w","cell"]).head(1)
        g[nm+"_spearman_pe5_u5"] = stats.spearmanr(s.pe5, s.u5)[0]
        g[nm+"_spearman_rr_u5"] = stats.spearmanr(s.rr, s.u5)[0]
        g[nm+"_spearman_fl_u5"] = stats.spearmanr(s.fl, s.u5)[0]
    out["gradients (long side u5)"] = pd.Series(g)
    t = {}
    for nm, m in [("loose", loose), ("upwide", upwide)]:
        q = df.pe5.where(m)
        med = q.median()
        t[nm+"_pe5_above_med"] = summ(df[m & (df.pe5>med)])
        t[nm+"_pe5_below_med"] = summ(df[m & (df.pe5<=med)])
        t[nm+"_rising"] = summ(df[m & (df.pe60>0.1)])
        t[nm+"_not_rising"] = summ(df[m & (df.pe60<=0.1)])
        t[nm+"_agitated"] = summ(df[m & (df.agit==True)])
        t[nm+"_calm"] = summ(df[m & (df.agit==False)])
    t["sit_long_r3"] = summ(df[sit], col="r3")
    t["sit_long_u5"] = summ(df[sit])
    t["sit_rising_long_u5"] = summ(df[sit & (df.pe60>0.1)])
    t["up_other_long_u5"] = summ(df[up & ~upwide])
    out["groups long-side"] = pd.DataFrame(t).T
    return out
