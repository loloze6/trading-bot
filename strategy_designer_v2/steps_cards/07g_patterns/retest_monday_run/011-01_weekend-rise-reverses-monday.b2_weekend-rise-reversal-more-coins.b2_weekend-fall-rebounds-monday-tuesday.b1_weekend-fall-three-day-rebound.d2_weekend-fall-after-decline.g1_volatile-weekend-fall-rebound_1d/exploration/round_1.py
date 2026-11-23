import pandas as pd, numpy as np
from scipy import stats

def _panel(data):
    rows=[]
    for coin,wins in data["bars"].items():
        g3=[]
        for w,b in wins.items():
            c=b["close"].astype(float).values
            g3+=list(c[3::3]/c[:-3:3][:len(c[3::3])]-1)
        drift=np.mean(g3); sd=np.std(g3,ddof=1)
        for w,b in wins.items():
            d=b[["timestamp","close","volume","forecast","postRebalance_current_allocation"]].copy()
            d["ts"]=pd.to_datetime(d["timestamp"],utc=True)
            d["wd"]=d["ts"].dt.weekday; d["yr"]=d["ts"].dt.year
            d["r1"]=d["close"].pct_change()
            d["r2"]=d["close"].pct_change(2)
            d["r5"]=d["close"].pct_change(5)
            d["vol20"]=d["r1"].rolling(20).std()
            d["relv"]=d["volume"]/d["volume"].rolling(20).mean().shift(1)
            for h in (1,3,5):
                d[f"f{h}"]=d["close"].shift(-h)/d["close"]-1
            d["ex3"]=d["f3"]-drift; d["sd3"]=sd
            d["coin"]=coin; d["win"]=w
            rows.append(d)
    return pd.concat(rows,ignore_index=True)

def _st(x):
    x=pd.Series(x).dropna()
    n=len(x)
    if n<3: return (n,np.nan,np.nan)
    return (n,x.mean(),x.mean()/(x.std()/np.sqrt(n)))

def explore(data):
    p=_panel(data).dropna(subset=["r1","vol20","ex3"])
    p["z"]=p["r1"]/p["vol20"]
    out={}
    # by weekday: falls and rises, mean excess 3d (in direction of reversal), slope on |z|
    t=[]
    for wd in range(7):
        q=p[p.wd==wd]
        f=q[q.r1<0]; r=q[q.r1>0]
        nf,mf,tf=_st(f.ex3); nr,mr,tr=_st(-r.ex3)
        sf=stats.linregress(-f.z,f.ex3/f.sd3); sr=stats.linregress(r.z,-r.ex3/r.sd3)
        big=q[q.z<-1.5]; bigr=q[q.z>1.5]
        t.append(dict(wd=wd,n_fall=nf,fall_ex3=mf,t_fall=tf,slope_fall_t=sf.slope/sf.stderr,
                      n_rise=nr,rise_rev_ex3=mr,t_rise=tr,slope_rise_t=sr.slope/sr.stderr,
                      bigfall_n=len(big),bigfall_ex3=big.ex3.mean(),bigrise_n=len(bigr),bigrise_rev=(-bigr.ex3).mean()))
    out["by_weekday"]=pd.DataFrame(t)
    # all days: excess 3d after z buckets
    p["zb"]=pd.cut(p.z,[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["zbucket_sunday_vs_other"]=p.assign(sun=p.wd==6).groupby(["zb","sun"],observed=True)["ex3"].agg(["count","mean"]).unstack()
    # sunday falls: volume interaction
    s=p[(p.wd==6)&(p.r1<0)].dropna(subset=["relv"]).copy()
    s["vq"]=pd.qcut(s.relv,3,labels=["lowvol","mid","highvol"])
    s["zq"]=pd.qcut(-s.z,3,labels=["small","med","large"])
    out["sun_fall_vol_x_size"]=s.groupby(["vq","zq"],observed=True)["ex3"].agg(["count","mean"]).unstack()
    # vol level (vol20 tercile within coin) for any-day falls z<-1
    p["vt"]=p.groupby("coin")["vol20"].transform(lambda v: pd.qcut(v,3,labels=False))
    a=p[p.z<-1]
    out["fall_by_voltercile_sun"]=a.groupby(["vt",a.wd==6])["ex3"].agg(["count","mean"]).unstack()
    # 5-day past return reversal
    p["z5"]=p["r5"]/(p["vol20"]*np.sqrt(5))
    p["z5b"]=pd.qcut(p.z5,5,labels=False)
    out["past5d_quintile_ex3_all"]=p.groupby("z5b")["ex3"].agg(["count","mean"])
    # trades by year
    tr=[]
    for coin,wins in data["trades"].items():
        for w,d in wins.items():
            if len(d): 
                d=d.copy(); d["yr"]=pd.to_datetime(d["entry_time"],utc=True).dt.year; tr.append(d)
    tr=pd.concat(tr)
    out["trades_by_year"]=tr.groupby("yr")["net_profit_loss_percent"].agg(["count","mean","median"])
    # book daily by year
    dd=[]
    for coin,wins in data["days"].items():
        for w,d in wins.items():
            d=d.copy(); d["coin"]=coin; d["win"]=w; dd.append(d)
    dd=pd.concat(dd)
    dd["dayts"]=pd.to_datetime(dd["day"],utc=True)
    bk=dd.groupby(["win","dayts"])[["book_return","coin_return"]].mean().reset_index()
    bk["yr"]=bk.dayts.dt.year; bk["wd"]=bk.dayts.dt.weekday
    out["book_by_year"]=bk.groupby("yr")[["book_return","coin_return"]].agg(["mean","std"])
    out["book_by_wd"]=bk.groupby("wd")[["book_return","coin_return"]].mean()
    return out
