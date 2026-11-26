def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            vol=r.rolling(30).std()
            net=(c-c.shift(30)).abs(); path=c.diff().abs().rolling(30).sum()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"er":net/path,"vol":vol,
                "s7":(c/c.shift(7)-1)/(vol*np.sqrt(7)),"f7":c.shift(-7)/c-1,"f1":c.shift(-1)/c-1,
                "s1":r/vol,"s3":(c/c.shift(3)-1)/(vol*np.sqrt(3)),"f3":c.shift(-3)/c-1,
                "vol90":r.rolling(90,min_periods=60).std(),"yr":ts.dt.year,"pos":np.arange(len(b)),
                "alloc":b["postRebalance_current_allocation"].astype(float)})
            daily.append(df)
    D=pd.concat(daily,ignore_index=True)
    D["volrel"]=D.vol/D.vol90
    D["volr"]=D.groupby("coin")["vol"].rank(pct=True)
    def sl(d,x,y):
        d=d[[x,y]].dropna()
        if len(d)<30: return [np.nan,np.nan,len(d)]
        lr=stats.linregress(d[x],d[y]); return [lr.slope,lr.slope/lr.stderr,len(d)]
    out={}
    G=D[D.pos%7==0].copy(); G["x"]=G.f7-G.groupby("coin")["f7"].transform("mean")
    G["vb"]=pd.cut(G.volr,[0,1/3,2/3,1.0],labels=["low","mid","high"])
    G["rb"]=pd.qcut(G.volrel,3,labels=["calmer","same","more agitated"])
    res=[]
    for k,g in G[G.vb=="low"].groupby("coin"): res.append(["low",k]+sl(g,"s7","x"))
    for k,g in G[G.vb=="low"].groupby("yr"): res.append(["low",str(k)]+sl(g,"s7","x"))
    for k,g in G.groupby("rb",observed=True): res.append(["volrel",str(k)]+sl(g,"s7","x"))
    out["week_cont_low_vol_split"]=pd.DataFrame(res,columns=["grp","k","slope","t","n"])
    D["d1"]=D.f1-D.groupby("coin")["f1"].transform("mean")
    D["vb"]=pd.cut(D.volr,[0,1/3,2/3,1.0],labels=["low","mid","high"])
    res=[]
    for k,g in D.groupby("coin"): res.append(["coin",k]+sl(g,"s1","d1"))
    for k,g in D.groupby("yr"): res.append(["yr",str(k)]+sl(g,"s1","d1"))
    for k,g in D.groupby("vb",observed=True): res.append(["vol",str(k)]+sl(g,"s1","d1"))
    out["next_day_reversal_split"]=pd.DataFrame(res,columns=["grp","k","slope","t","n"])
    D["q"]=pd.qcut(D.s1,5,labels=False)
    out["next_day_by_s1_quintile"]=D.groupby("q")["d1"].agg(["mean","count",lambda v:v.mean()/v.std()*np.sqrt(len(v))])
    G3=D[D.pos%3==0].copy(); G3["x"]=G3.f3-G3.groupby("coin")["f3"].transform("mean")
    res=[sl(G3,"s1","x"),sl(G3,"s3","x")]
    out["3day_on_s1_s3"]=pd.DataFrame(res,index=["s1","s3"],columns=["slope","t","n"])
    # book by side x s7 sign
    D["gain"]=D.alloc*D.f1
    D["drg"]=D.alloc*D.groupby("coin")["f1"].transform("mean")
    out["book_timing_vs_drift"]=pd.Series({"gain":D.gain.mean(),"drift_part":D.drg.mean()})
    return out
