import numpy as np, pandas as pd

def explore(data):
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).reset_index(drop=True)
            hi = b["high"].astype(float).reset_index(drop=True)
            lo = b["low"].astype(float).reset_index(drop=True)
            vlm = b["volume"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            lr = np.log(c).diff()
            vol = lr.rolling(30).std()
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            r1 = c / c.shift(1) - 1
            h60 = hi.rolling(60).max(); l60 = lo.rolling(60).min()
            pos60 = (c - l60) / (h60 - l60)
            vratio = vlm.rolling(10).mean() / vlm.rolling(60).mean()
            fwd = c.shift(-H) / c - 1
            n = len(c)
            for i in range(0, n, H):
                if i + H >= n:
                    break
                rows.append(dict(coin=coin, day=ts[i].normalize(), r20=r20[i], r60=r60[i], r1=r1[i],
                                 vol=vol[i], pos60=pos60[i], vratio=vratio[i], fwd=fwd[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["fwd"] - d.groupby("coin")["fwd"].transform("mean")
    d = d.dropna(subset=["r20", "r60", "vol", "ex", "pos60"])
    d["z20"] = d["r20"] / (d["vol"] * np.sqrt(20))
    d["z1"] = d["r1"] / d["vol"]

    def ct(x, day):
        x = pd.Series(x.values); day = pd.Series(day.values)
        m = x.mean(); s = (x - m).groupby(day).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return pd.Series(dict(mean=m, t=m / se if se > 0 else np.nan, n=len(x), days=day.nunique()))

    out = {}
    d["d20"] = pd.qcut(d["z20"], 10, labels=False)
    out["z20_decile_ex"] = d.groupby("d20").apply(lambda g: pd.concat([ct(g["ex"], g["day"]), pd.Series({"z20": g["z20"].mean()})]))
    d["p5"] = pd.qcut(d["pos60"], 5, labels=False)
    out["pos60_quintile_ex"] = d.groupby("p5").apply(lambda g: pd.concat([ct(g["ex"], g["day"]), pd.Series({"pos": g["pos60"].mean()})]))
    out["pos60_slope_ex"] = ct((d["pos60"] - d["pos60"].mean()) * d["ex"] / d["pos60"].var(), d["day"])
    up = d[d.r20 > 0].copy()
    up["vq"] = pd.qcut(up["vratio"], 3, labels=False)
    out["up20_by_volume_ratio"] = up.groupby("vq").apply(lambda g: ct(g["ex"], g["day"]))
    d["q1"] = pd.qcut(d["z1"], 6, labels=False)
    out["z1_sextile_ex"] = d.groupby("q1").apply(lambda g: ct(g["ex"], g["day"]))
    d["vt"] = d.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    top = d[d.d20 >= 8]
    out["top20pct_z20_by_vol"] = top.groupby("vt").apply(lambda g: ct(g["ex"], g["day"]))
    out["pos60_top_quint_by_vol"] = d[d.p5 == 4].groupby("vt").apply(lambda g: ct(g["ex"], g["day"]))
    return out
