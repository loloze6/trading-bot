def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=240
    rows=[]
    for coin,ws in data["bars"].items():
        recs=[]
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24=c/c.shift(24)-1
            mav=r24.abs().rolling(720,min_periods=500).mean()
            z=r24/mav
            r720=c/c.shift(720)-1
            r240p=c/c.shift(240)-1
            fwd=c.shift(-H)/c-1
            idx=np.arange(0,len(c),H)
            d=pd.DataFrame({"coin":coin,"w":w,"z":z.iloc[idx].values,"r720":r720.iloc[idx].values,
                            "r240p":r240p.iloc[idx].values,"mav":mav.iloc[idx].values,
                            "fwd":fwd.iloc[idx].values,"year":ts.iloc[idx].dt.year.values,
                            "hour":ts.iloc[idx].dt.hour.values,"fc":b["forecast"].iloc[idx].values})
            recs.append(d)
        d=pd.concat(recs)
        drift=d["fwd"].mean()
        sd=d["fwd"].std()
        d["unu"]=d["fwd"]-drift
        d["str"]=d["unu"]/sd
        d["volrank"]=d["mav"].rank(pct=True)
        rows.append(d)
    D=pd.concat(rows).dropna(subset=["fwd"])
    def summ(g):
        x=g["unu"].dropna()
        n=len(x)
        return pd.Series({"n":n,"mean_unu":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,
                          "strength":g["str"].mean()})
    out={}
    Dz=D.dropna(subset=["z"])
    Dz["zbin"]=pd.cut(Dz["z"],[-np.inf,-3,-2,-1,0,1,2,3,np.inf])
    out["by_z24"]=Dz.groupby("zbin").apply(summ)
    Dz["prior"]=np.where(Dz["r720"]>0,"r30d_up","r30d_down")
    out["by_z24_prior"]=Dz[Dz["z"].abs()>2].groupby([np.sign(Dz["z"]),"prior"]).apply(summ)
    D2=D.dropna(subset=["r720"]).copy()
    D2["r30bin"]=pd.qcut(D2.groupby("coin")["r720"].rank(pct=True),5,labels=False)
    out["by_r30d_quintile"]=D2.groupby("r30bin").apply(summ)
    D3=D.dropna(subset=["r240p"]).copy()
    D3["r10bin"]=pd.qcut(D3.groupby("coin")["r240p"].rank(pct=True),5,labels=False)
    out["by_r10d_quintile"]=D3.groupby("r10bin").apply(summ)
    D4=D.dropna(subset=["mav"]).copy()
    D4["vbin"]=pd.qcut(D4.groupby("coin")["mav"].rank(pct=True),3,labels=False)
    out["by_vol_tercile"]=D4.groupby("vbin").apply(summ)
    out["by_year"]=D.groupby("year").apply(summ)
    out["by_coin"]=D.groupby("coin").apply(summ)
    # book
    dl=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd[["day","book_return","coin_return"]].copy(); x["w"]=w; dl.append(x)
    DD=pd.concat(dl).dropna()
    day=DD.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    day["year"]=pd.to_datetime(day["day"]).dt.year
    out["book_by_year"]=day.groupby("year").agg(n=("book_return","size"),book_mean=("book_return","mean"),
        book_sd=("book_return","std"),coin_mean=("coin_return","mean"))
    out["book_by_window"]=day.groupby("w").agg(book_sum=("book_return","sum"),coin_sum=("coin_return","sum"),
        worst=("book_return","min"))
    # trades
    tl=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): x=t.copy(); x["coin"]=coin; tl.append(x)
    T=pd.concat(tl)
    T["fq"]=pd.qcut(T["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades_by_fc_quartile"]=T.groupby("fq").agg(n=("net_profit_loss_percent","size"),
        fc=("entry_forecast","mean"),pnl=("net_profit_loss_percent","mean"),
        med=("net_profit_loss_percent","median"),days=("duration_minutes",lambda s:s.mean()/1440))
    T["hour"]=pd.to_datetime(T["entry_time"]).dt.hour//6
    out["trades_by_entry_6h"]=T.groupby("hour")["net_profit_loss_percent"].agg(["size","mean","median"])
    return out
