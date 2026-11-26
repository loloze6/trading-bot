def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["nxt3"] = b["close"].shift(-3) / b["close"] - 1
            b["ret"] = b["close"] / b["close"].shift(1) - 1
            rng = (b["high"] - b["low"])
            b["cl"] = (b["close"] - b["low"]) / rng.replace(0, np.nan)
            b["rm"] = rng / rng.rolling(20).mean()
            b["vol20"] = b["ret"].rolling(20).std()
            b["zret"] = b["ret"] / b["vol20"].shift(1)
            b["r5"] = b["close"] / b["close"].shift(5) - 1
            b["z5"] = b["r5"] / (b["vol20"].shift(5) * np.sqrt(5))
            b["tr60"] = b["close"] / b["close"].shift(60) - 1
            b["vol30"] = b["ret"].rolling(30).std()
            b["volrank"] = b["vol30"].expanding(30).rank(pct=True)
            b["wd"] = b["ts"].dt.dayofweek
            b["year"] = b["ts"].dt.year
            b["day"] = b["ts"].dt.floor("D")
            b["coin"] = coin; b["win"] = w
            b["g3"] = (np.arange(len(b)) % 3 == 0)
            rows.append(b)
    d = pd.concat(rows, ignore_index=True)
    d = d[d["nxt"].notna()].copy()
    drift = d.groupby("coin")["nxt"].mean()
    d["ex"] = d["nxt"] - d["coin"].map(drift)
    d["exs"] = d["ex"] / d["coin"].map(d.groupby("coin")["nxt"].std())
    d["trend"] = pd.cut(d["tr60"], [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    d["agit"] = np.where(d["volrank"] > 0.5, "agit", "calm")
    d["prof"] = d["trend"].astype(str) + "_" + d["agit"]
    d["clq"] = pd.cut(d["cl"], [0, .2, .4, .6, .8, 1.0001], include_lowest=True, labels=["c1","c2","c3","c4","c5"])
    d["zq"] = pd.qcut(d["zret"], 5, labels=["z1","z2","z3","z4","z5"])
    d["z5q"] = pd.qcut(d["z5"], 5, labels=["q1","q2","q3","q4","q5"])
    def summ(g, col="exs"):
        g = g[g[col].notna()]
        n = len(g)
        if n < 3: return pd.Series({"n": n, "mean": np.nan, "t_day": np.nan, "days": 0})
        pd_ = g.groupby("day")[col].sum()
        nd = len(pd_)
        t = pd_.sum() / (pd_.std() * np.sqrt(nd)) if nd > 2 else np.nan
        return pd.Series({"n": n, "mean": g[col].mean(), "t_day": t, "days": nd})
    out = {}
    out["prof x clq"] = d.groupby(["prof", "clq"]).apply(summ)
    out["prof x zq (1-day z return)"] = d.groupby(["prof", "zq"]).apply(summ)
    ca = d[d.prof == "choppy_agit"]
    out["choppy agit x z5q (5-day z)"] = ca.groupby("z5q").apply(summ)
    out["choppy agit by year"] = ca.groupby("year").apply(summ)
    out["choppy agit by coin"] = ca.groupby("coin").apply(summ)
    out["choppy agit x weekday"] = ca.groupby("wd").apply(summ)
    out["weekday by year"] = d.groupby(["wd", "year"])["exs"].mean().unstack()
    out["weekday by coin"] = d.groupby(["wd", "coin"])["exs"].mean().unstack()
    fa = d[d.prof == "falling_agit"]
    fa_corr = fa[["cl", "zret", "rm", "exs"]].corr()["exs"]
    out["falling agit corr with exs"] = fa_corr
    fc = d[d.prof == "falling_calm"]
    out["falling calm corr with exs"] = fc[["cl", "zret", "rm", "exs"]].corr()["exs"]
    # 3-day forward on grid, falling agit by zq
    g3 = d[d.g3 & d.nxt3.notna()].copy()
    g3["ex3"] = g3["nxt3"] - g3["coin"].map(g3.groupby("coin")["nxt3"].mean())
    g3["ex3s"] = g3["ex3"] / g3["coin"].map(g3.groupby("coin")["nxt3"].std())
    out["3d fwd: prof x zq"] = g3.groupby(["prof", "zq"]).apply(lambda g: summ(g, "ex3s"))
    return out
