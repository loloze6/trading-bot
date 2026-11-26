def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]
    rows = []
    drift = {}
    for H in [1, 3, 5, 10]:
        for coin, wins in bars.items():
            allr = []
            for w, df in wins.items():
                df = df.reset_index(drop=True)
                c = df["close"].values
                o = df["open"].values; hi = df["high"].values; lo = df["low"].values
                n = len(df)
                rng = pd.Series(hi - lo)
                rm = (rng / rng.rolling(20, min_periods=20).mean()).values
                r5 = pd.Series(c).pct_change(5).values
                body = (c - o) / np.where(hi - lo > 0, hi - lo, np.nan)
                ts = pd.to_datetime(df["timestamp"])
                for t in range(0, n - H, H):
                    fr = c[t + H] / c[t] - 1
                    allr.append(fr)
                    f = df["forecast"].iloc[t]
                    if f > 0:
                        rows.append(dict(H=H, coin=coin, win=w, year=ts.iloc[t].year, day=ts.iloc[t].normalize(),
                                         f=f, fr=fr, r5=r5[t], rm=rm[t], body=body[t]))
            drift[(coin, H)] = np.mean(allr)
    d = pd.DataFrame(rows)
    d["u"] = d["fr"] - d.apply(lambda r: drift[(r.coin, r.H)], axis=1)

    def tstat(g):
        s = g.groupby("day")["u"].sum()
        nd = len(s); m = g["u"].mean()
        se = s.std(ddof=1) * np.sqrt(nd) / len(g) if nd > 1 else np.nan
        return pd.Series({"n": len(g), "days": nd, "mean_u": m, "t": m / se if se else np.nan})

    out = {}
    out["by_horizon"] = d.groupby("H").apply(tstat)
    d3 = d[d.H == 3].copy()
    out["H3_by_coin"] = d3.groupby("coin").apply(tstat)
    out["H3_by_year"] = d3.groupby("year").apply(tstat)
    d3["fq"] = pd.qcut(d3["f"], 4, labels=False, duplicates="drop")
    out["H3_by_forecast_q"] = d3.groupby("fq").apply(tstat)
    d3["rmq"] = pd.qcut(d3["rm"], 4, labels=False, duplicates="drop")
    out["H3_by_rangemult_q"] = d3.groupby("rmq").apply(tstat)
    d3["r5q"] = pd.qcut(d3["r5"], 4, labels=False, duplicates="drop")
    out["H3_by_rise_q"] = d3.groupby("r5q").apply(tstat)
    d3["bq"] = pd.cut(d3["body"], [-1.01, -0.33, 0.33, 1.01], labels=["close_low", "flat", "close_high"])
    out["H3_by_body"] = d3.groupby("bq").apply(tstat)
    d10 = d[d.H == 10].copy()
    d10["fq"] = pd.qcut(d10["f"], 4, labels=False, duplicates="drop")
    out["H10_by_forecast_q"] = d10.groupby("fq").apply(tstat)
    d10["rmq"] = pd.qcut(d10["rm"], 4, labels=False, duplicates="drop")
    out["H10_by_rangemult_q"] = d10.groupby("rmq").apply(tstat)
    out["H10_by_coin"] = d10.groupby("coin").apply(tstat)
    return out
