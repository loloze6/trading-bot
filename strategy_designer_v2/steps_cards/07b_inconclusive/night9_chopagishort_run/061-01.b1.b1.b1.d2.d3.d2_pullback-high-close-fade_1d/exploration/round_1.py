def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    # drift per coin per horizon, non-overlapping grid
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl) - h, h):
                    rs.append(cl[i + h] / cl[i] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]; hi = df["high"]; lo = df["low"]
            r1 = cl.pct_change()
            mab = r1.abs().rolling(20).mean()
            loc = (cl - lo) / (hi - lo)
            prior = cl.shift(1) / cl.shift(4) - 1
            tr60 = cl / cl.shift(60) - 1
            vol30 = r1.rolling(30).std()
            vmed = vol30.expanding(30).median()
            sit = (r1 > 0) & (prior < 0) & (loc >= 0.75)
            tested = (df["regime"] == "mean_reversion") & (df["forecast"] <= -2)
            n = len(df)
            for h in H:
                seen = set()
                for i in range(n - h):
                    if not sit.iloc[i]:
                        continue
                    cell = i // h
                    key = (cell,)
                    if key in seen:
                        continue
                    seen.add(key)
                    ret = cl.iloc[i + h] / cl.iloc[i] - 1
                    ex = -(ret - drift[(c, h)])
                    t60 = tr60.iloc[i]
                    trend = np.nan if pd.isna(t60) else ("rising" if t60 > .1 else "falling" if t60 < -.1 else "choppy")
                    ag = np.nan if pd.isna(vmed.iloc[i]) else ("agit" if vol30.iloc[i] > vmed.iloc[i] else "calm")
                    rows.append(dict(coin=c, w=w, h=h, ex=ex, tot=-ret, str=ex / usual[(c, h)],
                                     tested=bool(tested.iloc[i]), trend=trend, ag=ag,
                                     gain=r1.iloc[i] / mab.iloc[i] if mab.iloc[i] > 0 else np.nan,
                                     prior=prior.iloc[i] / mab.iloc[i] if mab.iloc[i] > 0 else np.nan,
                                     loc=loc.iloc[i], day=str(df["timestamp"].iloc[i])[:10],
                                     year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)
    def summ(g):
        d = g.groupby("day")["ex"].sum()
        t = g["ex"].mean() / (d.std(ddof=1) / np.sqrt(len(d)) * len(d) / len(g)) if len(d) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(d), mean=g["ex"].mean(), t=t, strength=g["str"].mean(),
                              hit=(g["ex"] > 0).mean()))
    out = {}
    T = R[R.tested]
    out["tested_by_h"] = T.groupby("h").apply(summ)
    out["all_sit_by_h_profile"] = R.dropna(subset=["trend", "ag"]).assign(p=lambda x: x.trend + "_" + x.ag).groupby(["h", "p"]).apply(summ).loc[[2, 5]]
    T5 = T[T.h == 5]
    out["tested5_by_coin"] = T5.groupby("coin").apply(summ)
    out["tested5_by_year"] = T5.groupby("year").apply(summ)
    out["tested5_by_window"] = T5.groupby("w").apply(summ)
    T5 = T5.copy()
    T5["gq"] = pd.qcut(T5["gain"], 3, labels=["small", "mid", "large"])
    T5["pq"] = pd.qcut(T5["prior"], 3, labels=["deep", "mid", "shallow"])
    T5["lq"] = pd.qcut(T5["loc"], 2, labels=["lower", "top"])
    out["tested5_by_gain"] = T5.groupby("gq").apply(summ)
    out["tested5_by_priorfall"] = T5.groupby("pq").apply(summ)
    out["tested5_by_loc"] = T5.groupby("lq").apply(summ)
    out["tested5_median_drop_share_top3"] = float(T5["ex"].nlargest(3).sum() / T5["ex"].sum())
    return out
