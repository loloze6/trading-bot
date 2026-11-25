def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"];h=b["high"];l=b["low"]
            rng=(h-l)
            d=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"])})
            d["clv"]=((h-c)/rng.replace(0,np.nan)).values
            r1=c.pct_change()
            d["r1p"]=r1.values
            sd=r1.rolling(30,min_periods=15).std().shift(1)
            d["z1"]=(r1/sd).values
            d["r2p"]=(c/c.shift(2)-1).values
            d["z2"]=((c/c.shift(2)-1)/(sd*np.sqrt(2))).values
            d["nr1"]=(c.shift(-1)/c-1).values
            rr=rng/c
            d["rrrel"]=(rr/rr.rolling(30,min_periods=10).mean()).values
            d["regime"]=b["regime"].values
            d["alloc"]=b["postRebalance_current_allocation"].values
            d["pos"]=np.arange(len(b))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    mu=D.groupby("coin")["nr1"].mean()
    D["ex1"]=D["nr1"]-D["coin"].map(mu)
    D["day"]=D["ts"].dt.floor("D")
    D["inreg"]=D["regime"].eq("mean_reversion")
    D["yr"]=D.ts.dt.year
    def tday(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna()
        if len(x)<10: return np.nan
        m=x.v.mean(); g=(x.v-m).groupby(x.d).sum()
        return m/(np.sqrt((g**2).sum())/len(x))
    def ols(sub,xs,y="ex1"):
        s=sub.dropna(subset=xs+[y])
        X=np.column_stack([np.ones(len(s))]+[((s[x]-s[x].mean())/s[x].std()).values for x in xs])
        Y=s[y].values
        XtX=np.linalg.inv(X.T@X); bta=XtX@X.T@Y; e=Y-X@bta
        G=pd.DataFrame(X*e[:,None]).groupby(s["day"].values).sum().values
        V=XtX@(G.T@G)@XtX
        return pd.DataFrame({"coef%":bta*100,"t":bta/np.sqrt(np.diag(V))},index=["const"]+xs).assign(n=len(s),days=s.day.nunique())
    def tab(sub,col,q=5,y="ex1"):
        s=sub.dropna(subset=[col,y]).copy()
        s["b"]=pd.qcut(s[col].rank(method="first"),q,labels=False)
        return s.groupby("b").apply(lambda g: pd.Series({"mean_x":g[col].mean(),"mean%":g[y].mean()*100,"t":tday(g[y],g["day"]),"n":len(g)}))
    res={}
    res["ols all z1"]=ols(D,["z1"])
    res["ols all r1p"]=ols(D,["r1p"])
    res["ols all z1+clv"]=ols(D,["z1","clv"])
    res["ols regime z1+clv"]=ols(D[D.inreg],["z1","clv"])
    res["ols out z1+clv"]=ols(D[~D.inreg],["z1","clv"])
    res["z1 quint all"]=tab(D,"z1")
    res["z2 quint all"]=tab(D,"z2")
    res["ols all z1, rrrel>median"]=ols(D[D.rrrel>D.rrrel.median()],["z1"])
    res["ols all z1, rrrel<=median"]=ols(D[D.rrrel<=D.rrrel.median()],["z1"])
    res["z1 corr by year"]=D.dropna(subset=["z1","ex1"]).groupby("yr").apply(lambda g: pd.Series({"corr":g.z1.corr(g.ex1),"n":len(g)}))
    res["z1 corr by coin"]=D.dropna(subset=["z1","ex1"]).groupby("coin").apply(lambda g: pd.Series({"corr":g.z1.corr(g.ex1),"n":len(g)}))
    res["z1 corr by window"]=D.dropna(subset=["z1","ex1"]).groupby("w").apply(lambda g: pd.Series({"corr":g.z1.corr(g.ex1),"n":len(g)}))
    # book's days
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=coin,w=w))
    B=pd.concat(dd,ignore_index=True)
    B["day"]=pd.to_datetime(B["day"]).dt.floor("D")
    bk=B.groupby("day")[["book_return","coin_return"]].mean().dropna()
    q=bk.book_return.quantile([0.05,0.95])
    res["book tails"]=pd.DataFrame({"n":[ (bk.book_return<=q.iloc[0]).sum(),(bk.book_return>=q.iloc[1]).sum()],
        "mean book%":[bk.book_return[bk.book_return<=q.iloc[0]].mean()*100,bk.book_return[bk.book_return>=q.iloc[1]].mean()*100],
        "mean coins%":[bk.coin_return[bk.book_return<=q.iloc[0]].mean()*100,bk.coin_return[bk.book_return>=q.iloc[1]].mean()*100]},index=["worst5%","best5%"])
    return res
