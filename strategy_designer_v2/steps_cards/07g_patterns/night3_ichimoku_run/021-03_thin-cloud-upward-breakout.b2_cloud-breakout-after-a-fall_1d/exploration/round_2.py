def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            n = len(d)
            f = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(n)})
            lr = np.log(c).diff()
            f["vol20"] = lr.rolling(20).std()
            f["r1"] = c.pct_change(1)
            f["r1z"] = f["r1"] / f["vol20"].shift(1)
            f["r26"] = c.pct_change(26)
            f["r26z"] = f["r26"] / (f["vol20"] * np.sqrt(26))
            f["year"] = pd.to_datetime(d["timestamp"]).dt.year
            for h in [1, 2, 3, 10]:
                f[f"fwd{h}"] = c.shift(-h) / c - 1
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def prep(h, ft):
        g = A[A["pos"] % h == 0].dropna(subset=[f"fwd{h}", ft]).copy()
        st = g.groupby("coin")[f"fwd{h}"].agg(["mean", "std"])
        g["un"] = g[f"fwd{h}"] - g["coin"].map(st["mean"])
        g["u"] = g["un"] / g["coin"].map(st["std"])
        g["q"] = g.groupby("coin")[ft].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        return g
    # 1-day reversal: quintiles of r1z, in bps raw unusual move
    for h in [1, 2, 3]:
        g = prep(h, "r1z")
        q = g.groupby("q").agg(n=("un", "size"), un_bps=("un", lambda x: x.mean() * 1e4), u=("u", "mean"))
        out[f"rev_quintiles_h{h}"] = q.round(3)
    g = prep(1, "r1z")
    pc = []
    for coin, x in g.groupby("coin"):
        rho, p = stats.spearmanr(x["r1z"], x["u"])
        top = x[x.q == 4]["un"]; bot = x[x.q == 0]["un"]
        pc.append(dict(coin=coin, n=len(x), rho=round(rho, 3), p=round(p, 4), bot_minus_top_bps=round((bot.mean() - top.mean()) * 1e4, 1), t=round(stats.ttest_ind(bot, top, equal_var=False).statistic, 2)))
    out["rev_by_coin"] = pd.DataFrame(pc)
    py = []
    for yr, x in g.groupby("year"):
        if len(x) < 100: continue
        rho, p = stats.spearmanr(x["r1z"], x["u"])
        py.append(dict(year=yr, n=len(x), rho=round(rho, 3), p=round(p, 4)))
    out["rev_by_year"] = pd.DataFrame(py)
    # windows: early vs late halves
    g["wn"] = g["win"].str[1:].astype(int)
    hw = []
    for lab, x in [("w1-12", g[g.wn <= 12]), ("w13-24", g[g.wn > 12])]:
        rho, p = stats.spearmanr(x["r1z"], x["u"])
        hw.append(dict(half=lab, n=len(x), rho=round(rho, 3), p=round(p, 4)))
    out["rev_by_half"] = pd.DataFrame(hw)
    # sign: rises vs falls separately
    up = g[g.r1z > 0]; dn = g[g.r1z < 0]
    out["rev_side"] = pd.DataFrame([dict(side="after up day", n=len(up), rho=round(stats.spearmanr(up.r1z, up.u)[0], 3), mean_un_bps=round(up.un.mean() * 1e4, 1)),
                                    dict(side="after down day", n=len(dn), rho=round(stats.spearmanr(dn.r1z, dn.u)[0], 3), mean_un_bps=round(dn.un.mean() * 1e4, 1))])
    # 26-day momentum at 10 days, by coin and half
    g = prep(10, "r26z"); g["wn"] = g["win"].str[1:].astype(int)
    mc = []
    for coin, x in g.groupby("coin"):
        rho, p = stats.spearmanr(x["r26z"], x["u"])
        mc.append(dict(coin=coin, n=len(x), rho=round(rho, 3), p=round(p, 3)))
    for lab, x in [("w1-12", g[g.wn <= 12]), ("w13-24", g[g.wn > 12])]:
        rho, p = stats.spearmanr(x["r26z"], x["u"])
        mc.append(dict(coin=lab, n=len(x), rho=round(rho, 3), p=round(p, 3)))
    out["mom10_by_coin_half"] = pd.DataFrame(mc)
    out["mom10_quintiles"] = g.groupby("q").agg(n=("un", "size"), un_pct=("un", lambda x: x.mean() * 100)).round(2)
    out["daily_std_pct"] = A.groupby("coin")["fwd1"].std().mul(100).round(2)
    return out
