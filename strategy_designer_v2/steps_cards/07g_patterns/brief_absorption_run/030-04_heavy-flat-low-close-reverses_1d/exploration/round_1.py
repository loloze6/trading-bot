def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; H = 5
    rows = []; ev = []; daily = []
    for coin, wins in bars.items():
        g_all = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            if len(b) < 30: continue
            c = b["close"]; o = b["open"]; hi = b["high"]; lo = b["low"]; v = b["volume"]
            rng = (hi - lo).replace(0, np.nan)
            d = pd.DataFrame({
                "cl": 2*(c-lo)/rng - 1,
                "vr": v / v.shift(1).rolling(20).mean(),
                "body": (c-o).abs()/rng,
                "rngrel": (hi-lo)/c,
                "past1": c/c.shift(1)-1,
                "past5": c/c.shift(5)-1,
                "past20": c/c.shift(20)-1,
                "vol20": (c/c.shift(1)-1).rolling(20).std(),
                "fwd": c.shift(-H)/c-1,
                "fwd1": c.shift(-1)/c-1,
                "wd": pd.to_datetime(b["timestamp"]).dt.dayofweek,
                "alloc": b["postRebalance_current_allocation"],
                "fc": b["forecast"],
            })
            d["coin"] = coin; d["w"] = w; d["pos"] = np.arange(len(d)); d["cell"] = d["pos"]//H
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    grid = D[(D.pos % H == 0) & D.fwd.notna()].copy()
    drift = grid.groupby("coin").fwd.mean(); usual = grid.groupby("coin").fwd.std()
    D["ex"] = (D.fwd - D.coin.map(drift)) / D.coin.map(usual)
    D["d1"] = D.coin.map(D.groupby("coin").fwd1.mean())
    grid = D[(D.pos % H == 0) & D.ex.notna()].copy()
    out = {}
    out["drift_usual"] = pd.DataFrame({"drift5": drift, "usual5": usual})
    def summ(s):
        s = s.dropna(); n = len(s)
        return pd.Series({"n": n, "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan})
    # close location graded by volume ratio buckets, grid bars
    grid["vrb"] = pd.cut(grid.vr, [0, 0.7, 1.0, 1.5, 2.0, 100])
    grid["clb"] = pd.cut(grid.cl, [-1.01, -0.6, -0.2, 0.2, 0.6, 1.01])
    out["ex_by_clb"] = grid.groupby("clb").ex.apply(summ).unstack()
    out["ex_by_vrb"] = grid.groupby("vrb").ex.apply(summ).unstack()
    # slope of ex on cl per vr bucket
    res = {}
    for k, gg in grid.dropna(subset=["cl", "vr"]).groupby("vrb"):
        if len(gg) > 20:
            r = stats.linregress(gg.cl, gg.ex); res[str(k)] = {"n": len(gg), "slope": r.slope, "t": r.slope/r.stderr}
    out["slope_ex_on_cl_by_vr"] = pd.DataFrame(res).T
    # past returns z
    grid["p5z"] = grid.past5 / grid.coin.map(usual)
    grid["p20z"] = grid.past20 / grid.coin.map(usual)
    out["ex_by_past5_q"] = grid.groupby(pd.qcut(grid.p5z, 5)).ex.apply(summ).unstack()
    out["ex_by_past20_q"] = grid.groupby(pd.qcut(grid.p20z, 5)).ex.apply(summ).unstack()
    out["ex_by_past1_q"] = grid.groupby(pd.qcut(grid.past1/grid.coin.map(usual), 5)).ex.apply(summ).unstack()
    grid["volrel"] = grid.vol20 / grid.groupby("coin").vol20.transform("median")
    out["ex_by_vol_q"] = grid.groupby(pd.qcut(grid.volrel, 5)).ex.apply(summ).unstack()
    out["ex_by_range_q"] = grid.groupby(pd.qcut(grid.rngrel/grid.coin.map(usual), 5)).ex.apply(summ).unstack()
    # weekday on daily returns (excess over coin daily mean, in units)
    D["e1"] = (D.fwd1 - D.d1)
    out["next_day_by_weekday"] = D.groupby("wd").e1.apply(summ).unstack()
    # heavy flat events, first per cell
    E = D[(D.vr >= 2) & (D.body <= 1/3) & D.ex.notna()].groupby(["coin", "w", "cell"]).head(1)
    out["heavyflat_by_cl_sign"] = E.groupby(E.cl < 0).ex.apply(summ).unstack()
    E2 = D[(D.vr >= 2) & D.ex.notna()].groupby(["coin", "w", "cell"]).head(1)
    out["heavy_any_by_clb"] = E2.groupby(pd.cut(E2.cl, [-1.01, -0.33, 0.33, 1.01])).ex.apply(summ).unstack()
    E3 = D[(D.vr >= 2) & D.ex.notna()].groupby(["coin", "w", "cell"]).head(1)
    out["heavy_by_past1sign"] = E3.groupby(E3.past1 > 0).ex.apply(summ).unstack()
    # book
    dd = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()])
    out["book_by_coin"] = dd.groupby("coin").book_return.apply(summ).unstack()
    tr = pd.concat([x.assign(coin=c) for c, ws in data["trades"].items() for x in ws.values()])
    out["trades_by_side"] = tr.groupby("side").net_profit_loss_percent.apply(summ).unstack()
    return out
