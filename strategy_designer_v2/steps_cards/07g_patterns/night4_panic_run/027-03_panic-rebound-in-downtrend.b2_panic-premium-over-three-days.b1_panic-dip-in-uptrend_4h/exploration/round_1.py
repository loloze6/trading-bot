def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; ev=[]; hr=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); rg=(b["high"]-b["low"])/c
            rr=rg.rolling(6).mean()/rg.rolling(180).mean()
            r6=c/c.shift(6)-1
            vol6=r6.abs().rolling(180).mean()
            z6=r6/vol6
            prior=c.shift(6)/c.shift(186)-1
            r1=c.pct_change()
            vol=r1.rolling(42).std()
            f18=c.shift(-18)/c-1; f42=c.shift(-42)/c-1; f1=c.shift(-1)/c-1
            df=pd.DataFrame({"coin":coin,"w":w,"rr":rr,"z6":z6,"prior":prior,"vol":vol,
                             "f18":f18,"f42":f42,"fc":b["forecast"],"pos":b.index,
                             "cell":b.index//18,"cell42":b.index//42})
            rows.append(df)
            ts=pd.to_datetime(b["timestamp"])
            hr.append(pd.DataFrame({"coin":coin,"h":ts.dt.hour,"wd":ts.dt.dayofweek,"f1":f1,"r1":r1}))
    A=pd.concat(rows,ignore_index=True)
    g18=A[A.pos%18==0].dropna(subset=["f18"])
    drift18=g18.groupby("coin").f18.mean(); sd18=g18.groupby("coin").f18.std()
    g42=A[A.pos%42==0].dropna(subset=["f42"])
    drift42=g42.groupby("coin").f42.mean()
    A["x18"]=A.f18-A.coin.map(drift18); A["s18"]=A.x18/A.coin.map(sd18)
    A["x42"]=A.f42-A.coin.map(drift42)
    def summ(d,col):
        d=d.dropna(subset=[col]); n=len(d); m=d[col].mean(); s=d[col].std()
        return pd.Series({"n":n,"mean":m,"t":m/(s/np.sqrt(n)) if n>1 else np.nan})
    out={}
    # panic events: first per 18-cell
    P=A[(A.rr>=3)&(A.z6<0)]
    Pe=P.groupby(["coin","w","cell"]).head(1).copy()
    Pe["side"]=np.where(Pe.prior>0,"prior_up","prior_down")
    out["panic18_by_prior"]=Pe.groupby("side").apply(lambda d:summ(d,"x18"))
    Pe42=P.groupby(["coin","w","cell42"]).head(1).copy(); Pe42["side"]=np.where(Pe42.prior>0,"up","down")
    out["panic42_by_prior"]=Pe42.groupby("side").apply(lambda d:summ(d,"x42"))
    # graded: rr bins with fall, on 18-grid
    G=A[A.pos%18==0].copy()
    G["rrb"]=pd.cut(G.rr,[0,0.7,1,1.5,2,3,99])
    out["grid18_rr_bins_fall"]=G[G.z6<0].groupby("rrb").apply(lambda d:summ(d,"x18"))
    out["grid18_rr_bins_rise"]=G[G.z6>0].groupby("rrb").apply(lambda d:summ(d,"x18"))
    G["zb"]=pd.cut(G.z6,[-99,-3,-2,-1,0,1,2,3,99])
    out["grid18_z6_bins"]=G.groupby("zb").apply(lambda d:summ(d,"x18"))
    G["vq"]=G.groupby("coin").vol.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["grid18_vol_quint"]=G.groupby("vq").apply(lambda d:summ(d,"x18"))
    G["pq"]=G.groupby("coin").prior.transform(lambda s:pd.qcut(s,5,labels=False,duplicates="drop"))
    out["grid18_prior_quint"]=G.groupby("pq").apply(lambda d:summ(d,"x18"))
    # forecast active
    Fa=A[A.fc>0].groupby(["coin","w","cell"]).head(1)
    out["fc_active_by_coin"]=Fa.groupby("coin").apply(lambda d:summ(d,"x18"))
    H=pd.concat(hr,ignore_index=True)
    H["x"]=H.f1-H.groupby("coin").f1.transform("mean")
    out["next4h_by_hour"]=H.groupby("h").apply(lambda d:summ(d,"x"))
    out["next4h_by_wd"]=H.groupby("wd").apply(lambda d:summ(d,"x"))
    # book
    D=pd.concat([d.assign(coin=c) for c,ws in data["days"].items() for d in ws.values()])
    out["book_by_coin"]=D.groupby("coin")[["book_return","coin_return"]].mean()
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for t in ws.values()])
    out["trades"]=T.groupby("coin").net_profit_loss_percent.agg(["count","mean","median"])
    return out
