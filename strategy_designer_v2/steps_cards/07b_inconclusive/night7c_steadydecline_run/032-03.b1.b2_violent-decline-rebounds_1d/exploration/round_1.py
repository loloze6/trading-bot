def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            rng = ((df["high"] - df["low"]) / df["close"]).values
            r28 = pd.Series(c).pct_change(28).values
            fc = df["forecast"].values
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i], fc=fc[i], reg=reg[i],
                                     r28=r28[i], ret=c[i + h] / c[i] - 1,
                                     rng5=np.nanmean(rng[max(0, i - 4):i + 1])))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    out = {}

    def summ(g):
        res = {"n": len(g), "mean_ex": g["ex"].mean(),
               "t_mean": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan}
        if len(g) > 5 and g["fc"].std() > 0:
            s = stats.linregress(g["fc"], g["ex"])
            res["slope"] = s.slope
            res["t_slope"] = s.slope / s.stderr
        return pd.Series(res)

    inr = d[d["fc"] > 0]
    out["by_horizon_inregime"] = inr.groupby("h").apply(summ)
    i5 = inr[inr["h"] == 5]
    out["by_coin_h5"] = i5.groupby("coin").apply(summ)
    out["by_window_h5"] = i5.groupby("w").apply(summ)
    out["by_year_h5"] = i5.groupby("year").apply(summ)
    i5 = i5.copy()
    i5["q"] = pd.qcut(i5["fc"], 5, labels=False, duplicates="drop")
    out["by_fc_quintile_h5"] = i5.groupby("q").agg(n=("ex", "size"), fc=("fc", "mean"),
                                                   r28=("r28", "mean"), mean_ex=("ex", "mean"))
    # calm declines: not in wide-range regime, 28d fall known and negative
    calm = d[(d["reg"] != "mean_reversion") & (d["r28"] < 0)].copy()
    calm["fc"] = -calm["r28"]
    out["calm_decline_by_h"] = calm.groupby("h").apply(summ)
    viol = d[(d["reg"] == "mean_reversion") & (d["r28"] < 0)].copy()
    viol["fc"] = -viol["r28"]
    out["violent_decline_rawfall_by_h"] = viol.groupby("h").apply(summ)
    return out
