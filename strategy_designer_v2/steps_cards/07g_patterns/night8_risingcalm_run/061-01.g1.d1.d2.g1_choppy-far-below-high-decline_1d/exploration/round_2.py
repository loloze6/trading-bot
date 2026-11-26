def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"day":ts.dt.floor("D"),
                "fwd":c.shift(-H)/c-1,"z":r/r.rolling(20).std().shift(1),
                "z5":(c/c.shift(5)-1)/(r.rolling(20).std().shift(1)*np.sqrt(5)),
                "sd30":r.rolling(30,min_periods=20).std(),"tr60":c/c.shift(60)-1,
                "yr":ts.dt.year})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    mu=A[A.pos%H==0].groupby("coin")["fwd"].mean()
    A["ex"]=A["fwd"]-A["coin"].map(mu)
    A["calm"]=A.groupby("coin")["sd30"].transform(lambda s:s<=s.median())
    G=A[(A.pos%H==0)&A.ex.notna()&A.z.notna()&A.sd30.notna()].copy()
    def ct(g,col):
        x=g[[col,"day"]].dropna(); n=len(x)
        if n<5: return pd.Series({"n":n,"days":0,"mean%":np.nan,"t":np.nan})
        m=x[col].mean(); d=(x[col]-m).groupby(x["day"]).sum(); D=len(d)
        se=np.sqrt((d**2).sum()*D/(D-1))/n
        return pd.Series({"n":n,"days":D,"mean%":100*m,"t":m/se})
    G["s"]=np.sign(G["z"])*G["ex"]
    G["az"]=G["z"].abs()
    G["azb"]=pd.cut(G["az"],[0,0.5,1,1.5,2,3,99],labels=False)
    out={}
    out["signed cont by |z| bin x calm"]=G.groupby(["calm","azb"]).apply(lambda g:ct(g,"s")).reset_index()
    G["dir"]=np.where(G.z>0,"up","down")
    big=G[G.az>1.5]
    out["|z|>1.5 cont by calm x dir"]=big.groupby(["calm","dir"]).apply(lambda g:ct(g,"s")).reset_index()
    G["sw"]=G["s"]*G["az"]/G.groupby("calm")["az"].transform("mean")
    out["|z|-weighted cont by calm"]=G.groupby("calm").apply(lambda g:ct(g,"sw")).reset_index()
    out["|z|-weighted cont calm by year"]=G[G.calm].groupby("yr").apply(lambda g:ct(g,"sw")).reset_index()
    out["|z|-weighted cont calm by window"]=G[G.calm].groupby("w").apply(lambda g:ct(g,"sw")).reset_index()
    G["trd"]=np.where(G.tr60>0.1,"rising",np.where(G.tr60<-0.1,"falling","choppy"))
    out["|z|-weighted cont calm x trend"]=G[G.calm].groupby("trd").apply(lambda g:ct(g,"sw")).reset_index()
    # 5-day move in swing units
    G["s5"]=np.sign(G["z5"])*G["ex"]; G["az5"]=G["z5"].abs()
    G["sw5"]=G["s5"]*G["az5"]/G.groupby("calm")["az5"].transform("mean")
    out["5d swing-unit move weighted cont by calm"]=G.groupby("calm").apply(lambda g:ct(g,"sw5")).reset_index()
    G["az5b"]=pd.cut(G["az5"],[0,0.5,1,1.5,2,99],labels=False)
    out["5d cont by |z5| bin x calm"]=G.groupby(["calm","az5b"]).apply(lambda g:ct(g,"s5")).reset_index()
    out["5d weighted cont calm by window"]=G[G.calm].groupby("w").apply(lambda g:ct(g,"sw5")).reset_index()
    return out
