def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            z=(c-sma)/sma/sd
            tr60=c/c.shift(60)-1
            # sign of trend from regime: within window, use longest available lookback up to 60
            trl=c/c.shift(30)-1
            sd30=r.rolling(30).std()
            fwd=c.shift(-H)/c-1
            day=pd.to_datetime(b["timestamp"]).dt.floor("D")
            rows.append(pd.DataFrame({"coin":coin,"w":w,"z":z,"tr60":tr60,"tr30":trl,"sd30":sd30,
                "fwd":fwd,"reg":b["regime"].astype(str),"pos":np.arange(len(b)),"day":day}))
    A=pd.concat(rows,ignore_index=True)
    g0=A[A.pos%H==0]
    drift=g0.groupby("coin")["fwd"].mean(); usd=g0.groupby("coin")["fwd"].std()
    A["ex"]=A["fwd"]-A.coin.map(drift); A["exs"]=A["ex"]/A.coin.map(usd)
    medsd=A.groupby("coin")["sd30"].median()
    A["agit"]=np.where(A.sd30>A.coin.map(medsd),"agit","calm")
    # trend side: regime 'chop' = |60d|>10 (trend). use tr60 where present else tr30 sign
    sgn=np.sign(A.tr60.fillna(A.tr30))
    A["prof"]=np.where(A.reg=="unknown","choppy",np.where(sgn>0,"rising","falling"))
    G=A[(A.pos%H==0)&A.ex.notna()&A.z.notna()].copy()
    def dayt(g,col="ex"):
        s=(g[col]-0).groupby(g.day).sum(); n=g.day.nunique()
        m=g[col].mean()
        # clustered: per-day sums
        dev=(g[col]-m).groupby(g.day).sum()
        se=np.sqrt((dev**2).sum())/len(g)
        return m/se, n
    out={}
    G["zq"]=pd.qcut(G.z,5,labels=False)
    def summ(g):
        t,nd=dayt(g)
        return pd.Series({"n":len(g),"days":nd,"zmean":g.z.mean(),"ex%":100*g.ex.mean(),"t_day":t,"str":g.exs.mean()})
    out["prof x zq"]=G.groupby(["prof","zq"]).apply(summ)
    out["prof x agit x side"]=G.assign(side=np.where(G.z>0,"up","dn")).groupby(["prof","agit","side"]).apply(summ)
    # signed-direction strength: unusual move in direction of z, graded by |z|
    G["dirx"]=np.sign(G.z)*G.ex
    G["az"]=G.z.abs()
    res={}
    for k,g in G.groupby(["prof","agit"]):
        s=stats.linregress(g.az,np.sign(g.z)*g.exs)
        gg=g[g.az>1]
        t,nd=dayt(gg.assign(ex=gg.dirx))
        res[str(k)]=[len(g),s.slope,s.slope/s.stderr,len(gg),100*gg.dirx.mean(),t]
    out["dir-signed slope on |z|"]=pd.DataFrame(res,index=["n","slope","t","n|z|>1","dirx%","t_day"]).T
    # by year-ish via window for falling below side
    F=G[(G.prof=="falling")&(G.z<0)]
    out["falling dn by window"]=F.groupby("w").apply(lambda g:pd.Series({"n":len(g),"ex%":100*g.ex.mean()}))
    R=G[(G.prof=="rising")&(G.z>0)]
    out["rising up by window"]=R.groupby("w").apply(lambda g:pd.Series({"n":len(g),"ex%":100*g.ex.mean()}))
    out["prof counts"]=G.prof.value_counts()
    return out
