import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    def tt(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    hrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r = c.pct_change()
            vol = r.rolling(168).std()
            r24lag = c.shift(1)/c.shift(25)-1  # prior 24h ending before this bar
            r24end = c/c.shift(24)-1           # known at close of this bar
            f24 = c.shift(-24)/c-1
            f6 = c.shift(-6)/c-1
            f2 = c.shift(-2)/c-1
            pos = np.arange(len(c))
            hrs.append(pd.DataFrame({"coin":coin,"w":w,"h":ts.dt.hour.values,"r":r.values,"vol":vol.values,
                                     "z":(r/vol).values,"r24lag":r24lag.values,"r24end":r24end.values,
                                     "f24":f24.values,"f6":f6.values,"f2":f2.values,"pos":pos,
                                     "al":b["postRebalance_current_allocation"].values}))
    A = pd.concat(hrs, ignore_index=True)
    late = A[A.h.isin([21,22])].dropna(subset=["r","r24lag"]).copy()
    late["pq"] = late.groupby("coin")["r24lag"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["h21_22_ret_by_lagged_prior24q"] = late.groupby("pq")["r"].apply(tt).unstack()
    # at close of hour 20 (known), next 2h return graded by 24h return ending at that close
    h20 = A[A.h==20].dropna(subset=["f2","r24end"]).copy()
    h20["pq"] = h20.groupby("coin")["r24end"].transform(lambda x: pd.qcut(x.rank(method="first"),5,labels=False))
    out["from_h20_close_next2h_by_24h_ret_q"] = h20.groupby("pq")["f2"].apply(tt).unstack()
    out["from_h20_next2h_all"] = tt(h20["f2"])
    # other hours next 2h from same grid for comparison: h8 close
    h8 = A[A.h==8].dropna(subset=["f2"])
    out["from_h8_next2h_all"] = tt(h8["f2"])
    # big down hour reversal, 24h grid, graded by z, per coin
    g24 = A[A.pos%24==0].dropna(subset=["z","f24"]).copy()
    neg = g24[g24.z<0].copy()
    res={}
    for coin,d in neg.groupby("coin"):
        s=stats.linregress(d.z,d.f24); res[coin]=(len(d),s.slope,s.slope/s.stderr)
    s=stats.linregress(neg.z,neg.f24); res["ALL"]=(len(neg),s.slope,s.slope/s.stderr)
    out["neg_hour_z_slope_on_f24"]=pd.DataFrame(res,index=["n","slope","t"]).T
    neg["zq"]=pd.qcut(neg["z"].rank(method="first"),5,labels=False)
    out["neg_hour_f24_by_zq"]=neg.groupby("zq")["f24"].apply(tt).unstack()
    pos_ = g24[g24.z>0].copy(); pos_["zq"]=pd.qcut(pos_["z"].rank(method="first"),5,labels=False)
    out["pos_hour_f24_by_zq"]=pos_.groupby("zq")["f24"].apply(tt).unstack()
    # book: timing part
    out["book_gain_by_hour_21_22_vs_other"] = pd.Series({
        "late": (A.loc[A.h.isin([21,22]),"al"].shift(0)).mean()})
    return out
