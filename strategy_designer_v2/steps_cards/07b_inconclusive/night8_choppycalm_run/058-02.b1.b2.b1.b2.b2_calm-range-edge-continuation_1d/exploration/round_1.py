def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    H = [1, 3, 5, 10, 20]
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            f = df["forecast"].values
            raw = df.get("debug_info.components.range_pos.last_history_value")
            raw = raw.values if raw is not None else np.full(n, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            r60 = pd.Series(c).pct_change(60).values
            for h in H:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, f=f[i], raw=raw[i],
                                     ret=c[i + h] / c[i] - 1, r60=r60[i],
                                     day=ts.iloc[i].normalize(), year=ts.iloc[i].year,
                                     regime=df["regime"].iloc[i]))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["mu"]
    a = d[(d["f"] != 0) & d["f"].notna()].copy()
    a["s"] = np.sign(a["f"])
    a["sx"] = a["s"] * a["ex"]
    a["w_"] = a["f"].abs()

    def stat(g):
        dd = g.groupby("day").apply(lambda x: pd.Series({"num": (x.sx * x.w_).sum(), "den": x.w_.sum()}))
        m = dd.num.sum() / dd.den.sum()
        res = dd.num - m * dd.den
        k = len(dd)
        se = np.sqrt((res ** 2).sum()) / dd.den.sum() * np.sqrt(k / max(k - 1, 1))
        return pd.Series({"wmean": m, "t": m / se if se > 0 else np.nan, "n": len(g), "days": k,
                          "umean": g.sx.mean()})

    out = {}
    out["by_horizon"] = a.groupby("h").apply(stat)
    a5 = a[a.h == 5].copy()
    a5["trend"] = pd.cut(a5.r60, [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    a5["side"] = np.where(a5.s > 0, "long_top", "short_bottom")
    out["h5_by_trend"] = a5.groupby("trend").apply(stat)
    out["h5_by_side"] = a5.groupby("side").apply(stat)
    out["h5_by_trend_side"] = a5.groupby(["trend", "side"]).apply(stat)
    a5["fq"] = pd.qcut(a5.w_.rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["h5_by_absf_quartile"] = a5.groupby("fq").apply(stat)
    out["h5_by_coin"] = a5.groupby("coin").apply(stat)
    out["h5_by_window"] = a5.groupby("w").apply(stat)
    out["h5_by_year"] = a5.groupby("year").apply(stat)
    a10 = a[a.h == 10].copy()
    a10["trend"] = pd.cut(a10.r60, [-np.inf, -0.10, 0.10, np.inf], labels=["falling", "choppy", "rising"])
    out["h10_by_trend"] = a10.groupby("trend").apply(stat)
    out["regimes"] = a5.regime.value_counts()
    return out
