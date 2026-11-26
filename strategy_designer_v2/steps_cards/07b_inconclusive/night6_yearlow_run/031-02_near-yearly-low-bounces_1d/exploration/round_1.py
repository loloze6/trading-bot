def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    raw_col = "debug_info.components.low_prox.last_history_value"
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            # 60-day past return inside window
            past60 = pd.Series(c).pct_change(60).values
            past20 = pd.Series(c).pct_change(20).values
            for h in [5, 10, 20, 40, 60]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, year=yr[i],
                                     fc=df["forecast"].iloc[i], raw=df[raw_col].iloc[i] if raw_col in df else np.nan,
                                     ret=c[i + h] / c[i] - 1, p60=past60[i], p20=past20[i]))
    R = pd.DataFrame(rows)
    R["ex"] = R["ret"] - R.groupby(["coin", "h"])["ret"].transform("mean")
    out["raw range"] = R["raw"].describe()
    R["D"] = 1 / R["raw"] - 1
    def slope(g, x="fc"):
        g = g.dropna(subset=[x, "ex"])
        if len(g) < 10 or g[x].std() == 0: return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan})
        r = stats.linregress(g[x], g["ex"])
        return pd.Series({"n": len(g), "slope": r.slope, "t": r.slope / r.stderr})
    out["by horizon (fc)"] = R.groupby("h").apply(slope)
    out["by horizon (raw prox)"] = R.groupby("h").apply(lambda g: slope(g, "raw"))
    R20 = R[R.h == 20].copy()
    out["h20 by coin"] = R20.groupby("coin").apply(slope)
    out["h20 by year"] = R20.groupby("year").apply(slope)
    R20["q"] = pd.qcut(R20["raw"].rank(method="first"), 5, labels=False)
    out["h20 by raw prox quintile"] = R20.groupby("q").agg(n=("ex", "size"), D_med=("D", "median"),
                                                          ex_mean=("ex", "mean"), ex_t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))),
                                                          ret_mean=("ret", "mean"))
    R20["fq"] = pd.qcut(R20["fc"].rank(method="first"), 5, labels=False)
    out["h20 by forecast quintile"] = R20.groupby("fq").agg(n=("ex", "size"), fc_mean=("fc", "mean"), D_med=("D", "median"),
                                                            ex_mean=("ex", "mean"), ex_t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    R20["trend"] = np.where(R20["p60"] < 0, "past60 down", "past60 up")
    out["h20 by 60d trend"] = R20.groupby("trend").apply(slope)
    out["h20 by 60d trend raw"] = R20.groupby("trend").apply(lambda g: slope(g, "raw"))
    out["h20 near low (D<10%) by p20 sign"] = R20[R20.D < 0.10].groupby(R20.p20 < 0).agg(n=("ex", "size"), ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))))
    return out
