def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); lo = b["low"].astype(float)
            ret30 = c / c.shift(30) - 1
            low10 = lo.shift(1).rolling(10).min()
            depth = c / low10 - 1
            vol20 = c.pct_change().rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "year": ts.dt.year, "dayk": ts.dt.floor("D").astype("int64"),
                               "ret30": ret30, "depth": depth, "vol20": vol20,
                               "dnorm": depth / vol20,
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "pp": b.get("debug_info.components.break_depth.post_pipeline_value")})
            df["f1"] = c.shift(-1) / c - 1
            df["f2"] = c.shift(-2) / c - 1
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["f1"].mean()
    d["x1"] = d.f1 - d.coin.map(drift)
    sit = d[(d.ret30 < 0) & (d.depth < 0)].dropna(subset=["x1"]).copy()
    def ct(s, wcol=None):
        s = s.dropna(subset=["x1"])
        if wcol is None:
            wts = pd.Series(1.0, index=s.index)
        else:
            wts = s[wcol].clip(lower=0)
        if wts.sum() == 0 or len(s) < 3:
            return pd.Series({"n": len(s), "days": s.dayk.nunique(), "mean": np.nan, "t_day": np.nan})
        m = (s.x1 * wts).sum() / wts.sum()
        dev = ((s.x1 - m) * wts).groupby(s.dayk).sum()
        se = np.sqrt((dev ** 2).sum()) / wts.sum()
        return pd.Series({"n": len(s), "days": s.dayk.nunique(), "mean": m, "t_day": m / se})
    out = {}
    out["all_unweighted_vs_weighted"] = pd.DataFrame({"unw": ct(sit), "w_alloc": ct(sit, "alloc")})
    sit["dq"] = pd.qcut(sit.depth, 5, labels=False)
    sit["rq"] = pd.qcut(sit.ret30, 3, labels=False)
    sit["nq"] = pd.qcut(sit.dnorm, 5, labels=False)
    out["alloc_and_pp_by_depth_q"] = sit.groupby("dq").agg(alloc=("alloc", "mean"), pp=("pp", "mean"), held=("alloc", lambda x: (x > 0).mean()))
    out["deepest_q_by_year"] = sit[sit.dq == 0].groupby("year").apply(lambda s: ct(s))
    out["deepest_q_excl2020"] = ct(sit[(sit.dq == 0) & (sit.year != 2020)])
    out["mostfallen_by_year"] = sit[sit.rq == 0].groupby("year").apply(lambda s: ct(s))
    out["volnorm_depth_q"] = sit.groupby("nq").apply(lambda s: ct(s))
    out["deep_x_fallen"] = sit.groupby([sit.dq <= 1, sit.rq == 0]).apply(lambda s: ct(s))
    out["deepest_q_by_coin"] = sit[sit.dq <= 1].groupby("coin").apply(lambda s: ct(s))
    out["ret30_depth_corr"] = pd.Series({"pearson_ret30_x1": sit[["ret30", "x1"]].corr().iloc[0, 1],
                                          "pearson_depth_x1": sit[["depth", "x1"]].corr().iloc[0, 1],
                                          "pearson_pp_x1": sit[["pp", "x1"]].corr().iloc[0, 1]})
    return out
