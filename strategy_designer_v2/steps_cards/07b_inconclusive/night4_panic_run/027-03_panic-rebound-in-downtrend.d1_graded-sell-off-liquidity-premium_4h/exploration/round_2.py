def explore(data):
    import numpy as np, pandas as pd
    H = 84
    hs = [18, 42, 84]
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
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for start in range(0, n - H, H):
                seg = np.arange(start, min(start + H, n - H))
                ok = seg[(~np.isnan(sc[seg])) & (~np.isnan(rratio[seg])) & (sc[seg] < 0) & (rratio[seg] > 1)]
                if len(ok) == 0:
                    continue
                score = (-sc[ok]) * rratio[ok]
                i = ok[np.argmax(score)]
                d = {"coin": coin, "yr": yr[i], "rr": rratio[i], "fall": -sc[i],
                     "score": score.max(), "p30": p30[i]}
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
    out["all_cell_worst_falls"] = pd.DataFrame({h: s(df["x%d" % h]) for h in hs}).T
    df["rq"] = pd.qcut(df["rr"].rank(method="first"), 5, labels=False)
    out["by_range_quintile_x84"] = df.groupby("rq")["rr"].mean().to_frame("rr").join(
        df.groupby("rq")["x84"].apply(s).unstack())
    out["by_range_quintile_x42"] = df.groupby("rq")["x42"].apply(s).unstack()
    df["fq"] = pd.qcut(df["fall"].rank(method="first"), 5, labels=False)
    out["by_fall_quintile_x84"] = df.groupby("fq")["fall"].mean().to_frame("fall").join(
        df.groupby("fq")["x84"].apply(s).unstack())
    df["sq"] = pd.qcut(df["score"].rank(method="first"), 5, labels=False)
    out["by_score_quintile_x84"] = df.groupby("sq")["score"].mean().to_frame("score").join(
        df.groupby("sq")["x84"].apply(s).unstack())
    top = df[df["rq"] == 4]
    out["top_range_by_year_x84"] = top.groupby("yr")["x84"].apply(s).unstack()
    out["top_range_by_coin_x84"] = top.groupby("coin")["x84"].apply(s).unstack()
    top2 = top.dropna(subset=["p30"]).copy()
    top2["prior"] = np.where(top2["p30"] > 0, "up30", "down30")
    out["top_range_by_prior"] = pd.DataFrame(
        {"%s_%d" % (p, h): s(top2.loc[top2["prior"] == p, "x%d" % h])
         for p in ["up30", "down30"] for h in hs}).T
    out["corr_score_x84_spearman"] = float(df[["score", "x84"]].corr(method="spearman").iloc[0, 1])
    out["corr_rr_x84_spearman"] = float(df[["rr", "x84"]].corr(method="spearman").iloc[0, 1])
    return out
