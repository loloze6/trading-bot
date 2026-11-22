import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H_list = [6, 18, 42, 84]
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            hi = df["high"].astype(float); lo = df["low"].astype(float)
            r6 = c / c.shift(6) - 1
            usual = r6.abs().rolling(180, min_periods=45).mean()
            depth = (-r6 / usual)
            rng = (hi.rolling(6).max() / lo.rolling(6).min() - 1)
            rng_ratio = rng / rng.rolling(180, min_periods=45).mean()
            n = len(df)
            for H in H_list:
                for i in range(0, n - H, H):
                    recs.append(dict(coin=coin, win=w, year=pd.Timestamp(df["timestamp"].iloc[i]).year,
                                     H=H, depth=depth.iloc[i], rng_ratio=rng_ratio.iloc[i],
                                     fwd=c.iloc[i + H] / c.iloc[i] - 1))
    R = pd.DataFrame(recs)
    R["drift"] = R.groupby(["coin", "H"])["fwd"].transform("mean")
    R["sd"] = R.groupby(["coin", "H"])["fwd"].transform("std")
    R["ex"] = R["fwd"] - R["drift"]
    R["str"] = R["ex"] / R["sd"]
    R = R.dropna(subset=["depth", "rng_ratio"])
    # panic score: range ratio on falls only, 0 on rises
    R["panic"] = np.where(R.depth > 0, R.rng_ratio, 0.0)
    R["fall_depth"] = R.depth.clip(lower=0)
    out = {}
    def st(d, x):
        if len(d) < 10 or d[x].std() == 0: return (np.nan, np.nan, len(d))
        s = stats.linregress(d[x], d["ex"]); return (s.slope, s.slope / s.stderr, len(d))
    rows = []
    for H in H_list:
        d = R[R.H == H]
        for x in ["fall_depth", "panic", "rng_ratio"]:
            s, t, n = st(d, x); rows.append(dict(H=H, x=x, slope=s, t=t, n=n))
        f = d[d.depth > 0]
        s, t, n = st(f, "rng_ratio"); rows.append(dict(H=H, x="rng_ratio|falls", slope=s, t=t, n=n))
        s, t, n = st(d[d.depth <= 0], "rng_ratio"); rows.append(dict(H=H, x="rng_ratio|rises", slope=s, t=t, n=n))
    out["slopes"] = pd.DataFrame(rows)
    rows = []
    for H in [18, 84]:
        d = R[R.H == H]
        for k in ["coin", "year"]:
            for g, dd in d.groupby(k):
                s1, t1, n1 = st(dd, "fall_depth"); s2, t2, n2 = st(dd, "panic")
                rows.append(dict(H=H, by=k, g=g, n=n1, t_depth=t1, t_panic=t2))
    out["by_group"] = pd.DataFrame(rows)
    rows = []
    for H in [18, 84]:
        d = R[(R.H == H) & (R.depth > 0)].copy()
        d["q"] = pd.qcut(d.rng_ratio.rank(method="first"), 4, labels=["r1","r2","r3","r4"])
        for q, dd in d.groupby("q"):
            v = dd.ex
            rows.append(dict(H=H, q=q, n=len(v), rr=dd.rng_ratio.mean(), ex=v.mean(), strength=dd.str.mean(),
                             t=v.mean() / (v.std() / np.sqrt(len(v)))))
    out["falls_by_range_q"] = pd.DataFrame(rows)
    d = R[(R.H == 18) & (R.depth > 1)]
    out["deep_fall_3d_size"] = pd.Series(dict(n=len(d), ex=d.ex.mean(), strength=d.str.mean(),
                                              total=d.fwd.mean(), usual=R[R.H == 18].sd.mean()))
    return out
