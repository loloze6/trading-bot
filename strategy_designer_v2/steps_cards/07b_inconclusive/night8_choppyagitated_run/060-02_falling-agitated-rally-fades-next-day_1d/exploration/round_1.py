def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    bars=data["bars"]
    mu={}
    for c,ws in bars.items():
        rr=[]
        for w,b in ws.items():
            r=b["close"].pct_change()
            rr.append(r.dropna())
        mu[c]=pd.concat(rr).mean()
    for c,ws in bars.items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sd=r.rolling(30).std()
            sc=r/sd
            for h in (1,2,3,5):
                b[f"f{h}"]=cl.shift(-h)/cl-1
            prof=(b["regime"]=="unknown")
            case=prof&(b["forecast"]<0)
            d=b[case].copy()
            d["coin"]=c; d["win"]=w; d["sc"]=sc[case]; d["absf"]=-d["forecast"]
            d["r0"]=r[case]
            d["year"]=pd.to_datetime(d["timestamp"]).dt.year
            for h in (1,2,3,5):
                d[f"x{h}"]=-(d[f"f{h}"]-h*mu[c])
            rows.append(d[["coin","win","year","timestamp","sc","absf","r0","x1","x2","x3","x5"]])
            # all profile bars, up and down, for comparison
            p=b[prof].copy(); p["coin"]=c; p["sc"]=sc[prof]; p["timestamp"]=b["timestamp"][prof]
            p["x1"]=-(p["f1"]-mu[c]); p["up"]=p["sc"]>0
            rows.append(p[["coin","timestamp","sc","x1","up"]].assign(kind="prof"))
    allr=pd.concat(rows,ignore_index=True)
    prof=allr[allr.get("kind")=="prof"]
    cs=allr[allr.get("kind")!="prof"].copy()
    def ct(s,ts):
        g=pd.DataFrame({"v":s,"t":ts}).dropna().groupby("t")["v"].sum()
        n=len(g); m=s.dropna().mean()
        se=g.std(ddof=1)*np.sqrt(n)/s.dropna().shape[0]
        return m, m/se if se>0 else np.nan, s.dropna().shape[0], n
    out={}
    res=[]
    for h in (1,2,3,5):
        m,t,n,nd=ct(cs[f"x{h}"],cs["timestamp"]); res.append([h,m,t,n,nd])
    out["mean by horizon (days)"]=pd.DataFrame(res,columns=["h","mean","t","n","days"])
    cs["q"]=pd.qcut(cs["sc"],5,labels=False)
    tab=[]
    for q,g in cs.groupby("q"):
        r=[q,g["sc"].mean()]
        for h in (1,2,3):
            m,t,n,nd=ct(g[f"x{h}"],g["timestamp"]); r+= [m,t]
        r.append(len(g)); tab.append(r)
    out["by scaled-rise quintile"]=pd.DataFrame(tab,columns=["q","sc","m1","t1","m2","t2","m3","t3","n"])
    cs["qf"]=pd.qcut(cs["absf"].rank(method="first"),5,labels=False)
    tab=[]
    for q,g in cs.groupby("qf"):
        m,t,n,nd=ct(g["x1"],g["timestamp"]); m3,t3,_,_=ct(g["x3"],g["timestamp"])
        tab.append([q,g["absf"].mean(),g["sc"].mean(),m,t,m3,t3,n])
    out["by |forecast| quintile"]=pd.DataFrame(tab,columns=["q","absf","sc","m1","t1","m3","t3","n"])
    out["corr absf vs sc"]=float(cs[["absf","sc"]].corr().iloc[0,1])
    tab=[]
    for c,g in cs.groupby("coin"):
        m,t,n,nd=ct(g["x1"],g["timestamp"]); m3,t3,_,_=ct(g["x3"],g["timestamp"]); tab.append([c,m,t,m3,t3,n])
    out["by coin"]=pd.DataFrame(tab,columns=["coin","m1","t1","m3","t3","n"])
    tab=[]
    for c,g in cs.groupby("year"):
        m,t,n,nd=ct(g["x1"],g["timestamp"]); m3,t3,_,_=ct(g["x3"],g["timestamp"]); tab.append([c,m,t,m3,t3,n])
    out["by year"]=pd.DataFrame(tab,columns=["year","m1","t1","m3","t3","n"])
    # profile up vs down days, next-day (sign flipped = short gain)
    tab=[]
    prof=prof.dropna(subset=["sc","x1"])
    prof["qq"]=pd.qcut(prof["sc"],6,labels=False)
    for q,g in prof.groupby("qq"):
        m,t,n,nd=ct(g["x1"],g["timestamp"]); tab.append([q,g["sc"].mean(),m,t,n])
    out["profile all days by scaled return sextile (short gain next day)"]=pd.DataFrame(tab,columns=["q","sc","m1","t1","n"])
    return out
