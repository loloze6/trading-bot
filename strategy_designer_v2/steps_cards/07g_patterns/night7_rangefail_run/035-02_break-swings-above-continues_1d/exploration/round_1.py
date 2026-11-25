def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r1 = c.pct_change()
            sw = r1.abs().rolling(20).mean()
            hh = hi.shift(1).rolling(20).max()
            ll = lo.shift(1).rolling(20).min()
            dist = (c / hh - 1) / sw
            distlo = (c / ll - 1) / sw
            fwd = c.shift(-H) / c - 1
            ret5p = c / c.shift(5) - 1
            tr60 = c / c.shift(60) - 1
            vol_rel = r1.rolling(20).std() / r1.rolling(60).std()
            z1 = r1 / sw
            wd = pd.to_datetime(b["timestamp"]).dt.weekday
            yr = pd.to_datetime(b["timestamp"]).dt.year
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            grid = np.arange(len(b)) % H == 0
            df = pd.DataFrame(dict(coin=coin, w=w, dist=dist, distlo=distlo, fwd=fwd, ret5p=ret5p,
                                   tr60=tr60, volrel=vol_rel, z1=z1, sw=sw, wd=wd, yr=yr, day=day,
                                   fc=b["forecast"], grid=grid, r1n=r1.shift(-1)))
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.grid & A.fwd.notna()].copy()
    cm = G.groupby("coin").fwd.mean()
    G["ex"] = G.fwd - G.coin.map(cm)

    def summ(g):
        x = g.ex.dropna()
        d = g.dropna(subset=["ex"]).groupby("day").ex.sum()
        n = len(x); D = len(d)
        t = x.sum() / np.sqrt((d**2).sum() * D / max(D-1, 1)) if D > 1 else np.nan
        return pd.Series(dict(n=n, days=D, mean_ex=x.mean(), t_day=t))
    out = {}
    G1 = G.dropna(subset=["dist"])
    G1["dbin"] = pd.cut(G1.dist, [-np.inf, -10, -6, -3, -1, 0, 1, 2, np.inf])
    out["dist_from_20d_high_swings"] = G1.groupby("dbin").apply(summ)
    G2 = G.dropna(subset=["distlo"])
    G2["lbin"] = pd.cut(G2.distlo, [-np.inf, 0, 1, 3, 6, 10, np.inf])
    out["dist_from_20d_low_swings"] = G2.groupby("lbin").apply(summ)
    G3 = G.dropna(subset=["z1"])
    G3["zbin"] = pd.cut(G3.z1, [-np.inf, -3, -1.5, -0.5, 0.5, 1.5, 3, np.inf])
    out["last_day_return_in_swings"] = G3.groupby("zbin").apply(summ)
    G4 = G.dropna(subset=["volrel"])
    G4["vbin"] = pd.qcut(G4.volrel, 4)
    out["vol20_over_vol60"] = G4.groupby("vbin").apply(summ)
    G5 = G.dropna(subset=["tr60"])
    G5["tbin"] = pd.cut(G5.tr60, [-np.inf, -0.1, 0.1, np.inf], labels=["falling", "choppy", "rising"])
    G5["brk"] = G5.dist > 0
    out["trend60_x_breakout"] = G5.groupby(["tbin", "brk"]).apply(summ)
    out["by_year"] = G.groupby("yr").apply(summ)
    # weekday of daily next-day return
    A2 = A.dropna(subset=["r1n"])
    out["weekday_next_day_ret"] = A2.groupby("wd").r1n.agg(["count", "mean", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # within breakouts: 5-day prior return
    Gb = G1[G1.dist > 0].copy()
    Gb["pbin"] = pd.qcut(Gb.ret5p, 3)
    out["breakout_by_prior5d_return"] = Gb.groupby("pbin").apply(summ)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    T["fbin"] = pd.qcut(T.entry_forecast, 3, duplicates="drop")
    out["trades_by_entry_forecast"] = T.groupby("fbin").net_profit_loss_percent.agg(["count", "mean", "median"])
    T["dur_d"] = (T.duration_minutes / 1440).round()
    out["trades_by_duration_days"] = T.groupby(pd.cut(T.dur_d, [0, 5, 7, 10, 20, 1000])).net_profit_loss_percent.agg(["count", "mean"])
    out["trades_by_coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count", "mean"])
    return out
