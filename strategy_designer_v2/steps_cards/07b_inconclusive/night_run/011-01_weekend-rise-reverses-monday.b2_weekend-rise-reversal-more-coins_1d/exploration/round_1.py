import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin mean non-overlapping 2-bar return
        g = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 2, 2)
            g.extend(c[idx + 2] / c[idx] - 1)
        m2 = np.nanmean(g)
        g1 = []
        for w, b in wins.items():
            c = b["close"].values
            g1.extend(c[1:] / c[:-1] - 1)
        m1 = np.nanmean(g1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"])
            wd = ts.dt.weekday.values
            yr = ts.dt.year.values
            r0 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            s = pd.Series(r0)
            z = (s - s.rolling(60, min_periods=20).mean()) / s.rolling(60, min_periods=20).std()
            vol = b["volume"].astype(float)
            vrel = vol / vol.rolling(60, min_periods=20).mean()
            n = len(c)
            for t in range(n - 2):
                rows.append((coin, w, yr[t], wd[t], r0[t], z.iloc[t], vrel.iloc[t],
                             b["forecast"].iloc[t], c[t+1]/c[t]-1-m1, c[t+2]/c[t]-1-m2))
    d = pd.DataFrame(rows, columns=["coin","w","yr","wd","r0","z","vrel","fc","e1","e2"])
    sun = d[(d.wd == 6) & (d.fc < 0)].copy()
    sun["x"] = (-sun.fc/10) * -sun.e2
    sun["third"] = pd.qcut(sun.fc.abs().rank(method="first"), 3, labels=["low","mid","top"])
    out = {}
    def tt(v):
        v = v.dropna(); return pd.Series({"n": len(v), "mean": v.mean(), "t": v.mean()/(v.std()/np.sqrt(len(v)))})
    out["sun_x_and_unweighted"] = pd.DataFrame({"x": tt(sun.x), "-e2": tt(-sun.e2), "-e1(Mon)": tt(-sun.e1)})
    out["sun_by_third"] = sun.groupby("third").agg(n=("e2","size"), e2=("e2","mean"), e1=("e1","mean"), fcabs=("fc", lambda v: v.abs().mean()), r0=("r0","mean"))
    # same-size rises on other weekdays (z>0), by weekday, e2
    up = d[(d.z > 0)].copy()
    up["q"] = pd.qcut(up.z.rank(method="first"), 3, labels=["low","mid","top"])
    out["rise_e2_by_weekday"] = up.groupby("wd").agg(n=("e2","size"), e2=("e2","mean"), e1=("e1","mean"), t2=("e2", lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
    out["rise_e2_wd_x_third"] = up.pivot_table(index="wd", columns="q", values="e2", aggfunc="mean")
    dn = d[(d.z < 0)]
    out["fall_e2_by_weekday"] = dn.groupby("wd").agg(n=("e2","size"), e2=("e2","mean"), t2=("e2", lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
    out["sun_by_year"] = sun.groupby("yr").agg(n=("e2","size"), e2=("e2","mean"), x=("x","mean"), t=("x", lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
    out["sun_by_coin"] = sun.groupby("coin").agg(n=("e2","size"), e2=("e2","mean"), t=("x", lambda v: v.mean()/(v.std()/np.sqrt(len(v)))))
    sun["vq"] = pd.qcut(sun.vrel.rank(method="first"), 3, labels=["lowvol","mid","highvol"])
    out["sun_by_relvolume"] = sun.groupby("vq").agg(n=("e2","size"), e2=("e2","mean"), e1=("e1","mean"))
    out["sun_vol_x_third"] = sun.pivot_table(index="vq", columns="third", values="e2", aggfunc="mean")
    return out
