def explore(data):
    import numpy as np, pandas as pd
    H = 84
    hs = [6, 18, 42, 84]
    rows = []
    for coin, wins in data["bars"].items():
        drift = {}
        for h in hs:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            drift[h] = np.mean(rr)
        for w, b in wins.items():
            c = b["close"].values
            n = len(c)
            rng = (b["high"] - b["low"]) / b["close"]
            rratio = (rng.rolling(6).mean() / rng.rolling(180).mean()).values
            r6 = b["close"].pct_change(6)
            sc = (r6 / r6.abs().rolling(180).mean()).values
            p30 = b["close"].pct_change(180).values
            p90 = b["close"].pct_change(540).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for start in range(0, n - H, H):
                seg = np.arange(start, min(start + H, n - H))
                ok = seg[(~np.isnan(sc[seg])) & (~np.isnan(rratio[seg])) & (sc[seg] < -1.5) & (rratio[seg] > 1)]
                if len(ok) == 0:
                    continue
                i = ok[0]  # first qualifying bar: causal, no look-ahead
                d = {"coin": coin, "yr": yr[i], "rr": rratio[i], "fall": -sc[i],
                     "score": -sc[i] * rratio[i], "p30": p30[i], "p90": p90[i]}
                for h in hs:
                    d["x%d" % h] = c[i + h] / c[i] - 1 - drift[h]
                rows.append(d)
    df = pd.DataFrame(rows)

    def s(x):
        x = pd.Series(x).dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 and x.std() > 0 else np.nan
        return pd.Series({"n": n, "mean": x.mean(), "t": t})

    out = {}
    out["first_fall_causal_by_horizon"] = pd.DataFrame({h: s(df["x%d" % h]) for h in hs}).T
    df["sq"] = pd.qcut(df["score"].rank(method="first"), 4, labels=False)
    out["causal_by_score_quartile_x84"] = df.groupby("sq")["score"].mean().to_frame("score").join(
        df.groupby("sq")["x84"].apply(s).unstack())
    out["causal_by_score_quartile_x18"] = df.groupby("sq")["x18"].apply(s).unstack()
    d3 = df.dropna(subset=["p90"]).copy()
    d3["prior90"] = np.where(d3["p90"] > 0, "up90", "down90")
    out["causal_by_prior90"] = pd.DataFrame(
        {"%s_%d" % (p, h): s(d3.loc[d3["prior90"] == p, "x%d" % h])
         for p in ["up90", "down90"] for h in [18, 42, 84]}).T
    d4 = df.dropna(subset=["p30"]).copy()
    d4["prior30"] = np.where(d4["p30"] > 0, "up30", "down30")
    out["causal_by_prior30"] = pd.DataFrame(
        {"%s_%d" % (p, h): s(d4.loc[d4["prior30"] == p, "x%d" % h])
         for p in ["up30", "down30"] for h in [18, 42, 84]}).T
    out["causal_by_year_x84"] = df.groupby("yr")["x84"].apply(s).unstack()
    up = d3[d3["prior90"] == "up90"].copy()
    if len(up) > 20:
        up["sq"] = pd.qcut(up["score"].rank(method="first"), 3, labels=False)
        out["up90_by_score_tercile_x84"] = up.groupby("sq")["score"].mean().to_frame("score").join(
            up.groupby("sq")["x84"].apply(s).unstack())
    out["spearman_score_x84"] = float(df[["score", "x84"]].corr(method="spearman").iloc[0, 1])
    return out
