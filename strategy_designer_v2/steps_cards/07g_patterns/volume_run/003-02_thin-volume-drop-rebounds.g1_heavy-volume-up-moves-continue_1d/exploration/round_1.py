def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r=c.pct_change()
            vol20=r.rolling(20).std()
            z=r/vol20.shift(1)
            vr=v/v.rolling(30).mean().shift(1)
            r5=r.rolling(5).sum()
            fwd5=c.shift(-5)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":z,"vr":vr,"vol20":vol20,
                            "r5":r5/vol20.shift(1),"fwd5":fwd5,"fwd1":fwd1,"fc":b["forecast"],
                            "alloc":b["postRebalance_current_allocation"],"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%5==0)&D.fwd5.notna()].copy()
    G["ex5"]=G.fwd5-G.groupby("coin").fwd5.transform("mean")
    D["ex1"]=D.fwd1-D.groupby("coin").fwd1.transform("mean")
    def summ(df,col,key):
        g=df.dropna(subset=[key,col]).groupby(key,observed=True)[col]
        out=pd.DataFrame({"n":g.size(),"mean":g.mean()})
        out["t"]=out["mean"]/(g.std()/np.sqrt(out["n"]))
        return out
    Gz=G.dropna(subset=["z","vr"]).copy()
    Gz["zq"]=pd.cut(Gz.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    Gz["vrt"]=Gz.groupby("coin").vr.transform(lambda s:pd.qcut(s,3,labels=["thin","mid","heavy"]))
    res={}
    res["ex5 by z bin"]=summ(Gz,"ex5","zq")
    big=Gz[Gz.z.abs()>1.5].copy(); big["side"]=np.where(big.z>0,"up","down")
    res["big move ex5 by side x volume"]=big.groupby(["side","vrt"],observed=True).ex5.agg(["size","mean",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))])
    Gz["r5q"]=pd.cut(Gz.r5,[-99,-3,-1.5,0,1.5,3,99])
    res["ex5 by past5d scaled ret"]=summ(Gz,"ex5","r5q")
    Gz["volt"]=Gz.groupby("coin").vol20.transform(lambda s:pd.qcut(s,3,labels=["lowvol","mid","highvol"]))
    res["ex5 by vol tercile"]=summ(Gz,"ex5","volt")
    res["ex5 by vr tercile all"]=summ(Gz,"ex5","vrt")
    res["ex1 by weekday"]=summ(D,"ex1","wd")
    res["ex5 by year"]=summ(G,"ex5","yr")
    res["ex5 by coin"]=summ(G,"ex5","coin")
    # forecast buckets every bar 1d
    D["fcb"]=pd.cut(D.fc,[-1,0,0.5,2,5,21])
    res["ex1 by forecast bucket"]=summ(D,"ex1","fcb")
    # 1-day after big moves by volume
    Dz=D.dropna(subset=["z","vr"]).copy()
    Dz["zq"]=pd.cut(Dz.z,[-99,-2,-1,1,2,99])
    res["ex1 by z bin"]=summ(Dz,"ex1","zq")
    # book: daily returns, days by state
    bk=[]
    for coin,ws in data["days"].items():
        for w,dd in ws.items():
            bk.append(dd.assign(coin=coin,w=w))
    B=pd.concat(bk).dropna(subset=["book_return"])
    res["book by coin"]=B.groupby("coin")[["book_return","coin_return"]].mean()
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    res["trades"]=tr.groupby("coin").agg(n=("net_profit_loss_percent","size"),mean=("net_profit_loss_percent","mean"),
        dur_days=("duration_minutes",lambda s:s.mean()/1440))
    res["alloc share>0"]=float((D.alloc.abs()>0.01).mean())
    return res
