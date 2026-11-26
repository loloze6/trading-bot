def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # drift per coin per horizon, non-overlapping grids
    def drift_usual(coin, H):
        r = []
        for w, b in data["bars"][coin].items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                r.append(c[i + H] / c[i] - 1)
        return np.mean(r), np.std(r, ddof=1)
    rows = []
    allbars = []
    for coin, wins in data["bars"].items():
        du = {H: drift_usual(coin, H) for H in (3, 5, 10, 20)}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; n = len(c)
            tr = (b["regime"] == "trending").values
            dep = pd.to_numeric(b.get("debug_info.components.depth.last_history_value",
                                      pd.Series(np.nan, index=b.index)), errors="coerce")
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            allbars.append(pd.DataFrame(dict(tr=tr, r1n=r1.shift(-1))))
            for i in range(n):
                if not tr[i]:
                    continue
                first = (i == 0) or (not tr[i - 1])
                # days since last break inside window
                prev = np.where(tr[:i])[0]
                gap = i - prev[-1] if len(prev) else 999
                fresh = gap > 10
                rec = dict(coin=coin, win=w, day=pd.Timestamp(b["timestamp"].iloc[i]).floor("D"),
                           first=first, fresh=fresh, depth=dep.iloc[i], r1=r1.iloc[i],
                           volr=r1.iloc[i] / vol20.iloc[i] if vol20.iloc[i] > 0 else np.nan)
                for H in (3, 5, 10, 20):
                    if i + H < n:
                        f = c.iloc[i + H] / c.iloc[i] - 1
                        rec[f"ab{H}"] = f - du[H][0]
                        rec[f"z{H}"] = (f - du[H][0]) / du[H][1]
                rows.append(rec)
    d = pd.DataFrame(rows)
    def cl(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series(dict(n=len(g)))
        m = g[col].mean()
        dev = (g[col] - m).groupby(g["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(g)
        return pd.Series(dict(n=len(g), days=g["day"].nunique(), mean=m, t=m / se if se > 0 else np.nan))
    out["break bars total"] = len(d)
    out["break bars, fresh episodes count"] = int(d.fresh.sum())
    out["all break bars by horizon (overlapping, day-clustered)"] = pd.DataFrame(
        {H: cl(d, f"ab{H}") for H in (3, 5, 10, 20)}).T
    fr = d[d.fresh]
    out["fresh breaks (no break in prior 10 days) by horizon"] = pd.DataFrame(
        {H: cl(fr, f"ab{H}") for H in (3, 5, 10, 20)}).T
    out["fresh breaks z by horizon"] = pd.DataFrame(
        {H: cl(fr, f"z{H}") for H in (3, 5, 10, 20)}).T
    # grading within fresh breaks
    x = fr.dropna(subset=["ab10"])
    for col in ["depth", "r1", "volr"]:
        y = x.dropna(subset=[col])
        if len(y) > 8:
            out[f"fresh: spearman {col} vs ab10"] = round(stats.spearmanr(y[col], y["ab10"]).correlation, 3)
            y = y.copy(); y["h"] = np.where(y[col] <= y[col].median(), "low", "high")
            out[f"fresh: ab10 by half of {col}"] = y.groupby("h").apply(lambda g: cl(g, "ab10"))
    # repeated breaks (episode continuation) vs first
    d["kind"] = np.where(d.fresh, "fresh", "repeat")
    out["ab10 fresh vs repeat"] = d.groupby("kind").apply(lambda g: cl(g, "ab10"))
    # next-day return after break bars vs other bars
    ab = pd.concat(allbars)
    out["next-day return break vs not"] = ab.groupby("tr")["r1n"].agg(["count", "mean", "std"])
    return out
