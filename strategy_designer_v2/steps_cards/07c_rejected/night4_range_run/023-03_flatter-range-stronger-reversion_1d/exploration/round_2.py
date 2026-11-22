def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            n = len(c)
            H = c.rolling(30).max(); L = c.rolling(30).min()
            pos = (c - L) / (H - L)
            d = 2 * pos - 1
            net = (c - c.shift(30)) / (H - L)
            flat = 1 - net.abs()
            r30 = c / c.shift(30) - 1
            vol = np.log(c).diff().rolling(30).std()
            for i in range(0, n, 10):
                rec = dict(coin=coin, w=w, year=ts[i].year, d=d[i], flat=flat[i], r30=r30[i], vol=vol[i])
                for h in (5, 10):
                    rec["r%d" % h] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    g = pd.DataFrame(rows).dropna(subset=["d", "flat", "r10"])
    for h in (5, 10):
        g["x%d" % h] = g["r%d" % h] - g.groupby("coin")["r%d" % h].transform("mean")
    g["c10"] = np.sign(g["d"]) * g["x10"]
    def tstat(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "t": s.mean() / (s.std() / np.sqrt(len(s))), "n": len(s)})
    out = {}
    out["h10_grid10_overall"] = tstat(g["c10"]).to_frame().T
    g["dq5"] = pd.qcut(g["d"], 5, labels=["far_below", "below", "mid", "above", "far_above"])
    out["x10_by_d_quintile_signed"] = g.groupby("dq5").apply(lambda x: tstat(x["x10"]))
    g["fh"] = np.where(g["flat"] > g["flat"].median(), "flatter", "less_flat")
    out["c10_by_flat_half"] = g.groupby("fh").apply(lambda x: tstat(x["c10"]))
    a = g.loc[g.fh == "flatter", "c10"]; b = g.loc[g.fh == "less_flat", "c10"]
    out["welch_flatter_minus_lessflat"] = float(stats.ttest_ind(a, b, equal_var=False)[0])
    out["c10_by_coin"] = g.groupby("coin").apply(lambda x: tstat(x["c10"]))
    out["c10_by_year"] = g.groupby("year").apply(lambda x: tstat(x["c10"]))
    wm = g.groupby(["coin", "w"])["c10"].mean()
    out["share_coin_windows_positive"] = float((wm > 0).mean())
    g["vh"] = pd.qcut(g["vol"], 3, labels=["low_vol", "mid_vol", "high_vol"])
    out["c10_by_vol"] = g.groupby("vh").apply(lambda x: tstat(x["c10"]))
    # graded: continuation per unit |d| by flatness half; regression of x10 on d and r30
    X = np.column_stack([np.ones(len(g)), g["d"], g["r30"].clip(-1, 2)])
    beta, *_ = np.linalg.lstsq(X, g["x10"].values, rcond=None)
    res = g["x10"].values - X @ beta
    s2 = res @ res / (len(g) - 3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["ols_x10_on_d_r30"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "d", "r30"])
    return out
