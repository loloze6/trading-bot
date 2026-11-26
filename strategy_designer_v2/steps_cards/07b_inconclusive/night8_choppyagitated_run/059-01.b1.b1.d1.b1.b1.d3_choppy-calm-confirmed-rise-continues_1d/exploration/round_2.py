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
            c = df["close"].values.astype(float)
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            lr = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd30 = pd.Series(lr).rolling(30, min_periods=20).std().values
            reg = df["regime"].astype(str).values
            sr = df.get("debug_info.components.signal_rise.last_history_value")
            for i in range(0, n - 7, 7):
                allret.append(c[i + 7] / c[i] - 1)
            for i in range(0, n - 7, 7):
                r = c[i + 7] / c[i] - 1
                if reg[i] == "trending":
                    recs.append(dict(kind="tested_t", coin=coin, window=w, year=yr[i], r=r,
                                     sig=sr.iloc[i] if sr is not None else np.nan))
                # signal measured now (lag 0), profile read at the bar 7 days later (approx)
                if i >= 7 and i + 7 < n and reg[i + 7] == "trending" and not np.isnan(sd30[i]):
                    s0 = (c[i] / c[i - 7] - 1) / (sd30[i] * np.sqrt(7))
                    if s0 > 0:
                        recs.append(dict(kind="first_week_from_signal", coin=coin, window=w, year=yr[i], r=r, sig=s0))
        mu = np.mean(allret)
        for d in recs:
            d["ex"] = d["r"] - mu
        rows += recs
    d = pd.DataFrame(rows).dropna(subset=["sig"])
    out = {}
    def summ(g):
        res = {"n": len(g), "mean_ex": g["ex"].mean(),
               "t_ex": g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan}
        if len(g) > 5 and g["sig"].std() > 0:
            s = stats.linregress(g["sig"], g["ex"])
            res["slope"] = s.slope; res["slope_t"] = s.slope / s.stderr
        return pd.Series(res)
    out["by_kind"] = d.groupby("kind").apply(summ)
    for k in ["tested_t", "first_week_from_signal"]:
        dk = d[d.kind == k].copy()
        dk["q"] = pd.qcut(dk["sig"], 3, labels=False, duplicates="drop")
        out[k + "_by_signal_tercile"] = dk.groupby("q").apply(summ).join(dk.groupby("q")["sig"].mean().rename("sig_mean"))
        out[k + "_by_year"] = dk.groupby("year").apply(summ)
        top = dk[dk["q"] == dk["q"].max()]
        out[k + "_top_tercile_by_year"] = top.groupby("year").apply(summ)
    return out
