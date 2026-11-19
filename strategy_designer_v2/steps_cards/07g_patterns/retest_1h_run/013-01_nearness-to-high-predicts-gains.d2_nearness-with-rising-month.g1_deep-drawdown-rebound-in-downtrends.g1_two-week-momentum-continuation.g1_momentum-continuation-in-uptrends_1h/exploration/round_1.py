def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    hrows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            c=b["close"].astype(float).reset_index(drop=True)
            n=len(c)
            r336=c/c.shift(336)-1
            r1440=c/c.shift(1440)-1
            r24=c/c.shift(24)-1
            near=c/b["high"].astype(float).reset_index(drop=True).rolling(1440,min_periods=336).max()
            lr=np.log(c).diff()
            vol=lr.rolling(336,min_periods=168).std()
            vratio=lr.rolling(24).std()/vol
            v=b["volume"].astype(float).reset_index(drop=True)
            vrel=v.rolling(24).sum()/v.rolling(336,min_periods=168).sum()*14
            fc=b["forecast"].astype(float).reset_index(drop=True)
            reg=b["regime"].reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            for p in range(0,n-168,168):
                rows.append(dict(coin=coin,w=w,f=fc[p],reg=reg[p],r336=r336[p],r1440=r1440[p],r24=r24[p],
                    near=near[p],vol=vol[p],vratio=vratio[p],vrel=vrel[p],fwd=c[p+168]/c[p]-1))
            # hourly next-1h returns grid (each bar once)
            nxt=c.shift(-1)/c-1
            hrows.append(pd.DataFrame(dict(coin=coin,h=ts.dt.hour,wd=ts.dt.weekday,nxt=nxt,r24=r24)))
    d=pd.DataFrame(rows)
    d["dfwd"]=d["fwd"]-d.groupby("coin")["fwd"].transform("mean")
    out={}
    def tq(col,sub,q=5,name=None):
        s=sub.dropna(subset=[col,"dfwd"]).copy()
        s["q"]=s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"),q,labels=False))
        g=s.groupby("q")["dfwd"].agg(["mean","count","std"])
        g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
        out[name or col]=g.round(4)
    tq("r336",d[d.reg=="trending"],5,"trend: r336 quintile")
    tq("r336",d[d.reg!="trending"],5,"downtrend: r336 quintile")
    tq("r1440",d,5,"all: r1440 quintile")
    tq("near",d,5,"all: nearness to 60d high quintile")
    tq("r24",d,5,"all: 1d return quintile")
    tq("vol",d,5,"all: 14d vol quintile")
    tq("vratio",d,5,"all: 1d/14d vol ratio quintile")
    tq("vrel",d,5,"all: 1d vol relative volume quintile")
    out["regime fwd"]=d.groupby("reg")["dfwd"].agg(["mean","count"]).round(4)
    h=pd.concat(hrows).dropna()
    h["dn"]=h["nxt"]-h.groupby("coin")["nxt"].transform("mean")
    g=h.groupby("h")["dn"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["hour next-1h"]=g.round(5)
    g=h.groupby("wd")["dn"].agg(["mean","count","std"]); g["t"]=g["mean"]/(g["std"]/np.sqrt(g["count"]))
    out["weekday next-1h"]=g.round(5)
    # book daily
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    D=pd.concat(dd)
    D["day"]=pd.to_datetime(D["day"])
    B=D.groupby(["w","day"])[["book_return","coin_return"]].mean().dropna()
    B["year"]=B.index.get_level_values("day").year
    out["book by year"]=B.groupby("year").agg(book=("book_return","mean"),hold=("coin_return","mean"),n=("book_return","count")).round(5)
    out["book by window"]=B.groupby(level="w").agg(book=("book_return","sum"),hold=("coin_return","sum")).round(3)
    return out
