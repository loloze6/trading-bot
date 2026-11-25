def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            df = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "r": r, "z": z, "fc": b["forecast"].astype(float),
                               "tr60": c / c.shift(60) - 1,
                               "vol_rank": sd.rolling(90, min_periods=40).rank(pct=True)})
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["pos"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    for h in (1, 2, 3, 5):
        d[f"x{h}"] = d[f"f{h}"] - d.groupby("coin")[f"f{h}"].transform("mean")

    def ct(s, days):
        s = s.dropna(); days = days.loc[s.index]
        n = len(s)
        if n < 5: return (n, np.nan, np.nan)
        dev = (s - s.mean()).groupby(days).sum()
        D = len(dev)
        se = np.sqrt(D / (D - 1) * (dev ** 2).sum()) / n
        return (n, s.mean(), s.mean() / se)

    def tab(g, col="x1"):
        res = {}
        for k, sub in g:
            n, m, t = ct(sub[col], sub["day"])
            res[k] = {"n": n, "mean": m, "t_day": t}
        return pd.DataFrame(res).T

    cases = d[d["fc"] > 0].copy()
    out["cases_total"] = ct(cases["x1"], cases["day"])
    cases["zbin"] = pd.cut(cases["z"], [-99, -3, -2.5, -2, -1.5, -1.2, 0])
    out["by_zbin_raw"] = tab(cases.groupby("zbin", observed=True))
    cases["fbin"] = pd.cut(cases["fc"], [0, 8, 12, 16, 19.99, 20])
    out["by_forecast_bin"] = tab(cases.groupby("fbin", observed=True))
    out["by_coin"] = tab(cases.groupby("coin"))
    out["by_window"] = tab(cases.groupby("win"))
    cases["trend"] = pd.cut(cases["tr60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    out["by_trend"] = tab(cases.groupby("trend", observed=True))
    cases["agit"] = np.where(cases["vol_rank"] > 0.5, "agitated", "calm")
    out["by_agit"] = tab(cases.groupby("agit"))
    out["by_trend_agit"] = tab(cases.groupby(["trend", "agit"], observed=True))
    hz = {}
    for h in (1, 2, 3, 5):
        hz[h] = dict(zip(["n", "mean", "t_day"], ct(cases[f"x{h}"], cases["day"])))
    out["by_horizon"] = pd.DataFrame(hz).T
    # all bars with z<=-1 (regime) vs forecast>0
    reg = d[d["z"] <= -1]
    out["all_z_le_-1"] = ct(reg["x1"], reg["day"])
    out["corr_z_x1_cases"] = cases[["z", "x1"]].corr().iloc[0, 1]
    out["corr_fc_x1_cases"] = cases[["fc", "x1"]].corr().iloc[0, 1]
    # trimmed: drop top/bottom 1% of x1
    q = cases["x1"].quantile([0.01, 0.99])
    tr = cases[(cases["x1"] > q.iloc[0]) & (cases["x1"] < q.iloc[1])]
    out["trimmed_1pct"] = ct(tr["x1"], tr["day"])
    out["median_x1"] = cases["x1"].median()
    out["share_x1_pos"] = (cases["x1"] > 0).mean()
    return out
