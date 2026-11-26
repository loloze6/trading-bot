import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    drift = {}
    for coin, ws in bars.items():
        for H in (1,2,3,4,5):
            rr=[]
            for w, b in ws.items():
                c = b["close"].values
                idx = np.arange(0, len(c)-H, H)
                rr += list(c[idx+H]/c[idx]-1)
            drift[(coin,H)] = np.mean(rr)
    rows=[]
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30).std()
            rng = (b["high"]-b["low"])/c/sd
            reg = b["regime"].astype(str).values
            fc = b["forecast"].fillna(0).values
            year = pd.to_datetime(b["timestamp"]).dt.year.values
            n=len(b)
            for H in (1,2,3,4,5):
                for i in range(1,n-H):
                    if i % H: continue
                    if reg[i]=="chop" or np.isnan(rng[i]) or not r[i]<0: continue
                    rows.append(dict(coin=coin,w=w,H=H,rng=rng[i],fc=fc[i],
                        ex=c[i+H]/c[i]-1-drift[(coin,H)],day=(w,i),year=year[i]))
    df=pd.DataFrame(rows)
    def clus(g):
        dev=g.ex-g.ex.mean()
        s=dev.groupby(g.day).sum(); G=len(s)
        se=np.sqrt((s**2).sum()*G/(G-1))/len(g)
        return pd.Series(dict(n=len(g),days=G,mean=g.ex.mean(),t=g.ex.mean()/se))
    out={}
    df["q"]=df.groupby("H")["rng"].transform(lambda x: pd.qcut(x,5,labels=False))
    out["H_rangeq_clustered"]=df.groupby(["H","q"]).apply(clus).unstack("q")["t"]
    out["H_rangeq_mean"]=df.groupby(["H","q"]).ex.mean().unstack("q")
    d3=df[df.H==3]
    out["H3_top40_by_year"]=d3[d3.q>=3].groupby("year").apply(clus)
    out["H3_top40_by_coin"]=d3[d3.q>=3].groupby("coin").apply(clus)
    out["H3_bottom60_all"]=clus(d3[d3.q<3]).to_frame("v")
    out["H3_top40_all"]=clus(d3[d3.q>=3]).to_frame("v")
    out["H3_corr_rng_fc"]=float(d3[["rng","fc"]].corr().iloc[0,1])
    d3=d3.copy(); d3["fq"]=pd.qcut(d3.fc.rank(method="first"),5,labels=False)
    out["H3_fcq"]=d3.groupby("fq").apply(clus)
    sl=np.polyfit(d3.rng,d3.ex,1)[0]
    out["H3_slope_rng"]=float(sl)
    out["rng_quintile_edges"]=d3.groupby("q").rng.agg(["min","max"])
    return out
