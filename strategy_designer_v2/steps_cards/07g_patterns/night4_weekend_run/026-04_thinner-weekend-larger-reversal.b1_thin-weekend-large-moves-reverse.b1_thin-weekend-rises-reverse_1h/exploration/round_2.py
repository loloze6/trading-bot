def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def tt(x):
        x=np.asarray(x,float); x=x[~np.isnan(x)]
        return x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x)>2 else np.nan
    grid=[]; hrs=[]
    for coin in bars:
        for w,b in bars[coin].items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float); n=len(c)
            yr=ts.dt.year.values
            for h in (24,12):
                for i in range(h, n-h, h):
                    if i-168<0: continue
                    vr=v[i-h+1:i+1].mean()/max(v[i-167:i-h+1].mean(),1e-12)
                    grid.append((coin,w,h,yr[i],c[i]/c[i-h]-1,c[i+h]/c[i]-1,vr,int(ts.iloc[i].hour)))
            r1=np.r_[c[1:]/c[:-1]-1,np.nan]
            hrs.append(pd.DataFrame({"coin":coin,"w":w,"yr":yr,"hour":((ts+pd.Timedelta(hours=1)).dt.hour).values,"r":r1}))
    G=pd.DataFrame(grid,columns=["coin","w","h","yr","p","n","vr","hr"])
    res=[]
    for h,g in G.groupby("h"):
        g=g.copy()
        sd=g.groupby("coin")["p"].transform("std"); mu=g.groupby("coin")["n"].transform("mean")
        g["z"]=g.p/sd; g["un"]=g.n-mu; g["unz"]=g.un/sd
        g["sig"]=-np.sign(g.z); g["unS"]=g.un*g.sig; g["totS"]=g.n*g.sig
        g["zq"]=g.groupby("coin")["z"].transform(lambda x:pd.qcut(x,5,labels=False))
        q=g.groupby("zq").agg(n=("un","size"),z=("z","mean"),un_pct=("un",lambda x:x.mean()*100),t=("un",tt))
        out[f"{h}h grid: past z quintile -> next {h}h unusual move %"]=q.round(3)
        ex=g[(g.zq==0)|(g.zq==4)]
        out[f"{h}h extremes (q0,q4) reversal by coin: unusual/total % in reversal dir"]=ex.groupby("coin").agg(n=("unS","size"),un_pct=("unS",lambda x:x.mean()*100),t=("unS",tt),tot_pct=("totS",lambda x:x.mean()*100),usual_pct=("p",lambda x:x.std()*100)).round(3)
        out[f"{h}h extremes reversal by year"]=ex.groupby("yr").agg(n=("unS","size"),un_pct=("unS",lambda x:x.mean()*100),t=("unS",tt)).round(3)
        ex=ex.copy(); ex["vq"]=ex.groupby("coin")["vr"].transform(lambda x:pd.qcut(x,3,labels=["low","mid","high"]))
        out[f"{h}h extremes reversal by volume tercile (past {h}h vol vs prior)"]=ex.groupby("vq",observed=True).agg(n=("unS","size"),un_pct=("unS",lambda x:x.mean()*100),t=("unS",tt)).round(3)
        if h==24:
            sl=stats.linregress(g.z,g.unz)
            out["24h: slope next unusual (usual moves) on past z"]=f"slope {sl.slope:.4f}, t {sl.slope/sl.stderr:.2f}, n {len(g)}"
            out["24h extremes reversal by grid hour"]=ex.groupby("hr").agg(n=("unS","size"),un_pct=("unS",lambda x:x.mean()*100),t=("unS",tt)).round(3)
    H=pd.concat(hrs).dropna()
    H["rd"]=H.r-H.groupby("coin")["r"].transform("mean")
    H["blk"]=np.where(H.hour.isin([21,22]),"21-22",np.where(H.hour.isin([1,2,3]),"01-03",np.where(H.hour==14,"14","other")))
    out["hour blocks by year (bps/hour)"]=H.groupby(["yr","blk"])["rd"].agg(lambda x:x.mean()*1e4).unstack().round(2)
    out["hour 21-22 by coin (bps/hour, t)"]=H[H.blk=="21-22"].groupby("coin")["rd"].agg(bps=lambda x:x.mean()*1e4,t=tt).round(2)
    return out
