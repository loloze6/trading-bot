def explore(data):
    import numpy as np, pandas as pd, json, ast
    out = {}
    rows = []
    sample_comp = None
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if sample_comp is None:
                sample_comp = str(b["debug_info.components"].dropna().iloc[0])[:300] if b["debug_info.components"].notna().any() else "none"
            c = b["close"]; h = b["high"]; l = b["low"]
            rng = (h - l)
            mr30 = rng.rolling(30).mean()
            low10 = l.shift(1).rolling(10).min()
            depth = ((low10 - c).clip(lower=0) / mr30)
            ret30 = c / c.shift(30) - 1
            nxt = c.shift(-1) / c - 1
            f = b["forecast"].fillna(0)
            # bets: rise >=2 from lowest since last bet
            low_since = 0.0
            for i in range(len(b)):
                fi = f.iloc[i]
                if fi - low_since >= 2 and fi > 0:
                    if not np.isnan(nxt.iloc[i]):
                        rows.append(dict(coin=coin, w=w, i=i, fc=fi, depth=depth.iloc[i],
                                         ret30=ret30.iloc[i], u=nxt.iloc[i] - mu, tot=nxt.iloc[i],
                                         wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek,
                                         yr=pd.Timestamp(b["timestamp"].iloc[i]).year,
                                         day=pd.Timestamp(b["timestamp"].iloc[i]).normalize()))
                    low_since = fi
                else:
                    low_since = min(low_since, fi)
    d = pd.DataFrame(rows)
    out["comp_sample"] = sample_comp
    def stat(g):
        s = g.groupby("day")["u"].sum()
        n = len(g); G = len(s)
        m = g["u"].mean()
        se = np.sqrt((s - g.groupby("day").size() * m).pow(2).sum() * G / (G - 1)) / n if G > 1 else np.nan
        return pd.Series(dict(n=n, days=G, mean=m, t=m / se if se else np.nan, median=g["u"].median(), hit=(g["u"] > 0).mean()))
    out["all"] = stat(d)
    out["by_coin"] = d.groupby("coin").apply(stat)
    out["by_window"] = d.groupby("w").apply(stat)
    out["by_year"] = d.groupby("yr").apply(stat)
    d["dq"] = pd.qcut(d["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["by_depth_tercile"] = d.groupby("dq").apply(stat)
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_forecast_tercile"] = d.groupby("fq").apply(stat)
    d["r30q"] = pd.qcut(d["ret30"].rank(method="first"), 3, labels=["mildfall", "mid", "deepfall"])
    out["by_fall30_tercile"] = d.groupby("r30q").apply(stat)
    out["corr_depth_u"] = float(d[["depth", "u"]].corr().iloc[0, 1])
    out["corr_fc_u"] = float(d[["fc", "u"]].corr().iloc[0, 1])
    out["depth_zero_share"] = float((d["depth"] <= 0).mean())
    return out
