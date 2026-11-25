def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]
            r = c.pct_change()
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret": r,
                "vol30": r.rolling(30, min_periods=20).std(),
                "n1": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c - 1,
                "n3": c.shift(-3) / c - 1,
                "r5": c / c.shift(5) - 1,
                "r20": c / c.shift(20) - 1,
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c.shift(1),
                "volrel": b["volume"] / b["volume"].rolling(20, min_periods=10).mean(),
                "agit": (b["regime"] != "chop").astype(int),
                "fc": b["forecast"],
                "pos": b["postRebalance_current_allocation"],
                "i": np.arange(len(b)),
            })
            d["z"] = d["ret"] / d["vol30"]
            d["rngz"] = d["rng"] / d["vol30"]
            d["dn2"] = ((r < 0) & (r.shift(1) < 0)).astype(int)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3):
        mu = D.groupby("coin")["n%d" % h].transform(lambda s: s.mean())
        # drift per coin from grid samples
        g = D[D["i"] % h == 0].groupby("coin")["n%d" % h].mean()
        D["x%d" % h] = D["n%d" % h] - D["coin"].map(g)
    D["wd"] = D["day"].dt.dayofweek
    D["yr"] = D["day"].dt.year

    def ct(sub, col):
        sub = sub.dropna(subset=[col])
        x = sub[col]
        n = len(x)
        if n < 5:
            return pd.Series({"n": n, "mean%": np.nan, "t": np.nan})
        m = x.mean()
        S = (x - m).groupby(sub["day"]).sum()
        se = np.sqrt((S ** 2).sum()) / n
        return pd.Series({"n": n, "days": sub["day"].nunique(), "mean%": 100 * m, "t": m / se})

    out = {}
    # 1. z buckets by agitation
    D["zb"] = pd.cut(D["z"], [-99, -2, -1.25, -0.75, -0.25, 0.25, 0.75, 1.5, 99])
    out["z bucket x agit, next-day excess"] = D.groupby(["agit", "zb"], observed=True).apply(lambda s: ct(s, "x1")).round(3)
    # 2. horizons 2,3 on grid, falls
    res = {}
    for h in (2, 3):
        S = D[(D["i"] % h == 0)]
        for a in (0, 1):
            for lab, m in [("z<-1.25", S["z"] < -1.25), ("-1.25<z<0", (S["z"] >= -1.25) & (S["z"] < 0)), ("z>0", S["z"] > 0)]:
                res[(h, a, lab)] = ct(S[m & (S["agit"] == a)], "x%d" % h)
    out["h2/h3 grid by agit and z"] = pd.DataFrame(res).T.round(3)
    F = D[(D["z"] < -0.75)]
    # 3. falls: close location, range, volume, prior 5d / 20d, consecutive
    F = F.copy()
    F["clvq"] = pd.qcut(F["clv"], 3, labels=["lowclose", "mid", "highclose"])
    out["falls z<-0.75: by clv tercile x agit"] = F.groupby(["agit", "clvq"], observed=True).apply(lambda s: ct(s, "x1")).round(3)
    F["volq"] = pd.qcut(F["volrel"], 3, labels=["lowvol", "mid", "highvol"])
    out["falls: by volume rel tercile x agit"] = F.groupby(["agit", "volq"], observed=True).apply(lambda s: ct(s, "x1")).round(3)
    F["r20q"] = pd.qcut(F["r20"], 3, labels=["r20low", "mid", "r20high"])
    out["falls: by prior 20d ret tercile x agit"] = F.groupby(["agit", "r20q"], observed=True).apply(lambda s: ct(s, "x1")).round(3)
    F["r5q"] = pd.qcut(F["r5"], 3, labels=["r5low", "mid", "r5high"])
    out["falls: by prior 5d ret tercile x agit"] = F.groupby(["agit", "r5q"], observed=True).apply(lambda s: ct(s, "x1")).round(3)
    out["falls: by weekday of fall x agit"] = F.groupby(["agit", "wd"]).apply(lambda s: ct(s, "x1")).round(3)
    out["falls: by year (agit)"] = F[F["agit"] == 1].groupby("yr").apply(lambda s: ct(s, "x1")).round(3)
    out["falls: by coin x agit"] = F.groupby(["coin", "agit"]).apply(lambda s: ct(s, "x1")).round(3)
    # 4. all bars: weekday, up moves
    out["all bars: next-day excess by weekday of next day"] = D.assign(nwd=(D["wd"] + 1) % 7).groupby("nwd").apply(lambda s: ct(s, "x1")).round(3)
    # 5. book: days returns; largest losses
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    DD = pd.concat(dd)
    BR = DD.groupby("day")["book_return"].mean().dropna()
    q = BR.quantile([0.02, 0.98])
    out["book daily quantiles"] = BR.describe().round(5)
    D2 = D.copy(); D2["bday"] = D2["day"] + pd.Timedelta(days=1)
    worst = BR[BR <= q.iloc[0]].index; best = BR[BR >= q.iloc[1]].index
    ww = D2[D2["bday"].isin(worst) & (D2["pos"].abs() > 0)]
    bb = D2[D2["bday"].isin(best) & (D2["pos"].abs() > 0)]
    out["held into worst/best book days: mean z, r5, rngz, agit"] = pd.DataFrame({
        "worst": ww[["z", "r5", "rngz", "clv", "volrel"]].mean(), "best": bb[["z", "r5", "rngz", "clv", "volrel"]].mean(),
        "all_held": D2[D2["pos"].abs() > 0][["z", "r5", "rngz", "clv", "volrel"]].mean()}).round(3)
    return out
