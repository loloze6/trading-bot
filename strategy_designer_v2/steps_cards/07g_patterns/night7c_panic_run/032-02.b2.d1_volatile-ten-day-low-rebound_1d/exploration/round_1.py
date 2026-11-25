def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]; o = b["open"]
            rng = (h - l) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "fwd": c.shift(-1) / c - 1,
                "fwd3": c.shift(-3) / c - 1,
                "r1": c / c.shift(1) - 1,
                "r30": c / c.shift(30) - 1,
                "rng_rel": rng / rng.rolling(30).mean().shift(1),
                "clv": (c - l) / (h - l).replace(0, np.nan),
                "depth10": (l.shift(1).rolling(10).min() - c) / ((h - l).rolling(30).mean()),
                "regime": b["regime"].values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "pos": b["postRebalance_current_allocation"].fillna(0),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
            })
            df["r1z"] = df["r1"] / df["r1"].rolling(30).std().shift(1)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["fwd"].mean()
    d["u"] = d["fwd"] - d["coin"].map(drift)
    sd = d.groupby("coin")["fwd"].std()
    d["s"] = d["u"] / d["coin"].map(sd)
    d = d.dropna(subset=["u"])

    def summ(g):
        x = g["u"]; dd = g.groupby("day")["u"].sum()
        n = len(x)
        tcl = dd.mean() / (dd.std(ddof=1) / np.sqrt(len(dd))) * (len(dd) / n) if len(dd) > 2 else np.nan
        # day-clustered t of mean
        dev = g.groupby("day")["u"].apply(lambda v: (v - x.mean()).sum())
        se = np.sqrt((dev ** 2).sum() * len(dev) / max(len(dev) - 1, 1)) / n
        return pd.Series({"n": n, "days": len(dev), "mean_u%": 100 * x.mean(),
                          "strength": g["s"].mean(), "t_cl": x.mean() / se if se > 0 else np.nan})

    out = {}
    d["inreg"] = d["regime"] == "mean_reversion"
    out["by_regime"] = d.groupby("inreg").apply(summ)
    reg = d[d["inreg"]].copy()
    reg["brk"] = reg["depth10"] > 0
    out["regime_break_vs_not"] = reg.groupby("brk").apply(summ)
    b = reg[reg["brk"]].copy()
    b["dq"] = pd.qcut(b["depth10"], 3, labels=False, duplicates="drop")
    out["regime_break_depth_terciles"] = b.groupby("dq").apply(summ)
    d["r1q"] = d.groupby("coin")["r1z"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["all_by_r1z_quint"] = d.groupby("r1q").apply(summ)
    out["reg_by_r1z_quint"] = d[d["inreg"]].groupby("r1q").apply(summ)
    out["notreg_by_r1z_quint"] = d[~d["inreg"]].groupby("r1q").apply(summ)
    d["rq"] = d.groupby("coin")["rng_rel"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["all_by_range_rel_quint"] = d.groupby("rq").apply(summ)
    d["cq"] = pd.qcut(d["clv"], 5, labels=False, duplicates="drop")
    out["all_by_closeloc_quint"] = d.groupby("cq").apply(summ)
    out["reg_by_closeloc_quint"] = d[d["inreg"]].groupby("cq").apply(summ)
    out["all_by_weekday"] = d.groupby("wd").apply(summ)
    d["r30q"] = d.groupby("coin")["r30"].transform(lambda v: pd.qcut(v, 5, labels=False, duplicates="drop"))
    out["all_by_r30_quint"] = d.groupby("r30q").apply(summ)
    # break below 10-day low outside regime
    nr = d[~d["inreg"]].copy()
    out["notreg_break_vs_not"] = nr.groupby(nr["depth10"] > 0).apply(summ)
    out["by_coin_inreg_break"] = b.groupby("coin").apply(summ)
    out["by_window_inreg_break"] = b.groupby("win").apply(summ)
    return out
