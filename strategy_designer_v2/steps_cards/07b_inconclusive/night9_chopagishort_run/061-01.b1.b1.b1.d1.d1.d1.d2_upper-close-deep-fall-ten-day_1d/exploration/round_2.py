def explore(data):
    import numpy as np, pandas as pd
    from scipy.stats import spearmanr
    bars = data["bars"]
    drift = {}
    for coin, wins in bars.items():
        for H in [2,3,5,10]:
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c)-H, H):
                    rets.append(c[i+H]/c[i]-1)
            drift[(coin,H)] = (np.mean(rets), np.std(rets)) if rets else (np.nan,np.nan)
    out = {}
    def summ(g, col="u"):
        x=g[col].dropna()
        if len(x)<2: return pd.Series({"n":len(x),"mean":x.mean() if len(x) else np.nan,"hit":np.nan,"t":np.nan})
        dd=g.loc[x.index].groupby("day")[col].sum()
        t = x.mean()/(dd.std(ddof=1)*np.sqrt(len(dd))/len(x)) if len(dd)>1 else np.nan
        return pd.Series({"n":len(x),"mean":x.mean(),"hit":(x>0).mean(),"t":t})
    hz = {}
    for H in [2,3,5,10]:
        rows=[]
        for coin, wins in bars.items():
            for w, df in wins.items():
                df=df.reset_index(drop=True)
                c=df["close"].values; f=df["forecast"].values; hi=df["high"].values; lo=df["low"].values
                n=len(df); seen=set()
                for i in range(n):
                    if f[i]<0 and i+H<n:
                        cell=i//H
                        if cell in seen: continue
                        seen.add(cell)
                        rows.append({"coin":coin,"win":w,"year":pd.Timestamp(df["timestamp"].iloc[i]).year,
                            "day":str(pd.Timestamp(df["timestamp"].iloc[i]).date()),"f":abs(f[i]),
                            "loc":(c[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,
                            "r20":c[i]/c[i-20]-1 if i>=20 else np.nan,
                            "r5":c[i]/c[i-5]-1 if i>=5 else np.nan,
                            "u":-((c[i+H]/c[i]-1)-drift[(coin,H)][0]),
                            "s":-((c[i+H]/c[i]-1)-drift[(coin,H)][0])/drift[(coin,H)][1]})
        d=pd.DataFrame(rows)
        s=summ(d); s["strength"]=d["s"].mean()
        s["sp_f"]=spearmanr(d["f"],d["u"]).correlation
        s["sp_loc"]=spearmanr(d["loc"],d["u"],nan_policy="omit").correlation
        s["sp_negr20"]=spearmanr(-d["r20"],d["u"],nan_policy="omit").correlation
        s["sp_negr5"]=spearmanr(-d["r5"],d["u"],nan_policy="omit").correlation
        hz[H]=s
        if H in [2,5]:
            d["locq"]=pd.cut(d["loc"],[0.5,0.7,0.85,1.01])
            out[f"H{H}_by_loc"]=d.groupby("locq").apply(summ)
            d["r20q"]=pd.qcut(d["r20"].rank(method="first"),3,labels=["deepest","mid","shallow"])
            out[f"H{H}_by_r20"]=d.groupby("r20q").apply(summ)
            d["r5q"]=pd.qcut(d["r5"].rank(method="first"),3,labels=["deep5","mid5","shallow5"])
            out[f"H{H}_by_r5"]=d.groupby("r5q").apply(summ)
            out[f"H{H}_by_year"]=d.groupby("year").apply(summ)
            core=d.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])
            out[f"H{H}_core"]=d.groupby(core).apply(summ)
    out["by_horizon"]=pd.DataFrame(hz).T
    return out
