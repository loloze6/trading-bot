def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; v=b["volume"]
            r1=c.pct_change()
            vol=r1.rolling(20,min_periods=15).std()
            z=r1/vol
            vr=v/v.rolling(20,min_periods=15).mean()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"z":z,"vr":vr,"vol":vol,
                            "alloc":b["postRebalance_current_allocation"]})
            for k in range(1,6):
                d[f"d{k}"]=c.shift(-k)/c.shift(-k+1)-1
            d["f1"]=d["d1"]
            d["f3"]=c.shift(-3)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def tt(x):
        x=x.dropna(); n=len(x); return pd.Series({"n":n,"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n))})
    for k in range(1,6):
        D[f"e{k}"]=D[f"d{k}"]-D.groupby("coin")[f"d{k}"].transform("mean")
    D["zb"]=pd.cut(D.z,[-99,-2,-1,-0.3,0.3,1,2,99])
    # day-by-day excess after z bucket (overlapping per day but each day is single-bar, fine for ex1 per offset; report)
    tab={}
    for k in range(1,6):
        tab[f"day{k}"]=D.groupby("zb")[f"e{k}"].mean()
    out["mean excess by day offset after z"]=pd.DataFrame(tab)
    # 1-day reversal after down by volume tercile, grid of 1 = all bars
    D["vrb"]=pd.qcut(D.vr,3,labels=["thin","mid","heavy"])
    dn=D[D.z<-1]
    out["ex1 after big down by volume"]=dn.groupby("vrb")["e1"].apply(tt).unstack()
    up=D[D.z>1]
    out["ex1 after big up by volume"]=up.groupby("vrb")["e1"].apply(tt).unstack()
    # graded: regress e1 on min(z,0) per coin
    res={}
    for coin,g in D.dropna(subset=["e1","z"]).groupby("coin"):
        x=np.minimum(g.z,0); s=stats.linregress(x,g.e1)
        res[coin]={"slope":s.slope,"t":s.slope/s.stderr,"n":len(g)}
    out["e1 on downside z per coin"]=pd.DataFrame(res).T
    # by window halves: early windows vs late
    D["wn"]=D.win.str[1:].astype(int)
    D["half"]=np.where(D.wn<=12,"w1-12","w13-24")
    out["e1 after z<-1 by half"]=D[D.z<-1].groupby("half")["e1"].apply(tt).unstack()
    # 3-day non-overlapping grid after down z
    G=D[D.pos%3==0].dropna(subset=["f3","z"]).copy()
    G["ex3"]=G.f3-G.groupby("coin")["f3"].transform("mean")
    out["ex3 grid by z"]=G.groupby("zb")["ex3"].apply(tt).unstack()
    # book gain on day after allocation by day position since shock: alloc vs z today
    D["gain"]=D.alloc*D.f1
    out["book gain by today z"]=D.groupby("zb").agg(alloc=("alloc","mean"),gain=("gain","mean"),e1=("e1","mean"))
    return out
