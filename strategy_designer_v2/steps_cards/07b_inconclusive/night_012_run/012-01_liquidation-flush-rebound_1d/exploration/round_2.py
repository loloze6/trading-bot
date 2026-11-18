def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    gm = {}
    for coin, wins in bars.items():
        for h in [3]:
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
            fall = (r1/vol20).values
            vr = (pd.Series(v)/pd.Series(v).shift(1).rolling(30).mean()).values
            rng = hi-lo
            wick = (np.minimum(o,c)-lo)/np.where(rng>0,rng,np.nan)
            f = df["forecast"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            last = -10
            for t in range(len(df)):
                if np.isnan(fall[t]) or fall[t] > -1: continue
                dup = (t-last<=3)
                last = t
                rows.append({"coin":coin,"year":yr[t],"flush":f[t]>0,"fall":fall[t],"vr":vr[t],"wick":wick[t],
                             "x3": c[t+3]/c[t]-1-gm[(coin,3)] if t+3<len(c) else np.nan,"dup":dup})
    D = pd.DataFrame(rows)
    D = D[~D.dup].dropna(subset=["x3","vr","wick"])
    def tt(s):
        s=s.dropna(); return pd.Series({"n":len(s),"mean":s.mean(),"t":s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out={}
    out["all big falls x3 by vr quintile"] = D.groupby(pd.qcut(D.vr.rank(method="first"),5,labels=False))["x3"].apply(tt).unstack()
    out["all big falls x3 by wick quintile"] = D.groupby(pd.qcut(D.wick.rank(method="first"),5,labels=False))["x3"].apply(tt).unstack()
    rs = stats.spearmanr(D.vr, D.x3); out["spearman vr,x3 all falls (rho,p,n)"] = pd.Series({"rho":rs[0],"p":rs[1],"n":len(D)})
    rs = stats.spearmanr(D.wick, D.x3); out["spearman wick,x3 all falls"] = pd.Series({"rho":rs[0],"p":rs[1]})
    D["hv"] = D.vr>=2
    out["vr>=2 vs <2 falls"] = D.groupby("hv")["x3"].apply(tt).unstack()
    a=D[D.hv].x3; b=D[~D.hv].x3
    out["welch hv minus lv"] = pd.Series(stats.ttest_ind(a,b,equal_var=False)._asdict())
    H = D[D.hv]
    out["vr>=2 falls by coin: spearman vr"] = H.groupby("coin").apply(lambda g: pd.Series({"n":len(g),"rho":stats.spearmanr(g.vr,g.x3)[0],"mean":g.x3.mean()}))
    out["vr>=2 falls by year"] = H.groupby("year")["x3"].apply(tt).unstack()
    fl = D[D.flush]; nf=D[~D.flush & D.hv]
    out["flush minus hv nonflush welch"] = pd.Series({"flush_mean":fl.x3.mean(),"hvnonflush_mean":nf.x3.mean(),"n_nf":len(nf),"t":stats.ttest_ind(fl.x3,nf.x3,equal_var=False)[0]})
    return out
