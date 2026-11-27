def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r1=c.pct_change()
            r20=c/c.shift(20)-1
            sd20=r1.rolling(20,min_periods=20).std()
            hi20=c.rolling(20,min_periods=20).max()
            depth=(hi20-c)/c/sd20
            ts=pd.to_datetime(b["timestamp"])
            df=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),"r1":r1,"r20":r20,
                             "z20":r20/(sd20*np.sqrt(20)),"depth":depth,"f10":c.shift(-10)/c-1,
                             "f5":c.shift(-5)/c-1,"choppy":(b["regime"]!="chop"),"yr":ts.dt.year,
                             "day":ts.dt.floor("D"),"alloc":b["postRebalance_current_allocation"]})
            rows.append(df)
    d=pd.concat(rows,ignore_index=True)
    for h in (10,5):
        g=d[d.pos%h==0]
        d[f"u{h}"]=d[f"f{h}"]-d.coin.map(g.groupby("coin")[f"f{h}"].mean())
    def tcl(s,days):
        x=pd.DataFrame({"v":s,"d":days}).dropna()
        if len(x)<5: return np.nan
        m=x.v.mean(); dd=x.groupby("d")["v"].apply(lambda v:(v-m).sum())
        se=np.sqrt((dd**2).sum())/len(x)
        return m/se
    def tab(sub,col,u,q):
        sub=sub.dropna(subset=[col,u]).copy()
        sub["b"]=pd.qcut(sub[col],q,labels=False,duplicates="drop")
        return sub.groupby("b").apply(lambda g: pd.Series({"lo":g[col].min(),"hi":g[col].max(),"mean_u":g[u].mean(),
               "t":tcl(g[u],g["day"]),"n":len(g),"days":g.day.nunique()}))
    out={}
    G=d[d.pos%10==0]; ch=G[G.choppy]
    out["choppy z20 10d"]=tab(ch,"z20","u10",5)
    G5=d[d.pos%5==0]; ch5=G5[G5.choppy]
    out["choppy z20 5d"]=tab(ch5,"z20","u5",5)
    out["choppy up r20<0 depth 5d"]=tab(ch5[(ch5.r1>0)&(ch5.r20<0)],"depth","u5",3)
    out["choppy down r20<0 depth 5d"]=tab(ch5[(ch5.r1<0)&(ch5.r20<0)],"depth","u5",3)
    out["choppy r20>0 depth 5d"]=tab(ch5[ch5.r20>0],"depth","u5",3)
    # corr of z20 with u10 in choppy by year (grid 5 for count)
    x=ch5.dropna(subset=["z20","u5"])
    out["choppy z20 vs u5 corr by year"]=x.groupby("yr").apply(lambda g: pd.Series({"corr":g.z20.corr(g.u5),"n":len(g)}))
    xs=ch5[(ch5.r20<0)].dropna(subset=["depth","u5"])
    out["choppy r20<0 depth corr by year"]=xs.groupby("yr").apply(lambda g: pd.Series({"corr":g.depth.corr(g.u5),"n":len(g)}))
    # book: gain by year
    D=pd.concat([x.assign(coin=c,w=w) for c,ws in data["days"].items() for w,x in ws.items()])
    D["yr"]=pd.to_datetime(D["day"]).dt.year
    out["book by year"]=D.groupby("yr")[["book_return","coin_return"]].mean()
    return out
