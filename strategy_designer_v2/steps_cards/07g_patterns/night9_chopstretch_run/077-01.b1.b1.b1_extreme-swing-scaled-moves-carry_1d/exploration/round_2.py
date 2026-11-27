import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=20).std()
            r14=c/c.shift(14)-1
            r60=c/c.shift(60)-1
            z=r14/(vol30*np.sqrt(14))
            zstd=(z-z.rolling(60,min_periods=20).mean())/z.rolling(60,min_periods=20).std()
            f7=c.shift(-7)/c-1
            vrank=vol30.rolling(120,min_periods=60).rank(pct=True)
            vrank_exp=vol30.expanding(min_periods=60).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b)),"z":z,"zstd":zstd,
                "r60":r60,"vrank":vrank,"vre":vrank_exp,"f7":f7,"regime":b["regime"].values,
                "day":ts.dt.floor("D"),"year":ts.dt.year,"fc":b["forecast"].values}))
    A=pd.concat(rows,ignore_index=True)
    out={}
    drift7=A.loc[A.pos%7==0,"f7"].mean()
    G=A[A.pos%7==0].dropna(subset=["z","f7","vrank"]).copy()
    G["u7"]=G.f7-drift7
    G["sz"]=np.sign(G.z)*G.u7
    def ct(g,col="sz"):
        x=g.dropna(subset=[col])
        if len(x)<5: return pd.Series({"n":len(x),"mean":np.nan,"t":np.nan,"tday":np.nan})
        m=x[col].mean()
        t=m/(x[col].std()/np.sqrt(len(x)))
        s=(x[col]-m).groupby(x.day).sum(); D=len(s)
        se=np.sqrt((s**2).sum()*D/(D-1))/len(x)
        return pd.Series({"n":len(x),"mean":m,"t":t,"tday":m/se})
    C=G[G.vrank<=0.5].copy()
    Ag=G[G.vrank>0.5].copy()
    C["azb"]=pd.cut(C.z.abs(),[0,0.5,1,1.5,2,9])
    Ag["azb"]=pd.cut(Ag.z.abs(),[0,0.5,1,1.5,2,9])
    out["calm: signed carry by |z| bin"]=C.groupby("azb").apply(ct)
    out["agitated: signed carry by |z| bin"]=Ag.groupby("azb").apply(ct)
    out["calm |z|>1 by direction"]=C[C.z.abs()>1].groupby(np.sign(C.z)).apply(ct)
    out["calm |z|>1 by year"]=C[C.z.abs()>1].groupby("year").apply(ct)
    out["calm |z|>1 by window"]=C[C.z.abs()>1].groupby("win").apply(ct)
    Ce=G[G.vre<=0.5]
    out["calm (expanding rank) |z|>1"]=ct(Ce[Ce.z.abs()>1])
    # continuous: z*u7 weighted
    for nm,S in [("calm",C),("ag",Ag)]:
        x=S.z*S.u7
        out[f"{nm}: mean z*u7, t, n"]=pd.Series({"m":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x))),"n":len(x)})
    # raw z vs standardised z inside calm
    Cs=C.dropna(subset=["zstd"])
    out["calm: corr u7 with z vs zstd"]=pd.Series({"z":np.corrcoef(Cs.z,Cs.u7)[0,1],"zstd":np.corrcoef(Cs.zstd,Cs.u7)[0,1],"n":len(Cs)})
    out["calm |z|>1 by coin"]=C[C.z.abs()>1].groupby("coin").apply(ct)
    return out
