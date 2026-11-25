def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            rng=(b.high-b.low)
            clh=(b.high-b.close)/rng.replace(0,np.nan)  # 0 at high, 1 at low
            r=b.close.pct_change()
            nxt=b.close.shift(-1)/b.close-1
            vol20=r.rolling(20,min_periods=10).std()
            rngrel=(rng/b.close)/vol20
            tr60=b.close/b.close.shift(60)-1
            vol30=r.rolling(30,min_periods=20).std()
            alloc=b.postRebalance_current_allocation
            turn=(alloc-b.previous_allocation).abs()
            gain=alloc*nxt
            d=pd.DataFrame({"coin":coin,"w":w,"clh":clh,"nxt":nxt,"r1":r,"rngrel":rngrel,
                "tr60":tr60,"vol30":vol30,"fc":b.forecast,"alloc":alloc,"turn":turn,"gain":gain,
                "pos":np.arange(len(b)),"year":pd.to_datetime(b.timestamp).dt.year})
            rows.append(d)
    D=pd.concat(rows)
    D=D.dropna(subset=["nxt","clh"])
    mean_by_coin=D.groupby("coin").nxt.mean()
    D["ex"]=D.nxt-D.coin.map(mean_by_coin)
    D["volmed"]=D.coin.map(D.groupby("coin").vol30.median())
    D["agit"]=np.where(D.vol30>D.volmed,"agit","calm")
    D["trend"]=pd.cut(D.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])
    out={}
    D["clq"]=pd.cut(D.clh,[-0.01,0.1,0.25,0.5,0.75,0.9,1.01])
    g=D.groupby("clq").ex.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["ex by close-from-high bucket"]=g
    D["rq"]=pd.qcut(D.rngrel,3,labels=["narrow","mid","wide"])
    D["sig"]=(D.clh-0.5)
    D["sx"]=D.sig*D.ex
    out["signed (clh-0.5)*ex by range tercile"]=D.groupby("rq").sx.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    ext=D[(D.clh>0.85)|(D.clh<0.15)].copy(); ext["side"]=np.where(ext.clh>0.85,"lowclose_long","highclose_short")
    ext["dirret"]=np.where(ext.side=="lowclose_long",ext.ex,-ext.ex)
    out["extreme cases by side x range"]=ext.groupby(["side","rq"]).dirret.agg(["mean","count",lambda x:x.mean()/x.std()*np.sqrt(len(x))])
    out["extreme by side x trend"]=ext.groupby(["side","trend"]).dirret.agg(["mean","count"])
    out["extreme by side x agit"]=ext.groupby(["side","agit"]).dirret.agg(["mean","count"])
    out["extreme by side, total move"]=ext.assign(tot=np.where(ext.side=="lowclose_long",ext.nxt,-ext.nxt)).groupby("side").tot.agg(["mean","count"])
    # day's own return: close at low after a down day vs up day
    ext["r1s"]=np.where(ext.r1<0,"downday","upday")
    out["extreme by side x day sign"]=ext.groupby(["side","r1s"]).dirret.agg(["mean","count"])
    # condition alone: wide range days without extreme close
    mid=D[(D.clh>=0.15)&(D.clh<=0.85)]
    out["wide-range non-extreme ex mean"]=mid.groupby("rq").ex.agg(["mean","count"])
    # book: gross gain, turnover
    out["book turnover and gain"]=pd.Series({"mean |alloc|":D.alloc.abs().mean(),"mean turnover/bar":D.turn.mean(),
        "mean gross gain/bar":D.gain.mean(),"cost/bar at 0.19%/2 per side":D.turn.mean()*0.00095,
        "share long":(D.alloc>0).mean(),"share short":(D.alloc<0).mean()})
    out["gross gain by side"]=D.assign(s=np.sign(D.alloc)).groupby("s").gain.agg(["mean","count"])
    out["gross gain by year"]=D.groupby("year").gain.mean()
    return out
