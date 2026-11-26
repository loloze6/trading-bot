import numpy as np
import pandas as pd

def _ct(x, day):
    x = np.asarray(x, float); m = x.mean(); n = len(x)
    d = pd.Series(x - m).groupby(np.asarray(day)).sum().values
    se = np.sqrt((d**2).sum()) / n
    return m / se if se > 0 else np.nan

def _cases(data, h, off=0):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            r1 = pd.Series(c).pct_change()
            ret20 = pd.Series(c).pct_change(20)
            ret60 = pd.Series(c).pct_change(60)
            sd20 = r1.rolling(20).std()
            sd60 = r1.rolling(60).std()
            z = ret20 / (sd20 * np.sqrt(20))
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for i in range(off, n - h, h):
                rows.append(dict(coin=coin, w=w, day=str(ts[i].date()), wd=ts[i].dayofweek, yr=ts[i].year,
                                 reg=b["regime"].iloc[i], z=z.iloc[i], ret60=ret60.iloc[i],
                                 volrel=(sd20 / sd60).iloc[i], r1=r1.iloc[i],
                                 fwd=c[i + h] / c[i] - 1))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    return df

def _slope(d, x, y="ex"):
    d = d.dropna(subset=[x, y])
    X = d[x].values - d[x].mean(); Y = d[y].values
    b = (X * (Y - Y.mean())).sum() / (X**2).sum()
    res = Y - Y.mean() - b * X
    s = pd.Series(X * res).groupby(d["day"].values).sum().values
    se = np.sqrt((s**2).sum()) / (X**2).sum()
    return pd.Series({"n": len(d), "days": d["day"].nunique(), "slope": b, "t": b / se})

def explore(data):
    res = {}
    for h in [7, 14, 21]:
        d = _cases(data, h)
        r = d[(d.reg == "unknown")]
        rp = r[r.z > 0]
        res[f"h{h} rising z>0: slope of ex on z"] = _slope(rp, "z")
        hi = rp[rp.z > rp.z.quantile(0.5)]
        res[f"h{h} rising, upper half of z>0: slope"] = _slope(hi, "z")
        res[f"h{h} rising: slope of ex on volrel"] = _slope(r, "volrel")
        res[f"h{h} rising: slope of ex on ret60"] = _slope(r, "ret60")
        res[f"h{h} all: slope ex on volrel"] = _slope(d, "volrel")
    d = _cases(data, 14)
    r = d[d.reg == "unknown"].dropna(subset=["z", "volrel"]).copy()
    res["14 rising: corr z, volrel"] = float(r[["z", "volrel"]].corr().iloc[0, 1])
    r["ztop"] = r.z >= r.z.quantile(0.8)
    res["14 rising top z quintile: by window"] = r[r.ztop].groupby("w")["ex"].agg(["size", "mean"])
    res["14 rising top z quintile: by coin"] = r[r.ztop].groupby("coin")["ex"].agg(["size", "mean"])
    r["vb"] = pd.qcut(r.volrel, 3, labels=False)
    r["zb"] = pd.qcut(r.z, 3, labels=False)
    res["14 rising: mean ex by z tercile x volrel tercile"] = r.pivot_table(index="zb", columns="vb", values="ex", aggfunc="mean")
    res["14 rising: count by z x volrel"] = r.pivot_table(index="zb", columns="vb", values="ex", aggfunc="size")
    # offset grids for robustness of top-z reversal
    outs = []
    for off in [0, 4, 9]:
        dd = _cases(data, 14, off)
        rr = dd[(dd.reg == "unknown")].dropna(subset=["z"])
        top = rr[rr.z >= rr.z.quantile(0.8)]
        outs.append(dict(off=off, n=len(top), mean=top.ex.mean(), t=_ct(top.ex, top.day)))
    res["14 rising top-z quintile, shifted grids"] = pd.DataFrame(outs)
    # weekday with day-clustered t, excess
    d1 = _cases(data, 1)
    d1["ex1"] = d1["fwd"] - d1.groupby("coin")["fwd"].transform("mean")
    res["1d next-day excess by weekday, day-clustered"] = pd.DataFrame(
        {"n": d1.groupby("wd").size(), "days": d1.groupby("wd")["day"].nunique(),
         "mean": d1.groupby("wd")["ex1"].mean(),
         "t_day": [_ct(g.ex1, g.day) for _, g in d1.groupby("wd")]})
    res["weekday Thu+Fri by year"] = d1[d1.wd.isin([3, 4])].groupby("yr")["ex1"].agg(["size", "mean"])
    return res
