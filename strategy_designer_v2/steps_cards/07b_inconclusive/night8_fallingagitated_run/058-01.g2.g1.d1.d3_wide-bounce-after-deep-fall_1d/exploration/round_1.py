def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    allret = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.shift(-1) / c - 1
            allret.append(r1.dropna())
            fw = {h: c.shift(-h) / c - 1 for h in (1, 2, 3, 5)}
            hl = (b["high"] - b["low"]) / c
            ret = c.pct_change()
            sd30 = ret.rolling(30).std()
            p3 = (c.shift(1) / c.shift(4) - 1) / sd30
            up = ret / sd30
            ts = pd.to_datetime(b["timestamp"])
            for i in range(len(b)):
                f = b["forecast"].iloc[i]
                if pd.notna(f) and f < 0:
                    rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, day=ts.iloc[i].normalize(),
                                     f=f, r1=fw[1].iloc[i], r2=fw[2].iloc[i], r3=fw[3].iloc[i], r5=fw[5].iloc[i],
                                     rng=hl.iloc[i] / sd30.iloc[i], p3=p3.iloc[i], upsz=up.iloc[i]))
    d = pd.DataFrame(rows)
    mu = pd.concat(allret).mean()
    for h in (1, 2, 3, 5):
        d[f"s{h}"] = -(d[f"r{h}"] - mu * h)
    cases = d[d.f <= -2].copy()
    def tday(x, col="s1"):
        x = x.dropna(subset=[col])
        g = x.groupby("day")[col].sum()
        n = len(x)
        if n < 3: return pd.Series(dict(n=n, mean=np.nan, t=np.nan))
        return pd.Series(dict(n=n, days=len(g), mean=x[col].mean(), t=g.mean() / (g.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    out = {}
    out["all_active_vs_cases"] = pd.DataFrame({"all_active": tday(d), "cases": tday(cases)})
    out["cases_by_coin"] = cases.groupby("coin").apply(tday)
    out["cases_by_year"] = cases.groupby("year").apply(tday)
    out["cases_by_window"] = cases.groupby("w").apply(tday)
    out["cases_horizon"] = pd.DataFrame({h: tday(cases, f"s{h}") for h in (1, 2, 3, 5)})
    out["active_horizon"] = pd.DataFrame({h: tday(d, f"s{h}") for h in (1, 2, 3, 5)})
    d["fq"] = pd.qcut(d.f.rank(method="first"), 5, labels=["q1_strong", "q2", "q3", "q4", "q5_weak"])
    out["active_by_forecast_quintile"] = d.groupby("fq").apply(tday)
    d["rq"] = pd.qcut(d.rng.rank(method="first"), 4, labels=["r1low", "r2", "r3", "r4high"])
    out["active_by_range_q"] = d.groupby("rq").apply(tday)
    d["pq"] = pd.qcut(d.p3.rank(method="first"), 4, labels=["p1deep", "p2", "p3", "p4shallow"])
    out["active_by_fall_q"] = d.groupby("pq").apply(tday)
    d["uq"] = pd.qcut(d.upsz.rank(method="first"), 4, labels=["u1small", "u2", "u3", "u4big"])
    out["active_by_upday_q"] = d.groupby("uq").apply(tday)
    out["n_active"] = len(d)
    return out
