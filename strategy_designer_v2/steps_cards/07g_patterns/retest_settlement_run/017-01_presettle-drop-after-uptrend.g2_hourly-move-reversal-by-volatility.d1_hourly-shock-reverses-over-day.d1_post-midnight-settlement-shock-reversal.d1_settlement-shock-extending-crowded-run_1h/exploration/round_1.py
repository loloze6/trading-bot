import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    drift={}
    for coin,ws in data["bars"].items():
        g=[]
        for w,b in ws.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-24,24)
            g.extend(c[idx+24]/c[idx]-1)
        drift[coin]=np.mean(g)
        for w,b in ws.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"])
            b["hour"]=ts.dt.hour.values
            b["dow"]=ts.dt.dayofweek.values
            b["year"]=ts.dt.year.values
            cl=b["close"]
            r1=cl/cl.shift(1)-1
            b["z"]=r1/r1.rolling(24).std()
            b["p23"]=cl.shift(1)/cl.shift(24)-1
            b["r24"]=cl/cl.shift(24)-1
            b["volrel"]=r1.rolling(24).std()/r1.rolling(24*30).std()
            b["fwd"]=(cl.shift(-24)/cl-1)-drift[coin]
            lv=np.log(b["volume"].replace(0,np.nan))
            b["vrel"]=lv-lv.rolling(24*7).mean()
            b["coin"]=coin; b["win"]=w
            b["active"]=b["regime"].eq("mean_reversion")
            rows.append(b[["coin","win","hour","dow","year","z","p23","r24","volrel","fwd","vrel","active"]])
    d=pd.concat(rows).dropna(subset=["z","p23","fwd"])
    d["al"]=np.sign(d["z"])==np.sign(d["p23"])
    d["x"]=-d["z"]
    def reg(s):
        s=s.dropna(subset=["x","fwd"])
        if len(s)<50: return pd.Series({"n":float(len(s))})
        sl=stats.linregress(s["x"],s["fwd"])
        m=(np.sign(s["x"])*s["fwd"])
        return pd.Series({"n":float(len(s)),"slope_bp":sl.slope*1e4,"t":sl.slope/sl.stderr,
                          "signmean_pct":m.mean()*100,"t_sign":m.mean()/(m.std()/np.sqrt(len(s)))})
    out={}
    out["active_hours"]=d[d.active].groupby("hour").size()
    out["by_hour_aligned"]=d[d.al].groupby("hour").apply(reg)
    out["by_hour_opposed"]=d[~d.al].groupby("hour").apply(reg)
    h0=d[d.hour==0]
    out["h0_aligned_by_year"]=h0[h0.al].groupby("year").apply(reg)
    out["h0_aligned_by_coin"]=h0[h0.al].groupby("coin").apply(reg)
    h0a=h0[h0.al].copy()
    h0a["vq"]=pd.qcut(h0a["volrel"],3,labels=["lowvol","mid","highvol"])
    out["h0_aligned_by_volrel"]=h0a.groupby("vq").apply(reg)
    h0a["zq"]=pd.qcut(h0a["z"].abs(),5,labels=False)
    out["h0_aligned_by_absz_q"]=h0a.groupby("zq").apply(reg)
    t=h0.copy(); t["x"]=-t["r24"]/t["r24"].std()
    out["h0_fade_r24_all"]=reg(t).to_frame().T
    out["h0_aligned_by_dow"]=h0a.groupby("dow").apply(reg)
    out["vrel_by_hour"]=d.groupby("hour")["vrel"].mean()
    return out
