def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd20=r.rolling(20).std()
            sd30=r.rolling(30).std()
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "year":pd.to_datetime(b["timestamp"]).dt.year,
                "z5":(c/c.shift(5)-1)/(sd20*np.sqrt(5)),
                "z10":(c/c.shift(10)-1)/(sd20*np.sqrt(10)),
                "z20":(c/c.shift(20)-1)/(sd20*np.sqrt(20)),
                "sd20":sd20,"sd30":sd30,
                "fwd5":c.shift(-5)/c-1,"fwd3":c.shift(-3)/c-1,"fwd10":c.shift(-10)/c-1,
                "choppy":(b["regime"]=="unknown").values,"fc":b["forecast"].values})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    def ctt(g,col="u"):
        s=g.groupby("day")[col].sum(); n=len(g); G=len(s)
        if n<5 or G<3: return pd.Series({"mean":np.nan,"n":n,"days":G,"t":np.nan})
        m=g[col].mean()
        dev=(g[col]-m).groupby(g["day"]).sum()
        se=np.sqrt((dev**2).sum()*G/(G-1))/n
        return pd.Series({"mean":round(m,4),"n":n,"days":G,"t":round(m/se,2)})
    out={}
    for h in [3,5,10]:
        G=A[(A.pos%h==0)&A["fwd%d"%h].notna()].copy()
        G["u"]=G["fwd%d"%h]-G.coin.map(G.groupby("coin")["fwd%d"%h].mean())
        G["sdrel"]=G.sd30/G.groupby("coin").sd30.transform("median")
        G=G.dropna(subset=["z20","z5","sd30"])
        G["calm"]=G.sdrel<=1
        if h==5:
            G["z20q"]=pd.qcut(G.z20,5,labels=False); G["z5q"]=pd.qcut(G.z5,5,labels=False)
            G["z10q"]=pd.qcut(G.z10,5,labels=False)
            out["h5 choppy z20q clustered"]=G[G.choppy].groupby("z20q").apply(ctt)
            out["h5 choppy z10q clustered"]=G[G.choppy].groupby("z10q").apply(ctt)
            out["h5 calm z5q clustered"]=G[G.calm].groupby("z5q").apply(ctt)
            out["h5 agitated z5q clustered"]=G[~G.calm].groupby("z5q").apply(ctt)
            out["h5 calm z20q clustered"]=G[G.calm].groupby("z20q").apply(ctt)
            C=G[G.choppy].copy(); C["sig"]=-C.z20*C.u
            out["choppy z20 slope by year: mean(-z20*u)"]=C.groupby("year").apply(lambda g: ctt(g,"sig"))
            K=G[G.calm].copy(); K["sig"]=K.z5*K.u
            out["calm z5 momentum by year: mean(z5*u)"]=K.groupby("year").apply(lambda g: ctt(g,"sig"))
            Q=G[~G.calm].copy(); Q["sig"]=-Q.z5*Q.u
            out["agitated z5 reversal by year: mean(-z5*u)"]=Q.groupby("year").apply(lambda g: ctt(g,"sig"))
            # forecast in choppy: standardised vs raw
            F=G[G.choppy&(G.fc<0)].copy(); F["fq"]=pd.qcut(F.fc,3,labels=False,duplicates="drop")
            out["choppy fc<0 terciles (0=most negative)"]=F.groupby("fq").apply(ctt)
        else:
            G["z20q"]=pd.qcut(G.z20,5,labels=False); G["z5q"]=pd.qcut(G.z5,5,labels=False)
            out["h%d choppy z20q"%h]=G[G.choppy].groupby("z20q").apply(ctt)
            out["h%d calm z5q"%h]=G[G.calm].groupby("z5q").apply(ctt)
    return out
