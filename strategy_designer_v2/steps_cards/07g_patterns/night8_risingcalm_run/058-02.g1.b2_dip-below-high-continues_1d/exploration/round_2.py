def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            sd30=r1.rolling(30,min_periods=20).std()
            d=pd.DataFrame({"coin":coin,"win":w,"pos":np.arange(len(b))})
            d["dayid"]=pd.to_datetime(b["timestamp"]).dt.floor("D")
            mx=c.rolling(5,min_periods=5).max()
            d["dip"]=(c-mx)/mx/sd30
            mx10=c.rolling(10,min_periods=10).max()
            d["dip10"]=(c-mx10)/mx10/sd30
            mn5=c.rolling(5,min_periods=5).min()
            d["above_low"]=(c-mn5)/mn5/sd30
            d["tr60"]=c/c.shift(60)-1
            d["tr30"]=c/c.shift(30)-1
            d["sd30"]=sd30
            d["f5"]=c.shift(-5)/c-1
            d["f3"]=c.shift(-3)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["agit"]=D.sd30>D.coin.map(D.groupby("coin").sd30.median())
    G=D[(D.pos%5==0)&D.f5.notna()].copy()
    drift=G.groupby("coin").f5.mean(); usual=G.groupby("coin").f5.std()
    G["ex"]=G.f5-G.coin.map(drift); G["exz"]=G.ex/G.coin.map(usual)
    def slope(X,col):
        X=X[[col,"ex","dayid"]].dropna()
        if len(X)<30: return np.nan,np.nan,len(X)
        x=X[col]-X[col].mean(); y=X.ex-X.ex.mean()
        bta=(x*y).sum()/(x*x).sum(); e=y-bta*x
        g=(x*e).groupby(X.dayid).sum()
        se=np.sqrt((g**2).sum())/(x*x).sum()
        return bta,bta/se,len(X)
    def tday(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna()
        m=x.v.mean(); g=(x.v-m).groupby(x.d).sum(); se=np.sqrt((g**2).sum())/len(x)
        return m,m/se,len(x)
    res={}
    G["tr"]=np.where(G.tr60>0.10,"rising",np.where(G.tr60<-0.10,"falling",np.where(G.tr60.notna(),"choppy","na")))
    G["tr30c"]=np.where(G.tr30>0.10,"rising",np.where(G.tr30<-0.10,"falling",np.where(G.tr30.notna(),"choppy","na")))
    out=[]
    for col in ["dip","dip10","above_low"]:
        for key in ["tr","tr30c"]:
            for (tr,ag),g in G.groupby([key,"agit"]):
                b,t,n=slope(g,col)
                deep=g[g[col]<=g[col].quantile(0.2)] if col!="above_low" else g[g[col]>=g[col].quantile(0.8)]
                m,tt,nn=tday(deep.ex,deep.dayid)
                atop=g[g[col]>=-1e-12] if col!="above_low" else g[g[col]<=1e-12]
                m2,t2,n2=tday(atop.ex,atop.dayid)
                out.append({"x":col,"trkey":key,"trend":tr,"agit":ag,"slope":b,"t":t,"n":n,"ext20_ex":m,"ext20_t":tt,"edge0_ex":m2,"edge0_t":t2,"edge0_n":n2})
    res["by_profile"]=pd.DataFrame(out)
    out=[]
    for col in ["dip","dip10"]:
        b,t,n=slope(G,col); out.append({"x":col,"slope":b,"t":t,"n":n})
        for w,g in G.groupby("win"):
            b,t,n=slope(g,col); out.append({"x":col+"_"+w,"slope":b,"t":t,"n":n})
    res["slope_by_window"]=pd.DataFrame(out)
    return res
