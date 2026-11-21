def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    H = [12, 24, 48, 96, 168]
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            f = df["forecast"].values.astype(float)
            r24 = np.full(n, np.nan); r24[24:] = c[24:] / c[:-24] - 1
            r720 = np.full(n, np.nan); r720[720:] = c[720:] / c[:-720] - 1
            hr = np.full(n, np.nan); hr[1:] = c[1:] / c[:-1] - 1
            vol24 = pd.Series(hr).rolling(24).std().values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for i in range(0, n, 48):
                d = {"coin": coin, "win": w, "year": yr[i], "f": f[i], "r24": r24[i], "r720": r720[i], "v24": vol24[i]}
                for h in H:
                    # grid for h only measured on 48 grid; overlap ok for h<=48; flagged
                    d["fw%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(d)
    g = pd.DataFrame(rows)
    for h in H:
        g["ex%d" % h] = g["fw%d" % h] - g.groupby("coin")["fw%d" % h].transform("mean")
    def slope_t(s, y="ex48", x="f"):
        s = s[[x, y]].dropna()
        if len(s) < 30 or s[x].std() == 0: return pd.Series({"n": len(s), "slope": np.nan, "t": np.nan})
        r = stats.linregress(s[x], s[y]); return pd.Series({"n": len(s), "slope": r.slope, "t": r.slope / r.stderr})
    out = {}
    out["by_coin"] = g.groupby("coin").apply(slope_t)
    out["by_year"] = g.groupby("year").apply(slope_t)
    out["by_horizon"] = pd.DataFrame({h: slope_t(g, y="ex%d" % h) for h in H}).T
    pos = g[g.f > 0].copy()
    pos["fq"] = pd.qcut(pos.f, 5, labels=False, duplicates="drop")
    out["pos_by_fquint"] = pos.groupby("fq").agg(n=("ex48", "size"), fmean=("f", "mean"), r24=("r24", "mean"), ex48=("ex48", "mean"), ex96=("ex96", "mean"), ex168=("ex168", "mean"))
    out["zero_vs_pos"] = g.assign(p=g.f > 0).groupby("p").agg(n=("ex48", "size"), ex48=("ex48", "mean"), ex168=("ex168", "mean"))
    # depth of fall vs grind: regress on both
    p = pos[["f", "r24", "v24", "ex48"]].dropna()
    p["r24n"] = p.r24 / p.v24
    X = np.column_stack([np.ones(len(p)), p.f, p.r24n]); y = p.ex48.values
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b
    cov = np.linalg.inv(X.T @ X) * (res @ res) / (len(y) - 3)
    out["pos_multi_f_and_depth"] = pd.DataFrame({"b": b, "t": b / np.sqrt(np.diag(cov))}, index=["c", "f", "r24/vol"])
    pos["dq"] = pd.qcut(pos.r24 / pos.v24, 3, labels=["deep", "mid", "shallow"])
    pos["fh"] = pos.f > pos.f.median()
    out["depth_x_grind_ex48"] = pos.pivot_table(index="dq", columns="fh", values="ex48", aggfunc="mean")
    out["depth_x_grind_n"] = pos.pivot_table(index="dq", columns="fh", values="ex48", aggfunc="size")
    pos["trend"] = np.where(pos.r720 > 0, "up30d", np.where(pos.r720 <= 0, "down30d", "na"))
    out["pos_by_trend"] = pos.groupby("trend").apply(slope_t)
    out["pos_by_trend_means"] = pos.groupby(["trend", "fh"])["ex48"].agg(["size", "mean"])
    return out
