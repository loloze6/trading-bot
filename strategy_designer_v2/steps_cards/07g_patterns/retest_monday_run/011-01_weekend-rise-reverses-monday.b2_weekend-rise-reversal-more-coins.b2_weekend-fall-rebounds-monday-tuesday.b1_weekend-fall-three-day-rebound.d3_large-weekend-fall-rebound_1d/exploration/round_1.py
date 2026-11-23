import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        g = []
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            d = pd.DataFrame(index=b.index)
            d["coin"] = coin; d["win"] = w
            d["wd"] = ts.dt.weekday; d["year"] = ts.dt.year
            r1 = c.pct_change(); v = r1.rolling(20).std()
            d["z"] = r1 / v
            d["z2"] = (c / c.shift(2) - 1) / (v * np.sqrt(2))
            d["z20"] = (c / c.shift(20) - 1) / (v * np.sqrt(20))
            d["vrel"] = v / v.rolling(120, min_periods=40).median()
            vol = b["volume"].astype(float)
            d["volrel"] = np.log(vol / vol.rolling(20).mean().shift(1))
            for h in (1, 3, 5):
                d[f"f{h}"] = c.shift(-h) / c - 1
            d["pos"] = np.arange(len(d))
            g.append(d)
        g = pd.concat(g)
        for h in (1, 3, 5):
            grid = g[g.pos % h == 0][f"f{h}"].dropna()
            g[f"x{h}"] = g[f"f{h}"] - grid.mean()
            g[f"s{h}"] = g[f"x{h}"] / grid.std()
        rows.append(g)
    A = pd.concat(rows)

    def tt(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    out = {}
    res = {}
    for wd, s in A.groupby("wd"):
        s = s.dropna(subset=["z", "s3"])
        lr = stats.linregress(s.z, s.s3)
        fa = s[s.z < -1.5].s3; ri = s[s.z > 1.5].s3
        res[wd] = {"slope_s3_on_z": lr.slope, "t_slope": lr.slope / lr.stderr, "n": len(s),
                   "fall_n": len(fa), "fall_s3": fa.mean(), "fall_t": tt(fa)["t"],
                   "rise_n": len(ri), "rise_s3": ri.mean(), "rise_t": tt(ri)["t"]}
    out["by_weekday_z_to_s3"] = pd.DataFrame(res).T

    S = A[A.wd == 6].copy()
    S["zb"] = pd.cut(S.z, [-99, -3, -2, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, 2, 99])
    out["sunday_zbucket"] = S.groupby("zb", observed=True).agg(
        n=("s3", "count"), x1=("x1", "mean"), x3=("x3", "mean"), s3=("s3", "mean"), x5=("x5", "mean"))

    A["zb"] = pd.cut(A.z, [-99, -3, -2, -1.5, -1, 1, 1.5, 2, 3, 99])
    out["alldays_zbucket_s3"] = A.groupby("zb", observed=True).s3.apply(tt).unstack()

    F = S[S.z < -1].copy()
    F["volq"] = pd.qcut(F.volrel, 3, labels=["lowvolume", "mid", "highvolume"])
    out["sunfall_by_volume"] = F.groupby("volq", observed=True).s3.apply(tt).unstack()
    F["vq"] = pd.qcut(F.vrel, 3, labels=["calm", "mid", "turbulent"])
    out["sunfall_by_volregime"] = F.groupby("vq", observed=True).s3.apply(tt).unstack()
    F["tq"] = pd.qcut(F.z20, 3, labels=["down20", "mid", "up20"])
    out["sunfall_by_trend20"] = F.groupby("tq", observed=True).s3.apply(tt).unstack()
    out["sunfall_by_year"] = F.groupby("year").s3.apply(tt).unstack()

    S2 = S.dropna(subset=["z2", "s3"])
    lr = stats.linregress(S2.z2, S2.s3)
    out["sun_weekend2day_slope"] = f"slope {lr.slope:.4f} t {lr.slope/lr.stderr:.2f} n {len(S2)}"

    B = A.dropna(subset=["z", "s3", "volrel"]).copy()
    B["volq"] = pd.qcut(B.volrel, 3, labels=["lowvolume", "mid", "highvolume"])
    r2 = {}
    for q, s in B.groupby("volq", observed=True):
        lr = stats.linregress(s.z, s.s3)
        r2[q] = {"slope": lr.slope, "t": lr.slope / lr.stderr, "n": len(s)}
    out["alldays_slope_by_volume"] = pd.DataFrame(r2).T

    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"] = D.groupby("wd").agg(
        book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    return out
