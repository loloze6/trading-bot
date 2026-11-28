import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            r=c.pct_change()
            sd=r.rolling(30).std()
            sw=(c/c.shift(7)-1)/(sd*np.sqrt(7))
            r7=c/c.shift(7)-1
            reg=b["regime"].astype(str)
            n=len(b)
            for h in (1,3,5,7):
                fwd=c.shift(-h)/c-1
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,h=h,sw=sw[i],r7=r7[i],fwd=fwd[i],reg=reg[i],
                                     inprof=reg[i] in ("mean_reversion","unknown"),fc=b["forecast"][i]))
    d=pd.DataFrame(rows).dropna(subset=["sw","fwd"])
    drift=d.groupby(["coin","h"])["fwd"].mean().rename("drift")
    d=d.join(drift,on=["coin","h"]); d["y"]=d["fwd"]-d["drift"]
    out={}
    def reg_t(s):
        if len(s)<10: return pd.Series(dict(n=len(s),slope=np.nan,t=np.nan,meany=np.nan))
        lr=stats.linregress(s["sw"],s["y"])
        return pd.Series(dict(n=len(s),slope=lr.slope,t=lr.slope/lr.stderr,meany=s["y"].mean(),
                              t_meany=s["y"].mean()/(s["y"].std()/np.sqrt(len(s)))))
    out["slope_by_h_prof"]=d.groupby(["inprof","h"]).apply(reg_t)
    fa=d[d.inprof]
    fa=fa.assign(side=np.where(fa.r7>0,"up","down"))
    out["fa_by_h_side"]=fa.groupby(["h","side"]).apply(reg_t)
    fa3=fa[fa.h==3].copy()
    fa3["q"]=pd.qcut(fa3["sw"],5,labels=False)
    out["fa_h3_quintile"]=fa3.groupby("q").agg(n=("y","size"),sw=("sw","mean"),y=("y","mean"),fwd=("fwd","mean"))
    fa5=fa[fa.h==5].copy(); fa5["q"]=pd.qcut(fa5["sw"],5,labels=False)
    out["fa_h5_quintile"]=fa5.groupby("q").agg(n=("y","size"),sw=("sw","mean"),y=("y","mean"))
    out["fa_h3_coin"]=fa3.groupby(["coin"]).apply(reg_t)
    out["fa_h3_side_coin"]=fa3.groupby(["coin","side"]).apply(reg_t)
    fa3["yr"]=fa3["w"]
    out["fa_h3_window"]=fa3.groupby("w").apply(reg_t)
    out["drift"]=drift.unstack()
    return out
