def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; H = 5
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 30: continue
            c = b["close"]; o = b["open"]; hi = b["high"]; lo = b["low"]; v = b["volume"]
            rng = (hi - lo).replace(0, np.nan)
            d = pd.DataFrame({
                "cl": 2*(c-lo)/rng - 1,
                "vr": v / v.shift(1).rolling(20).mean(),
                "body": (c-o).abs()/rng,
                "past1": c/c.shift(1)-1,
                "dayret": c/o-1,
                "fwd": c.shift(-H)/c-1,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            d["coin"] = coin; d["w"] = w; d["pos"] = np.arange(len(d)); d["cell"] = d["pos"]//H
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    grid = D[(D.pos % H == 0) & D.fwd.notna()]
    drift = grid.groupby("coin").fwd.mean(); usual = grid.groupby("coin").fwd.std()
    D["ex"] = (D.fwd - D.coin.map(drift)) / D.coin.map(usual)
    D["tot"] = D.fwd / D.coin.map(usual)
    D["exraw"] = D.fwd - D.coin.map(drift)
    D["d1z"] = D.past1 / D.coin.map(usual)
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    E = D[(D.vr >= 2) & D.ex.notna() & D.cl.notna()].groupby(["coin", "w", "cell"]).head(1).copy()
    E["vrb"] = pd.cut(E.vr, [2, 2.5, 3.5, 1000])
    up = E[E.cl > 0.33]
    out["heavy_upclose_by_vr"] = up.groupby("vrb").ex.apply(summ).unstack()
    out["heavy_upclose_by_coin"] = up.groupby("coin").ex.apply(summ).unstack()
    out["heavy_upclose_by_year"] = up.groupby("yr").ex.apply(summ).unstack()
    out["heavy_upclose_rawpct"] = pd.DataFrame({"ex_pct": summ(up.exraw), "tot_pct": summ(up.fwd)})
    # graded: ex on cl*vr in heavy days
    E["clvr"] = E.cl * E.vr
    r = stats.linregress(E.clvr, E.ex); r2 = stats.linregress(E.cl, E.ex)
    r3 = stats.linregress(E.d1z, E.ex)
    out["heavy_slopes"] = pd.DataFrame({"x": ["cl*vr", "cl", "past1z"], "n": [len(E)]*3,
        "slope": [r.slope, r2.slope, r3.slope], "t": [r.slope/r.stderr, r2.slope/r2.stderr, r3.slope/r3.stderr]})
    out["heavy_cl_x_daysign"] = E.groupby([E.cl > 0.33, E.dayret > 0]).ex.apply(summ).unstack()
    # placebo: ordinary-volume days, upper close
    N = D[(D.vr < 1.5) & D.ex.notna() & D.cl.notna()].groupby(["coin", "w", "cell"]).head(1)
    out["normal_by_clsign"] = N.groupby(N.cl > 0.33).ex.apply(summ).unstack()
    # trades
    tr = pd.concat([x.assign(coin=c) for c, ws in data["trades"].items() for x in ws.values()])
    s = tr[tr.side == "SHORT"]
    out["short_by_coin"] = s.groupby("coin").net_profit_loss_percent.agg(["count", "mean", "median"])
    out["short_by_year"] = s.groupby(pd.to_datetime(s.entry_time).dt.year).net_profit_loss_percent.agg(["count", "mean", "median"])
    out["trade_pl_stats"] = tr.groupby("side").net_profit_loss_percent.agg(["mean", "median", "min", "max", lambda x: (x > 0).mean()])
    out["trade_duration_days"] = tr.groupby("side").duration_minutes.median()/1440
    return out
