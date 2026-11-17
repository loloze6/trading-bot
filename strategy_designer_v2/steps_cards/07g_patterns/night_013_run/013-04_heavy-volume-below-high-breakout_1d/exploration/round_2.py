def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            ts = pd.to_datetime(b["timestamp"])
            f = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "year": ts.dt.year.values,
                "wd": ts.dt.dayofweek.values,
                "vr": v.rolling(5).mean() / v.rolling(30, min_periods=30).mean(),
                "vr10": v.rolling(10).mean() / v.rolling(30, min_periods=30).mean(),
                "ret5p": c / c.shift(5) - 1,
                "dist30": c / b["high"].astype(float).rolling(30, min_periods=30).max() - 1,
                "fwd1": c.shift(-1) / c - 1,
                "fwd5": c.shift(-5) / c - 1,
                "fwd10": c.shift(-10) / c - 1,
            })
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    for h in [1, 5, 10]:
        m = A[A.pos % h == 0].groupby("coin")[f"fwd{h}"].mean()
        A[f"x{h}"] = A[f"fwd{h}"] - A["coin"].map(m)
    def qtab(feat, h, by=None):
        d = A[A.pos % h == 0].dropna(subset=[feat, f"x{h}"]).copy()
        d["q"] = d.groupby("coin")[feat].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        if by is None:
            g = d.groupby("q")[f"x{h}"].agg(["mean", "count", "std"])
            g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
            return g.drop(columns="std").round(5)
        res = {}
        for k, dd in d.groupby(by):
            top = dd[dd.q == 4][f"x{h}"]; bot = dd[dd.q == 0][f"x{h}"]
            sp = stats.spearmanr(dd[feat], dd[f"x{h}"]).correlation
            res[k] = {"top": top.mean(), "bot": bot.mean(), "top-bot": top.mean() - bot.mean(),
                      "t": stats.ttest_ind(top, bot, equal_var=False).statistic, "spear": sp, "n": len(dd)}
        return pd.DataFrame(res).T.round(4)
    out["vr_x5_by_coin"] = qtab("vr", 5, "coin")
    out["vr_x5_by_year"] = qtab("vr", 5, "year")
    out["vr_x10"] = qtab("vr", 10)
    out["vr10_x10"] = qtab("vr10", 10)
    out["vr_x1"] = qtab("vr", 1)
    out["dist30_x10_by_coin"] = qtab("dist30", 10, "coin")
    # vr conditional on sign of 5d return
    d = A[A.pos % 5 == 0].dropna(subset=["vr", "x5", "ret5p"]).copy()
    d["q"] = d.groupby("coin")["vr"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    d["up"] = np.where(d.ret5p > 0, "up", "down")
    g = d.groupby(["up", "q"])["x5"].agg(["mean", "count", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["vr_x5_by_ret5sign"] = g.drop(columns="std").round(5)
    # weekday by coin and by year
    d = A.dropna(subset=["x1"])
    out["wd_by_coin"] = d.groupby(["coin", "wd"])["x1"].mean().unstack().round(4)
    out["wd_by_year"] = d.groupby(["year", "wd"])["x1"].mean().unstack().round(4)
    return out
