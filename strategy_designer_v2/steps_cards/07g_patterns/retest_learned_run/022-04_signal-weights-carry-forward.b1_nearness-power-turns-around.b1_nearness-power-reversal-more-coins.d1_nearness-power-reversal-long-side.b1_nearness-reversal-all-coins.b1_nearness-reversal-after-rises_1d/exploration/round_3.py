def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            d = df.copy().reset_index(drop=True)
            d["day"] = pd.to_datetime(d["day"])
            c = d["close"]
            r = d["coin_return"]
            v30 = r.rolling(30).std()
            d["v30"] = v30
            d["vrel"] = v30 / v30.rolling(180, min_periods=60).mean()
            d["prev1z"] = r.shift(1) / v30.shift(1)
            d["prev5z"] = (c.shift(1) / c.shift(6) - 1) / (v30.shift(1) * np.sqrt(5))
            d["r30z"] = (c.shift(1) / c.shift(31) - 1) / (v30.shift(1) * np.sqrt(30))
            d["volu"] = df["close"] * 0
            d["coin"] = coin; d["w"] = w
            d["wd"] = d["day"].dt.dayofweek
            d["yr"] = d["day"].dt.year
            d["rz"] = r / v30.shift(1)
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["coin_return"])
    res = {}
    S = D[D.wd == 5].copy()
    O = D[D.wd != 5].copy()
    def graded(sub, col, q=4, y="coin_return"):
        x = sub.dropna(subset=[col, y]).copy()
        x["b"] = pd.qcut(x[col], q, labels=False, duplicates="drop")
        out = []
        for b, z in x.groupby("b"):
            m = z.groupby("day")[y].mean()
            out.append(dict(b=b, n=len(z), lo=z[col].min(), hi=z[col].max(), mean=z[y].mean(),
                            t_days=m.mean() / (m.std() / np.sqrt(len(m)))))
        out = pd.DataFrame(out).set_index("b")
        x["rk"] = x[col].rank(pct=True) - 0.5
        cov = x.groupby("day").apply(lambda z: (z["rk"] * z[y]).sum())
        out["slope_t_clustered"] = cov.mean() / (cov.std() / np.sqrt(len(cov)))
        return out.round(5)
    res["sat_by_prev1z"] = graded(S, "prev1z")
    res["sat_by_prev5z"] = graded(S, "prev5z")
    res["sat_by_r30z"] = graded(S, "r30z")
    res["sat_by_vrel"] = graded(S, "vrel")
    res["sat_by_v30"] = graded(S, "v30")
    res["sat_rz_by_v30"] = graded(S, "v30", 4, "rz")
    res["other_days_by_v30"] = graded(O, "v30")
    pc = S.groupby("coin")["coin_return"].agg(["size", "mean", "std"])
    pc["t"] = pc["mean"] / (pc["std"] / np.sqrt(pc["size"]))
    res["sat_by_coin"] = pc.round(5)
    sm = S.groupby("day")["coin_return"].mean()
    om = O.groupby("day")["coin_return"].mean()
    res["sat_minus_other_welch"] = pd.Series({"sat_mean": sm.mean(), "other_mean": om.mean(),
        "t": stats.ttest_ind(sm, om, equal_var=False).statistic, "n_sat": len(sm), "n_other": len(om)}).round(5)
    res["sat_std_vs_other"] = pd.Series({"sat_sd": S.coin_return.std(), "other_sd": O.coin_return.std()}).round(5)
    return res
