def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float); l=b["low"].astype(float); o=b["open"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b))})
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["dayid"]=d["ts"].dt.floor("D")
            d["dip"]=(c-c.rolling(5,min_periods=5).max())/c.rolling(5,min_periods=5).max()/sd30
            d["r1z"]=r1/sd30
            d["r5past"]=(c/c.shift(5)-1)/(sd30*np.sqrt(5))
            d["r20past"]=(c/c.shift(20)-1)/(sd30*np.sqrt(20))
            d["tr60"]=c/c.shift(60)-1
            d["sd30"]=sd30
            d["clv"]=((c-l)/(h-l)).where(h>l)
            d["rng"]=((h-l)/c)/sd30
            d["f5"]=c.shift(-5)/c-1
            d["f1"]=c.shift(-1)/c-1
            d["wd"]=d["ts"].dt.weekday
            d["alloc"]=b["postRebalance_current_allocation"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%5==0)&D.f5.notna()].copy()
    drift=G.groupby("coin").f5.mean(); usual=G.groupby("coin").f5.std()
    G["ex"]=G.f5-G.coin.map(drift); G["exz"]=G.ex/G.coin.map(usual)
    def tday(s,days):
        x=pd.DataFrame({"v":s-s.mean() if False else s,"d":days}).dropna()
        m=x.v.mean(); g=(x.v-m).groupby(x.d).sum(); n=len(x)
        se=np.sqrt((g**2).sum())/n
        return m, m/se if se>0 else np.nan, n
    def tab(col,q=5,sub=None):
        X=G if sub is None else sub
        X=X[X[col].notna()].copy()
        X["b"]=pd.qcut(X[col].rank(method="first"),q,labels=False)
        out=[]
        for k,g in X.groupby("b"):
            m,t,n=tday(g.ex,g.dayid)
            out.append({"bin":k,"x_mean":g[col].mean(),"ex5_mean":m,"t":t,"n":n,"exz":g.exz.mean()})
        return pd.DataFrame(out)
    G["trend"]=np.where(G.tr60>0.10,"rising",np.where(G.tr60<-0.10,"falling",np.where(G.tr60.notna(),"choppy","na")))
    res={}
    res["dip_q5_all"]=tab("dip")
    for tr in ["rising","choppy","falling"]:
        res["dip_q5_"+tr]=tab("dip",5,G[G.trend==tr])
    res["r1z_q5"]=tab("r1z")
    res["r5past_q5"]=tab("r5past")
    res["r20past_q5"]=tab("r20past")
    res["sd30_q5"]=tab("sd30")
    res["clv_q5"]=tab("clv")
    res["rng_q5"]=tab("rng")
    # weekday on daily returns
    D["f1ex"]=D.f1-D.coin.map(D.groupby("coin").f1.mean())
    wd=[]
    for k,g in D[D.f1.notna()].groupby("wd"):
        m,t,n=tday(g.f1ex,g.dayid); wd.append({"wd_of_bar":k,"ex1":m,"t":t,"n":n})
    res["weekday_next1"]=pd.DataFrame(wd)
    res["trend_counts"]=G.trend.value_counts()
    # book: largest gains/losses days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["win"]=w; dd.append(x)
    DD=pd.concat(dd); 
    bk=DD.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    res["book_by_window"]=bk.groupby(level=0).agg(["mean","count"])
    return res
