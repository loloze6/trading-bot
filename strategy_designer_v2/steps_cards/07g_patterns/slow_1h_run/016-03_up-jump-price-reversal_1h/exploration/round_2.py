import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 72
    hrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(168).std()
            r24 = c/c.shift(24)-1
            f1 = c.shift(-1)/c-1
            f6 = c.shift(-6)/c-1
            f24 = c.shift(-24)/c-1
            hrs.append(pd.DataFrame({"coin":coin,"w":w,"yr":ts.dt.year,"h":ts.dt.hour,"r":r,"vol":vol,
                                     "z":r/vol,"r24":r24,"f1":f1,"f6":f6,"f24":f24,
                                     "al":b["postRebalance_current_allocation"]}))
    A = pd.concat(hrs)
    late = A[A.h.isin([21,22])].dropna(subset=["r"])
    def tt(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["h21_22_by_coin"] = late.groupby("coin")["r"].apply(tt).unstack()
    out["h21_22_by_year"] = late.groupby("yr")["r"].apply(tt).unstack()
    other = A[~A.h.isin([21,22])]["r"].dropna()
    out["h21_22_vs_other_welch"] = stats.ttest_ind(late["r"], other, equal_var=False).statistic
    # graded by vol: normalized return in hour 21-22 by vol quintile
    late = late.dropna(subset=["vol"]).copy()
    late["vq"] = late.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["h21_22_by_volq"] = late.groupby("vq")["r"].apply(tt).unstack()
    # graded by prior 24h return
    late["pq"] = late.groupby("coin")["r24"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["h21_22_by_prior24q"] = late.groupby("pq")["r"].apply(tt).unstack()
    # after large hourly moves: non-overlapping 6h grid
    g6 = A[A.groupby(["coin","w"]).cumcount()%6==0].dropna(subset=["z","f6"]).copy()
    g6["zq"] = pd.qcut(g6["z"].rank(method="first"),7,labels=False)
    out["f6_by_hour_z_septile"] = g6.groupby("zq")["f6"].apply(tt).unstack()
    g24 = A[A.groupby(["coin","w"]).cumcount()%24==0].dropna(subset=["z","f24"]).copy()
    g24["zq"] = pd.qcut(g24["z"].rank(method="first"),7,labels=False)
    out["f24_by_hour_z_septile"] = g24.groupby("zq")["f24"].apply(tt).unstack()
    # 72h grid: grind share continuous regression within up moves, per coin
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c=b["close"].values; r1=np.r_[np.nan,c[1:]/c[:-1]-1]; n=len(c)
            for i in range(H,n-H,H):
                past=c[i]/c[i-H]-1
                if past<=0: continue
                hr=r1[i-H+1:i+1]
                gs=min(np.sort(hr)[-3:].sum()/past,1)
                pos=(hr>0).mean()
                rows.append((coin,past,c[i+H]/c[i]-1,gs,pos))
    U=pd.DataFrame(rows,columns=["coin","past","fwd","gs","pos"])
    res={}
    for coin,d in U.groupby("coin"):
        s=stats.linregress(d.gs,d.fwd); res[coin]=(len(d),s.slope,s.slope/s.stderr)
    s=stats.linregress(U.gs,U.fwd); res["ALL"]=(len(U),s.slope,s.slope/s.stderr)
    out["up_fwd_on_gshare"]=pd.DataFrame(res,index=["n","slope","t"]).T
    U["posq"]=pd.qcut(U["pos"].rank(method="first"),5,labels=False)
    out["up_fwd_by_share_of_up_hours_q"]=U.groupby("posq")["fwd"].apply(tt).unstack()
    # book daily: worst/best days, coin return around them
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            x=d[["book_return","coin_return"]].copy(); x["next_cr"]=x["coin_return"].shift(-1); dd.append(x)
    D=pd.concat(dd).dropna()
    D["bq"]=pd.qcut(D["book_return"].rank(method="first"),10,labels=False)
    out["book_decile_coin_same_next"]=D.groupby("bq")[["book_return","coin_return","next_cr"]].mean()
    return out
