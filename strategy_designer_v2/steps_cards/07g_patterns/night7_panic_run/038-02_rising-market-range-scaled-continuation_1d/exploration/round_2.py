import numpy as np, pandas as pd
from scipy import stats

def _t(x):
    x = pd.Series(x).dropna()
    if len(x) < 3: return np.nan
    return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

def _tday(d, col="ex"):
    s = d.groupby("ts")[col].sum()
    n = d.groupby("ts")[col].size()
    m = d[col].mean()
    dev = d[col] - m
    sd = dev.groupby(d["ts"]).sum()
    se = np.sqrt((sd**2).sum()) / len(d)
    return m / se if se > 0 else np.nan, d["ts"].nunique()

def _cslope(d, x, y="ex"):
    X = d[x].values; Y = d[y].values
    xm = X - X.mean()
    b = (xm * (Y - Y.mean())).sum() / (xm**2).sum()
    a = Y.mean() - b * X.mean()
    e = Y - a - b * X
    sc = pd.Series(xm * e).groupby(d["ts"].values).sum()
    se = np.sqrt((sc**2).sum()) / (xm**2).sum()
    return b, b / se, len(d), d["ts"].nunique()

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            ts = pd.to_datetime(b["timestamp"])
            rng = (b["high"] - b["low"]) / c
            mr30 = rng.rolling(30, min_periods=30).mean()
            r1 = c / c.shift(1) - 1
            r3 = c / c.shift(3) - 1
            vol10 = r1.rolling(10).std(); vol30 = r1.rolling(30).std()
            vol365 = r1.rolling(30).std()
            agit = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "ts": ts.dt.normalize(),
                "year": ts.dt.year, "wd": ts.dt.dayofweek,
                "s1": r1 / mr30, "s3": r3 / mr30, "f3": c.shift(-3) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "tr60": c / c.shift(60) - 1, "vr": vol10 / vol30, "agit": agit, "r1": r1,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["prof"] = np.where(A.tr60 > 0.10, "rising", np.where(A.tr60 < -0.10, "falling", "choppy"))
    A.loc[A.tr60.isna(), "prof"] = np.nan
    G = A[A["pos"] % 3 == 0].copy()
    drift = G.groupby("coin")["f3"].mean()
    G["ex"] = G["f3"] - G["coin"].map(drift)
    G = G.dropna(subset=["ex", "s1", "s3", "prof"])
    out = {}
    res = []
    for p in ["rising", "choppy", "falling"]:
        for sgn, cond in [("s1>0", G.s1 > 0), ("s3>0", G.s3 > 0)]:
            d = G[(G.prof == p) & cond]
            x = "s1" if sgn == "s1>0" else "s3"
            b, t, n, nd = _cslope(d, x)
            res.append({"prof": p, "set": sgn, "slope": b, "t_day": t, "n": n, "days": nd, "mean_ex": d.ex.mean()})
    out["slopes by profile, day-clustered"] = pd.DataFrame(res)
    # top s1 quintile outside rising by window-year
    NR = G[G.prof != "rising"].copy()
    q = NR.s1.quantile(0.8)
    top = NR[NR.s1 >= q]
    out["not rising top-s1 fade by year"] = top.groupby("year")["ex"].agg(["mean", "size"])
    tt, nd = _tday(top)
    out["not rising top-s1 fade t_day, days"] = f"mean {top.ex.mean():.4f} t {tt:.2f} days {nd}"
    # rising top s3 by year
    R = G[G.prof == "rising"]
    qr = R.s3.quantile(0.8)
    tr = R[R.s3 >= qr]
    out["rising top-s3 by year"] = tr.groupby("year")["ex"].agg(["mean", "size"])
    tt, nd = _tday(tr)
    out["rising top-s3 t_day"] = f"mean {tr.ex.mean():.4f} t {tt:.2f} days {nd}"
    # agitation within rising top s3
    tr2 = tr.dropna(subset=["agit"])
    out["rising top-s3 by agitation"] = tr2.groupby(tr2.agit > 0.5)["ex"].agg(["mean", "size"])
    # weekday, day-clustered: mean across coins per day
    A1 = A.dropna(subset=["r1"])
    dm = A1.groupby("ts").agg(r=("r1", "mean"), wd=("wd", "first"), yr=("year", "first"))
    w = dm.groupby("wd")["r"].agg(["mean", "size"])
    w["t"] = dm.groupby("wd")["r"].apply(_t)
    out["weekday, day-mean of coins"] = w
    dm["friSat"] = dm.wd.isin([4, 5])
    out["fri+sat minus others by year"] = dm.groupby(["yr", "friSat"])["r"].mean().unstack()
    # vol ratio low quintile, day-clustered, by profile
    V = G.dropna(subset=["vr"]).copy()
    V["vq"] = pd.qcut(V.vr, 5, labels=False)
    vv = []
    for p in ["rising", "choppy", "falling"]:
        d = V[(V.vq == 0) & (V.prof == p)]
        tt, nd = _tday(d)
        vv.append({"prof": p, "mean_ex": d.ex.mean(), "t_day": tt, "n": len(d), "days": nd})
    d = V[V.vq == 0]; tt, nd = _tday(d)
    vv.append({"prof": "all", "mean_ex": d.ex.mean(), "t_day": tt, "n": len(d), "days": nd})
    out["low vol10/30 quintile"] = pd.DataFrame(vv)
    b, t, n, nd = _cslope(V, "vr")
    out["slope ex on vr, all"] = f"slope {b:.4f} t {t:.2f} n {n} days {nd}"
    return out
