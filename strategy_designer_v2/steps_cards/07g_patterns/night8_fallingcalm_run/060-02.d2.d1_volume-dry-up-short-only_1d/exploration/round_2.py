def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vm = v.rolling(30).mean()
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                               "yr": pd.to_datetime(b["timestamp"]).dt.year,
                               "ret60": c / c.shift(60) - 1, "ret10": c / c.shift(10) - 1,
                               "vr": np.log(vm / vm.shift(30)), "r1": r1,
                               "sd30": r1.rolling(30).std(),
                               "fwd": c.shift(-H) / c - 1, "fwd1": c.shift(-1) / c - 1,
                               "fwd2": c.shift(-2) / c - 1,
                               "rng": (b["high"] - b["low"]) / c,
                               "clpos": (c - b["low"]) / (b["high"] - b["low"])})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["agit"] = d.groupby("coin")["sd30"].transform(lambda s: s > s.median()).map({True: "agitated", False: "calm"})
    d.loc[d.sd30.isna(), "agit"] = np.nan
    d["trend"] = np.where(d.ret60 > 0.10, "rising", np.where(d.ret60 < -0.10, "falling", "choppy"))
    d.loc[d.ret60.isna(), "trend"] = np.nan
    for col in ["fwd", "fwd1", "fwd2"]:
        step = 5 if col == "fwd" else (2 if col == "fwd2" else 1)
        dr = d.loc[(d.pos % step == 0), col].groupby(d["coin"]).mean()
        d["u" + col] = d[col] - d["coin"].map(dr)

    def ct(x, col):
        x = x[[col, "day"]].dropna()
        if len(x) < 5: return pd.Series({"n": len(x), "days": 0, "mean": np.nan, "t_day": np.nan})
        m = x[col].mean(); s = (x[col] - m).groupby(x["day"]).sum(); G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t_day": m / se})

    out = {}
    one = d[d.fwd1.notna() & d.trend.notna() & d.agit.notna()].copy()
    one["cq"] = pd.cut(one.clpos, [-0.01, 0.1, 0.2, 0.4, 0.6, 1.01])
    out["1d: trend x agit x close position"] = one.groupby(["trend", "agit", "cq"]).apply(lambda x: ct(x, "ufwd1")).round(4)
    two = one[one.pos % 2 == 0]
    fl = two[two.trend == "falling"].copy()
    fl["cq"] = pd.cut(fl.clpos, [-0.01, 0.2, 0.4, 1.01])
    out["2d falling: agit x close pos"] = fl.groupby(["agit", "cq"]).apply(lambda x: ct(x, "ufwd2")).round(4)
    flo = one[(one.trend == "falling") & (one.clpos <= 0.2)]
    out["1d falling low close by year"] = flo.groupby("yr").apply(lambda x: ct(x, "ufwd1")).round(4)
    flo2 = flo.copy(); flo2["rq"] = pd.qcut(flo2.rng / flo2.sd30, 3, labels=False)
    out["1d falling low close by range/swing tercile x agit"] = flo2.groupby(["agit", "rq"]).apply(lambda x: ct(x, "ufwd1")).round(4)
    out["1d falling low close by window"] = flo.groupby("w").apply(lambda x: ct(x, "ufwd1")).round(4)
    # 5d grid: falling, agit x vr sign, and ret10 sign
    g = d[(d.pos % H == 0) & d.fwd.notna() & d.trend.notna() & d.agit.notna() & d.vr.notna()]
    gf = g[g.trend == "falling"]
    out["5d falling: agit x vr<0 x ret10<0"] = gf.groupby(["agit", gf.vr < 0, gf.ret10 < 0]).apply(lambda x: ct(x, "ufwd")).round(4)
    gr = g[g.trend == "rising"].copy()
    gr["vq"] = pd.qcut(gr.vr, 3, labels=False)
    out["5d rising: agit x vr tercile"] = gr.groupby(["agit", "vq"]).apply(lambda x: ct(x, "ufwd")).round(4)
    # falling: up days followed
    fu = one[one.trend == "falling"].copy()
    fu["z"] = fu.r1 / fu.sd30
    fu["zq"] = pd.cut(fu.z, [-99, -1, 0, 1, 2, 99])
    out["1d falling: agit x today z"] = fu.groupby(["agit", "zq"]).apply(lambda x: ct(x, "ufwd1")).round(4)
    return out
