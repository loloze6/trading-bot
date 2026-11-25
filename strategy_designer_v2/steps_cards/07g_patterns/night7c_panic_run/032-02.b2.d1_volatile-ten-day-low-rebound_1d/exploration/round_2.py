def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]
            mr = (h - l).rolling(30).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-1) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "dist_hi": (h - c) / mr,
                "dist_lo": (c - l) / mr,
                "rng_rel": (h - l) / mr,
                "r1z": (c / c.shift(1) - 1) / (c / c.shift(1) - 1).rolling(30).std().shift(1),
                "depth10": (l.shift(1).rolling(10).min() - c) / (h - l).rolling(30).mean(),
                "inreg": (b["regime"] == "mean_reversion").values,
                "day": ts.dt.floor("D"), "year": ts.dt.year,
                "grid3": (np.arange(len(b)) % 3 == 0),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for col in ["fwd", "fwd3"]:
        if col == "fwd3":
            g = d[d["grid3"]]
        else:
            g = d
        dr = g.groupby("coin")[col].mean()
        sd = g.groupby("coin")[col].std()
        d["u" if col == "fwd" else "u3"] = d[col] - d["coin"].map(dr)
        d["s" if col == "fwd" else "s3"] = d["u" if col == "fwd" else "u3"] / d["coin"].map(sd)

    def summ(g, uc="u", sc="s"):
        g = g.dropna(subset=[uc]); x = g[uc]; n = len(x)
        if n < 3: return pd.Series({"n": n})
        dev = g.groupby("day")[uc].apply(lambda v: (v - x.mean()).sum())
        se = np.sqrt((dev ** 2).sum() * len(dev) / max(len(dev) - 1, 1)) / n
        return pd.Series({"n": n, "days": len(dev), "mean_u%": 100 * x.mean(),
                          "strength": g[sc].mean(), "t_cl": x.mean() / se if se > 0 else np.nan})

    out = {}
    nb = d[~(d["depth10"] > 0)].copy()
    nb["cq"] = pd.qcut(nb["clv"], 5, labels=False, duplicates="drop")
    out["nobreak_by_clv_quint"] = nb.groupby("cq").apply(summ)
    d["dhq"] = d.groupby("coin")["dist_hi"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["all_by_dist_from_high_quint"] = d.groupby("dhq").apply(summ)
    nb["dhq"] = nb.groupby("coin")["dist_hi"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["nobreak_by_dist_from_high_quint"] = nb.groupby("dhq").apply(summ)
    d["dlq"] = d.groupby("coin")["dist_lo"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["all_by_dist_from_low_quint"] = d.groupby("dlq").apply(summ)
    g3 = d[d["grid3"]].copy()
    g3["dhq"] = g3.groupby("coin")["dist_hi"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["grid3_fwd3_by_dist_from_high_quint"] = g3.groupby("dhq").apply(lambda g: summ(g, "u3", "s3"))
    top = d[d["dhq"] == 4]
    out["top_dist_hi_by_year"] = top.groupby("year").apply(summ)
    out["top_dist_hi_by_coin"] = top.groupby("coin").apply(summ)
    out["top_dist_hi_by_regime"] = top.groupby("inreg").apply(summ)
    # regression of u on dist_hi, per coin standardised
    d["z"] = d.groupby("coin")["dist_hi"].transform(lambda v: (v - v.mean()) / v.std())
    dd = d.dropna(subset=["z", "s"])
    beta = (dd["z"] * dd["s"]).sum() / (dd["z"] ** 2).sum()
    res = dd["s"] - beta * dd["z"]
    sc = (dd["z"] * res).groupby(dd["day"]).sum()
    se = np.sqrt((sc ** 2).sum()) / (dd["z"] ** 2).sum()
    out["slope_strength_on_z_dist_hi"] = pd.Series({"beta": beta, "t_cl": beta / se, "n": len(dd), "days": dd["day"].nunique()})
    # book largest days
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; bk.append(x)
    bk = pd.concat(bk).dropna(subset=["book_return"])
    bd = bk.groupby("day").agg(br=("book_return", "mean"), cr=("coin_return", "mean"))
    q = bd["br"].quantile([0.01, 0.99])
    out["book_extreme_days"] = pd.Series({"n_days": len(bd), "top1pct_mean_br%": 100 * bd[bd["br"] >= q[0.99]]["br"].mean(),
        "bot1pct_mean_br%": 100 * bd[bd["br"] <= q[0.01]]["br"].mean(), "share_gain_from_top1pct": bd[bd["br"] >= q[0.99]]["br"].sum() / bd["br"].sum()})
    return out
