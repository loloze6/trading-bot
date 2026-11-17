import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            r1=c/c.shift(1)-1
            vol=r1.rolling(20,min_periods=15).std()
            d=pd.DataFrame({"coin":coin,"w":w,"wd":ts.dt.weekday,"year":ts.dt.year,
                "r1":r1,"z":r1/vol,"vol":vol,
                "f1":c.shift(-1)/c-1,"f3":c.shift(-3)/c-1,"f7":c.shift(-7)/c-1,
                "z7":(c/c.shift(7)-1)/(vol*np.sqrt(7)),"z14":(c/c.shift(14)-1)/(vol*np.sqrt(14)),
                "pos":b["postRebalance_current_allocation"]})
            d["k"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    m1=D.groupby("coin")["f1"].mean()
    m7=D[D.k%7==0].groupby("coin")["f7"].mean()
    D["x1"]=D.f1-D.coin.map(m1); D["x7"]=D.f7-D.coin.map(m7)
    out={}
    # 7-day momentum on non-overlapping grid k%7==0 (any weekday)
    G=D[D.k%7==0].dropna(subset=["z7","x7"])
    s=stats.linregress(G.z7,G.x7); out["grid7 z7->x7 slope,t,n"]=f"{s.slope:.5f},{s.slope/s.stderr:.2f},{len(G)}"
    G=D[D.k%7==0].dropna(subset=["z14","x7"])
    s=stats.linregress(G.z14,G.x7); out["grid7 z14->x7 slope,t,n"]=f"{s.slope:.5f},{s.slope/s.stderr:.2f},{len(G)}"
    # within-window demeaned
    G=D[D.k%7==0].dropna(subset=["z7","f7"]).copy()
    G["fd"]=G.f7-G.groupby(["coin","w"]).f7.transform("mean")
    s=stats.linregress(G.z7,G.fd); out["grid7 z7->f7 window-demeaned slope,t"]=f"{s.slope:.5f},{s.slope/s.stderr:.2f}"
    res=[]
    for k,g in D[D.k%7==0].dropna(subset=["z7","x7"]).groupby("year"):
        s=stats.linregress(g.z7,g.x7); res.append([k,len(g),s.slope,s.slope/s.stderr])
    out["z7->x7 by year"]=pd.DataFrame(res,columns=["year","n","slope","t"])
    res=[]
    for k,g in D[D.k%7==0].dropna(subset=["z7","x7"]).groupby("coin"):
        s=stats.linregress(g.z7,g.x7); res.append([k,len(g),s.slope,s.slope/s.stderr])
    out["z7->x7 by coin"]=pd.DataFrame(res,columns=["coin","n","slope","t"])
    # 1-day reversal all days, by vol tercile
    A=D.dropna(subset=["z","x1","vol"]).copy()
    A["vq"]=A.groupby("coin")["vol"].transform(lambda v: pd.qcut(v,3,labels=False))
    res=[]
    for q,g in A.groupby("vq"):
        s=stats.linregress(g.z,g.x1); res.append([q,len(g),s.slope,s.slope/s.stderr])
    out["1d reversal by vol tercile (all days)"]=pd.DataFrame(res,columns=["vq","n","slope","t"])
    res=[]
    for k,g in A.groupby("year"):
        s=stats.linregress(g.z,g.x1); res.append([k,len(g),s.slope,s.slope/s.stderr])
    out["1d reversal by year"]=pd.DataFrame(res,columns=["year","n","slope","t"])
    # Saturday return (bar wd==5 day's own return = r1 on wd5) mean by year
    Sat=D[D.wd==5].dropna(subset=["r1"]).copy()
    Sat["xr"]=Sat.r1-Sat.coin.map(m1)
    g=Sat.groupby("year").xr
    out["Saturday excess return by year"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    # book: daily returns, coin returns; largest gains/losses context
    dd=[]
    for coin,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    B=pd.concat(dd).dropna(subset=["book_return","coin_return"])
    B["wd"]=pd.to_datetime(B["day"],utc=True).dt.weekday
    g=B.groupby("wd")
    out["book & coin daily by weekday"]=pd.DataFrame({"book_mean":g.book_return.mean(),"book_t":g.book_return.mean()/(g.book_return.std()/np.sqrt(g.size())),"coin_mean":g.coin_return.mean(),"n":g.size()})
    act=B[B.book_return.abs()>0]
    q=act.book_return.quantile([0.05,0.95])
    out["book active days: share top5% / bottom5% by weekday"]=pd.DataFrame({"top":act[act.book_return>=q[0.95]].wd.value_counts(),"bot":act[act.book_return<=q[0.05]].wd.value_counts()})
    return out
