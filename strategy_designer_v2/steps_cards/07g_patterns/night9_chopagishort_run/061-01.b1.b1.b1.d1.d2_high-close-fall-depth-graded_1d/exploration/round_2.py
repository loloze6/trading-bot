def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            rng = (hi - lo).replace(0, np.nan)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            # agitation: 30d vol vs its past-year values (only what the window holds)
            agit = vol30.rolling(365, min_periods=120).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                               "cl": (c - lo) / rng, "r1": r1, "r5": c / c.shift(5) - 1,
                               "r10": c / c.shift(10) - 1, "r20": c / c.shift(20) - 1,
                               "r60": c / c.shift(60) - 1, "vol30": vol30, "agit": agit,
                               "fwd": c.shift(-H) / c - 1, "yr": ts.dt.year})
            df["z20"] = df.r20 / (vol30 * np.sqrt(20))
            df["z1"] = df.r1 / vol30
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift = D[D.pos % H == 0].groupby("coin")["fwd"].mean()
    D["ufwd"] = D["fwd"] - D["coin"].map(drift)
    G = D[D.pos % H == 0].dropna(subset=["ufwd", "r20"]).copy()
    G["trend"] = pd.cut(G.r60, [-10, -0.1, 0.1, 10], labels=["fall", "chop", "rise"])
    G["ag"] = np.where(G.agit > 0.5, "agit", np.where(G.agit.notna(), "calm", "na"))

    def ct(g):
        g = g.dropna(subset=["ufwd"])
        n = len(g)
        if n < 5: return pd.Series({"n": n, "days": 0, "mean": np.nan, "t_day": np.nan})
        m = g.ufwd.mean()
        s = (g.ufwd - m).groupby(g.day).sum()
        se = np.sqrt((s ** 2).sum()) / n
        return pd.Series({"n": n, "days": g.day.nunique(), "mean": round(m, 4), "t_day": round(m / se, 2)})

    out = {}
    G["z20q"] = pd.qcut(G.z20, 5)
    out["z20 quintile"] = G.groupby("z20q", observed=True).apply(ct)
    out["z20 quintile x trend"] = G.dropna(subset=["trend"]).groupby(["trend", "z20q"], observed=True).apply(ct)
    out["z20 quintile x agitation"] = G[G.ag != "na"].groupby(["ag", "z20q"], observed=True).apply(ct)
    out["z20 quintile x year"] = G.groupby(["yr", pd.cut(G.z20, [-99, -0.5, 0.5, 99])], observed=True).apply(ct)
    out["z20 quintile x half"] = G.groupby([G.w.isin(["w7","w8","w9","w10","w11","w12"]), "z20q"], observed=True).apply(ct)
    # signed graded: corr of z20 with ufwd
    out["spearman z20 vs ufwd"] = float(G[["z20", "ufwd"]].corr(method="spearman").iloc[0, 1])
    G["z1q"] = pd.qcut(G.z1, 5)
    out["z1 quintile x trend"] = G.dropna(subset=["trend"]).groupby(["trend", "z1q"], observed=True).apply(ct)
    # high close in chop agit vs chop calm (the brief's second falsifier)
    G["hc"] = G.cl >= 0.75
    out["choppy high close by agitation"] = G[(G.trend == "chop") & (G.ag != "na")].groupby(["ag", "hc"]).apply(ct)
    # book: biggest days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dd)
    br = DD.groupby("day")["book_return"].mean().dropna()
    out["book days nonzero"] = int((br != 0).sum())
    out["book top10 day share of sum"] = float(br.sort_values().tail(10).sum() / br.sum())
    out["book worst10 day sum"] = float(br.sort_values().head(10).sum())
    return out
