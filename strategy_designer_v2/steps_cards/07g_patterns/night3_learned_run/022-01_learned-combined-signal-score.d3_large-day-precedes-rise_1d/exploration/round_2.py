def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sc = r1.abs().rolling(60, min_periods=20).mean().shift(1)
            z = r1 / sc
            r3 = c / c.shift(3) - 1
            sd60 = r1.rolling(60, min_periods=20).std().shift(1)
            z3 = r3 / (sd60 * np.sqrt(3))
            vol60 = r1.rolling(60, min_periods=40).std()
            near = (c / c.rolling(60, min_periods=40).max() - 1) / (vol60 * np.sqrt(20))
            n = len(b)
            wnum = int(w[1:])
            for h in (1, 5, 10):
                fwd = c.shift(-h) / c - 1
                fwd_skip = c.shift(-h) / c.shift(-1) - 1
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, win=wnum, h=h, z=z[i], z3=z3[i], near=near[i],
                                     fwd=fwd[i], fskip=fwd_skip[i], sd=sd60[i]))
    df = pd.DataFrame(rows)
    df["drift"] = df.groupby(["coin", "h"])["fwd"].transform("mean")
    df["ex"] = df["fwd"] - df["drift"]
    df["half"] = np.where(df["win"] <= 12, "w1-12", "w13-24")
    # graded within up days: positive z only, terciles of z
    res = []
    for h in (1, 5, 10):
        d = df[(df.h == h) & (df.z > 0)].dropna(subset=["z", "ex"])
        q = d["z"].rank(pct=True)
        top, bot = d[q > 2/3]["ex"], d[q <= 1/3]["ex"]
        res.append(dict(h=h, n=len(d), top=top.mean(), bot=bot.mean(), diff=top.mean()-bot.mean(),
                        t=stats.ttest_ind(top, bot, equal_var=False).statistic,
                        rho=stats.spearmanr(d["z"], d["ex"]).correlation))
        d = df[(df.h == h) & (df.z < 0)].dropna(subset=["z", "ex"])
        q = (-d["z"]).rank(pct=True)
        top, bot = d[q > 2/3]["ex"], d[q <= 1/3]["ex"]
        res.append(dict(h=-h, n=len(d), top=top.mean(), bot=bot.mean(), diff=top.mean()-bot.mean(),
                        t=stats.ttest_ind(top, bot, equal_var=False).statistic,
                        rho=stats.spearmanr(-d["z"], d["ex"]).correlation))
    out["graded_within_side (h<0 = down days, by size)"] = pd.DataFrame(res).round(4)
    # signed z top-bot quintile per half and per coin at h5
    d5 = df[df.h == 5].dropna(subset=["z", "ex"]).copy()
    d5["q"] = d5.groupby("coin")["z"].transform(lambda s: pd.qcut(s, 5, labels=False))
    def tb(g):
        top, bot = g[g.q == 4]["ex"], g[g.q == 0]["ex"]
        return pd.Series(dict(n=len(g), top=top.mean(), bot=bot.mean(), diff=top.mean()-bot.mean(),
                              t=stats.ttest_ind(top, bot, equal_var=False).statistic,
                              rho=stats.spearmanr(g["z"], g["ex"]).correlation,
                              top_unusual_over_sd5=(top / (g.loc[top.index, "sd"] * np.sqrt(5))).mean()))
    out["signed_z_h5_by_half"] = d5.groupby("half").apply(tb).round(4)
    out["signed_z_h5_by_coin"] = d5.groupby("coin").apply(tb).round(4)
    # skip-first-day forward return after top-quintile z
    d5["exs"] = d5["fskip"] - d5.groupby("coin")["fskip"].transform("mean")
    g = d5.groupby("q")[["ex", "exs"]].mean(); g["n"] = d5.groupby("q").size()
    out["h5_vs_days2to5_by_zquint"] = g.round(4)
    # 3-day signed return z, 5 day horizon
    d = df[df.h == 5].dropna(subset=["z3", "ex"])
    q = d["z3"].rank(pct=True)
    top, bot = d[q > 2/3]["ex"], d[q <= 1/3]["ex"]
    out["z3_h5"] = pd.Series(dict(n=len(d), top=top.mean(), bot=bot.mean(), t=stats.ttest_ind(top, bot, equal_var=False).statistic,
                                  rho=stats.spearmanr(d["z3"], d["ex"]).correlation)).round(4)
    # h1 reversal size per case
    d1 = df[df.h == 1].dropna(subset=["z", "ex"])
    out["h1_rho_z"] = float(stats.spearmanr(d1["z"], d1["ex"]).correlation)
    q = d1["z"].rank(pct=True)
    out["h1_top_quint_ex"] = float(d1[q > 0.8]["ex"].mean()); out["h1_bot_quint_ex"] = float(d1[q <= 0.2]["ex"].mean())
    out["h1_by_half"] = d1.groupby("half").apply(lambda g: pd.Series(dict(rho=stats.spearmanr(g.z, g.ex).correlation, n=len(g)))).round(4)
    return out
