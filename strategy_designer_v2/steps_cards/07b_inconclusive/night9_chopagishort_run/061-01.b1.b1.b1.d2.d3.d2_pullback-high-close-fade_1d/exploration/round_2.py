def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [2, 3, 5, 10]
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
            n = len(df)
            for variant in ["full", "noprior"]:
                if variant == "full":
                    sit = (r1 > 0) & (prior < 0) & (loc >= 0.75)
                else:
                    sit = (r1 > 0) & (loc >= 0.75)
                for h in H:
                    seen = set()
                    for i in range(n - h):
                        if not sit.iloc[i]:
                            continue
                        t60 = tr60.iloc[i]
                        if pd.isna(t60) or pd.isna(vmed.iloc[i]):
                            continue
                        trend = "rising" if t60 > .1 else "falling" if t60 < -.1 else "choppy"
                        ag = "agit" if vol30.iloc[i] > vmed.iloc[i] else "calm"
                        if trend != "choppy":
                            continue
                        cell = i // h
                        if (cell, ag) in seen:
                            continue
                        seen.add((cell, ag))
                        ret = cl.iloc[i + h] / cl.iloc[i] - 1
                        ex = -(ret - drift[(c, h)])
                        rows.append(dict(v=variant, coin=c, w=w, h=h, ex=ex, str=ex / usual[(c, h)], ag=ag,
                                         gain=r1.iloc[i] / mab.iloc[i] if mab.iloc[i] > 0 else np.nan,
                                         loc=loc.iloc[i], day=str(df["timestamp"].iloc[i])[:10],
                                         year=str(df["timestamp"].iloc[i])[:4]))
    R = pd.DataFrame(rows)
    def summ(g):
        d = g.groupby("day")["ex"].sum()
        t = g["ex"].mean() / (d.std(ddof=1) / np.sqrt(len(d)) * len(d) / len(g)) if len(d) > 2 else np.nan
        return pd.Series(dict(n=len(g), days=len(d), mean=g["ex"].mean(), t=t, strength=g["str"].mean(),
                              hit=(g["ex"] > 0).mean()))
    out = {}
    out["by_variant_h_ag"] = R.groupby(["v", "h", "ag"]).apply(summ)
    A5 = R[(R.v == "full") & (R.h == 5) & (R.ag == "agit")].copy()
    A5["gq"] = pd.qcut(A5["gain"], 2, labels=["small_gain", "large_gain"])
    A5["lq"] = pd.qcut(A5["loc"], 2, labels=["lower", "nearer_high"])
    out["full5_agit_by_gain"] = A5.groupby("gq").apply(summ)
    out["full5_agit_by_loc"] = A5.groupby("lq").apply(summ)
    out["full5_agit_by_year"] = A5.groupby("year").apply(summ)
    out["full5_agit_by_coin"] = A5.groupby("coin").apply(summ)
    out["full5_agit_corr_gain_ex"] = float(A5[["gain", "ex"]].corr().iloc[0, 1])
    out["full5_agit_corr_loc_ex"] = float(A5[["loc", "ex"]].corr().iloc[0, 1])
    A10 = R[(R.v == "full") & (R.h == 10) & (R.ag == "agit")].copy()
    out["full10_agit_corr_gain_ex"] = float(A10[["gain", "ex"]].corr().iloc[0, 1])
    out["full10_agit_corr_loc_ex"] = float(A10[["loc", "ex"]].corr().iloc[0, 1])
    out["full5_agit_top3_share"] = float(A5["ex"].nlargest(3).sum() / A5["ex"].sum())
    return out
