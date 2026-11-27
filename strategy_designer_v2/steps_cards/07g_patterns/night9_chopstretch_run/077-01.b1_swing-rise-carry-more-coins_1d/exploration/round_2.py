import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            ts=pd.to_datetime(b["timestamp"])
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "v7":(c/c.shift(7)-1)/(sd*np.sqrt(7)),
                "v14":(c/c.shift(14)-1)/(sd*np.sqrt(14)),
                "v28":(c/c.shift(28)-1)/(sd*np.sqrt(28)),
                "f3":c.shift(-3)/c-1,"f7":c.shift(-7)/c-1,"f14":c.shift(-14)/c-1,
                "f1":c.shift(-1)/c-1,
                "cc":(b["regime"]!="chop").values,"day":ts.dt.floor("D").values,
                "yr":ts.dt.year.values,"wd":ts.dt.weekday.values})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    out={}
    def clus_slope(df,x,y):
        df=df.dropna(subset=[x,y])
        if len(df)<10: return pd.Series({"n":len(df),"days":np.nan,"beta":np.nan,"t":np.nan,"rho":np.nan})
        X=df[x]-df[x].mean(); Y=df[y]-df[y].mean()
        beta=(X*Y).sum()/(X*X).sum()
        e=Y-beta*X
        s=(X*e).groupby(df["day"]).sum()
        G=len(s)
        var=(s**2).sum()/((X*X).sum()**2)*G/(G-1)
        return pd.Series({"n":len(df),"days":G,"beta":beta,"t":beta/np.sqrt(var),"rho":stats.spearmanr(df[x],df[y])[0]})
    res={}
    for h in [3,7,14]:
        g=D[D.pos%h==0].copy()
        dr=g.groupby("coin")[f"f{h}"].mean()
        g["u"]=g[f"f{h}"]-g["coin"].map(dr)
        for L in ["v7","v14","v28"]:
            res[(h,L,"cc")]=clus_slope(g[g.cc],L,"u")
            res[(h,L,"other")]=clus_slope(g[~g.cc],L,"u")
    out["slope u_h on vsr_L, day-clustered"]=pd.DataFrame(res).T
    g=D[D.pos%7==0].copy()
    dr=g.groupby("coin")["f7"].mean(); g["u"]=g["f7"]-g["coin"].map(dr)
    gc=g[g.cc]
    out["cc h7 v14 by year"]=gc.groupby("yr").apply(lambda x:clus_slope(x,"v14","u"))
    out["cc h7 v14 by window"]=gc.groupby("w").apply(lambda x:clus_slope(x,"v14","u"))
    out["cc h7 v14 by coin"]=gc.groupby("coin").apply(lambda x:clus_slope(x,"v14","u"))
    out["cc h7 v14 excl 2021"]=clus_slope(gc[gc.yr!=2021],"v14","u")
    out["cc h7 v14 neg side only"]=clus_slope(gc[gc.v14<0],"v14","u")
    out["cc h7 v14 pos side only"]=clus_slope(gc[gc.v14>0],"v14","u")
    g1=D.dropna(subset=["f1"])
    out["wed f1 by year"]=g1[g1.wd==2].groupby("yr")["f1"].agg(["count","mean"])
    return out
