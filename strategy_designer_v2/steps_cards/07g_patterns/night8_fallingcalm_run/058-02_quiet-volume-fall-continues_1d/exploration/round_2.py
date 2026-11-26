def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "fwd": c.shift(-H) / c - 1, "r1": r1,
                "r5p": c / c.shift(5) - 1, "r10p": c / c.shift(10) - 1,
                "r30": c / c.shift(30) - 1, "r60": c / c.shift(60) - 1,
                "vol30": vol30,
                "vrat": v.rolling(30).mean() / v.expanding().mean().shift(30),
                "vrat5": v.rolling(5).mean() / v.rolling(30).mean(),
                "clv": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "rng": (b["high"] - b["low"]) / c,
                "fc": b["forecast"].astype(float), "reg": b["regime"].astype(str),
                "bret": b["postRebalance_total_value"].astype(float).pct_change(),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            d["volz"] = d["vol30"] / d["vol30"].expanding(min_periods=30).median()
            d["s1"] = d["r1"] / d["vol30"].shift(1)
            d["s5"] = d["r5p"] / (d["vol30"].shift(5) * np.sqrt(5))
            d["s30"] = d["r30"] / (d["vol30"] * np.sqrt(30))
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift = A[A.pos % H == 0].groupby("coin")["fwd"].mean()
    A["fx"] = A["fwd"] - A["coin"].map(drift)
    G = A[(A.pos % H == 0) & A.fx.notna()].copy()
    G["tr"] = np.where(G.r60 > 0.1, "rising", np.where(G.r60 < -0.1, "falling", "choppy"))
    G.loc[G.r60.isna(), "tr"] = "na"
    G["ag"] = np.where(G.volz > 1, "agit", "calm")

    def ct(x, ts):
        m = x.mean(); s = (x - m).groupby(ts).sum()
        se = np.sqrt((s ** 2).sum()) / len(x)
        return m / se if se > 0 else np.nan, s.shape[0]

    def summ(g):
        t, nd = ct(g["fx"], g["ts"])
        return pd.Series({"n": len(g), "days": nd, "mean%": 100 * g.fx.mean(), "t_day": t})

    def slope(g, col):
        g = g[g[col].notna()]
        if len(g) < 20: return pd.Series({"n": len(g)})
        rho, p = stats.spearmanr(g[col], g.fx)
        return pd.Series({"n": len(g), "spearman": rho, "p": p})

    out = {}
    cols = ["s1", "s5", "s30", "r10p", "vrat", "vrat5", "clv", "rng"]
    rs = []
    for (tr, ag), g in G[G.tr != "na"].groupby(["tr", "ag"]):
        for col in cols:
            s = slope(g, col); s["prof"] = tr + " " + ag; s["col"] = col; rs.append(s)
    R = pd.DataFrame(rs)
    out["spearman by profile x predictor"] = R.pivot(index="col", columns="prof", values="spearman").round(3)
    out["p by profile x predictor"] = R.pivot(index="col", columns="prof", values="p").round(3)
    ca = G[(G.tr == "choppy") & (G.ag == "agit")].copy()
    for col in ["s5", "s30", "vrat", "s1"]:
        x = ca[ca[col].notna()].copy()
        x["q"] = pd.qcut(x[col], 3, labels=False, duplicates="drop")
        out["choppy agit terciles " + col] = x.groupby("q").apply(summ)
    out["choppy agit by coin"] = ca.groupby("coin").apply(summ)
    out["choppy agit by year"] = ca.groupby(ca.ts.dt.year).apply(summ)
    fcal = G[(G.tr == "falling") & (G.ag == "calm")].copy()
    fcal["qr"] = pd.qcut(fcal["s30"], 2, labels=["deep", "shallow"])
    fcal["qv"] = pd.qcut(fcal["vrat"], 2, labels=["light", "heavy"])
    out["falling calm s30 x vrat"] = fcal.groupby(["qr", "qv"]).apply(summ)
    # s1 top quintile across profiles
    x = G[G.s1.notna()].copy()
    x["top"] = x.s1 > x.s1.quantile(0.8)
    out["s1 top quintile by trend"] = x[x.top].groupby("tr").apply(summ)
    out["s1 top quintile all"] = summ(x[x.top])
    # book largest days
    B = A[A.bret.notna() & (A.bret.abs() > 1e-9)].copy()
    lo, hi = B.bret.quantile(0.05), B.bret.quantile(0.95)
    def ctx(g):
        return pd.Series({"n": len(g), "s30": g.s30.mean(), "vrat": g.vrat.mean(),
                          "s1": g.s1.mean(), "volz": g.volz.mean(), "alloc": g.alloc.mean()})
    B["grp"] = np.where(B.bret <= lo, "worst5%", np.where(B.bret >= hi, "best5%", "mid"))
    out["book extremes context"] = B.groupby("grp").apply(ctx)
    return out
