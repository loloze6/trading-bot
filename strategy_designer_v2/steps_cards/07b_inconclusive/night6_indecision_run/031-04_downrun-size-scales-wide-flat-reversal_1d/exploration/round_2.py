def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    stats_coin = {}
    for coin, wins in data["bars"].items():
        g = {H: [] for H in (1, 3, 5, 10)}
        for w, b in wins.items():
            c = b["close"].values.astype(float)
            for H in g:
                for i in range(0, len(c) - H, H):
                    g[H].append(c[i + H] / c[i] - 1)
        stats_coin[coin] = {H: (np.mean(v), np.std(v, ddof=1)) for H, v in g.items()}
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            o, h, l, c = [b[x].values.astype(float) for x in ["open", "high", "low", "close"]]
            rng = h - l
            mr = pd.Series(rng).rolling(20, min_periods=20).mean().values
            wide = rng / mr
            body = np.abs(c - o) / np.where(rng > 0, rng, np.nan)
            n = len(c)
            for t in range(5, n):
                d = {"coin": coin, "w": w, "t": t, "wide": wide[t], "body": body[t],
                     "r5z": (c[t] / c[t - 5] - 1) / stats_coin[coin][5][1],
                     "day": str(pd.Timestamp(b["timestamp"].values[t]).date())}
                for H in (1, 3, 5, 10):
                    if t + H < n:
                        d[f"ex{H}"] = (c[t + H] / c[t] - 1 - stats_coin[coin][H][0]) / stats_coin[coin][H][1]
                    else:
                        d[f"ex{H}"] = np.nan
                rows.append(d)
    df = pd.DataFrame(rows)

    def dedupe(g, H):
        keep = []
        for (coin, w), gg in g.groupby(["coin", "w"]):
            last = -10**9
            for idx, t in zip(gg.index, gg.t):
                if t - last > H:
                    keep.append(idx); last = t
        return g.loc[keep]

    def clus_t(g, ycol):
        s = g.groupby("day")[ycol].apply(lambda x: (x - g[ycol].mean()).sum())
        G = len(s); se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(g)
        return g[ycol].mean() / se, G

    wf = df[(df.wide >= 1.5) & (df.body <= 0.1)]
    for H in (1, 3, 5, 10):
        for side, m in [("down", wf.r5z < 0), ("up", wf.r5z > 0)]:
            g = dedupe(wf[m].dropna(subset=[f"ex{H}"]), H).copy()
            g["rev"] = -np.sign(g.r5z) * g[f"ex{H}"]
            t, G = clus_t(g, "rev")
            out[f"wide-flat {side}, H{H}: n, mean rev (usual moves), t, days"] = f"{len(g)}, {g.rev.mean():.3f}, {t:.2f}, {G}"
    # wide days of any body, after a down run: graded by fall
    for nm, sel in [("wide any body", df.wide >= 1.5), ("wide, body<=.33", (df.wide >= 1.5) & (df.body <= 0.33)),
                    ("wide, body>.5", (df.wide >= 1.5) & (df.body > 0.5))]:
        g = dedupe(df[sel & (df.r5z < 0)].dropna(subset=["ex5"]), 5)
        r = stats.linregress(-g.r5z, g.ex5)
        out[f"{nm}, prior down: n, mean ex5, slope on fall t"] = f"{len(g)}, {g.ex5.mean():.3f}, {r.slope:.3f} t {r.slope/r.stderr:.2f}"
    # all days non-overlapping, graded slope of ex5 on prior 5-day return
    allg = df[(df.t % 5 == 0)].dropna(subset=["ex5"])
    r = stats.linregress(allg.r5z, allg.ex5)
    out["all days grid: slope ex5 on r5z"] = f"{r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(allg)}"
    # narrow flat days, prior down, non-overlap
    nf = dedupe(df[(df.wide < 0.8) & (df.body <= 0.1) & (df.r5z < 0)].dropna(subset=["ex5"]), 5)
    out["narrow-flat prior down: n, mean ex5"] = f"{len(nf)}, {nf.ex5.mean():.3f}, t {nf.ex5.mean()/(nf.ex5.std()/np.sqrt(len(nf))):.2f}"
    return out
