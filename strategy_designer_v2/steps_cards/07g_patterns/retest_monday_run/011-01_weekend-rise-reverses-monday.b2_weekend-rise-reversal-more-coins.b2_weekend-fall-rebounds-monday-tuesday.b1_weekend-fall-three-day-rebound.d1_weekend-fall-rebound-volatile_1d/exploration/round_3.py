import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]
    for coin, wins in data["bars"].items():
        g3=[]
        for w, b in wins.items():
            c=b["close"].values
            n=min(len(c[0::3]),len(c[3::3]))
            g3+=list(c[3::3][:n]/c[0::3][:n]-1)
        m3=np.mean(g3)
        for w, b in wins.items():
            b=b.copy()
            ts=pd.to_datetime(b["timestamp"],utc=True)
            b["date"]=ts.dt.floor("D").values
            b["wd"]=ts.dt.weekday.values; b["year"]=ts.dt.year.values
            c=b["close"]
            b["r1"]=c/c.shift(1)-1
            b["r2"]=c/c.shift(2)-1
            b["vol20"]=b["r1"].rolling(20).std()
            b["z"]=b["r1"]/b["vol20"]
            b["z2"]=b["r2"]/(b["vol20"]*np.sqrt(2))
            b["vr2"]=(b["volume"]+b["volume"].shift(1))/(2*b["volume"].rolling(20).mean().shift(2))
            b["x3"]=c.shift(-3)/c-1-m3
            b["x3s"]=b["x3"]/(b["vol20"]*np.sqrt(3))
            b["coin"]=coin; b["win"]=w
            rows.append(b[["coin","win","date","wd","year","z","z2","vr2","x3","x3s"]])
    D=pd.concat(rows).dropna(subset=["z","x3s"])
    out={}
    # per-coin slopes: Friday continuation, Sunday reversal
    res=[]
    for coin,g in D.groupby("coin"):
        F=g[g.wd==4]; S=g[g.wd==6].dropna(subset=["vr2"])
        sf=stats.linregress(F.z,F.x3s); ss=stats.linregress(S.z,S.x3s)
        Sl=S[np.log(S.vr2)<np.log(S.vr2).median()]
        sl=stats.linregress(Sl.z,Sl.x3s)
        res.append([coin,len(F),sf.slope,sf.slope/sf.stderr,ss.slope,ss.slope/ss.stderr,sl.slope,sl.slope/sl.stderr])
    P=pd.DataFrame(res,columns=["coin","n","fri_slope","fri_t","sun_slope","sun_t","sunlowv_slope","sunlowv_t"])
    out["per_coin"]=P
    out["per_coin_summary"]=pd.DataFrame({"share_fri_pos":[(P.fri_slope>0).mean()],"share_sun_neg":[(P.sun_slope<0).mean()],"share_sunlowv_neg":[(P.sunlowv_slope<0).mean()]})
    # Sunday low-volume reversal by year (clustered by date)
    S=D[D.wd==6].dropna(subset=["vr2"]).copy()
    S["lv"]=np.log(S.vr2); S["low"]=S.lv<S.groupby("coin").lv.transform("median")
    res=[]
    for y,g in S[S.low].groupby("year"):
        pm=(g.z*g.x3s).groupby(g.date).mean()
        res.append([y,len(pm),pm.mean(),stats.ttest_1samp(pm,0).statistic])
    out["sun_lowvol_by_year"]=pd.DataFrame(res,columns=["year","dates","z_x3s","t"])
    # graded: Sunday z quintile x3, low-volume half
    Sl=S[S.low]
    out["sun_lowvol_zq"]=Sl.groupby(pd.qcut(Sl.z,5,labels=False))["x3"].agg(["mean","count"])
    return out
