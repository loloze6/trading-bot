def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    ev = []
    grid = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c, hi, lo = b["close"], b["high"], b["low"]
            rng = (hi - lo) / c
            fwd = c.shift(-H) / c - 1
            ph = hi.shift(1).rolling(12).max(); pl = lo.shift(1).rolling(12).min()
            up = (c / ph - 1).clip(lower=0); dn = (pl / c - 1).clip(lower=0)
            base = rng.rolling(180, min_periods=60).mean()
            dn_rel = dn / base
            up_rel = up / base
            quiet = base / rng.rolling(42).mean()
            narrow = base / ((ph - pl) / c)
            past1 = c / c.shift(6) - 1
            vol30 = c.pct_change().rolling(180, min_periods=60).std()
            p1z = past1 / (vol30 * np.sqrt(6))
            year = pd.to_datetime(b["timestamp"]).dt.year
            cell = np.arange(len(b)) // H
            g = pd.DataFrame({"coin": coin, "win": w, "cell": cell, "fwd": fwd, "dn": dn, "dn_rel": dn_rel,
                              "up_rel": up_rel, "quiet": quiet, "narrow": narrow, "p1z": p1z, "year": year})
            grid.append(g.iloc[::H])
            # events: first down-break bar in each cell, and first up-break
            for side, col in [("dn", "dn"), ("up", "up_rel")]:
                e = g[g[col] > 0].groupby("cell").head(1).copy()
                e["side"] = side
                ev.append(e)
    gd = pd.concat(grid).dropna(subset=["fwd"])
    drift = gd.groupby("coin")["fwd"].mean()
    usual = gd.groupby("coin")["fwd"].std()
    E = pd.concat(ev).dropna(subset=["fwd"])
    E["ex"] = E["fwd"] - E["coin"].map(drift)
    E["str"] = E["ex"] / E["coin"].map(usual)
    gd["ex"] = gd["fwd"] - gd["coin"].map(drift)
    gd["str"] = gd["ex"] / gd["coin"].map(usual)
    def summ(x, by):
        o = x.groupby(by).agg(n=("ex", "size"), mean_ex=("ex", "mean"), sd=("ex", "std"), strength=("str", "mean"), tot=("fwd", "mean"))
        o["t"] = o["mean_ex"] / (o["sd"] / np.sqrt(o["n"]))
        return o.drop(columns="sd").round(5)
    out = {}
    D = E[E.side == "dn"].dropna(subset=["dn_rel"]).copy()
    U = E[E.side == "up"].dropna(subset=["up_rel"]).copy()
    D["q"] = D.groupby("coin")["dn_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    U["q"] = U.groupby("coin")["up_rel"].transform(lambda s: pd.qcut(s.rank(method="first"), 4, labels=False))
    out["dn_events_by_size_q"] = summ(D, "q")
    out["up_events_by_size_q"] = summ(U, "q")
    out["dn_top_half_by_coin"] = summ(D[D.q >= 2], "coin")
    out["dn_top_half_by_year"] = summ(D[D.q >= 2], "year")
    out["dn_spearman_by_coin"] = D.groupby("coin").apply(lambda x: stats.spearmanr(x["dn_rel"], x["ex"])[0]).round(3)
    out["dn_spearman_all"] = float(stats.spearmanr(D["dn_rel"], D["ex"])[0])
    # one-day drop in vol units, grid
    G = gd.dropna(subset=["p1z"]).copy()
    G["q"] = G.groupby("coin")["p1z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["grid_by_p1z"] = summ(G, "q")
    out["grid_p1z_low_by_coin"] = summ(G[G.q == 0], "coin")
    out["grid_p1z_low_by_year"] = summ(G[G.q == 0], "year")
    # quiet week -> lower move? by coin and year for top quintile
    Q = gd.dropna(subset=["quiet"]).copy()
    Q["q"] = Q.groupby("coin")["quiet"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["quiet_top_by_coin"] = summ(Q[Q.q == 4], "coin")
    out["quiet_top_by_year"] = summ(Q[Q.q == 4], "year")
    out["quiet_absmove_by_q"] = Q.groupby("q")["fwd"].agg(lambda s: s.abs().mean()).round(5)
    # book's largest days
    dd = pd.concat([df.assign(coin=c, win=w) for c, ws in data["days"].items() for w, df in ws.items()]).dropna(subset=["book_return"])
    dd = dd.sort_values(["coin", "win", "day"])
    dd["next_coin"] = dd.groupby(["coin", "win"])["coin_return"].shift(-1)
    dd["prev_coin"] = dd.groupby(["coin", "win"])["coin_return"].shift(1)
    lo_q, hi_q = dd["book_return"].quantile([0.01, 0.99])
    out["book_extremes"] = pd.DataFrame({
        "worst1pct": dd[dd.book_return <= lo_q][["book_return", "coin_return", "prev_coin", "next_coin"]].mean(),
        "best1pct": dd[dd.book_return >= hi_q][["book_return", "coin_return", "prev_coin", "next_coin"]].mean()}).round(5)
    return out
