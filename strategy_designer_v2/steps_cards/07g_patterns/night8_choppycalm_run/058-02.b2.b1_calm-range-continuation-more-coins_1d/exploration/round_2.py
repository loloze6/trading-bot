def explore(data):
    import numpy as np, pandas as pd
    H=5
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; hi=b["high"].rolling(20).max(); lo=b["low"].rolling(20).min()
            r1=c.pct_change()
            vol30=r1.rolling(30).std()
            x=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "rp":(c-lo)/(hi-lo),"ret60":c/c.shift(60)-1,
                "vrel":vol30/vol30.expanding(30).median(),
                "z1":r1/r1.rolling(20).std().shift(1),
                "fwd":c.shift(-H)/c-1,"inprof":(b["regime"]=="unknown").astype(int),
                "alloc":b["postRebalance_current_allocation"]})
            rows.append(x)
    d=pd.concat(rows)
    g=d[d.pos%H==0].dropna(subset=["fwd"]).copy()
    g["ex"]=g["fwd"]-g.groupby("coin")["fwd"].transform("mean")
    g["trend"]=np.where(g.ret60>0.10,"rising",np.where(g.ret60<-0.10,"falling","choppy"))
    g.loc[g.ret60.isna(),"trend"]="na"
    g["agit"]=np.where(g.vrel>1,"agit","calm"); g.loc[g.vrel.isna(),"agit"]="na"
    def slope(df,xc):
        df=df.dropna(subset=[xc,"ex"])
        if len(df)<30: return pd.Series({"n":len(df),"slope":np.nan,"t":np.nan})
        xx=df[xc]-df[xc].mean(); b=(xx*df.ex).sum()/(xx**2).sum()
        res=df.ex-df.ex.mean()-b*xx
        s=(xx*res).groupby(df.day).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/(xx**2).sum()
        return pd.Series({"n":len(df),"days":G,"slope":b,"t":b/se})
    def qt(df,col):
        df=df.dropna(subset=[col]).copy()
        df["q"]=pd.qcut(df[col],5,labels=False,duplicates="drop")
        out=[]
        for q,s in df.groupby("q"):
            dm=s.groupby("day")["ex"].sum(); n=len(s)
            m=s.ex.mean(); t=dm.sum()/np.sqrt(((dm-dm.mean()*0)**2).sum()) if n>1 else np.nan
            out.append([q,n,m,t])
        return pd.DataFrame(out,columns=["q","n","mean","t_day"]).round(4)
    out={}
    out["rp slope by trend"]=g.groupby("trend").apply(lambda s:slope(s,"rp")).round(4)
    out["rp slope by trend x agit"]=g.groupby(["trend","agit"]).apply(lambda s:slope(s,"rp")).round(4)
    out["z1 slope by trend"]=g.groupby("trend").apply(lambda s:slope(s,"z1")).round(4)
    out["rp q all"]=qt(g,"rp")
    out["rp q falling"]=qt(g[g.trend=="falling"],"rp")
    out["rp q choppy"]=qt(g[g.trend=="choppy"],"rp")
    out["z1 q all"]=qt(g,"z1")
    # half split stability of rp slope all
    g["half"]=np.where(g.w.str[1:].astype(int)<=12,"B","C")
    out["rp slope by fold"]=g.groupby("half").apply(lambda s:slope(s,"rp")).round(4)
    # book: long vs short contribution per bar
    d["g"]=d["alloc"]*(d.groupby(["coin","w"])["fwd"].transform(lambda s:s)*0+ (d.groupby(["coin","w"]).apply(lambda s: s.fwd*0).values if False else 0))
    return out
