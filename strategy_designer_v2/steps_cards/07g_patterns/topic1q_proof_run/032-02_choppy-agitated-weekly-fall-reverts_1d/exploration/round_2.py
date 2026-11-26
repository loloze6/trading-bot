import numpy as np, pandas as pd
from scipy import stats

def tt(x):
    x = pd.Series(x).dropna()
    return x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float); o = b["open"].values.astype(float)
            h = b["high"].values.astype(float); l = b["low"].values.astype(float)
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            prof = (b["regime"].astype(str) == "unknown").values
            for i in range(1, n-2):
                r1 = c[i]/c[i-1]-1
                nx1 = c[i+1]/c[i]-1
                nx2 = c[i+2]/c[i]-1
                rng = (h[i]-l[i])/c[i-1]
                clv = (c[i]-l[i])/(h[i]-l[i]) if h[i] > l[i] else 0.5
                tr = c[i]/c[i-60]-1 if i >= 60 else np.nan
                v30 = np.std(np.diff(np.log(c[max(0,i-30):i+1]))) if i >= 10 else np.nan
                rows.append((coin, w, ts.iloc[i].normalize(), ts.iloc[i].weekday(), prof[i], r1, nx1, nx2, rng, clv, tr, v30))
    d = pd.DataFrame(rows, columns=["coin","w","day","wd","prof","r1","nx1","nx2","rng","clv","tr","v30"])
    sd = d.groupby("coin")["r1"].transform("std")
    d["nz"] = d["nx1"]/sd; d["nz2"] = d["nx2"]/sd
    d["rz"] = d["rng"]/d.groupby("coin")["rng"].transform("median")
    d["trend"] = np.where(d.tr.isna(), "na", np.where(d.tr > .1, "rising", np.where(d.tr < -.1, "falling", "choppy")))
    up = d[d.r1 > 0].copy(); dn = d[d.r1 <= 0].copy()
    up["q"] = up.groupby("coin")["rz"].transform(lambda x: pd.qcut(x, 5, labels=False))
    dn["q"] = dn.groupby("coin")["rz"].transform(lambda x: pd.qcut(x, 5, labels=False))
    agg = dict(n=("nz","size"), nz=("nz","mean"), t=("nz", tt), nz2=("nz2","mean"), t2=("nz2", tt))
    out["UP days: range quintile -> next day z"] = up.groupby("q").agg(**agg)
    out["DOWN days: range quintile -> next day z"] = dn.groupby("q").agg(**agg)
    wu = up[up.q == 4].copy()
    out["wide UP: by trend"] = wu.groupby("trend").agg(**agg)
    out["wide UP: by window"] = wu.groupby("w").agg(n=("nz","size"), nz=("nz","mean"))
    out["wide UP: by coin"] = wu.groupby("coin").agg(**agg)
    out["wide UP: by year"] = wu.assign(y=wu.day.dt.year).groupby("y").agg(**agg)
    wu["cq"] = pd.qcut(wu.clv, 3, labels=False)
    out["wide UP: close location tercile"] = wu.groupby("cq").agg(**agg)
    # day-clustered graded slope among up days: range z -> next day z
    upc = up.groupby("day").agg(rz=("rz","mean"), nz=("nz","sum"), k=("nz","size"))
    r = stats.linregress(up["rz"], up["nz"])
    out["up days slope rz->nz (bar-level)"] = f"slope {r.slope:.3f} t {r.slope/r.stderr:.2f} n {len(up)}"
    out["wide UP day-clustered mean nz"] = f"{wu.groupby('day').nz.sum().mean():.3f} t {tt(wu.groupby('day').nz.sum()):.2f} days {wu.day.nunique()}"
    # weekday effect by trend
    out["weekday -> next day z by trend"] = d[d.trend != "na"].groupby(["trend","wd"]).agg(n=("nz","size"), nz=("nz","mean"), t=("nz", tt)).unstack(0)
    out["weekday -> next day z by year"] = d.assign(y=d.day.dt.year, thfr=d.wd.isin([3,4])).groupby(["y","thfr"]).nz.mean().unstack()
    # vol level: agitation proxy (v30 vs coin median) for wide up days
    wu["agit"] = wu.v30 > d.groupby("coin").v30.transform("median").loc[wu.index]
    out["wide UP: by agitation proxy"] = wu.groupby("agit").agg(**agg)
    return out
