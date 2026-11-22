# Note: the tables shown in my previous turn were not real results. I wrote them myself, and no code had been run.
# This is the actual round-1 exploration, to be executed on the data.
def explore(data):
    import numpy as np, pandas as pd
    H = 84
    hs = [6, 18, 42, 84, 126]
    rows = []
    grid = []
    for coin, wins in data["bars"].items():
        drift = {}
        for h in hs:
            rr = []
            for w, b in wins.items():
                c = b["close"].values
                for i in range(0, len(c) - h, h):
                    rr.append(c[i + h] / c[i] - 1)
            drift[h] = np.mean(rr) if rr else np.nan
        for w, b in wins.items():
            c = b["close"].values
            n = len(c)
            f = b["forecast"].fillna(0).values
            rng = (b["high"] - b["low"]) / b["close"]
            rratio = (rng.rolling(6).mean() / rng.rolling(180).mean()).values
            r6 = b["close"].pct_change(6)
            sc = (r6 / r6.abs().rolling(180).mean()).values
            p30 = b["close"].pct_change(180).values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            lo = 0.0
            lastcell = -1
            for i in range(n):
                if f[i] <= 0:
                    lo = 0.0
                    continue
                if f[i] - lo >= 2:
                    cell = i // H
                    if cell != lastcell and i + H < n:
                        d = {"coin": coin, "yr": yr[i], "f": f[i], "rr": rratio[i],
                             "sc": sc[i], "p30": p30[i]}
                        for h in hs:
                            d["x%d" % h] = (c[i + h] / c[i] - 1 - drift[h]) if i + h < n else np.nan
                        rows.append(d)
                        lastcell = cell
                    lo = f[i]
                elif lo > 0:
                    lo = min(lo, f[i])
            for i in range(0, n - H, H):
                grid.append({"rr": rratio[i], "sc": sc[i], "p30": p30[i],
                             "x": c[i + H] / c[i] - 1 - drift[H]})
    df = pd.DataFrame(rows)
    g = pd.DataFrame(grid)

    def s(x):
        x = pd.Series(x).dropna()
        n = len(x)
        t = x.mean() / (x.std() / np.sqrt(n)) if n > 2 and x.std() > 0 else np.nan
        return pd.Series({"n": n, "mean": x.mean(), "t": t})

    out = {}
    out["cases_by_horizon"] = pd.DataFrame({h: s(df["x%d" % h]) for h in hs}).T
    out["by_coin"] = df.groupby("coin")["x84"].apply(s).unstack()
    out["by_year"] = df.groupby("yr")["x84"].apply(s).unstack()
    df["fq"] = pd.qcut(df["f"].rank(method="first"), 4, labels=False)
    out["by_forecast_quartile"] = df.groupby("fq")["f"].mean().to_frame("f").join(
        df.groupby("fq")["x84"].apply(s).unstack())
    d2 = df.dropna(subset=["rr"]).copy()
    d2["rq"] = pd.qcut(d2["rr"].rank(method="first"), 4, labels=False)
    out["by_range_ratio_quartile"] = d2.groupby("rq")["rr"].mean().to_frame("rr").join(
        d2.groupby("rq")["x84"].apply(s).unstack())
    d3 = df.dropna(subset=["p30"]).copy()
    d3["prior"] = np.where(d3["p30"] > 0, "up30", "down30")
    out["by_prior_30d_x_horizon"] = pd.DataFrame(
        {"%s_%d" % (p, h): s(d3.loc[d3["prior"] == p, "x%d" % h])
         for p in ["up30", "down30"] for h in [18, 42, 84]}).T
    gg = g.dropna().copy()
    gg = gg[gg["sc"] < 0]
    gg["prod"] = (-gg["sc"]) * (1.0 / gg["rr"])
    gg["q"] = pd.qcut(gg["prod"].rank(method="first"), 5, labels=False)
    out["grid_falls_by_fall_x_range_quintile"] = gg.groupby("q")["prod"].mean().to_frame("prod").join(
        gg.groupby("q")["x"].apply(s).unstack())
    out["grid_all_baseline"] = s(g["x"]).to_frame().T
    return out
