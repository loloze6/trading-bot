def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=7
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            vr=v/v.rolling(20,min_periods=10).mean()
            vol20=r1.rolling(20,min_periods=10).std()
            hi20=b["high"].astype(float).rolling(20,min_periods=10).max()
            near=c/hi20-1
            r7p=c/c.shift(7)-1
            fwd=c.shift(-H)/c-1
            ts=pd.to_datetime(b["timestamp"])
            for i in range(0,len(b),H):
                if i+H>=len(b): break
                rows.append(dict(coin=coin,w=w,fc=b["forecast"].iloc[i],vr=vr.iloc[i],r1=r1.iloc[i],
                    vol=vol20.iloc[i],near=near.iloc[i],r7p=r7p.iloc[i],fwd=fwd.iloc[i],wd=ts.iloc[i].dayofweek,
                    yr=ts.iloc[i].year,signed=np.sign(r1.iloc[i])*vr.iloc[i] if pd.notna(r1.iloc[i]) else np.nan))
    d=pd.DataFrame(rows)
    d["ex"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    out={}
    def qtab(col,q=5):
        x=d.dropna(subset=[col,"ex"]).copy()
        x["q"]=x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"),q,labels=False))
        g=x.groupby("q")["ex"].agg(["mean","count","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        return g.round(4)
    def slope(col):
        res={}
        for coin,x in d.dropna(subset=[col,"ex"]).groupby("coin"):
            s=stats.linregress(x[col],x["ex"]); res[coin]=round(s.slope/s.stderr,2)
        x=d.dropna(subset=[col,"ex"]); s=stats.linregress(x[col],x["ex"]); res["pooled"]=round(s.slope/s.stderr,2)
        return pd.Series(res)
    for col in ["fc","vr","r1","vol","near","r7p","signed"]:
        out["q_"+col]=qtab(col)
    out["slopes_t"]=pd.DataFrame({c:slope(c) for c in ["fc","vr","r1","vol","near","r7p","signed"]})
    # up-day vs down-day vol ratio interaction
    x=d.dropna(subset=["vr","r1","ex"]).copy()
    x["hv"]=x.groupby("coin")["vr"].transform(lambda s:s>s.median())
    x["up"]=x["r1"]>0
    out["upXhv"]=x.groupby(["up","hv"])["ex"].agg(["mean","count"]).round(4)
    out["by_year_fc_slope"]=d.dropna(subset=["fc","ex"]).groupby("yr").apply(lambda g: round(stats.linregress(g["fc"],g["ex"]).slope/stats.linregress(g["fc"],g["ex"]).stderr,2))
    # book: daily
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            dd=dd.copy(); dd["coin"]=coin; dd["w"]=w; dl.append(dd)
    D=pd.concat(dl)
    D["wd"]=pd.to_datetime(D["day"]).dt.dayofweek
    out["book_by_wd"]=D.groupby("wd")[["book_return","coin_return"]].mean().round(5)
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].agg(["mean","std"]).round(5)
    bw=D.groupby("w")[["book_return","coin_return"]].mean().round(5)
    out["book_by_window"]=bw
    return out
