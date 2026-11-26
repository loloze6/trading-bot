def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        grid = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 5, 5):
                grid.append(c[i + 5] / c[i] - 1)
        drift[coin] = np.mean(grid); usual[coin] = np.std(grid, ddof=1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            o, h, l, c = [b[x].values.astype(float) for x in ["open", "high", "low", "close"]]
            rng = h - l
            mr = pd.Series(rng).rolling(20, min_periods=20).mean().values
            wide = rng / mr
            body = np.abs(c - o) / np.where(rng > 0, rng, np.nan)
            n = len(c)
            for t in range(5, n):
                r5 = c[t] / c[t - 5] - 1
                d = {"coin": coin, "w": int(w[1:]), "t": t, "wide": wide[t], "body": body[t], "r5": r5,
                     "z5": r5 / usual[coin] if False else r5, "fc": b["forecast"].values[t],
                     "regime": b["regime"].values[t], "year": pd.Timestamp(b["timestamp"].values[t]).year}
                for H in (1, 3, 5, 10):
                    d[f"f{H}"] = c[t + H] / c[t] - 1 if t + H < n else np.nan
                rows.append(d)
    df = pd.DataFrame(rows)
    for coin in drift:
        m = df.coin == coin
        df.loc[m, "ex5"] = df.loc[m, "f5"] - drift[coin]
        df.loc[m, "z_r5"] = df.loc[m, "r5"] / usual[coin]
        df.loc[m, "zf5"] = df.loc[m, "ex5"] / usual[coin]
    wf = df[(df.wide >= 1.5) & (df.body <= 0.1)].copy()
    out = {}
    out["n wide-flat, regime match share"] = f"{len(wf)}, {np.mean(wf.regime=='mean_reversion'):.2f}"
    wf["side"] = np.where(wf.r5 < 0, "prior down", "prior up")
    def summ(g):
        x = g["ex5"].dropna()
        return pd.Series({"n": len(x), "mean_ex5": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_reverse": np.mean(np.sign(g.loc[x.index, "f5"]) == -np.sign(g.loc[x.index, "r5"])),
                          "mean_f1": g.f1.mean(), "mean_f3": g.f3.mean(), "mean_f10": g.f10.mean()})
    out["by side"] = wf.groupby("side").apply(summ)
    # signed reversal: excess in direction against run, by run size bucket
    wf["rev5"] = -np.sign(wf.r5) * wf.ex5
    wf["absz"] = wf.z_r5.abs()
    wf["bucket"] = pd.qcut(wf.absz, 4, labels=["q1", "q2", "q3", "q4"])
    out["reversal by |run| quartile, side"] = wf.groupby(["side", "bucket"]).agg(n=("rev5", "count"), mean_rev5=("rev5", "mean"), mean_absz=("absz", "mean"))
    # slopes
    for s in ["prior down", "prior up"]:
        g = wf[wf.side == s].dropna(subset=["ex5"])
        r = stats.linregress(g.z_r5, g.ex5)
        out[f"slope ex5 on z_r5, {s}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(g)}"
    g = wf.dropna(subset=["ex5"]); r = stats.linregress(g.z_r5, g.ex5)
    out["slope ex5 on z_r5, all"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(g)}"
    # comparison: narrow flat days and all days
    nf = df[(df.wide < 0.8) & (df.body <= 0.1)].copy()
    alld = df.dropna(subset=["ex5"])
    for nm, g in [("narrow-flat", nf.dropna(subset=["ex5"])), ("all days", alld)]:
        r = stats.linregress(g.z_r5, g.ex5)
        out[f"slope ex5 on z_r5, {nm}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(g)}"
    out["wide-flat by coin, side"] = wf.groupby(["coin", "side"]).agg(n=("rev5", "count"), mean_rev5=("rev5", "mean")).unstack()
    out["wide-flat by year"] = wf.groupby("year").agg(n=("rev5", "count"), mean_rev5=("rev5", "mean"), mean_ex5=("ex5", "mean"))
    # by width grading
    wf["wbin"] = pd.qcut(wf.wide, 3, labels=["w_lo", "w_mid", "w_hi"])
    out["reversal by width tercile"] = wf.groupby(["side", "wbin"]).agg(n=("rev5", "count"), mean_rev5=("rev5", "mean"))
    # relaxed flatness body<=0.25, wide>=1.3
    wf2 = df[(df.wide >= 1.3) & (df.body <= 0.25)].dropna(subset=["ex5"]).copy()
    wf2["rev5"] = -np.sign(wf2.r5) * wf2.ex5
    wf2["side"] = np.where(wf2.r5 < 0, "prior down", "prior up")
    out["relaxed (wide>=1.3, body<=.25) by side"] = wf2.groupby("side").agg(n=("rev5", "count"), mean_rev5=("rev5", "mean"), sd=("rev5", "std"))
    for s in ["prior down", "prior up"]:
        g = wf2[wf2.side == s]; r = stats.linregress(g.z_r5, g.ex5)
        out[f"relaxed slope, {s}"] = f"slope {r.slope:.4f} t {r.slope/r.stderr:.2f} n {len(g)}"
    return out
