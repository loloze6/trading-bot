def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            sma=c.rolling(20).mean(); sd=r.rolling(20).std()
            st=(c-sma)/sma/sd
            z1=r/sd.shift(1)
            ret60=c/c.shift(60)-1
            ts=pd.to_datetime(b["timestamp"])
            sd30=r.rolling(30).std()
            vp=sd30.rolling(365,min_periods=120).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"st":st,"z1":z1,
              "f1":c.shift(-1)/c-1,"f5":c.shift(-5)/c-1,"f2":c.shift(-2)/c-1,"ret60":ret60,"vp":vp,
              "reg":b["regime"],"day":ts.dt.floor("D"),"wd":ts.dt.weekday,"yr":ts.dt.year})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    m5=D[D.i%5==0].groupby("coin")["f5"].mean(); D["u5"]=D.f5-D.coin.map(m5)
    m1=D.groupby("coin")["f1"].mean(); D["u1"]=D.f1-D.coin.map(m1)
    m2=D[D.i%2==0].groupby("coin")["f2"].mean(); D["u2"]=D.f2-D.coin.map(m2)
    D["trend"]=np.where(D.ret60>0.10,"rising",np.where(D.ret60<-0.10,"falling","choppy"))
    D.loc[D.ret60.isna(),"trend"]=np.nan
    D["agit"]=np.where(D.vp>0.5,"agit","calm"); D.loc[D.vp.isna(),"agit"]=np.nan
    def ct(x,val):
        x=x.dropna(subset=[val])
        if len(x)<10: return pd.Series({"n":len(x),"days":np.nan,"mean%":np.nan,"tday":np.nan})
        dev=x[val]-x[val].mean()
        s=dev.groupby(x["day"]).sum(); Dn=len(s); n=len(x)
        se=np.sqrt((s**2).sum()*Dn/(Dn-1))/n
        return pd.Series({"n":n,"days":Dn,"mean%":100*x[val].mean(),"tday":x[val].mean()/se})
    out={}
    G=D[D.i%5==0].dropna(subset=["st","u5","trend"]).copy()
    G["carry"]=np.sign(G.st)*G.u5
    G["carryw"]=G.st.clip(-5,5)*G.u5
    G["side"]=np.where(G.st>0,"above","below")
    out["carry by trend x side (day t)"]=G.groupby(["trend","side"]).apply(lambda x:ct(x,"carry"))
    out["graded carry st*u5 by trend"]=G.groupby("trend").apply(lambda x:ct(x,"carryw"))
    out["carry rising/falling by year"]=G[G.trend!="choppy"].groupby("yr").apply(lambda x:ct(x,"carry"))
    G2=G.dropna(subset=["agit"])
    out["carry by trend x agit"]=G2.groupby(["trend","agit"]).apply(lambda x:ct(x,"carry"))
    # stretch bins in rising/falling with day t
    G["stq"]=pd.cut(G.st,[-99,-2,-1,0,1,2,99])
    out["u5 by stretch, rising"]=G[G.trend=="rising"].groupby("stq").apply(lambda x:ct(x,"u5"))
    out["u5 by stretch, falling"]=G[G.trend=="falling"].groupby("stq").apply(lambda x:ct(x,"u5"))
    # weekday day-clustered
    out["u1 by weekday day t"]=D.groupby("wd").apply(lambda x:ct(x,"u1"))
    out["u1 weekday 4 minus 0 by year"]=D[D.wd.isin([0,4])].groupby(["yr","wd"])["u1"].mean().unstack()*100
    # 1d shock grid 2
    H=D[D.i%2==0].dropna(subset=["z1","u2","trend"]).copy()
    H["zq"]=pd.cut(H.z1,[-99,-2,-1,1,2,99])
    out["u2 after 1d shock by trend"]=H.groupby(["trend","zq"]).apply(lambda x:ct(x,"u2"))
    return out
