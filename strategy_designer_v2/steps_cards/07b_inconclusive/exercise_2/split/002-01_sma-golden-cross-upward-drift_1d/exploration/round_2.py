def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            raw = df["debug_info.components.sma_cross.last_history_value"].astype(float).values
            ts = pd.to_datetime(df["timestamp"])
            sgn = np.sign(np.nan_to_num(raw))
            age = np.full(len(df), np.nan)
            last = None
            for i in range(len(df)):
                if i > 0 and sgn[i] != sgn[i-1] and sgn[i] != 0:
                    last = i
                age[i] = (i - last) if last is not None else np.nan
            for k, i in enumerate(range(0, len(df) - H, H)):
                rows.append((coin, w, k, ts.iloc[i].year, f[i], raw[i], sgn[i], age[i], c[i + H] / c[i] - 1))
    b = pd.DataFrame(rows, columns=["coin", "win", "k", "year", "f", "raw", "sgn", "age", "r"])
    b["mkt"] = b.groupby(["win", "k"])["r"].transform("mean")
    b["ncoin"] = b.groupby(["win", "k"])["r"].transform("count")
    b["rel"] = b["r"] - b["mkt"]
    b["ex"] = b["r"] - b.groupby("coin")["r"].transform("mean")

    def reg(g, y):
        g = g.dropna(subset=["f", y])
        if len(g) < 8 or g["f"].std() == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g["f"], g[y])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    def summ(g, y):
        x = g[y].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "pos": (x > 0).mean()})
    out = {}
    out["slope_ex"] = reg(b, "ex")
    out["slope_rel_to_market"] = reg(b[b["ncoin"] >= 4], "rel")
    out["slope_rel_active_only"] = reg(b[(b["ncoin"] >= 4) & (b["f"] > 0)], "rel")
    # demean within window
    b["ex_w"] = b["r"] - b.groupby("win")["r"].transform("mean")
    out["slope_within_window"] = reg(b, "ex_w")
    out["fbucket_rel"] = b[b["ncoin"] >= 4].groupby(pd.cut(b["f"], [-0.01, 0, 5, 10, 15, 19.99, 20.01])).apply(lambda g: summ(g, "rel"))
    b["ageb"] = pd.cut(b["age"], [-1, 10, 30, 60, 120, 10000])
    up = b[b["sgn"] > 0]
    dn = b[b["sgn"] < 0]
    out["up_by_age_ex"] = up.groupby("ageb").apply(lambda g: summ(g, "ex"))
    out["up_by_age_rel"] = up[up["ncoin"] >= 4].groupby("ageb").apply(lambda g: summ(g, "rel"))
    out["down_by_age_ex"] = dn.groupby("ageb").apply(lambda g: summ(g, "ex"))
    out["up_vs_down_ex"] = b.groupby("sgn").apply(lambda g: summ(g, "ex"))
    out["up_vs_down_rel"] = b[b["ncoin"] >= 4].groupby("sgn").apply(lambda g: summ(g, "rel"))
    out["share_var_market"] = float(np.corrcoef(b["r"], b["mkt"])[0, 1] ** 2)
    out["rawspread_q_up_ex"] = up.groupby(pd.qcut(up["raw"], 5, duplicates="drop")).apply(lambda g: summ(g, "ex"))
    return out
