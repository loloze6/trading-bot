def explore(data):
    import numpy as np, pandas as pd
    rows = []; other = []
    cost = 0.19
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(720, min_periods=720).std().values
            r24 = pd.Series(c).pct_change(24).values
            mabs = pd.Series(np.abs(r24)).rolling(720, min_periods=200).mean().values
            n = len(c)
            f48 = np.full(n, np.nan); f48[:n-48] = c[48:] / c[:n-48] - 1
            pnl = (b["postRebalance_total_value"].shift(-48) / b["postRebalance_total_value"] - 1).values
            alloc = b["postRebalance_current_allocation"].values
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            idx = np.where((hr == 23) & ~np.isnan(f48) & ~np.isnan(mabs) & ~np.isnan(vol))[0]
            for i in idx:
                d = dict(coin=coin, w=w, year=ts[i].year, sc=r24[i]/mabs[i], vol=vol[i], f48=f48[i],
                         alloc=alloc[i], bookpnl=pnl[i])
                (rows if wd[i] == 6 else other).append(d)
    S = pd.DataFrame(rows); O = pd.DataFrame(other)
    for D in (S, O):
        D["rev48"] = -np.sign(D["sc"]) * D["f48"] * 100
        D["side"] = np.where(D.sc > 0, "rise", "fall")
        D["absc"] = D.sc.abs()
        D["scq"] = D.groupby("coin")["absc"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
        D["volq"] = D.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    def agg(g):
        return pd.Series({"n": len(g), "rev48": g.rev48.mean(), "t": g.rev48.mean()/(g.rev48.std()/np.sqrt(len(g)))})
    out = {}
    out["sun_side_volq"] = S.groupby(["side", "volq"]).apply(agg)
    out["oth_side_volq"] = O.groupby(["side", "volq"]).apply(agg)
    out["oth_side_scq"] = O.groupby(["side", "scq"]).apply(agg)
    out["sun_side_scq3"] = S.groupby(["side", "scq"]).apply(agg)
    S["bookpnl_pct"] = S.bookpnl * 100
    out["book48_by_volq"] = S.groupby("volq").agg(n=("bookpnl_pct", "size"), book48=("bookpnl_pct", "mean"),
                                                 absalloc=("alloc", lambda x: x.abs().mean()))
    out["book48_by_side"] = S.groupby("side").agg(book48=("bookpnl_pct", "mean"), absalloc=("alloc", lambda x: x.abs().mean()))
    # simulated stakes per case (one-coin, net of one round trip cost times stake)
    S["volrank"] = S.groupby("coin")["vol"].rank(pct=True)
    sims = {}
    for name, stake in {
        "book_alloc_as_is": S.alloc.abs(),
        "equal_stake": pd.Series(1.0, index=S.index),
        "stake_by_vol_rank": 2 * S.volrank,
        "top_vol_third_only": (S.volq == 2).astype(float),
        "long_falls_only_vol": 2 * S.volrank * (S.side == "fall"),
    }.items():
        net = stake * (S.rev48 - cost)
        act = stake > 0
        sims[name] = {"cases": int(act.sum()), "mean_net_per_case": net[act].mean() / stake[act].mean(),
                      "t": net.mean() / (net.std() / np.sqrt(len(net))),
                      "worst_year": S.assign(n_=net).groupby("year").n_.mean().min()}
    out["sim"] = pd.DataFrame(sims).T
    out["sim_vol_by_year"] = S.assign(n_=2*S.volrank*(S.rev48-cost)).groupby("year").n_.mean()
    return out
