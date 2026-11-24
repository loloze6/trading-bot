import numpy as np, pandas as pd

def explore(data):
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            hi = b["high"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            lr = np.log(c).diff()
            vol = lr.rolling(30).std()
            vol180 = lr.rolling(90, min_periods=60).std()
            r20 = c / c.shift(20) - 1
            h60 = hi.rolling(60).max()
            dh = np.log(c / h60)
            fwd = c.shift(-H) / c - 1
            n = len(c)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                rows.append(dict(coin=coin, day=ts[i].normalize(), year=ts[i].year, r20=r20[i],
                                 vol=vol[i], vrel=vol[i] / vol180[i], dh=dh[i], fwd=fwd[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d = d.dropna(subset=["r20", "vol", "ex", "dh"])
    d["z20"] = d["r20"] / (d["vol"] * np.sqrt(20))
    d["zdh"] = d["dh"] / (d["vol"] * np.sqrt(20))

    def ct(x, day):
        x = pd.Series(x.values); day = pd.Series(day.values)
        m = x.mean(); s = (x - m).groupby(day).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series(dict(mean=m, t=m / se if se > 0 else np.nan, n=len(x), days=day.nunique()))

    def slope(g, col):
        x = g[col] - g[col].mean()
        return ct(x * g["ex"] / (x ** 2).mean(), g["day"])

    out = {}
    d["vt"] = d.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    out["slope_ex_on_z20_by_volterc"] = d.groupby("vt").apply(lambda g: slope(g, "z20"))
    out["slope_ex_on_z20_up_only_by_volterc"] = d[d.r20 > 0].groupby("vt").apply(lambda g: slope(g, "z20"))
    out["slope_ex_on_z20_down_only"] = slope(d[d.r20 < 0], "z20")
    d["dq"] = pd.qcut(d["zdh"], 6, labels=False, duplicates="drop")
    out["dist_to_60d_high_sextile"] = d.groupby("dq").apply(lambda g: pd.concat([ct(g["ex"], g["day"]), pd.Series({"zdh": g["zdh"].mean()})]))
    out["slope_ex_on_zdh_by_volterc"] = d.groupby("vt").apply(lambda g: slope(g, "zdh"))
    d["early"] = np.where(d["year"] <= 2021, "<=2021", ">=2022")
    out["slope_z20_up_by_period"] = d[d.r20 > 0].groupby("early").apply(lambda g: slope(g, "z20"))
    d2 = d.dropna(subset=["vrel"]).copy()
    d2["rq"] = pd.qcut(d2["vrel"], 3, labels=False)
    out["slope_z20_up_by_vol_vs_own_90d"] = d2[d2.r20 > 0].groupby("rq").apply(lambda g: slope(g, "z20"))
    return out
