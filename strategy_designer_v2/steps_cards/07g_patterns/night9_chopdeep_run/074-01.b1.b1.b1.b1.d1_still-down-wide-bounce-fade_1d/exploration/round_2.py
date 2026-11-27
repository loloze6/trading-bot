def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l)
            r1 = c / c.shift(1) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "ret1": r1,
                "ret5": c / c.shift(5) - 1,
                "trend60": c / c.shift(60) - 1,
                "wide": rng / rng.rolling(20).mean(),
                "loc": (c - l) / rng.replace(0, np.nan),
                "z": r1 / r1.rolling(20).std().shift(1),
                "vol30": r1.rolling(30).std(),
                "nxt": c.shift(-1) / c - 1,
                "n2": c.shift(-2) / c.shift(-1) - 1,
                "n3": c.shift(-3) / c.shift(-2) - 1,
                "alloc": b["postRebalance_current_allocation"],
                "pos": np.arange(len(b)),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    for k in ["nxt", "n2", "n3"]:
        d["u_" + k] = d[k] - d["coin"].map(d.groupby("coin")["nxt"].mean())
    d["trend"] = np.where(d["trend60"] < -0.10, "falling", np.where(d["trend60"] > 0.10, "rising", "choppy"))
    d.loc[d["trend60"].isna(), "trend"] = np.nan
    med = d.groupby("coin")["vol30"].transform("median")
    d["agit"] = np.where(d["vol30"] > med, "agit", "calm")
    d.loc[d["vol30"].isna(), "agit"] = np.nan

    def summ(g, col="u_nxt"):
        g = g.dropna(subset=[col])
        n = len(g)
        if n == 0:
            return pd.Series({"n": 0, "days": 0, "mean%": np.nan, "t": np.nan})
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / n
        return pd.Series({"n": n, "days": len(dev), "mean%": m * 100, "t": m / se if se > 0 else np.nan})

    out = {}
    up = d[(d.ret1 > 0)].dropna(subset=["trend", "agit"])
    # choppy up days by agitation and z
    up["zb"] = pd.cut(up["z"], [0, 1, 2, 3, 99])
    out["up_by_trend_agit_z"] = up.groupby(["trend", "agit", "zb"], observed=True).apply(summ).round(3)
    # falling wide up: later days
    fw = d[(d.trend == "falling") & (d.ret1 > 0) & (d.wide >= 1.5)]
    out["fall_wideup_next_days"] = pd.DataFrame({k: summ(fw, "u_" + k) for k in ["nxt", "n2", "n3"]}).T.round(3)
    # graded: spearman in falling up days and rising up days
    res = {}
    for tr in ["falling", "choppy", "rising"]:
        g = d[(d.trend == tr) & (d.ret1 > 0)].dropna(subset=["u_nxt", "wide", "z", "loc", "ret5"])
        for v in ["wide", "z", "loc", "ret5"]:
            r, p = stats.spearmanr(g[v], g["u_nxt"])
            res[(tr, v)] = {"n": len(g), "rho": round(r, 4), "p": round(p, 4)}
    out["spearman_up_days"] = pd.DataFrame(res).T
    # falling up days high close by loc and agitation
    fu = d[(d.trend == "falling") & (d.ret1 > 0)].dropna(subset=["agit"])
    fu["lb"] = pd.cut(fu["loc"], [-0.01, 0.5, 0.75, 0.9, 1.01])
    out["fall_up_by_agit_loc"] = fu.groupby(["agit", "lb"], observed=True).apply(summ).round(3)
    # all days by trend x agit
    out["all_trend_agit"] = d.dropna(subset=["trend", "agit"]).groupby(["trend", "agit"]).apply(summ).round(3)
    # book days: largest gains/losses context
    bd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bd.append(x.assign(coin=coin))
    bd = pd.concat(bd)
    bd = bd[bd["book_return"].abs() > 1e-9]
    out["book_active_days"] = pd.Series({"n": len(bd), "mean%": bd.book_return.mean() * 100,
                                         "win_share": (bd.book_return > 0).mean(),
                                         "top5_share_of_sum": bd.book_return.nlargest(5).sum() / bd.book_return.sum()})
    return out
