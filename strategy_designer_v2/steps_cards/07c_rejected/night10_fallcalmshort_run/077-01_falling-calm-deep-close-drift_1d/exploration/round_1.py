def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float)
            r = c.pct_change()
            sd = r.rolling(20).std()
            H = h.rolling(20).max()
            depth = ((c - H) / H) / sd
            n = len(b)
            for hz in [1, 3, 5, 10]:
                fwd = c.shift(-hz) / c - 1
                for i in range(0, n, hz):
                    if np.isnan(fwd.iloc[i]) or np.isnan(depth.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, win=w, hz=hz, depth=depth.iloc[i],
                                     ret=fwd.iloc[i], regime=b["regime"].iloc[i],
                                     ppv=b.get("debug_info.components.peak_depth.post_pipeline_value", pd.Series([np.nan]*n)).iloc[i],
                                     ret20=c.iloc[i]/c.iloc[max(0,i-20)]-1, idx=i, day=str(b["timestamp"].iloc[i])[:10]))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "hz"])["ret"].mean().rename("drift")
    df = df.join(drift, on=["coin", "hz"]); df["ex"] = df["ret"] - df["drift"]
    out = {}
    out["regime_counts_hz3"] = df[df.hz == 3].groupby("regime").size()
    res = []
    for hz in [1, 3, 5, 10]:
        for reg in ["unknown", "chop"]:
            d = df[(df.hz == hz) & (df.regime == reg)].copy()
            if len(d) < 30: continue
            d["q"] = pd.qcut(d["depth"], 5, labels=False, duplicates="drop")
            g = d.groupby("q")["ex"].agg(["mean", "count"])
            sl = stats.linregress(d["depth"], d["ex"])
            res.append(dict(hz=hz, reg=reg, n=len(d), slope=sl.slope, t=sl.slope / sl.stderr,
                            q0_deep=g["mean"].iloc[0], q4_shallow=g["mean"].iloc[-1],
                            mean_ex=d["ex"].mean(), t_mean=stats.ttest_1samp(d["ex"], 0).statistic,
                            mean_tot=d["ret"].mean()))
    out["slope_by_hz_regime"] = pd.DataFrame(res)
    d3 = df[(df.hz == 3) & (df.regime == "unknown")].copy()
    d3["q"] = pd.qcut(d3["depth"], 5, labels=False)
    out["q_hz3_unknown"] = d3.groupby("q").agg(depth=("depth", "mean"), ex=("ex", "mean"), tot=("ret", "mean"), n=("ex", "size"),
                                               down=("ret", lambda x: (x < 0).mean()))
    cs = []
    for coin, d in d3.groupby("coin"):
        sl = stats.linregress(d["depth"], d["ex"])
        cs.append(dict(coin=coin, n=len(d), slope=sl.slope, t=sl.slope / sl.stderr, mean_ex=d["ex"].mean()))
    out["by_coin_hz3"] = pd.DataFrame(cs)
    d3["year"] = d3["day"].str[:4]
    ys = []
    for y, d in d3.groupby("year"):
        if len(d) < 15: continue
        sl = stats.linregress(d["depth"], d["ex"])
        ys.append(dict(year=y, n=len(d), slope=sl.slope, t=sl.slope / sl.stderr, mean_ex=d["ex"].mean()))
    out["by_year_hz3"] = pd.DataFrame(ys)
    # deepest closes (depth below -3) vs others
    d3["deep"] = d3["depth"] < d3["depth"].quantile(0.2)
    d3["short_run"] = pd.qcut(d3["ret20"], 3, labels=["fell_most", "mid", "fell_least"])
    out["deep_by_ret20"] = d3.groupby(["short_run", "deep"])["ex"].agg(["mean", "count"])
    return out
