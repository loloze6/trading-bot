def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            dist = b["debug_info.components.above_ma.last_history_value"].astype(float)
            above = (dist > 0).astype(int)
            # bars since last cross above (within window)
            grp = (above != above.shift()).cumsum()
            since = above.groupby(grp).cumcount()
            sma = c / (1 + dist / 100.0)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "f": b["forecast"].astype(float),
                "dist": dist,
                "r1": c.pct_change(),
                "fwd": c.shift(-20) / c - 1,
                "past20": c / c.shift(20) - 1,
                "sma_slope20": sma / sma.shift(20) - 1,
                "since": np.where(above == 1, since, -1),
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    mu = df.groupby("coin")["r1"].mean()
    df["exc"] = df["fwd"] - 20 * df["coin"].map(mu)
    df = df.dropna(subset=["fwd"])
    on = df[df.f > 0].copy()

    def summ(g):
        nb = g[g.pos % 20 == 0]["exc"]
        return pd.Series({"n": len(g), "exc": g["exc"].mean(), "med": g["exc"].median(),
                          "hit": (g["exc"] > 0).mean(),
                          "n_nonov": len(nb),
                          "t_nonov": stats.ttest_1samp(nb, 0).statistic if len(nb) > 2 else np.nan,
                          "exc_trim": stats.trim_mean(g["exc"], 0.05)})
    out = {}
    out["on_all"] = summ(on).to_frame().T
    on["mom"] = np.where(on["past20"] > 0, "past20_up", "past20_dn")
    out["by_mom"] = on.groupby("mom").apply(summ)
    on["slope"] = np.where(on["sma_slope20"] > 0, "sma_up", "sma_dn")
    out["by_slope"] = on.groupby("slope").apply(summ)
    out["by_mom_slope"] = on.groupby(["mom", "slope"]).apply(summ)
    on["age"] = pd.cut(on["since"], [-1, 20, 60, 150, 10000], labels=["0-20", "21-60", "61-150", "150+"])
    out["by_age"] = on.groupby("age").apply(summ)
    on["fhi"] = np.where(on["f"] >= 10, "f>=10", "f<10")
    out["by_fhi_mom"] = on.groupby(["fhi", "mom"]).apply(summ)
    sub = on[(on.mom == "past20_up")]
    out["mom_up_by_coin"] = sub.groupby("coin").apply(summ)
    out["mom_up_by_year"] = sub.groupby("year").apply(summ)
    out["off_bars_by_mom"] = df[df.f <= 0].assign(m=lambda x: np.where(x.past20 > 0, "up", "dn")).groupby("m").apply(summ)
    return out
