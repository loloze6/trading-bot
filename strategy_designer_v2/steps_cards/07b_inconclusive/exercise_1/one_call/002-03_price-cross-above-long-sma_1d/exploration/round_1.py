def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
                "f": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "dist": b["debug_info.components.above_ma.last_history_value"].astype(float),
                "r1": c.pct_change(),
                "fwd": c.shift(-20) / c - 1,
                "past20": c / c.shift(20) - 1,
                "past60": c / c.shift(60) - 1,
                "vol20": c.pct_change().rolling(20).std(),
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    df = pd.concat(rows, ignore_index=True)
    mu = df.groupby("coin")["r1"].mean()
    df["exc"] = df["fwd"] - 20 * df["coin"].map(mu)
    df = df.dropna(subset=["fwd"])
    df["on"] = df["f"] > 0

    def summ(g):
        on = g[g.on]; off = g[~g.on]
        t = stats.ttest_1samp(on["exc"], 0).statistic if len(on) > 2 else np.nan
        return pd.Series({"n_on": len(on), "exc_on": on["exc"].mean(), "t_naive": t,
                          "hit_on": (on["exc"] > 0).mean(), "med_on": on["exc"].median(),
                          "n_off": len(off), "exc_off": off["exc"].mean()})
    out = {}
    out["all"] = summ(df).to_frame().T
    out["by_coin"] = df.groupby("coin").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    on = df[df.on].copy()
    on["fq"] = pd.qcut(on["f"], 5, labels=False, duplicates="drop")
    out["by_forecast_q"] = on.groupby("fq").agg(n=("exc", "size"), f=("f", "mean"), exc=("exc", "mean"),
                                                 med=("exc", "median"), hit=("exc", lambda x: (x > 0).mean()))
    on["dq"] = pd.qcut(on["dist"], 5, labels=False, duplicates="drop")
    out["by_dist_q"] = on.groupby("dq").agg(n=("exc", "size"), dist=("dist", "mean"), exc=("exc", "mean"),
                                             med=("exc", "median"), hit=("exc", lambda x: (x > 0).mean()))
    on["vq"] = pd.qcut(on["vol20"], 3, labels=False, duplicates="drop")
    out["by_vol_q"] = on.groupby("vq").agg(n=("exc", "size"), vol=("vol20", "mean"), exc=("exc", "mean"),
                                            med=("exc", "median"), hit=("exc", lambda x: (x > 0).mean()))
    on["p20s"] = np.sign(on["past20"])
    out["by_past20_sign"] = on.groupby("p20s").agg(n=("exc", "size"), exc=("exc", "mean"),
                                                    med=("exc", "median"), hit=("exc", lambda x: (x > 0).mean()))
    # weighted contribution per coin and std of fwd excess
    on["wexc"] = on["alloc"] * on["exc"]
    out["dispersion"] = pd.Series({"std_exc_on": on["exc"].std(), "skew_exc_on": stats.skew(on["exc"]),
                                   "share_top5pct_of_sum": on["exc"].nlargest(int(len(on)*0.05)).sum() / on["exc"].sum(),
                                   "mean_alloc_on": on["alloc"].mean()}).to_frame()
    return out
