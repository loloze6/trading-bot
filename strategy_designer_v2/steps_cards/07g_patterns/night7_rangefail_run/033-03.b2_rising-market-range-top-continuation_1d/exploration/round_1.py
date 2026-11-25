def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            mx=c.rolling(20).max(); mn=c.rolling(20).min()
            rp=2*(c-mn)/(mx-mn)-1
            r1=c.pct_change()
            vol20=r1.rolling(20).std()
            r5p=c/c.shift(5)-1
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"rp":rp,"r1":r1,"r5p":r5p,
                            "vol20":vol20,"f5":f5,"f1":f1,"reg":b["regime"].values,
                            "alloc":b["postRebalance_current_allocation"].astype(float),
                            "fc":b["forecast"].astype(float),"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[D.pos%5==0].dropna(subset=["f5"]).copy()
    drift=G.groupby("coin")["f5"].mean()
    G["ex5"]=G["f5"]-G["coin"].map(drift)
    G["rising"]=np.where(G.reg=="unknown","rising","not")
    def slope(df,x,y="ex5"):
        df=df.dropna(subset=[x,y])
        if len(df)<20: return pd.Series({"n":len(df)})
        r=stats.linregress(df[x],df[y])
        return pd.Series({"n":len(df),"slope":r.slope,"t":r.slope/r.stderr,"meany":df[y].mean()})
    out={}
    out["rp slope by profile"]=G.groupby("rising").apply(lambda g:slope(g,"rp"))
    G["rpq"]=pd.cut(G.rp,[-1.01,-0.6,-0.2,0.2,0.6,0.99,1.01],labels=["q1","q2","q3","q4","q5","top"])
    out["ex5 by rp bin x profile"]=G.groupby(["rising","rpq"])["ex5"].agg(["count","mean"]).unstack(0)
    G["volt"]=G.groupby("coin")["vol20"].transform(lambda s:pd.qcut(s,3,labels=["lo","mid","hi"]))
    out["rp slope by vol tercile x profile"]=G.groupby(["rising","volt"]).apply(lambda g:slope(g,"rp"))
    out["rp slope by year (rising)"]=G[G.rising=="rising"].groupby("yr").apply(lambda g:slope(g,"rp"))
    out["r5p slope by profile"]=G.groupby("rising").apply(lambda g:slope(g,"r5p"))
    out["r1 slope by profile"]=G.groupby("rising").apply(lambda g:slope(g,"r1"))
    out["rp slope by coin (all)"]=G.groupby("coin").apply(lambda g:slope(g,"rp"))
    # next day by weekday
    D1=D.dropna(subset=["f1"])
    out["f1 by weekday"]=D1.groupby("wd")["f1"].agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    # large moves: r1 extremes next 5
    G["r1z"]=G.r1/G.vol20
    G["r1q"]=pd.cut(G.r1z,[-99,-2,-1,1,2,99])
    out["ex5 by r1 z"]=G.groupby(["rising","r1q"])["ex5"].agg(["count","mean"]).unstack(0)
    # book by side
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            x=d.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    DD=pd.concat(dd)
    BD=DD.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    out["book by window"]=BD.groupby(level=0).agg(["mean","count"])
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; T.append(tt)
    T=pd.concat(T)
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median",lambda s:(s>0).mean()])
    return out
