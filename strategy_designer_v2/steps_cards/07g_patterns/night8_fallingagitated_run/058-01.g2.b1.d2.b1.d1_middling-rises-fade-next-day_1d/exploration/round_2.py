def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30,min_periods=20).std()
            ts=pd.to_datetime(b["timestamp"])
            d={"coin":coin,"w":w,"pos":np.arange(len(b)),"inprof":(b["regime"]=="unknown").values,
               "tr60":(c/c.shift(60)-1).values,"day":ts.dt.floor("D").values,"sd":sd.values}
            for k in (2,3,5):
                d[f"z{k}"]=((c/c.shift(k)-1)/(sd*np.sqrt(k))).values
            for h in (1,2,3,5):
                d[f"f{h}"]=(c.shift(-h)/c-1).values
            d["z1"]=(r/sd).values
            rows.append(pd.DataFrame(d))
    D=pd.concat(rows,ignore_index=True)
    vol=D.groupby("coin")["sd"].transform(lambda x: x.rank(pct=True))
    D["agit"]=vol>0.5
    drift={h:D.loc[D.pos%h==0,f"f{h}"].mean() for h in (1,2,3,5)}
    def summ(g,col):
        g=g.dropna(subset=[col])
        if len(g)<8: return pd.Series({"n":len(g),"days":np.nan,"mean":np.nan,"t_day":np.nan})
        m=g[col].mean()
        s=g.groupby("day")[col].apply(lambda x:(x-m).sum()); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/len(g)
        return pd.Series({"n":len(g),"days":G,"mean":m,"t_day":m/se})
    out={}
    for k,h in [(2,2),(3,3),(3,5),(5,5),(5,3)]:
        G=D[(D.pos%h==0)].copy(); G["u"]=G[f"f{h}"]-drift[h]
        G["b"]=pd.cut(G[f"z{k}"],[-99,-1,-0.3,0.3,0.8,1.3,99])
        out[f"inprof_z{k}_next{h}"]=G[G.inprof].groupby("b").apply(lambda g:summ(g,"u"))
        # correlation slope within up side
        gp=G[G.inprof&(G[f"z{k}"]>0)].dropna(subset=["u",f"z{k}"])
        out[f"inprof_up_corr_z{k}_next{h}"]=pd.Series({"n":len(gp),"corr":gp[[f"z{k}","u"]].corr().iloc[0,1]})
    # choppy agitated, up days next 1 and 3-day rises next 3
    D["trend"]=pd.cut(D["tr60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G1=D.copy(); G1["u"]=G1["f1"]-drift[1]
    G1["b"]=pd.cut(G1["z1"],[-99,-1,0,1,99])
    out["nonprof_trend_agit_z1_next1"]=G1[~G1.inprof].groupby(["trend","agit","b"]).apply(lambda g:summ(g,"u"))["mean"].unstack()
    out["nonprof_trend_agit_z1_next1_t"]=G1[~G1.inprof].groupby(["trend","agit","b"]).apply(lambda g:summ(g,"u"))["t_day"].unstack()
    G3=D[D.pos%3==0].copy(); G3["u"]=G3["f3"]-drift[3]
    G3["b"]=pd.cut(G3["z3"],[-99,-0.5,0.5,99])
    out["nonprof_trend_z3_next3_t"]=G3[~G3.inprof].groupby(["trend","b"]).apply(lambda g:summ(g,"u")).unstack()
    # in-profile by year: up day z 0-1 next1
    g=G1[G1.inprof&(G1.z1>0)&(G1.z1<=1)].copy(); g["yr"]=pd.to_datetime(g["day"]).dt.year
    out["inprof_mid_up_by_year"]=g.groupby("yr").apply(lambda x:summ(x,"u"))
    g=G1[G1.inprof&(G1.z1<-1)].copy(); g["yr"]=pd.to_datetime(g["day"]).dt.year
    out["inprof_bigdown_by_year"]=g.groupby("yr").apply(lambda x:summ(x,"u"))
    return out
