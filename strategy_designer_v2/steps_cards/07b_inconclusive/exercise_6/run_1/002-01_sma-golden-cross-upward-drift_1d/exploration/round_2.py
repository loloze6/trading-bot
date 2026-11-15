import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    h=10
    for coin,ws in data["bars"].items():
        for w,df in ws.items():
            df=df.reset_index(drop=True)
            c=df["close"].values; f=df["forecast"].values
            vol=df["sizing_realised_vol"].values
            yr=pd.to_datetime(df["timestamp"]).dt.year.values
            on=(f>0).astype(int)
            run=np.zeros(len(df)); k=0
            for i in range(len(df)):
                k=k+1 if on[i] else 0; run[i]=k
            fresh=np.full(len(df),np.nan)
            # bars since turning on, only if turn-on seen inside window
            seen_off=False; start=None
            for i in range(len(df)):
                if not on[i]: seen_off=True; start=None
                else:
                    if start is None and seen_off: start=i
                    fresh[i]=(i-start) if start is not None else np.nan
            n=len(df)
            for i in range(0,n-h,h):
                past=c[i]/c[i-20]-1 if i>=20 else np.nan
                rows.append(dict(coin=coin,wi=int(w[1:]),yr=yr[i],f=f[i],vol=vol[i],fresh=fresh[i],past=past,r=c[i+h]/c[i]-1))
    d=pd.DataFrame(rows)
    d["ex"]=d["r"]-d.groupby("coin")["r"].transform("mean")
    d["pos"]=(d.r>0).astype(float)-d.groupby("coin")["r"].transform(lambda x:(x>0).mean())
    def sl(x):
        x=x.dropna(subset=["f","ex"])
        if len(x)<15 or x.f.std()==0: return pd.Series(dict(n=len(x)))
        s=stats.linregress(x.f,x.ex)
        a=x[x.f>0].ex; b=x[x.f<=0].ex
        return pd.Series(dict(n=len(x),n_on=len(a),slope=s.slope,t=s.slope/s.stderr,on=a.mean(),off=b.mean(),
                              t_onoff=stats.ttest_ind(a,b,equal_var=False).statistic if len(a)>2 and len(b)>2 else np.nan))
    out={}
    out["by_year"]=d.groupby("yr").apply(sl)
    d["vt"]=d.groupby("coin")["vol"].transform(lambda x:pd.qcut(x.rank(method="first"),3,labels=False))
    out["by_vol_tercile"]=d.groupby("vt").apply(sl)
    d["pt"]=pd.qcut(d.past,3,labels=False)
    out["by_past20_tercile"]=d.groupby("pt").apply(sl)
    on=d[d.f>0].copy()
    on["fb"]=pd.cut(on.fresh,[-1,10,30,60,500])
    out["on_by_fresh"]=on.groupby("fb")["ex"].agg(["count","mean","std"])
    out["on_fresh_unknown"]=float(on.fresh.isna().sum())
    out["on_ex_t"]=stats.ttest_1samp(on.ex,0).statistic
    out["on_pos_share"]=on.pos.mean()
    a=d.dropna(subset=["past"])
    s=stats.linregress(a.past,a.ex); out["past20_slope_t"]=s.slope/s.stderr
    out["past20_n"]=len(a)
    return out
