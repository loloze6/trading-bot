def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    gm = {}
    for coin, wins in bars.items():
        # coin grid means for horizons
        for h in [1,2,3,5,7,10]:
            vals = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                vals += list(c[idx+h]/c[idx]-1)
            gm[(coin,h)] = np.mean(vals)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; o=df["open"].values; hi=df["high"].values; lo=df["low"].values; v=df["volume"].values
            r1 = pd.Series(c).pct_change()
            vol20 = r1.rolling(20).std()
            fall = r1/vol20
            vr = pd.Series(v)/pd.Series(v).shift(1).rolling(30).mean()
            rng = hi-lo
            wick = (np.minimum(o,c)-lo)/np.where(rng>0,rng,np.nan)
            f = df["forecast"].values
            last = -10
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for t in range(len(df)):
                isflush = f[t] > 0
                bigfall = fall.iloc[t] <= -1 if not np.isnan(fall.iloc[t]) else False
                if not (isflush or bigfall): continue
                d = {"coin":coin,"win":w,"year":yr[t],"flush":isflush,"fc":f[t],
                     "fall":fall.iloc[t],"vr":vr.iloc[t],"wick":wick[t],"r1":r1.iloc[t],
                     "dup": isflush and (t-last<=3)}
                if isflush: last = t
                for h in [1,2,3,5,7,10]:
                    d[f"x{h}"] = c[t+h]/c[t]-1-gm[(coin,h)] if t+h < len(c) else np.nan
                # prior 10-day return
                d["p10"] = c[t]/c[t-10]-1 if t>=10 else np.nan
                rows.append(d)
    D = pd.DataFrame(rows)
    F = D[D.flush & ~D.dup]
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan,"hit":(s>0).mean()})
    out = {}
    out["flush by horizon"] = pd.DataFrame({h:tt(F[f"x{h}"]) for h in [1,2,3,5,7,10]}).T
    nf = D[(~D.flush)]
    out["nonflush falls<=-1sd by horizon"] = pd.DataFrame({h:tt(nf[f"x{h}"]) for h in [1,2,3,5,7,10]}).T
    out["flush x3 by coin"] = F.groupby("coin")["x3"].apply(tt).unstack()
    out["flush x3 by year"] = F.groupby("year")["x3"].apply(tt).unstack()
    F2 = F.copy()
    F2["fcq"] = pd.qcut(F2["fc"].rank(method="first"),4,labels=False)
    out["x3 by forecast quartile"] = F2.groupby("fcq")["x3"].apply(tt).unstack()
    F2["fallq"] = pd.qcut(F2["fall"].rank(method="first"),4,labels=False)
    out["x3 by fall quartile (0=deepest)"] = F2.groupby("fallq")["x3"].apply(tt).unstack()
    F2["vrq"] = pd.qcut(F2["vr"].rank(method="first"),4,labels=False)
    out["x3 by vr quartile"] = F2.groupby("vrq")["x3"].apply(tt).unstack()
    F2["wq"] = pd.qcut(F2["wick"].rank(method="first"),4,labels=False)
    out["x3 by wick quartile"] = F2.groupby("wq")["x3"].apply(tt).unstack()
    F2["pq"] = pd.qcut(F2["p10"].rank(method="first"),3,labels=False)
    out["x3 by prior10d tercile"] = F2.groupby("pq")["x3"].apply(tt).unstack()
    out["spearman fc,x3"] = stats.spearmanr(F["fc"],F["x3"],nan_policy="omit")[0]
    out["spearman wick,x3"] = stats.spearmanr(F["wick"],F["x3"],nan_policy="omit")[0]
    out["spearman vr,x3"] = stats.spearmanr(F["vr"],F["x3"],nan_policy="omit")[0]
    out["spearman fall,x3"] = stats.spearmanr(F["fall"],F["x3"],nan_policy="omit")[0]
    out["x3 skew/median"] = pd.Series({"median":F.x3.median(),"skew":F.x3.skew(),"mean_trim5":stats.trim_mean(F.x3.dropna(),0.05)})
    return out
