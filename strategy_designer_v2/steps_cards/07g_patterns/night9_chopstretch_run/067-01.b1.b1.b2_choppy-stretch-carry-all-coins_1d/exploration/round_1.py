def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            st=(c-sma)/sma/sd
            r1=r  # today's return
            z1=r1/sd.shift(1)
            ret60=c/c.shift(60)-1
            hi20=c.rolling(20).max(); lo20=c.rolling(20).min()
            pos20=(c-lo20)/(hi20-lo20)
            n=len(b)
            for h in (1,5):
                pass
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            f10=c.shift(-10)/c-1
            wd=pd.to_datetime(b["timestamp"]).dt.weekday
            yr=pd.to_datetime(b["timestamp"]).dt.year
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(n),"st":st,"z1":z1,"f1":f1,"f5":f5,"f10":f10,
                             "reg":b["regime"],"fc":b["forecast"],"alloc":b["postRebalance_current_allocation"],
                             "sd":sd,"wd":wd,"yr":yr,"pos20":pos20,"ret60":ret60})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    m5=D[D.i%5==0].groupby("coin")["f5"].mean()
    D["drift5"]=D.coin.map(m5)
    D["u5"]=D.f5-D.drift5
    m1=D.groupby("coin")["f1"].mean(); D["u1"]=D.f1-D.coin.map(m1)
    G=D[(D.i%5==0)].dropna(subset=["st","u5"])
    out={}
    def tab(g,col,val):
        def f(x):
            v=x[val].dropna()
            return pd.Series({"n":len(v),"mean%":100*v.mean(),"t":v.mean()/(v.std()/np.sqrt(len(v))) if len(v)>2 else np.nan})
        return g.groupby(col).apply(f)
    G=G.copy()
    G["stq"]=pd.cut(G.st,[-99,-2,-1,-0.3,0.3,1,2,99])
    out["u5 by stretch bin, regime"]=tab(G,["reg","stq"],"u5")
    # signed carry by regime
    G["carry"]=np.sign(G.st)*G.u5
    out["signed carry u5 by regime"]=tab(G,"reg","carry")
    # one-day shock, all bars non-overlap for 5d
    G["z1q"]=pd.cut(G.z1,[-99,-2,-1,1,2,99])
    out["u5 by 1d shock z, regime"]=tab(G,["reg","z1q"],"u5")
    # range position
    G["pq"]=pd.cut(G.pos20,[-0.01,0.1,0.3,0.7,0.9,1.01])
    out["u5 by 20d range pos (choppy)"]=tab(G[G.reg=="unknown"],"pq","u5")
    # weekday next-day
    out["u1 by weekday all"]=tab(D.dropna(subset=["u1"]),"wd","u1")
    # vol level
    D2=D.dropna(subset=["sd","u1"]).copy()
    D2["sdq"]=D2.groupby("coin")["sd"].transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    G["sdq"]=G.groupby("coin")["sd"].transform(lambda x: pd.qcut(x,4,labels=False,duplicates="drop"))
    out["signed carry by vol quartile choppy"]=tab(G[G.reg=="unknown"],"sdq","carry")
    # book days
    dd=[]
    for coin,ws in data["days"].items():
        for w,d in ws.items():
            d=d.copy(); d["coin"]=coin; d["w"]=w; dd.append(d)
    DD=pd.concat(dd)
    bk=DD.groupby(["w","day"])["book_return"].mean().dropna()
    out["book days n,mean%,sd%"]=pd.Series({"n":len(bk),"mean%":100*bk.mean(),"sd%":100*bk.std(),
        "top5%share_of_sum":bk.nlargest(int(len(bk)*0.05)).sum()/bk.sum(),"bot5%sum":bk.nsmallest(int(len(bk)*0.05)).sum()})
    bw=bk.groupby(level=0).agg(["mean","count"]); bw["mean"]*=100
    out["book by window"]=bw
    # trades
    tr=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            t=t.copy(); t["coin"]=coin; tr.append(t)
    T=pd.concat(tr)
    T["dd"]=T.duration_minutes/1440
    T["dq"]=pd.cut(T.dd,[0,5,10,20,60,1000])
    out["trades by side"]=T.groupby("side")["net_profit_loss_percent"].agg(["count","mean","median"])
    out["trades by duration"]=T.groupby("dq")["net_profit_loss_percent"].agg(["count","mean"])
    return out
