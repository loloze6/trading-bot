def explore(data):
    import numpy as np, pandas as pd
    daily=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r1=c.pct_change()
            df=pd.DataFrame({"coin":coin,"w":w,"ts":pd.to_datetime(b["timestamp"]),"r1":r1,
                "r7p":c/c.shift(7)-1,"r30":c/c.shift(30)-1,"r60":c/c.shift(60)-1,
                "vol30":r1.rolling(30).std(),"inprof":(b["regime"]=="unknown"),
                "pos":b["postRebalance_current_allocation"],"fc":b["forecast"],
                "clpos":(c-b["low"])/(b["high"]-b["low"]).replace(0,np.nan),
                "hi30":c/c.rolling(30).max()-1,"lo30":c/c.rolling(30).min()-1})
            df["volrel"]=df["vol30"]/df["vol30"].expanding(30).median()
            df["f7"]=c.shift(-7)/c-1; df["f3"]=c.shift(-3)/c-1
            df["i"]=np.arange(len(df)); daily.append(df)
    D=pd.concat(daily,ignore_index=True); D["day"]=D["ts"].dt.floor("D")
    D["drift7"]=D.groupby("coin")["f7"].transform(lambda s: s[D.loc[s.index,"i"]%7==0].mean())
    D["ex7"]=D["f7"]-D["drift7"]
    def tday(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna().groupby("d")["v"].mean(); n=len(x)
        return pd.Series({"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan,"days":n})
    G=D[(D["i"]%7==0)&D["ex7"].notna()].copy()
    G["trend"]=pd.cut(G["r60"],[-9,-0.1,0.1,99],labels=["fall","chop","rise"])
    G["agit"]=np.where(G["volrel"]>1,"ag","calm")
    out={}
    def bk(df,col,q=3):
        d=df.dropna(subset=[col,"ex7"]).copy(); d["b"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        return d.groupby("b").apply(lambda g: pd.concat([pd.Series({"x":g[col].mean(),"n":len(g)}),tday(g["ex7"],g["day"])]))
    ca=G[(G.trend=="chop")&(G.agit=="ag")]; cc=G[(G.trend=="chop")&(G.agit=="calm")]
    out["chop-ag ex7 by r30 terc"]=bk(ca,"r30")
    out["chop-calm ex7 by r30 terc"]=bk(cc,"r30")
    out["chop-ag ex7 by r7 terc"]=bk(ca,"r7p")
    out["chop-ag ex7 by dist from 30d high terc"]=bk(ca,"hi30")
    out["chop-ag ex7 by volrel terc"]=bk(ca,"volrel")
    out["chop-ag by window"]=ca.groupby("w").apply(lambda g: tday(g["ex7"],g["day"]))
    out["chop-ag by coin"]=ca.groupby("coin").apply(lambda g: tday(g["ex7"],g["day"]))
    out["all ex7 by dist from 30d high quint"]=bk(G,"hi30",5)
    out["fall ex7 by r30 terc"]=bk(G[G.trend=="fall"],"r30")
    out["rise ex7 by r30 terc"]=bk(G[G.trend=="rise"],"r30")
    # every-bar check in exact profile (overlapping, informative only), counted as share
    P=D[D.inprof&D.ex7.notna()]
    out["exact profile bars: n, mean ex7, share neg"]=pd.Series({"n":len(P),"mean":P["ex7"].mean(),"neg":(P["ex7"]<0).mean(),"coin_days":P["day"].nunique()})
    return out
