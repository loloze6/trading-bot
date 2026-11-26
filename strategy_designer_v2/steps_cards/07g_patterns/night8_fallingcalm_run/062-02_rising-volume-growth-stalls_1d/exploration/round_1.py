def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); v=b["volume"].astype(float)
            r1=c.pct_change()
            ret60=c/c.shift(60)-1
            vr=np.log(v.rolling(30).mean()/v.shift(30).rolling(30).mean())
            vr10=np.log(v.rolling(10).mean()/v.shift(10).rolling(20).mean())
            ret5p=c/c.shift(5)-1
            ret20p=c/c.shift(20)-1
            vol20=r1.rolling(20).std()
            vol60=r1.rolling(60).std()
            fwd5=c.shift(-5)/c-1
            fwd1=c.shift(-1)/c-1
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"ret60":ret60,"vr":vr,"vr10":vr10,
              "ret5p":ret5p,"ret20p":ret20p,"volratio":vol20/vol60,"vol20":vol20,"fwd5":fwd5,"fwd1":fwd1,
              "wd":ts.dt.weekday,"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    G=A[(A.pos%5==0)&A.fwd5.notna()].copy()
    drift=G.groupby("coin").fwd5.mean(); G["ex"]=G.fwd5-G.coin.map(drift)
    sd=G.groupby("coin").fwd5.std(); G["z"]=G.ex/G.coin.map(sd)
    G["trend"]=np.where(G.ret60>0.1,"rising",np.where(G.ret60<-0.1,"falling","choppy"))
    G.loc[G.ret60.isna(),"trend"]="na"
    out={}
    def slope(df,x):
        d=df[[x,"z"]].dropna()
        if len(d)<30: return (len(d),np.nan,np.nan)
        s=stats.linregress(d[x],d["z"]); return (len(d),s.slope,s.slope/s.stderr)
    res=[]
    for tr in ["rising","choppy","falling","na","all"]:
        sub=G if tr=="all" else G[G.trend==tr]
        for x in ["vr","vr10","ret5p","ret20p","volratio"]:
            n,s,t=slope(sub,x); res.append((tr,x,n,s,t))
    out["slopes_z_on_feature"]=pd.DataFrame(res,columns=["trend","feat","n","slope","t"])
    # quintile tables in all bars
    for x in ["vr","ret5p","ret20p","volratio"]:
        d=G[[x,"z","ex"]].dropna().copy(); d["q"]=pd.qcut(d[x],5,labels=False)
        out["q_"+x]=d.groupby("q").agg(n=("z","size"),z=("z","mean"),ex=("ex","mean"),t=("z",lambda s:s.mean()/s.std()*np.sqrt(len(s))))
    out["weekday_fwd1"]=A.groupby("wd").fwd1.agg(["count","mean",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    G["yr"]=None
    out["trend_ex"]=G.groupby("trend").agg(n=("z","size"),ex=("ex","mean"),z=("z","mean"))
    D=pd.concat([d.assign(coin=c,w=w) for c,ws in data["days"].items() for w,d in ws.items()])
    bk=D.groupby(["w","day"]).book_return.mean()
    out["book_by_window"]=bk.groupby(level=0).agg(["count","mean","std"])
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=T.groupby(["coin","side"]).net_profit_loss_percent.agg(["count","mean","median"])
    return out
