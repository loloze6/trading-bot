def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rets = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rets += list(c[idx + H] / c[idx] - 1)
        drift[coin] = np.mean(rets)
        usual = np.std(rets)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; f = b["forecast"].fillna(0).values
            ret30 = pd.Series(c).pct_change(180).values
            ret7 = pd.Series(c).pct_change(42).values
            n = len(c)
            for g in range(0, n - H, H):
                for t in range(g, min(g + H, n - H)):
                    prev = f[t - 1] if t > 0 else 0
                    if f[t] >= 2 and prev < 2:
                        rows.append({"coin": coin, "year": pd.Timestamp(b["timestamp"].iloc[t]).year,
                                     "fc": f[t], "ret30": ret30[t], "ret7": ret7[t],
                                     "u18": c[t + 18] / c[t] - 1 - drift[coin],
                                     "s18": (c[t + 18] / c[t] - 1 - drift[coin]) / usual})
                        break
    d = pd.DataFrame(rows).dropna(subset=["ret30"])
    def agg(g):
        x = g["u18"]
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))),
                          "strength": g["s18"].mean()})
    out = {}
    d["up30"] = d["ret30"] > 0
    out["by_sign30"] = d.groupby("up30").apply(agg)
    out["by_sign30_year"] = d.groupby(["year", "up30"])["u18"].mean().unstack()
    pos = d[d["up30"]].copy()
    pos["rq"] = pd.qcut(pos["ret30"], 4, labels=False)
    out["pos_by_ret30_quart"] = pos.groupby("rq").apply(agg)
    pos["fq"] = pd.qcut(pos["fc"].rank(method="first"), 3, labels=False)
    out["pos_by_fc_third"] = pos.groupby("fq").apply(agg)
    out["pos_coins_positive_share"] = float((pos.groupby("coin")["u18"].mean() > 0).mean())
    out["pos_by_coin"] = pos.groupby("coin").apply(agg)
    d["r7q"] = pd.qcut(d["ret7"], 5, labels=False)
    out["by_7d_ret_quint"] = d.groupby("r7q").apply(agg)
    out["corr_ret30_u18_spearman"] = float(d[["ret30", "u18"]].corr(method="spearman").iloc[0, 1])
    return out
