import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            lhv = b.get("debug_info.components.hpm.last_history_value")
            n = len(b)
            for h in (5, 10, 30):
                for p in range(0, n - h, h):
                    if p < 30: past30 = np.nan
                    else: past30 = c[p]/c[p-30]-1
                    past5 = c[p]/c[p-5]-1 if p>=5 else np.nan
                    W = np.nan
                    if lhv is not None and past30 == past30 and abs(past30) > 1e-9:
                        W = lhv.iloc[p]/past30
                    rv = np.std(np.diff(np.log(c[max(0,p-20):p+1]))) if p>=10 else np.nan
                    vol_ratio = b["volume"].iloc[max(0,p-4):p+1].mean()/b["volume"].iloc[max(0,p-29):p+1].mean() if p>=29 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, p=p, fwd=c[p+h]/c[p]-1,
                                     fc=b["forecast"].iloc[p], past30=past30, past5=past5, W=W,
                                     rv=rv, volr=vol_ratio,
                                     wd=pd.Timestamp(b["timestamp"].iloc[p]).dayofweek))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby(["coin","h"])["fwd"].transform("mean")
    def slope(df, x):
        d = df[[x,"ex"]].dropna()
        if len(d) < 20: return (np.nan, np.nan, len(d))
        r = stats.linregress(d[x], d["ex"]); return (r.slope, r.slope/r.stderr, len(d))
    res = []
    for h in (5,10,30):
        d = g[g.h==h]
        for x in ("fc","past30","past5","W","rv","volr"):
            s,t,nn = slope(d,x); res.append(dict(h=h,x=x,slope=s,t=t,n=nn))
    out["slopes_pooled"] = pd.DataFrame(res)
    # by coin, h=30 and h=10 past30
    res=[]
    for coin, d in g.groupby("coin"):
        for h in (10,30):
            for x in ("past30","W","rv"):
                s,t,nn = slope(d[d.h==h],x); res.append(dict(coin=coin,h=h,x=x,slope=s,t=t,n=nn))
    out["slopes_by_coin"] = pd.DataFrame(res)
    # depth quintiles at h=30 and 10
    for h in (10,30):
        d = g[(g.h==h)].dropna(subset=["W"]).copy()
        d["Wq"] = pd.qcut(d["W"],4,labels=False,duplicates="drop")
        out[f"Wq_h{h}"] = d.groupby("Wq").agg(n=("ex","size"),mean_ex=("ex","mean"),
            t=("ex",lambda s: s.mean()/(s.std()/np.sqrt(len(s)))),past30=("past30","mean"))
        d["rvq"] = pd.qcut(d["rv"],4,labels=False,duplicates="drop")
        out[f"rvq_h{h}"] = d.groupby("rvq").agg(n=("ex","size"),mean_ex=("ex","mean"),
            t=("ex",lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    # daily: next-day return after large moves, by weekday, book
    dd=[]
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy().reset_index(drop=True)
            d["nxt"] = d["coin_return"].shift(-1)
            d["nxt5"] = d["close"].shift(-5)/d["close"]-1
            d["coin"]=coin; d["w"]=w
            d["wd"]=pd.to_datetime(d["day"]).dt.dayofweek
            d["yr"]=pd.to_datetime(d["day"]).dt.year
            dd.append(d)
    D = pd.concat(dd, ignore_index=True)
    D["z"] = D["coin_return"]/D.groupby("coin")["coin_return"].transform("std")
    D["zq"] = pd.cut(D["z"],[-99,-2,-1,0,1,2,99])
    out["next_day_by_move"] = D.groupby("zq").agg(n=("nxt","count"),nxt=("nxt","mean"),
        t=("nxt",lambda s: s.mean()/(s.std()/np.sqrt(s.count()))))
    out["by_weekday"] = D.groupby("wd").agg(coin=("coin_return","mean"),
        tc=("coin_return",lambda s: s.mean()/(s.std()/np.sqrt(s.count()))),
        book=("book_return","mean"),
        tb=("book_return",lambda s: s.mean()/(s.std()/np.sqrt(s.count()))))
    out["book_by_year"] = D.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","count"))
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"),
        sh=("book_return",lambda s: s.mean()/s.std()*np.sqrt(365)))
    return out
