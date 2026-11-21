def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            n = len(b)
            for h in (1, 2, 3, 5):
                for i in range(0, n - h, h):
                    if i < 21: continue
                    # past h-day return standardised by daily vol * sqrt(h)
                    past = c.iloc[i] / c.iloc[i - h] - 1
                    rows.append(dict(coin=coin, w=w, h=h, y=ts.iloc[i].year,
                                     z=past / (vol20.iloc[i] * np.sqrt(h)),
                                     zv=vol20.iloc[i],
                                     fwd=c.iloc[i + h] / c.iloc[i] - 1))
    R = pd.DataFrame(rows).dropna()
    R["adj"] = R["fwd"] - R.groupby(["coin", "h"])["fwd"].transform("mean")
    R["sadj"] = R["adj"] / (R["zv"] * np.sqrt(R["h"]))
    R["zc"] = R["z"].clip(-3, 3)
    def tstat(x):
        return x.mean() / (x.std() / np.sqrt(len(x)))
    # slope of standardised forward on clipped z, per h, with t
    sl = []
    for h, g in R.groupby("h"):
        s = stats.linregress(g["zc"], g["sadj"])
        sl.append(dict(h=h, n=len(g), slope=s.slope, t=s.slope / s.stderr))
    out["slope_by_h"] = pd.DataFrame(sl)
    # per coin, per year slopes at h=1
    for key in ("coin", "y"):
        sl = []
        for k, g in R[R.h == 1].groupby(key):
            s = stats.linregress(g["zc"], g["sadj"])
            sl.append(dict(k=k, n=len(g), slope=s.slope, t=s.slope / s.stderr))
        out[f"h1_slope_by_{key}"] = pd.DataFrame(sl)
    # bins at h=1,2,3 with raw adj mean
    R["zbin"] = pd.cut(R["z"], [-100, -2, -1, -0.5, 0, 0.5, 1, 2, 100])
    for h in (1, 2, 3):
        g = R[R.h == h]
        out[f"h{h}_by_z"] = g.groupby("zbin", observed=True)["adj"].agg(["count", "mean", tstat])
    # by vol tercile at h=1, slope
    g = R[R.h == 1].copy()
    g["vq"] = g.groupby("coin")["zv"].transform(lambda x: pd.qcut(x, 3, labels=False))
    sl = []
    for k, gg in g.groupby("vq"):
        s = stats.linregress(gg["zc"], gg["sadj"])
        sl.append(dict(vq=k, n=len(gg), slope=s.slope, t=s.slope / s.stderr,
                       mean_abs_move=gg["adj"].abs().mean()))
    out["h1_slope_by_volq"] = pd.DataFrame(sl)
    return out
