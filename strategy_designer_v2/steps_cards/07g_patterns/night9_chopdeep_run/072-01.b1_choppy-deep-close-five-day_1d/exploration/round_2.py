def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float); h=b["high"].astype(float)
            r=c.pct_change(); sd=r.rolling(20).std(); hh=h.rolling(20).max()
            depth=(c-hh)/hh/sd
            sd30=r.rolling(30).std()
            df=pd.DataFrame({"coin":coin,"w":w,"i":np.arange(len(b)),"r":r,"depth":depth,"sd30":sd30,
              "choppy":(b["regime"]=="unknown"),"f5":c.shift(-5)/c-1,"f1":c.shift(-1)/c-1,
              "fc":b["forecast"].astype(float),"alloc":b["postRebalance_current_allocation"].astype(float),
              "yr":pd.to_datetime(b["timestamp"]).dt.year,
              "r20":c/c.shift(20)-1})
            rows.append(df)
    D=pd.concat(rows,ignore_index=True)
    D["sdrank"]=D.groupby("coin")["sd30"].rank(pct=True)
    g=D[D["i"]%5==0].copy()
    g["f5x"]=g["f5"]-g.groupby("coin")["f5"].transform("mean")
    out={}
    def tab(df,key,col):
        a=df.dropna(subset=[key,col]).groupby(key,observed=True)[col]
        t=a.agg(["mean","count","std"]); t["t"]=t["mean"]/(t["std"]/np.sqrt(t["count"])); return t[["mean","count","t"]]
    ch=g[g.choppy].dropna(subset=["depth","f5x"]).copy()
    ch["q"]=pd.qcut(ch["depth"],5,labels=False)
    out["depth quintile edges choppy"]=ch.groupby("q")["depth"].agg(["min","max"])
    deep=ch[ch.q==0]
    out["deepest q choppy by coin"]=tab(deep,"coin","f5x")
    out["deepest q choppy by window"]=deep.groupby("w")["f5x"].agg(["mean","count"])
    out["deepest q choppy by year"]=tab(deep,"yr","f5x")
    deep=deep.copy(); deep["up"]=deep["r"]>0
    out["deepest q choppy by up day"]=tab(deep,"up","f5x")
    ch["hv"]=ch["sdrank"]>0.5
    out["choppy depth q x high-vol (coin-rank proxy)"]=ch.groupby(["hv","q"])["f5x"].agg(["mean","count"])
    # deciles in choppy, raw depth
    ch["d"]=pd.qcut(ch["depth"],10,labels=False)
    out["choppy depth decile"]=tab(ch,"d","f5x")
    # forecast (standardised) vs raw depth in choppy
    s=ch[ch.fc<0].copy()
    out["corr fc vs depth choppy"]=float(s[["fc","depth"]].corr().iloc[0,1]) if len(s)>2 else np.nan
    s["fq"]=pd.qcut(s["fc"],5,labels=False,duplicates="drop")
    out["choppy f5x by forecast quintile"]=tab(s,"fq","f5x")
    # 20d return in choppy (deep closes may be a fall over 20 days)
    ch["rq"]=pd.qcut(ch["r20"],5,labels=False)
    out["choppy f5x by 20d return q"]=tab(ch,"rq","f5x")
    # allocation on deepest bars
    out["mean alloc choppy by depth q"]=ch.groupby("q")["alloc"].mean()
    return out
