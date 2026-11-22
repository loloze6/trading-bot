def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().shift(1).rolling(720, min_periods=240).mean()
            vr = v / v.shift(1).rolling(720, min_periods=240).mean()
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r6p = c/c.shift(6)-1
            r24p = c/c.shift(24)-1
            sd24 = r1.shift(1).rolling(720, min_periods=240).std()
            df = pd.DataFrame({"coin": coin, "w": w, "z": r1/mabs, "vr": vr,
                               "f2": c.shift(-2)/c-1, "f6": c.shift(-6)/c-1, "f24": c.shift(-24)/c-1,
                               "z6": r6p/(sd24*np.sqrt(6)), "z24": r24p/(sd24*np.sqrt(24)),
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "pos": np.arange(len(b)), "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    out = {}
    def tt(x):
        x = x.dropna(); n = len(x)
        return pd.Series({"n": n, "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    # graded tests on 6h grid
    g6 = d[d.pos % 6 == 0].copy()
    g6["u6"] = g6.f6 - g6.coin.map(g6.groupby("coin").f6.mean())
    g2 = d[d.pos % 2 == 0].copy()
    g2["u2"] = g2.f2 - g2.coin.map(g2.groupby("coin").f2.mean())
    g24 = d[d.pos % 24 == 0].copy()
    g24["u24"] = g24.f24 - g24.coin.map(g24.groupby("coin").f24.mean())
    reg = {}
    for name, g, y, x, cond in [
        ("u6~z | vr>2", g6, "u6", "z", lambda g: g.vr > 2),
        ("u6~z*log(vr) all", g6, "u6", "zlv", lambda g: g.vr > 0),
        ("u2~z | vr>2", g2, "u2", "z", lambda g: g.vr > 2),
        ("u6~z | vr<1", g6, "u6", "z", lambda g: g.vr < 1),
        ("u6~z6", g6, "u6", "z6", lambda g: g.vr > 0),
        ("u6~z24", g6, "u6", "z24", lambda g: g.vr > 0),
        ("u24~z24", g24, "u24", "z24", lambda g: g.vr > 0),
        ("u24~z", g24, "u24", "z", lambda g: g.vr > 0),
        ("u24~z6", g24, "u24", "z6", lambda g: g.vr > 0),
    ]:
        gg = g.copy(); gg["zlv"] = gg.z * np.log(gg.vr.clip(lower=1e-6))
        gg = gg[cond(gg)].dropna(subset=[y, x])
        for coin, s in list(gg.groupby("coin")) + [("both", gg)]:
            res = stats.linregress(s[x], s[y])
            reg[(name, coin)] = {"n": len(s), "slope_bp": res.slope*1e4, "t": res.slope/res.stderr}
    out["graded_regressions"] = pd.DataFrame(reg).T
    # weekday / hour stability by coin and year
    out["thu_u6_by_coin_year"] = g6[g6.wd == 3].groupby(["coin", "yr"]).u6.apply(tt).unstack()
    out["wd_u24_by_coin"] = g24.groupby(["wd", "coin"]).u24.apply(tt).unstack()
    out["hour_u6_by_coin"] = g6.groupby(["hour", "coin"]).u6.apply(tt).unstack().iloc[:, [1, 2, 4, 5]]
    # book day stats: largest gains / losses
    dd = pd.concat([x.assign(coin=c, w=w) for c, ws in data["days"].items() for w, x in ws.items()]).dropna(subset=["book_return"])
    q = dd.book_return.quantile([0.02, 0.98])
    out["book_extreme_days"] = pd.DataFrame({
        "worst2pct": [dd[dd.book_return <= q.iloc[0]].book_return.mean()*1e4, dd[dd.book_return <= q.iloc[0]].coin_return.mean()*1e4],
        "best2pct": [dd[dd.book_return >= q.iloc[1]].book_return.mean()*1e4, dd[dd.book_return >= q.iloc[1]].coin_return.mean()*1e4]},
        index=["book_bp", "coin_bp"])
    out["book_by_coin"] = dd.groupby("coin").book_return.apply(tt).unstack()
    return out
