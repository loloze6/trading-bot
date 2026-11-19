import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    rows = []
    for c in bars:
        g2 = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl)-2, 2)
            g2.append(cl[idx+2]/cl[idx]-1)
        m2 = np.concatenate(g2).mean()
        for w, b in bars[c].items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            b["hour"] = ts.dt.hour.values; b["year"] = ts.dt.year.values
            cl = b["close"]
            r72 = cl/cl.shift(72)-1
            b["z"] = (r72/r72.abs().rolling(72, min_periods=20).mean().shift(1)).clip(-2,2)
            b["fwd2"] = cl.shift(-2)/cl-1-m2
            b["fwd1"] = cl.shift(-1)/cl-1
            b["r1"] = cl/cl.shift(1)-1
            b["vol24"] = b["r1"].rolling(24).std()
            b["vol168"] = b["r1"].rolling(168).std()
            b["coin"]=c; b["win"]=w
            rows.append(b[["coin","win","year","hour","z","fwd2","fwd1","r1","vol24","vol168"]])
    d = pd.concat(rows, ignore_index=True)
    # reversal after large 1h move, graded by vol level, by coin and by year
    e = d.dropna(subset=["r1","fwd1","vol24","vol168"]).copy()
    e["zr"]=(e["r1"]/e["vol24"]).clip(-5,5)
    e["vratio"]=e["vol24"]/e["vol168"]
    e["vq"]=e.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x,5,labels=False))
    def reg(g, x, y):
        s=stats.linregress(g[x],g[y]); return pd.Series({"n":len(g),"slope_bp":s.slope*1e4,"t":s.slope/s.stderr})
    hv = e[e["vq"]>=3]
    out["rev_highvol_by_coin"]=hv.groupby("coin").apply(reg,"zr","fwd1")
    out["rev_highvol_by_year"]=hv.groupby("year").apply(reg,"zr","fwd1")
    out["rev_by_vol_quintile"]=e.groupby("vq").apply(reg,"zr","fwd1")
    # raw return slope (not normalised) by quintile: does reversal in % grow with vol
    out["rev_raw_r1_by_quintile"]=e.groupby("vq").apply(lambda g: reg(g.assign(x=g["r1"].clip(g["r1"].quantile(.001),g["r1"].quantile(.999))),"x","fwd1"))
    # 2h reversal: non-overlapping grid
    e2=[]
    for (c,w),g in d.groupby(["coin","win"]):
        g=g.reset_index(drop=True).iloc[::2]
        e2.append(g)
    e2=pd.concat(e2).dropna(subset=["r1","fwd2","vol24"])
    e2["zr"]=(e2["r1"]/e2["vol24"]).clip(-5,5)
    e2["vq"]=e2.groupby("coin")["vol24"].transform(lambda x: pd.qcut(x,3,labels=False))
    out["rev_fwd2_grid_by_vol_tercile"]=e2.groupby("vq").apply(reg,"zr","fwd2")
    # hour 21/22 drift by coin and year
    h = d[d["hour"].isin([21,22])].dropna(subset=["r1"])
    def tm(g): return pd.Series({"n":len(g),"mean_bp":g["r1"].mean()*1e4,"t":g["r1"].mean()/(g["r1"].std()/np.sqrt(len(g)))})
    out["h21_22_by_coin"]=h.groupby("coin").apply(tm)
    out["h21_22_by_year"]=h.groupby("year").apply(tm)
    # trend slope hours 12 (reversal) and 22 (continuation) by year
    for hr in [12,15,22]:
        g=d[d["hour"]==hr].dropna(subset=["z","fwd2"])
        out[f"slope_h{hr}_by_year"]=g.groupby("year").apply(reg,"z","fwd2")
        out[f"slope_h{hr}_by_coin"]=g.groupby("coin").apply(reg,"z","fwd2")
    return out
