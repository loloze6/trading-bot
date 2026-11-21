import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin,wins in data["bars"].items():
        for w,b in wins.items():
            c=b["close"].values.astype(float); v=b["volume"].values.astype(float)
            ts=pd.to_datetime(b["timestamp"])
            hr=np.r_[np.nan,c[1:]/c[:-1]-1]
            n=len(c)
            for t in range(72,n-72,24):
                h=hr[t-23:t+1]; vv=v[t-23:t+1]
                if np.isnan(h).any() or vv.sum()<=0: continue
                r24=c[t]/c[t-24]-1
                rows.append(dict(coin=coin,w=w,r24=r24,r72=c[t]/c[t-72]-1,
                  f6=c[t+6]/c[t]-1,f24=c[t+24]/c[t]-1,f72=c[t+72]/c[t]-1,f2472=c[t+72]/c[t+24]-1,
                  jump=np.abs(h).max()/(np.abs(h).sum()+1e-12),
                  vconc=vv.max()/vv.sum(),
                  eff=abs(r24)/(np.abs(h).sum()+1e-12),
                  vol=np.std(h),hour=ts.iloc[t].hour,wd=ts.iloc[t].weekday(),
                  fc=b["forecast"].iloc[t]))
    d=pd.DataFrame(rows)
    for k in ["f6","f24","f72","f2472"]:
        d[k+"x"]=d[k]-d.groupby("coin")[k].transform("mean")
    d["z24"]=d.groupby("coin")["r24"].transform(lambda s:(s-s.mean())/s.std())
    out={}
    def reg(sub,x,y):
        s=sub[[x,y]].dropna()
        r=stats.linregress(s[x],s[y]); return pd.Series(dict(n=len(s),slope=r.slope,t=r.slope/r.stderr))
    tab={}
    for y in ["f6x","f24x","f72x","f2472x"]:
        tab["all_"+y]=reg(d,"z24",y)
        tab["down72_"+y]=reg(d[d.r72<0],"z24",y)
        tab["up72_"+y]=reg(d[d.r72>=0],"z24",y)
    out["reg_z24"]=pd.DataFrame(tab).T
    d["q"]=pd.qcut(d.z24,5,labels=False)
    out["quint_r24"]=d.groupby("q")[["f24x","f72x","f2472x"]].agg(["mean","count"])
    # jump vs grind among falls
    dn=d[d.r24<0].copy()
    dn["jq"]=pd.qcut(dn.jump,3,labels=False); dn["vq"]=pd.qcut(dn.vconc,3,labels=False)
    out["falls_by_jump"]=dn.groupby("jq")[["f24x","f72x","f2472x","z24"]].mean()
    out["falls_by_vconc"]=dn.groupby("vq")[["f24x","f72x","f2472x","z24"]].mean()
    up=d[d.r24>0].copy(); up["jq"]=pd.qcut(up.jump,3,labels=False)
    out["rises_by_jump"]=up.groupby("jq")[["f24x","f72x","f2472x","z24"]].mean()
    d["sgnf24"]=d.f24x*np.sign(d.r24)
    d["volq"]=d.groupby("coin")["vol"].transform(lambda s:pd.qcut(s,3,labels=False))
    out["by_volq_signed_follow"]=d.groupby("volq")[["sgnf24"]].agg(["mean","count",lambda s:s.mean()/s.std()*np.sqrt(len(s))])
    out["by_coin_down72_slope24"]=pd.DataFrame({c:reg(g[g.r72<0],"z24","f24x") for c,g in d.groupby("coin")}).T
    # book
    dy=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            x=x.copy(); x["coin"]=coin; x["w"]=w; dy.append(x)
    dy=pd.concat(dy); dy["year"]=pd.to_datetime(dy["day"]).dt.year
    out["book_by_year"]=dy.groupby("year")[["book_return","coin_return"]].mean()
    out["book_by_coin"]=dy.groupby("coin")[["book_return","coin_return"]].mean()
    return out
