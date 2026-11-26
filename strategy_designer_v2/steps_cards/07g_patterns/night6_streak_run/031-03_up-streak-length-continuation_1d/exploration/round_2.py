def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            vol=r.rolling(20,min_periods=10).std()
            f5=c.shift(-5)/c-1
            f1=c.shift(-1)/c-1
            up=(r>0).astype(int)
            us=up.groupby((up!=up.shift()).cumsum()).cumsum()*up
            df=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r1z":r/vol,"us":us,"vol":vol,"f5":f5,"f1":f1,"fc":b["forecast"].astype(float),
                "alloc":b["postRebalance_current_allocation"].astype(float),"pos":np.arange(len(b))})
            rows.append(df)
    A=pd.concat(rows)
    d=A[A.pos%5==0].dropna(subset=["f5","r1z"]).copy()
    d["ex"]=d["f5"]-d.groupby("coin")["f5"].transform("mean")
    d["exs"]=d["ex"]/(d["vol"]*np.sqrt(5))
    res={}
    def clus(x,y,day):
        X=np.column_stack([np.ones(len(x)),x]); beta=np.linalg.lstsq(X,y,rcond=None)[0]
        e=y-X@beta; XtXi=np.linalg.inv(X.T@X)
        S=np.zeros((2,2))
        for _,idx in pd.Series(np.arange(len(x))).groupby(day.values):
            u=(X[idx.values]*e[idx.values,None]).sum(0); S+=np.outer(u,u)
        V=XtXi@S@XtXi; return beta[1], beta[1]/np.sqrt(V[1,1])
    out=[]
    for name,s in [("all",d)]+list(d.groupby("coin")):
        x=s["r1z"].clip(-4,4).values; y=s["exs"].values
        b,t=clus(x,y,s["day"])
        bp,tp=clus(np.clip(x,0,4),y,s["day"]); bn,tn=clus(np.clip(x,-4,0),y,s["day"])
        out.append([name,len(s),s["day"].nunique(),b,t,bp,tp,bn,tn])
    res["slope exs on 1d z (pos/neg parts)"]=pd.DataFrame(out,columns=["g","n","days","b","t","b_pos","t_pos","b_neg","t_neg"]).set_index("g")
    # by year half for stability
    d["yr"]=d["day"].dt.year
    o=[]
    for y,s in d.groupby(d["yr"]<=2021):
        b,t=clus(s["r1z"].clip(-4,4).values,s["exs"].values,s["day"]); o.append([("<=2021" if y else ">2021"),len(s),b,t])
    res["1d z slope by period"]=pd.DataFrame(o,columns=["g","n","b","t"])
    # forecast deciles among positive: excess
    p=d[d.fc>0].copy(); p["q"]=pd.qcut(p.fc.rank(method="first"),5,labels=False)
    res["fc quintile"]=p.groupby("q").agg(n=("ex","size"),ex=("ex",lambda v:v.mean()*100),fc=("fc","mean"))
    # book: largest gain/loss days
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items(): dd.append(x.assign(coin=coin,w=w))
    D=pd.concat(dd); D["day"]=pd.to_datetime(D["day"])
    bk=D.groupby("day")[["book_return","coin_return"]].mean().dropna().sort_index()
    bk["nb1"]=bk["book_return"].shift(-1); bk["pb1"]=bk["book_return"].shift(1)
    bk["q"]=pd.qcut(bk["book_return"].rank(method="first"),10,labels=False)
    res["book deciles"]=bk.groupby("q")[["book_return","coin_return","pb1","nb1"]].mean()*100
    res["book beta to coins"]=float(np.polyfit(bk["coin_return"],bk["book_return"],1)[0])
    res["mean alloc"]=float(A["alloc"].mean())
    return res
