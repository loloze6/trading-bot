import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [3, 5, 10]
    recs = []
    drift = {}
    for coin, wins in bars.items():
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            rs = np.array(rs)
            drift[(coin, h)] = (np.nanmean(rs), np.nanstd(rs, ddof=1))
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            o, hi, lo, c = df["open"], df["high"], df["low"], df["close"]
            rng = hi - lo
            mr = rng.rolling(20, min_periods=20).mean()
            mult = rng / mr
            loc = (c - lo) / rng.replace(0, np.nan)
            fall = c.shift(1) / c.shift(6) - 1
            r60 = c / c.shift(60) - 1
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(n):
                if not (mult.iloc[i] >= 1.5 and loc.iloc[i] >= 0.75):
                    continue
                for h in H:
                    if i + h >= n:
                        continue
                    ret = c.iloc[i + h] / c.iloc[i] - 1
                    d, s = drift[(coin, h)]
                    recs.append(dict(coin=coin, win=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     h=h, cell=i // h, fell=fall.iloc[i] < 0, fall5=fall.iloc[i],
                                     mult=mult.iloc[i], r60=r60.iloc[i],
                                     dayret=c.iloc[i] / c.iloc[i - 1] - 1 if i > 0 else np.nan,
                                     up=(ret - d), strength=(ret - d) / s))
    R = pd.DataFrame(recs).drop_duplicates(subset=["coin", "win", "h", "cell", "fell"])

    def st(g):
        m = g["up"].mean()
        dev = g["up"] - m
        ds = dev.groupby(g["day"]).sum()
        nd = len(ds)
        t = m * len(g) / np.sqrt((ds ** 2).sum()) if nd > 1 else np.nan
        return pd.Series(dict(n=len(g), days=nd, mean_up=m, t=t, hit=(g["up"] > 0).mean(),
                              strength=g["strength"].mean()))

    out = {}
    N = R[~R.fell].copy()
    N5 = N[N.h == 5].copy()
    out["nofall_h5_by_year"] = N5.groupby("year").apply(st)
    out["nofall_h5_by_coin"] = N5.groupby("coin").apply(st)
    N5["mq"] = pd.qcut(N5["mult"], 4, labels=False, duplicates="drop")
    out["nofall_h5_by_mult_q"] = N5.groupby("mq").apply(st)
    N5["rq"] = pd.qcut(N5["fall5"], 4, labels=False, duplicates="drop")
    out["nofall_h5_by_prior5_q (3=strongest rise)"] = N5.groupby("rq").apply(st)
    N5["bull60"] = N5["r60"] > 0
    out["nofall_h5_by_r60"] = N5.groupby("bull60").apply(st)
    # slope of up move on mult, all non-fall cases per horizon
    sl = {}
    for h in H:
        g = N[N.h == h].dropna(subset=["mult", "up"])
        b = np.polyfit(g["mult"], g["up"], 1)[0]
        g2 = R[(R.fell) & (R.h == h)].dropna(subset=["mult", "up"])
        b2 = np.polyfit(g2["mult"], g2["up"], 1)[0]
        g3 = R[(R.h == h)].dropna(subset=["fall5", "up"])
        b3 = np.polyfit(g3["fall5"], g3["up"], 1)[0]
        sl[h] = dict(slope_up_on_mult_nofall=b, slope_up_on_mult_fell=b2, slope_up_on_prior5ret_all=b3)
    out["slopes"] = pd.DataFrame(sl).T
    out["all_by_h"] = R.groupby("h").apply(st)
    return out
