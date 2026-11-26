def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = [1, 3, 5, 10]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            hi5 = c.rolling(5, min_periods=5).max()
            sd30 = c.pct_change().rolling(30, min_periods=20).std()
            dip = (hi5 - c) / hi5 / sd30
            tr60 = (c / c.shift(60) - 1) * 100
            for h in H:
                fr = c.shift(-h) / c - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if i + h >= len(b):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4],
                                     inprof=b["regime"].iloc[i] == "unknown",
                                     fc=b["forecast"].iloc[i], dip=dip.iloc[i], tr=tr60.iloc[i],
                                     ret=fr.iloc[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "h"])["ret"].transform("mean")
    df["ex"] = df["ret"] - drift
    out = {}

    def slope_t(d, x):
        d = d.dropna(subset=[x, "ex"])
        if len(d) < 20 or d[x].std() == 0:
            return pd.Series(dict(n=len(d), slope=np.nan, t=np.nan, mean_ex=np.nan))
        X = d[x] - d[x].mean()
        bta = (X * d["ex"]).sum() / (X ** 2).sum()
        res = d["ex"] - d["ex"].mean() - bta * X
        g = (X * res).groupby(d["day"]).sum()
        se = np.sqrt((g ** 2).sum()) / (X ** 2).sum()
        return pd.Series(dict(n=len(d), slope=bta, t=bta / se, mean_ex=d["ex"].mean()))

    ip = df[df.inprof]
    out["by_horizon_inprof_fc"] = pd.DataFrame({h: slope_t(ip[ip.h == h], "fc") for h in H}).T
    out["by_horizon_inprof_dip"] = pd.DataFrame({h: slope_t(ip[ip.h == h], "dip") for h in H}).T
    i5 = ip[ip.h == 5]
    out["by_coin_h5"] = i5.groupby("coin").apply(lambda d: slope_t(d, "fc"))
    out["by_year_h5"] = i5.groupby("year").apply(lambda d: slope_t(d, "fc"))
    i5 = i5.copy()
    i5["dq"] = pd.qcut(i5["dip"].rank(method="first"), 5, labels=False)
    out["dip_quintile_h5"] = i5.groupby("dq").agg(n=("ex", "size"), dip=("dip", "mean"), fc=("fc", "mean"),
                                                 ex=("ex", "mean"), ret=("ret", "mean"))
    # outside profile, by trend bucket (recomputed 60d trend)
    a5 = df[(df.h == 5)].copy()
    a5["tb"] = pd.cut(a5["tr"], [-1e9, -10, 10, 1e9], labels=["fall", "chop", "rise"])
    a5["grp"] = np.where(a5.inprof, "inprof", "out_" + a5["tb"].astype(str))
    out["dip_slope_by_group_h5"] = a5.groupby("grp").apply(lambda d: slope_t(d, "dip"))
    return out
