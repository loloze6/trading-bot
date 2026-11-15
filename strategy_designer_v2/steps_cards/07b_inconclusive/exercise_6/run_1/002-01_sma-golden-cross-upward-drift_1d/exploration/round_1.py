import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    H=[5,10,20,40]
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; f=df["forecast"].values
            raw=df.get("debug_info.components.sma_cross.last_history_value")
            raw=raw.values if raw is not None else np.full(len(df),np.nan)
            n=len(df)
            for h in H:
                for i in range(0,n-h,h):
                    rows.append(dict(coin=coin,w=w,wi=int(w[1:]),h=h,f=f[i],raw=raw[i],r=c[i+h]/c[i]-1))
    d=pd.DataFrame(rows)
    d["ex"]=d["r"]-d.groupby(["coin","h"])["r"].transform("mean")
    out={}
    # slope and on/off by horizon
    res=[]
    for h,g in d.groupby("h"):
        s=stats.linregress(g["f"],g["ex"])
        on=g[g.f>0]["ex"]; off=g[g.f<=0]["ex"]
        t=stats.ttest_ind(on,off,equal_var=False)
        gr=g.dropna(subset=["raw"]); sr=stats.linregress(gr["raw"],gr["ex"]) if len(gr)>10 else None
        res.append(dict(h=h,n=len(g),slope=s.slope,t=s.slope/s.stderr,on_mean=on.mean(),off_mean=off.mean(),n_on=len(on),t_onoff=t.statistic,
                        raw_slope_t=(sr.slope/sr.stderr if sr else np.nan),n_raw=len(gr)))
    out["by_h"]=pd.DataFrame(res)
    g=d[d.h==10]
    def sl(x):
        if len(x)<8 or x.f.std()==0: return pd.Series(dict(n=len(x),n_on=(x.f>0).sum()))
        s=stats.linregress(x["f"],x["ex"])
        return pd.Series(dict(n=len(x),n_on=(x.f>0).sum(),slope=s.slope,t=s.slope/s.stderr,on=x[x.f>0].ex.mean(),off=x[x.f<=0].ex.mean()))
    out["by_coin_h10"]=g.groupby("coin").apply(sl)
    out["by_window_h10"]=g.groupby("wi").apply(sl)
    g2=g.copy(); g2["b"]=pd.cut(g2.f,[-0.1,0,5,10,15,20.1])
    out["buckets_h10"]=g2.groupby("b")["ex"].agg(["count","mean","std"])
    g4=d[d.h==40].copy(); g4["b"]=pd.cut(g4.f,[-0.1,0,5,10,15,20.1])
    out["buckets_h40"]=g4.groupby("b")["ex"].agg(["count","mean","std"])
    out["raw_desc"]=d[d.h==10]["raw"].describe()
    return out
