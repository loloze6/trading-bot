def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        for H in [2,5,10,20]:
            rets = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c)-H, H):
                    rets.append(c[i+H]/c[i]-1)
            drift[(coin,H)] = (np.mean(rets), np.std(rets)) if rets else (np.nan,np.nan)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].values
            hi=df["high"].values; lo=df["low"].values
            n=len(df); seen=set()
            for i in range(n):
                if f[i] < 0:
                    cell = i//10
                    if cell in seen: continue
                    seen.add(cell)
                    r = {"coin":coin,"win":w,"year":pd.Timestamp(df["timestamp"].iloc[i]).year,
                         "f":abs(f[i]),"day":str(pd.Timestamp(df["timestamp"].iloc[i]).date()),
                         "loc":(c[i]-lo[i])/(hi[i]-lo[i]) if hi[i]>lo[i] else np.nan,
                         "r20": c[i]/c[i-20]-1 if i>=20 else np.nan}
                    for H in [2,5,10,20]:
                        r[f"u{H}"] = -((c[i+H]/c[i]-1) - drift[(coin,H)][0]) if i+H<n else np.nan
                        r[f"tot{H}"] = -(c[i+H]/c[i]-1) if i+H<n else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col="u10"):
        x=g[col].dropna()
        dd=g.loc[x.index].groupby("day")[col].sum() if len(x) else pd.Series(dtype=float)
        t = x.mean()/ (dd.std(ddof=1)*np.sqrt(len(dd))/len(x)) if len(dd)>1 else np.nan
        return pd.Series({"n":len(x),"mean":x.mean(),"median":x.median(),"hit":(x>0).mean(),"t":t})
    out={}
    out["by_horizon"]=pd.DataFrame({h:summ(d,f"u{h}") for h in [2,5,10,20]}).T
    out["by_coin"]=d.groupby("coin").apply(summ)
    out["by_win"]=d.groupby("win").apply(summ)
    out["by_year"]=d.groupby("year").apply(summ)
    d["fq"]=pd.qcut(d["f"].rank(method="first"),3,labels=["lowF","midF","highF"])
    out["by_fsize"]=d.groupby("fq").apply(summ)
    d["r20q"]=pd.qcut(d["r20"].rank(method="first"),3,labels=["deepest","mid","shallow"]) if d["r20"].notna().sum()>5 else "na"
    out["by_r20"]=d.groupby("r20q").apply(summ)
    d["locq"]=pd.cut(d["loc"],[0.5,0.7,0.85,1.01])
    out["by_loc"]=d.groupby("locq").apply(summ)
    core=d.coin.isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"])
    out["core_vs_other"]=d.groupby(core).apply(summ)
    out["trim_top5_mean"]=float(d["u10"].dropna().sort_values().iloc[:-5].mean())
    out["trim_bot5_mean"]=float(d["u10"].dropna().sort_values().iloc[5:].mean())
    return out
