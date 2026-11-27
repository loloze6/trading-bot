import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            rng = hi - lo
            cl = np.where(rng > 0, (c - lo) / np.where(rng > 0, rng, 1), np.nan)
            agit = (df["regime"] != "chop").values
            n = len(df)
            for i in range(0, n - 2):
                rows.append(dict(coin=coin, win=w, ts=df["timestamp"].iloc[i], cl=cl[i], agit=agit[i],
                                 r1=c[i + 1] / c[i] - 1, r2=c[i + 2] / c[i + 1] - 1))
    R = pd.DataFrame(rows).dropna(subset=["cl"])
    R["x1"] = R["r1"] - R.groupby("coin")["r1"].transform("mean")
    R["x2"] = R["r2"] - R.groupby("coin")["r2"].transform("mean")
    R["day"] = pd.to_datetime(R["ts"]).dt.floor("D")
    R["year"] = pd.to_datetime(R["ts"]).dt.year
    R["lowside"] = 0.5 - R["cl"]   # positive on lower-half closes
    def tcl(s, col):
        m = s[col].mean(); dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return m, (m / se if se > 0 else np.nan), len(s), s["day"].nunique()
    out = {}
    A = R[R.agit]
    res = []
    for key, grp in [("year", "year"), ("coin", "coin")]:
        for k, s in A.groupby(grp):
            if len(s) < 30: continue
            rho = stats.spearmanr(s.cl, s.x1)[0]
            lo_ = s[s.cl < 0.5]
            m, t, nn, nd = tcl(lo_, "x1")
            w = lo_["lowside"]
            wm = (lo_.x1 * w).sum() / w.sum()
            res.append(dict(by=key, k=str(k), rho_cl_x1=rho, lower_mean_x1=m, lower_t=t, lower_wmean=wm, n_lower=nn))
    out["agit_next_day_by"] = pd.DataFrame(res)
    lo_ = A[A.cl < 0.5]
    m, t, nn, nd = tcl(lo_, "x1")
    w = lo_["lowside"]
    out["agit_lower_pooled"] = pd.Series(dict(mean_x1=m, t=t, n=nn, days=nd,
                                              wmean_x1=(lo_.x1 * w).sum() / w.sum(),
                                              mean_raw_r1=lo_.r1.mean(),
                                              mean_x2=lo_.x2.mean(),
                                              rho_lowside_x1=stats.spearmanr(lo_.lowside, lo_.x1)[0]))
    C = R[~R.agit]; lc = C[C.cl < 0.5]
    m2, t2, n2, d2 = tcl(lc, "x1")
    out["calm_lower_pooled"] = pd.Series(dict(mean_x1=m2, t=t2, n=n2, days=d2))
    return out
