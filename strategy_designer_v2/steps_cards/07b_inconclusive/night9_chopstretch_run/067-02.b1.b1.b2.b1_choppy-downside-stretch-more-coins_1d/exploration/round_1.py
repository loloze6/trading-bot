def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            sma = pd.Series(c).rolling(20).mean().values
            r = pd.Series(c).pct_change()
            sd = r.rolling(20).std().values
            stretch = (c - sma) / sma / sd
            vol30 = r.rolling(30).std()
            agit = vol30.rank(pct=True).values  # crude within-window
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for h in [1, 3, 5, 10]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, yr=yr[i],
                                     day=str(df["timestamp"].iloc[i])[:10],
                                     ret=c[i + h] / c[i] - 1, fc=df["forecast"].iloc[i],
                                     reg=df["regime"].iloc[i], st=stretch[i], ag=agit[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["ret"].transform("mean")
    d["ex"] = d["ret"] - d["drift"]
    ch = d[d.reg == "unknown"].dropna(subset=["st"]).copy()
    def summ(g):
        g = g.copy()
        dd = g.groupby("day")["sx"].sum()
        m = g["sx"].mean()
        D = len(dd)
        se = np.sqrt((dd - m * g.groupby("day").size()).pow(2).sum()) / len(g) if len(g) > 1 else np.nan
        return pd.Series(dict(n=len(g), days=D, mean=m, t=m / se if se else np.nan))
    out = {}
    # short side below average
    below = ch[ch.st < 0].copy(); below["sx"] = -below["ex"]
    above = ch[ch.st > 0].copy(); above["sx"] = above["ex"]
    out["below_by_h"] = below.groupby("h").apply(summ)
    out["above_by_h_long"] = above.groupby("h").apply(summ)
    b5 = below[below.h == 5].copy()
    b5["q"] = pd.qcut(b5["st"], 5, labels=["q1_far", "q2", "q3", "q4", "q5_near"])
    out["below5_by_stretch_q"] = b5.groupby("q").apply(summ)
    a5 = above[above.h == 5].copy()
    a5["q"] = pd.qcut(a5["st"], 5, labels=["q1_near", "q2", "q3", "q4", "q5_far"])
    out["above5_by_stretch_q"] = a5.groupby("q").apply(summ)
    out["below5_by_coin"] = b5.groupby("coin").apply(summ)
    out["below5_by_window"] = b5.groupby("w").apply(summ)
    out["below5_by_year"] = b5.groupby("yr").apply(summ)
    b5["agi"] = np.where(b5.ag > 0.5, "agit", "calm")
    out["below5_by_agit"] = b5.groupby("agi").apply(summ)
    b10 = below[below.h == 10].copy()
    b10["q"] = pd.qcut(b10["st"], 5, labels=["q1_far", "q2", "q3", "q4", "q5_near"])
    out["below10_by_stretch_q"] = b10.groupby("q").apply(summ)
    return out
