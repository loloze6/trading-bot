def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            ts=pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"z":r/sd,"sd":sd,
                "fwd":c.shift(-5)/c-1,"fwd3":c.shift(-3)/c-1,"wd":ts.dt.dayofweek,"day":ts.dt.floor("D"),
                "yr":ts.dt.year}))
    A=pd.concat(rows,ignore_index=True)
    A["agit"]=A.groupby("coin")["sd"].rank(pct=True)>0.5
    dr=A.loc[A.pos%5==0].groupby("coin")["fwd"].mean(); A["ex"]=A.fwd-A.coin.map(dr)
    dr3=A.loc[A.pos%3==0].groupby("coin")["fwd3"].mean(); A["ex3"]=A.fwd3-A.coin.map(dr3)
    A["zc"]=A.z.clip(-4,4)
    def signed(g,col):
        g=g.dropna(subset=[col,"zc"]); s=np.sign(g.zc)
        v=g[col]*s; m=v.mean(); d=(v-m).groupby(g.day).sum(); D=len(d)
        se=np.sqrt((d**2).sum()*D/(D-1))/len(g)
        w=g[col]*g.zc; mw=w.mean(); dw=(w-mw).groupby(g.day).sum()
        sew=np.sqrt((dw**2).sum()*D/(D-1))/len(g)
        big=g[g.zc.abs()>1.5]; vb=big[col]*np.sign(big.zc)
        return [len(g),D,m,m/se,mw,mw/sew,len(big),vb.mean()]
    cols=["n","days","signed_ex","t","zweighted","t_zw","n_big","big_signed"]
    out={}
    res={}
    for ag in [False,True]:
        for off in range(5):
            res[(ag,off)]=signed(A[(A.agit==ag)&(A.pos%5==off)],"ex")
    out["5d continuation calm/agit x offset"]=pd.DataFrame(res,index=cols).T
    res={}
    for ag in [False,True]:
        for off in range(3):
            res[(ag,off)]=signed(A[(A.agit==ag)&(A.pos%3==off)],"ex3")
    out["3d continuation calm/agit x offset"]=pd.DataFrame(res,index=cols).T
    G=A[(A.pos%5==0)&(~A.agit)]
    out["calm by coin"]=pd.DataFrame({k:signed(g,"ex") for k,g in G.groupby("coin")},index=cols).T
    out["calm by year"]=pd.DataFrame({k:signed(g,"ex") for k,g in G.groupby("yr")},index=cols).T
    return out
