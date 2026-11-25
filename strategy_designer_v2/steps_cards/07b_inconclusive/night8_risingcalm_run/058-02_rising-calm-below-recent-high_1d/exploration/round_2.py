def explore(data):
    import numpy as np, pandas as pd
    rows = []
    H = [1, 2, 3, 5, 7]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            hi5 = c.rolling(5, min_periods=5).max()
            sd30 = r.rolling(30, min_periods=20).std()
            dip = (hi5 - c) / hi5 / sd30
            ret5 = c / c.shift(5) - 1
            tr60 = (c / c.shift(60) - 1) * 100
            v30 = r.rolling(30, min_periods=20).std()
            vpct = v30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            for h in H:
                fr = c.shift(-h) / c - 1
                for i in range(0, len(b), h):
                    if i + h >= len(b):
                        continue
                    ts = str(b["timestamp"].iloc[i])
                    rows.append(dict(coin=coin, w=w, h=h, day=ts[:10], year=ts[:4],
                                     inprof=b["regime"].iloc[i] == "unknown",
                                     dip=dip.iloc[i], r5=ret5.iloc[i] / sd30.iloc[i] if sd30.iloc[i] else np.nan,
                                     tr=tr60.iloc[i], vp=vpct.iloc[i], ret=fr.iloc[i]))
    df = pd.DataFrame(rows)
    df["ex"] = df["ret"] - df.groupby(["coin", "h"])["ret"].transform("mean")

    def slope_t(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 20 or d[x].std() == 0:
            return pd.Series(dict(n=len(d), days=np.nan, slope=np.nan, t=np.nan))
        X = d[x] - d[x].mean()
        bta = (X * d["ex"]).sum() / (X ** 2).sum()
        res = d["ex"] - d["ex"].mean() - bta * X
        g = (X * res).groupby(d["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(n=len(d), days=d["day"].nunique(), slope=bta, t=bta / se))

    def mean_t(d):
        d = d.dropna(subset=["ex"])
        g = d.groupby("day")["ex"].sum()
        m = d["ex"].mean()
        se = np.sqrt(((g - d.groupby("day")["ex"].size() * m) ** 2).sum()) / len(d)
        return pd.Series(dict(n=len(d), mean_ex=m, t=m / se if se else np.nan))

    out = {}
    ip = df[df.inprof]
    out["inprof_dip_slope_by_h"] = pd.DataFrame({h: slope_t(ip[ip.h == h], "dip") for h in H}).T
    out["inprof_r5_slope_by_h"] = pd.DataFrame({h: slope_t(ip[ip.h == h], "r5") for h in H}).T
    i5 = ip[ip.h == 5].dropna(subset=["dip"]).copy()
    i5["deep"] = np.where(i5.dip > i5.dip.median(), "deep_half", "shallow_half")
    out["inprof_h5_halves"] = i5.groupby("deep").apply(mean_t)
    out["inprof_h5_dip_slope_by_year"] = i5.groupby("year").apply(lambda d: slope_t(d, "dip"))
    out["inprof_h5_dip_slope_by_coin"] = i5.groupby("coin").apply(lambda d: slope_t(d, "dip"))
    a = df[df.h == 5].dropna(subset=["tr", "vp"]).copy()
    a["prof"] = np.select([a.tr > 10, a.tr < -10], ["rising", "falling"], "choppy") + "_" + np.where(a.vp > 0.5, "agit", "calm")
    out["h5_dip_slope_by_profile"] = a.groupby("prof").apply(lambda d: slope_t(d, "dip"))
    a1 = df[df.h == 2].dropna(subset=["tr", "vp"]).copy()
    a1["prof"] = np.select([a1.tr > 10, a1.tr < -10], ["rising", "falling"], "choppy") + "_" + np.where(a1.vp > 0.5, "agit", "calm")
    out["h2_dip_slope_by_profile"] = a1.groupby("prof").apply(lambda d: slope_t(d, "dip"))
    return out
