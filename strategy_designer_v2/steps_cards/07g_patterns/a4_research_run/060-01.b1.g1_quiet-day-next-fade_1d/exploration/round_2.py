def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            s20 = r.rolling(20, min_periods=15).std()
            s30 = r.rolling(30, min_periods=25).std()
            pct = s30.rolling(365, min_periods=120).apply(lambda a: (a <= a[-1]).mean(), raw=True)
            nxt = c.shift(-1) / c - 1
            rng = (b["high"] - b["low"]).astype(float)
            df = pd.DataFrame({
                "coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "z": r / s20, "absz": (r / s20).abs(), "nxt": nxt,
                "rngz": (rng / c) / s20,
                "ret60": c / c.shift(60) - 1, "ret30": c / c.shift(30) - 1,
                "agit": pct > 0.5, "has_pct": pct.notna(),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["adj"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d = d.dropna(subset=["adj", "z"])
    out = {}

    def ct(x):
        if len(x) < 5: return pd.Series({"n": len(x), "mean": np.nan, "t_day": np.nan, "days": 0})
        dev = x.groupby("day")["adj"].sum()
        m = x["adj"].mean()
        dd = x.groupby("day").apply(lambda g: (g["adj"] - m).sum())
        D = len(dd)
        se = np.sqrt((dd ** 2).sum() * D / (D - 1)) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t_day": m / se, "days": D})

    d["trend"] = pd.cut(d["ret60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    x = d[d["has_pct"]].dropna(subset=["trend"]).copy()
    x["prof"] = x["trend"].astype(str) + "_" + np.where(x["agit"], "agit", "calm")
    out["all bars by profile"] = x.groupby("prof").apply(ct)
    x["zb"] = pd.cut(x["z"], [-99, -1, 1, 99], labels=["bigdown", "mid", "bigup"])
    out["profile x z bucket"] = x.groupby(["prof", "zb"], observed=True).apply(ct)
    # graded: within falling profile, ret30 deciles
    y = d.dropna(subset=["ret30"]).copy()
    y["b"] = pd.qcut(y["ret30"], 5)
    out["ret30 quintiles day-t"] = y.groupby("b", observed=True).apply(ct)
    out["ret30 quintiles by window share neg (q2)"] = y[y["b"] == y["b"].cat.categories[1]].groupby("win")["adj"].mean().describe()
    # big absz by window
    big = d[d["absz"] > 1.168]
    out["big absz day-t"] = ct(big)
    out["big absz signed"] = d.assign(zb=pd.cut(d["z"], [-99, -1.168, 1.168, 99])).groupby("zb", observed=True).apply(ct)
    out["big absz by coin"] = big.groupby("coin").apply(ct)
    out["wide range top quint day-t"] = ct(d[d["rngz"] > 2.093])
    out["wide range by coin"] = d[d["rngz"] > 2.093].groupby("coin").apply(ct)
    return out
