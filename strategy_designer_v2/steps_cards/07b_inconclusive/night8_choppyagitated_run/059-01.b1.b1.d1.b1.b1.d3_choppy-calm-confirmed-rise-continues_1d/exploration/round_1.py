def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        allret = []
        recs = []
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            sr = df.get("debug_info.components.signal_rise.last_history_value")
            fw = df.get("debug_info.components.first_week.last_history_value")
            for i in range(0, n - 7, 7):
                r = c[i + 7] / c[i] - 1
                allret.append(r)
                f = df["forecast"].iloc[i]
                if pd.notna(f) and f > 0:
                    recs.append(dict(coin=coin, window=w, year=yr[i], fc=f, r=r,
                                     sr=(sr.iloc[i] if sr is not None else np.nan),
                                     fw=(fw.iloc[i] if fw is not None else np.nan),
                                     r1=c[i + 1] / c[i] - 1 if i + 1 < n else np.nan,
                                     r3=c[min(i + 3, n - 1)] / c[i] - 1,
                                     r14=(c[i + 14] / c[i] - 1) if i + 14 < n else np.nan))
        mu = np.mean(allret) if allret else np.nan
        for d in recs:
            d["ex"] = d["r"] - mu
            d["mu"] = mu
        rows += recs
    d = pd.DataFrame(rows)
    out = {}
    def summ(g):
        return pd.Series({"n": len(g), "mean_ex": g["ex"].mean(), "mean_r": g["r"].mean(),
                          "t_ex": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    d["fq"] = pd.qcut(d["fc"], 5, labels=False, duplicates="drop")
    out["by_forecast_quintile"] = d.groupby("fq").apply(summ).join(d.groupby("fq")["fc"].mean().rename("fc_mean"))
    d["fw_pos"] = d["fw"] > 0
    out["by_firstweek_positive"] = d.groupby("fw_pos").apply(summ)
    d["srq"] = pd.qcut(d["sr"], 3, labels=False, duplicates="drop")
    out["by_signal_tercile"] = d.groupby("srq").apply(summ)
    d["fwq"] = pd.qcut(d["fw"], 3, labels=False, duplicates="drop")
    out["by_firstweek_tercile"] = d.groupby("fwq").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("window").apply(summ)
    s = stats.linregress(d["fc"], d["ex"])
    out["slope_all"] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(d), "intercept": s.intercept})
    for col in ["sr", "fw"]:
        dd = d.dropna(subset=[col])
        s = stats.linregress(dd[col], dd["ex"])
        out["slope_on_" + col] = pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(dd)})
    dd = d.dropna(subset=["r14"])
    out["longer_horizon_r14_by_fq"] = dd.groupby("fq")["r14"].agg(["count", "mean"])
    out["mu_mean"] = d["mu"].mean()
    return out
