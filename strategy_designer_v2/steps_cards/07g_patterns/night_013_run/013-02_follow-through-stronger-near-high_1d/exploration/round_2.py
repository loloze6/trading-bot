import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].values
            lhv = b.get("debug_info.components.hpm.last_history_value")
            n = len(b)
            for h in (5, 10, 30):
                for p in range(0, n - h, h):
                    past30 = c[p]/c[p-30]-1 if p>=30 else np.nan
                    past5 = c[p]/c[p-5]-1 if p>=5 else np.nan
                    W = np.nan
                    if lhv is not None and past30 == past30 and abs(past30) > 0.02:
                        W = lhv.iloc[p]/past30
                    volr = v[max(0,p-4):p+1].mean()/v[p-29:p+1].mean() if p>=29 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, p=p, fwd=c[p+h]/c[p]-1, past30=past30,
                                     past5=past5, W=W, volr=volr,
                                     yr=pd.Timestamp(b["timestamp"].iloc[p]).year))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby(["coin","h"])["fwd"].transform("mean")
    def sl(d, x):
        d = d[[x,"ex"]].dropna()
        if len(d) < 15: return pd.Series(dict(slope=np.nan,t=np.nan,n=len(d),rho=np.nan))
        r = stats.linregress(d[x], d["ex"]); rho = stats.spearmanr(d[x], d["ex"]).correlation
        return pd.Series(dict(slope=r.slope,t=r.slope/r.stderr,n=len(d),rho=rho))
    # volume ratio: by coin, quartiles, by year; partial on past5
    res=[]
    for coin,d in g[g.h==5].groupby("coin"): res.append(sl(d,"volr").rename(coin))
    out["volr_h5_by_coin"]=pd.DataFrame(res)
    res=[]
    for yr,d in g[g.h==5].groupby("yr"): res.append(sl(d,"volr").rename(yr))
    out["volr_h5_by_year"]=pd.DataFrame(res)
    for h in (5,10):
        d=g[g.h==h].dropna(subset=["volr"]).copy()
        d["q"]=pd.qcut(d["volr"],5,labels=False)
        out[f"volr_q_h{h}"]=d.groupby("q").agg(n=("ex","size"),volr=("volr","mean"),mean_ex=("ex","mean"),
            t=("ex",lambda s:s.mean()/(s.std()/np.sqrt(len(s)))),past5=("past5","mean"))
        dd=d.dropna(subset=["past5"])
        X=np.column_stack([np.ones(len(dd)),dd["volr"],dd["past5"]])
        beta,_,_,_=np.linalg.lstsq(X,dd["ex"].values,rcond=None)
        resid=dd["ex"].values-X@beta; s2=resid@resid/(len(dd)-3)
        se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        out[f"volr_past5_joint_h{h}"]=pd.DataFrame(dict(beta=beta,t=beta/se),index=["c","volr","past5"])
    # W robustness at h=30, h=10 by quartile and rank
    for h in (10,30):
        d=g[g.h==h].dropna(subset=["W"])
        out[f"W_rank_h{h}"]=sl(d,"W")
    # daily: reversal after big down days, by coin and year; Saturday by coin/year
    dd=[]
    for coin, ws in days.items():
        for w, d in ws.items():
            d=d.copy().reset_index(drop=True)
            d["nxt"]=d["coin_return"].shift(-1); d["coin"]=coin
            d["wd"]=pd.to_datetime(d["day"]).dt.dayofweek; d["yr"]=pd.to_datetime(d["day"]).dt.year
            d["sd20"]=d["coin_return"].rolling(20,min_periods=10).std().shift(1)
            dd.append(d)
    D=pd.concat(dd,ignore_index=True)
    D["z"]=D["coin_return"]/D["sd20"]
    tt=lambda s:s.mean()/(s.std()/np.sqrt(s.count()))
    D["zq"]=pd.cut(D["z"],[-99,-2.5,-1.5,-0.5,0.5,1.5,2.5,99])
    out["next_by_localz"]=D.groupby("zq").agg(n=("nxt","count"),nxt=("nxt","mean"),t=("nxt",tt))
    big=D[D.z<=-1.5]
    out["bigdown_by_coin"]=big.groupby("coin").agg(n=("nxt","count"),nxt=("nxt","mean"),t=("nxt",tt))
    out["bigdown_by_year"]=big.groupby("yr").agg(n=("nxt","count"),nxt=("nxt","mean"),t=("nxt",tt))
    dz=D.dropna(subset=["z","nxt"])
    r=stats.linregress(dz["z"].clip(-5,5),dz["nxt"]); out["nxt_on_z"]=pd.Series(dict(slope=r.slope,t=r.slope/r.stderr,n=len(dz)))
    neg=dz[dz.z<0]; r=stats.linregress(neg["z"].clip(-5,0),neg["nxt"]); out["nxt_on_z_neg"]=pd.Series(dict(slope=r.slope,t=r.slope/r.stderr,n=len(neg)))
    sat=D[D.wd==5]
    out["sat_by_coin"]=sat.groupby("coin").agg(n=("coin_return","count"),r=("coin_return","mean"),t=("coin_return",tt))
    out["sat_by_year"]=sat.groupby("yr").agg(n=("coin_return","count"),r=("coin_return","mean"),t=("coin_return",tt))
    return out
