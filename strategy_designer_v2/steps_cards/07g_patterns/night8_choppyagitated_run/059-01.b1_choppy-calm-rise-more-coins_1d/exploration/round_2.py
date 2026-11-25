def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"].astype(float)
            r1=c.pct_change()
            vol30=r1.rolling(30,min_periods=20).std()
            z1=r1/vol30
            z=(c/c.shift(7)-1)/(vol30*np.sqrt(7))
            r60=c/c.shift(60)-1
            vrank=vol30.rolling(120,min_periods=60).rank(pct=True)
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z1":z1,"z":z,"r60":r60,"vrank":vrank,
              "fwd1":c.shift(-1)/c-1,"fwd2":c.shift(-2)/c-1,"fwd3":c.shift(-3)/c-1,"fwd7":c.shift(-7)/c-1,
              "day":ts.dt.floor("D"),"yr":ts.dt.year,"inprof":(b["regime"]=="unknown")})
            rows.append(df)
    A=pd.concat(rows,ignore_index=True)
    A["trend"]=pd.cut(A.r60,[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    A["agit"]=np.where(A.vrank>0.5,"hi",np.where(A.vrank.notna(),"lo",None))
    out={}
    def ct(g,col):
        g=g[[col,"day"]].dropna()
        if len(g)<10: return pd.Series({"n":len(g),"days":np.nan,"mean":np.nan,"t_day":np.nan})
        m=g[col].mean(); s=(g[col]-m).groupby(g.day).sum(); D=len(s)
        se=np.sqrt((s**2).sum()*D/(D-1))/len(g)
        return pd.Series({"n":len(g),"days":D,"mean":m,"t_day":m/se})
    for h in [1,2,3]:
        col=f"fwd{h}"
        S=A[A.pos%h==0].copy()
        S["ex"]=S[col]-S.coin.map(S.groupby("coin")[col].mean())
        S["q"]=pd.qcut(S.z1,5,labels=False)
        out[f"ex{h} after 1-day move q, by profile, t"]=S.groupby(["trend","agit","q"]).apply(lambda g:ct(g,"ex"))["t_day"].unstack()
        out[f"ex{h} after 1-day move q, by profile, mean"]=S.groupby(["trend","agit","q"]).apply(lambda g:ct(g,"ex"))["mean"].unstack()
        if h==1:
            out["ex1 by 1-day q, by year"]=S.groupby(["yr","q"]).apply(lambda g:ct(g,"ex"))["t_day"].unstack()
            out["ex1 low q, counts by profile"]=S[S.q==0].groupby(["trend","agit"]).size()
    G=A[(A.pos%7==0)].copy()
    G["ex"]=G.fwd7-G.coin.map(G.groupby("coin")["fwd7"].mean())
    G["zq"]=pd.qcut(G.z,5,labels=False)
    out["ex7 by z q, in profile, day-clustered"]=G[G.inprof].groupby("zq").apply(lambda g:ct(g,"ex"))
    out["ex7 top z q in profile by year"]=G[G.inprof&(G.zq==4)].groupby("yr").apply(lambda g:ct(g,"ex"))
    return out
