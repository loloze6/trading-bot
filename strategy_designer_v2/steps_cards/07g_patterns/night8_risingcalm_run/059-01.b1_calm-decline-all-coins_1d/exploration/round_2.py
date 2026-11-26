def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30,min_periods=20).std()
            s14=(c/c.shift(14)-1)/(sd30*np.sqrt(14))
            tr60=c/c.shift(60)-1
            f5=c.shift(-5)/c-1
            rng=(b["high"]-b["low"])/c/sd30
            clo=(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan)
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"s14":s14,"tr60":tr60,"f5":f5,
                "agit":(b["regime"]=="chop"),"fc":b["forecast"],"rng":rng,"clo":clo,"yr":ts.dt.year,
                "day":ts.dt.floor("D")})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    G=D[(D.pos%5==0)&D.f5.notna()].copy()
    G["x5"]=G.f5-G.coin.map(G.groupby("coin").f5.mean())
    def ct(g,col="x5",sign=1.0):
        g=g.dropna(subset=[col]); v=sign*g[col]
        m=v.mean(); dev=(v-m).groupby(g["day"]).sum()
        se=np.sqrt((dev**2).sum())/len(v) if len(v)>1 else np.nan
        return pd.Series({"n":len(v),"days":g["day"].nunique(),"mean%":100*m,"t_day":m/se if se>0 else np.nan})
    out={}
    C=G[~G.agit].dropna(subset=["s14"]).copy()
    # graded: slope of x5 on s14 in calm, clustered by day via per-window
    out["calm: s14 bins -> excess5 (day t)"]=C.assign(b=pd.cut(C.s14,[-9,-2,-1,-0.5,0,0.5,1,2,9])).groupby("b").apply(ct).round(3)
    C["side"]=np.sign(C.s14)
    C["sx"]=C.side*C.x5
    C["wx"]=C.s14.clip(-3,3)*C.x5
    out["calm: momentum signed s14*x5 by window"]=C.groupby("w").apply(lambda g:ct(g,"wx")).round(3)
    out["calm: momentum by year"]=C.groupby("yr").apply(lambda g:ct(g,"wx")).round(3)
    out["calm: momentum by side x trend"]=C.assign(tr=pd.cut(C.tr60,[-9,-0.1,0.1,9],labels=["fall","chop","rise"])).dropna(subset=["tr"]).groupby(["tr","side"]).apply(lambda g:ct(g,"sx")).round(3)
    A=G[G.agit].dropna(subset=["s14"]).copy(); A["wx"]=A.s14.clip(-3,3)*A.x5
    out["agit: momentum all"]=pd.DataFrame(ct(A,"wx")).T.round(3)
    out["calm: momentum all"]=pd.DataFrame(ct(C,"wx")).T.round(3)
    # forecast vs raw s14 on calm neg cases
    N=C[C.s14<0]
    out["calm neg: share fc<0, corr fc vs s14"]=pd.Series({"share_fc_neg":(N.fc<0).mean(),"corr":N[["fc","s14"]].corr().iloc[0,1],"n":len(N)}).round(3)
    out["calm neg: fc<0 vs fc==0 excess"]=N.assign(act=N.fc<0).groupby("act").apply(ct).round(3)
    # narrow range low close
    R=G.dropna(subset=["rng","clo"]).copy()
    R["narrow"]=R.rng<R.rng.median(); R["low"]=R.clo<0.33
    out["narrow x low x agit"]=R.groupby(["agit","narrow","low"]).apply(ct).round(3)
    R["cl3"]=pd.cut(R.clo,[-0.01,0.2,0.4,0.6,0.8,1.01])
    out["narrow days: close loc bins"]=R[R.narrow].groupby("cl3").apply(ct).round(3)
    out["narrow low by window"]=R[R.narrow&R.low].groupby("w").apply(ct).round(3)
    return out
