def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 72
    drift = {}; usd = {}
    for coin, ws in bars.items():
        rr = []
        for w, b in ws.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                rr.append(c[i + H] / c[i] - 1)
        rr = np.array(rr); drift[coin] = rr.mean(); usd[coin] = rr.std()
    G = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; hi = b["high"]; lo = b["low"]; n = len(b)
            ph = hi.shift(1).rolling(12).max(); pl = lo.shift(1).rolling(12).min()
            up = (c > ph).values; dn = (c < pl).values
            r180 = (c / c.shift(180) - 1).values
            r90 = (c / c.shift(90) - 1).values
            r360 = (c / c.shift(360) - 1).values
            lv = np.log(c).diff()
            vol = lv.rolling(180, min_periods=60).std().values
            z180 = np.log(c / c.shift(180)).values / (vol * np.sqrt(180))
            cv = c.values
            f72 = np.full(n, np.nan); f72[:n - H] = cv[H:] / cv[:n - H] - 1
            f144 = np.full(n, np.nan); f144[:n - 144] = cv[144:] / cv[:n - 144] - 1
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            for i in range(0, n - H, H):
                G.append(dict(coin=coin, w=w, yr=yr[i], r180=r180[i], r90=r90[i], r360=r360[i], z=z180[i],
                              up=up[i], dn=dn[i], tot=f72[i], u72=f72[i] - drift[coin],
                              u144=f144[i] - 2 * drift[coin], s72=(f72[i] - drift[coin]) / usd[coin]))
    G = pd.DataFrame(G)
    def agg(df, col="u72"):
        x = df[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(len(x))),
                              tot=df["tot"].mean(), strength=df["s72"].mean()))
    out = {}
    g = G.dropna(subset=["z", "u72"]).copy()
    g["qz"] = pd.qcut(g.z, 10, labels=False)
    out["grid_by_z_decile"] = g.groupby("qz").apply(agg)
    out["grid_by_z_decile_144"] = g.groupby("qz").apply(lambda d: agg(d, "u144"))
    sp = lambda a, b: stats.spearmanr(a, b, nan_policy="omit")
    out["spearman_z_s72"] = str(sp(g.z, g.s72))
    out["spearman_r90_s72"] = str(sp(g.r90, g.s72))
    out["spearman_r360_s72"] = str(sp(g.r360, g.s72))
    # sign of r180 graded, per coin correlation
    pc = g.groupby("coin").apply(lambda d: pd.Series(dict(n=len(d), rho=stats.spearmanr(d.z, d.s72)[0])))
    out["per_coin_rho_z"] = pc
    out["share_coins_rho_pos"] = float((pc.rho > 0).mean())
    out["by_year_rho_z"] = g.groupby("yr").apply(lambda d: pd.Series(dict(n=len(d), rho=stats.spearmanr(d.z, d.s72)[0])))
    # breakout add-on within negative z
    neg = g[g.z < 0].copy()
    neg["qz"] = pd.qcut(neg.z, 3, labels=False)
    neg["kind"] = np.where(neg.up, "up", np.where(neg.dn, "dn", "none"))
    out["neg_z_by_tercile_kind"] = neg.groupby(["qz", "kind"]).apply(agg)
    pos = g[g.z > 0].copy()
    pos["qz"] = pd.qcut(pos.z, 3, labels=False)
    pos["kind"] = np.where(pos.up, "up", np.where(pos.dn, "dn", "none"))
    out["pos_z_by_tercile_kind"] = pos.groupby(["qz", "kind"]).apply(agg)
    # leave-out 2025
    g2 = g[g.yr != 2025]
    out["spearman_z_s72_no2025"] = str(sp(g2.z, g2.s72))
    # book: daily return vs held position sign
    T = []
    for coin, ws in data["trades"].items():
        for w, x in ws.items():
            if len(x): T.append(x.assign(coin=coin))
    T = pd.concat(T)
    T["days"] = T.duration_minutes / 1440
    T["dq"] = pd.cut(T.days, [-1, 3, 8, 13, 20, 40, 200])
    out["trades_by_duration"] = T.groupby("dq").agg(n=("net_profit_loss_percent", "count"),
        mean_gross=("profit_loss_percent", "mean"), mean_net=("net_profit_loss_percent", "mean"),
        med_net=("net_profit_loss_percent", "median"))
    alloc = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"]
            alloc.append(dict(mean_abs=a.abs().mean(), share_in=(a.abs() > 1e-6).mean(), max_abs=a.abs().max()))
    out["alloc"] = pd.DataFrame(alloc).describe()
    return out
