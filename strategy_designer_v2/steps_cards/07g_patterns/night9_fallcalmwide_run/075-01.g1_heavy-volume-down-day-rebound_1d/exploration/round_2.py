def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            cl=b["close"].astype(float); v=b["volume"].astype(float)
            d=pd.DataFrame(index=b.index)
            d["coin"]=c; d["w"]=w
            d["ts"]=pd.to_datetime(b["timestamp"])
            d["r0"]=cl/cl.shift(1)-1
            d["r1"]=cl.shift(-1)/cl-1
            d["r3"]=cl.shift(-3)/cl-1
            d["vr"]=v/v.shift(1).rolling(20).mean()
            d["clpos"]=(cl-b["low"].astype(float))/(b["high"].astype(float)-b["low"].astype(float)).replace(0,np.nan)
            d["r60"]=cl/cl.shift(60)-1
            d["vol20"]=d["r0"].rolling(20).std()
            d["vol90"]=d["r0"].rolling(90).std()
            d["r5"]=cl/cl.shift(5)-1
            d["alloc"]=b["postRebalance_current_allocation"].astype(float)
            d["gain"]=d["alloc"]*d["r1"]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D=D.dropna(subset=["r0","r1"])
    mu=D.groupby("coin")["r1"].mean()
    D["ex"]=D["r1"]-D["coin"].map(mu)
    D["z0"]=D["r0"]/D["vol20"]
    D["lvr"]=np.log(D["vr"].where(D["vr"]>0))
    D["year"]=D["ts"].dt.year; D["wd"]=D["ts"].dt.weekday
    D["day"]=D["ts"].dt.floor("D")
    D["agit"]=np.where(D["vol20"]>D["vol90"],"agit","calm")
    def tstat(x):
        x=x.dropna(); n=len(x)
        if n<3: return pd.Series({"n":n,"mean%":np.nan,"t":np.nan})
        return pd.Series({"n":n,"mean%":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(n))})
    def dayt(df,col="ex"):
        return tstat(df.groupby("day")[col].mean())
    out={}
    def safe(name,f):
        try: out[name]=f()
        except Exception as e: out[name]="err: "+str(e)[:80]
    E=D.dropna(subset=["lvr"]).copy()
    E["dn"]=np.where(E["r0"]<0,"down","up")
    E["vq"]=E.groupby("dn")["lvr"].transform(lambda s: pd.qcut(s,5,labels=False,duplicates="drop"))
    E["vq3"]=E.groupby("dn")["lvr"].transform(lambda s: pd.qcut(s,3,labels=False,duplicates="drop"))
    safe("A ex by dir x vol quintile",lambda: E.groupby(["dn","vq"]).apply(dayt).round(3))
    Dn=E[E.r0<0].copy()
    Dn["zq"]=pd.qcut(Dn["z0"],4,labels=False,duplicates="drop")
    safe("B down: z-move quartile(0=biggest fall) x vol tercile ex%",lambda: (Dn.groupby(["zq","vq3"])["ex"].mean().unstack()*100).round(3))
    safe("C down: z-move quartile x vol tercile dayt",lambda: Dn.groupby(["zq","vq3"]).apply(lambda g: dayt(g)["t"]).unstack().round(2))
    Dn["cq"]=pd.qcut(Dn["clpos"],3,labels=False,duplicates="drop")
    safe("D down: closepos tercile(0=near low) x vol tercile ex%",lambda: (Dn.groupby(["cq","vq3"])["ex"].mean().unstack()*100).round(3))
    E["tr"]=pd.cut(E["r60"],[-np.inf,-0.1,0.1,np.inf],labels=["fall","chop","rise"])
    safe("E trend x dir x vol tercile",lambda: E.groupby(["tr","dn","vq3"]).apply(dayt).round(3))
    safe("F agitation x dir x vol tercile",lambda: E.groupby(["agit","dn","vq3"]).apply(dayt).round(3))
    safe("G z0 bucket ex (all days)",lambda: E.groupby(pd.cut(E["z0"],[-np.inf,-2,-1,0,1,2,np.inf])).apply(dayt).round(3))
    safe("H z0 bucket ex 3-day",lambda: E.groupby(pd.cut(E["z0"],[-np.inf,-2,-1,0,1,2,np.inf])).apply(lambda g: tstat(g[g.index%3==0]["r3"])).round(3))
    safe("I r5 quintile ex",lambda: E.groupby(pd.qcut(E["r5"],5,labels=False)).apply(dayt).round(3))
    safe("J weekday ex",lambda: E.groupby("wd").apply(dayt).round(3))
    safe("K up: closepos tercile x vol tercile ex%",lambda: (E[E.dn=="up"].groupby([pd.qcut(E[E.dn=="up"]["clpos"],3,labels=False,duplicates="drop"),"vq3"])["ex"].mean().unstack()*100).round(3))
    safe("L down: top vol tercile ex by year",lambda: Dn[Dn.vq3==2].groupby("year").apply(dayt).round(3))
    safe("M book gain% by window",lambda: (D.groupby("w")["gain"].mean()*100).round(4))
    # book days: largest gains/losses
    B=[]
    for c,ws in data["days"].items():
        for w,dd in ws.items():
            x=dd.copy(); x["coin"]=c; x["w"]=w; B.append(x)
    B=pd.concat(B,ignore_index=True)
    br=B.groupby(["w","day"]).agg(book=("book_return","mean"),coin=("coin_return","mean")).dropna()
    safe("N book vs coin by book decile",lambda: br.groupby(pd.qcut(br["book"],10,labels=False,duplicates="drop"))[["book","coin"]].mean().mul(100).round(3))
    return out
