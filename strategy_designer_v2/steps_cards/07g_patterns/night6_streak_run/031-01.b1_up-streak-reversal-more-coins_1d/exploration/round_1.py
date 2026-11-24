def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            up = (r > 0).astype(int); dn = (r < 0).astype(int)
            gu = (up != up.shift()).cumsum(); gd = (dn != dn.shift()).cumsum()
            us = up.groupby(gu).cumsum() * up
            ds = dn.groupby(gd).cumsum() * dn
            streak = us - ds
            fwd = c.shift(-H) / c - 1
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            vol20 = r.rolling(20).std()
            vol120 = r.rolling(120, min_periods=60).std()
            df = pd.DataFrame({"coin": coin, "win": w, "ts": b["timestamp"].values,
                               "fwd": fwd, "r1": r, "streak": streak, "past5": past5,
                               "past20": past20, "vratio": vol20 / vol120,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            df = df.iloc[::H]
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D = D.dropna(subset=["fwd"])
    g = D.groupby("coin")["fwd"]
    D["drift"] = g.transform("mean"); D["usd"] = g.transform("std")
    D["unus"] = D["fwd"] - D["drift"]
    D["z"] = D["unus"] / D["usd"]
    D["wd"] = pd.to_datetime(D["ts"]).dt.weekday
    D["yr"] = pd.to_datetime(D["ts"]).dt.year

    def pt(sub, col="unus"):
        sub = sub.dropna(subset=[col])
        n = len(sub)
        if n < 10: return pd.Series({"n": n, "mean": np.nan, "z": np.nan, "t": np.nan, "days": 0})
        m = sub[col].mean()
        S = (sub[col] - m).groupby(sub["ts"]).sum()
        G = len(S)
        se = np.sqrt(G / (G - 1) * (S ** 2).sum()) / n
        return pd.Series({"n": n, "mean": m, "z": sub["z"].mean(), "t": m / se, "days": G})

    out = {}
    D["sk"] = D["streak"].clip(-6, 6)
    out["by_streak_signed"] = D.groupby("sk").apply(pt)
    for col in ["past5", "past20", "r1", "vratio"]:
        D[col + "_q"] = D.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["by_" + col + "_quintile"] = D.groupby(col + "_q").apply(pt)
    out["by_weekday"] = D.groupby("wd").apply(pt)
    out["by_year"] = D.groupby("yr").apply(pt)
    # streak x vol regime
    D["hv"] = (D["vratio_q"] >= 3).astype(int)
    out["streak_x_highvol"] = D.groupby(["hv", D["streak"].clip(-3, 3)]).apply(pt)[["n", "z", "t"]]
    # by coin: up-streak>=3 vs rest
    out["coin_upstreak3"] = D[D["streak"] >= 3].groupby("coin").apply(pt)[["n", "z", "t"]]
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    DD = pd.concat(dd)
    out["book_daily_by_year"] = DD.groupby(pd.to_datetime(DD["day"]).dt.year)[["book_return", "coin_return"]].mean()
    return out
