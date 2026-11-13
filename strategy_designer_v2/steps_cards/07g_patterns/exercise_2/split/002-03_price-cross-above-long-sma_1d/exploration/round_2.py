def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []; trades = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            ts = pd.to_datetime(b["timestamp"])
            bv = b["postRebalance_total_value"].astype(float)
            br = bv.pct_change()
            d = pd.DataFrame({"coin": coin, "w": w, "i": np.arange(len(b)), "fc": b["forecast"].astype(float),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "dist": b["debug_info.components.above_ma.last_history_value"].astype(float),
                              "r1": r1, "f1": c.shift(-1)/c-1, "f5": c.shift(-5)/c-1, "f20": c.shift(-20)/c-1,
                              "p5": c/c.shift(5)-1, "br": br, "vol20": vol20, "wd": ts.dt.weekday, "yr": ts.dt.year})
            d["z"] = r1 / vol20.shift(1)
            d["fcprev"] = d["fc"].shift(1)
            rows.append(d)
        for w, t in data["trades"][coin].items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; trades.append(t)
    D = pd.concat(rows, ignore_index=True)
    T = pd.concat(trades, ignore_index=True)
    out = {}
    N = D[D["i"] % 20 == 0].copy()  # non-overlapping 20-bar samples
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    N["fcb"] = pd.cut(N["fc"], [-0.01, 0.0001, 5, 10, 15, 20.01], labels=["0","0-5","5-10","10-15","15-20"])
    out["nonoverlap f20 by fc bucket"] = N.groupby("fcb", observed=True)["f20"].apply(tt).unstack()
    N["db"] = pd.cut(N["dist"], [-np.inf, -15, 0, 30, 60, np.inf])
    out["nonoverlap f20 by dist"] = N.groupby("db", observed=True)["f20"].apply(tt).unstack()
    # big z up moves continuation, by active state
    D["zb"] = pd.cut(D["z"], [-np.inf, -2, 2, np.inf], labels=["dn2", "mid", "up2"])
    out["f5 after z move x above-SMA"] = D.groupby(["zb", D.dist > 0], observed=True)["f5"].apply(tt).unstack()
    # weekday by year (Saturday and Friday)
    out["sat r1 by year"] = D[D.wd == 5].groupby("yr")["r1"].apply(tt).unstack()
    out["weekday r1 by coin t"] = D.groupby(["coin", "wd"])["r1"].apply(lambda x: x.mean()/x.std()*np.sqrt(x.count())).unstack()
    # weekday of r1 means label? check: r1 on bar timestamp weekday = return into that day close
    # crossing events: fc going 0->positive, f20 after, and number of re-crosses
    D["entry"] = (D.fcprev == 0) & (D.fc > 0)
    out["f20/f5 after up-cross (fc 0->pos)"] = pd.concat({"f5": tt(D.loc[D.entry, "f5"]), "f20": tt(D.loc[D.entry, "f20"]), "f20_all": tt(N["f20"])}, axis=1)
    # trades by entry forecast
    T["efb"] = pd.cut(T["entry_forecast"], [-0.01, 2, 5, 10, 15, 20.01])
    out["trades by entry fc"] = T.groupby("efb", observed=True)["net_profit_loss_percent"].agg(["count", "mean", "median", lambda x: (x > 0).mean()])
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    # book largest losses/gains days: prior conditions
    q = D["br"].quantile([0.01, 0.99])
    big_l = D[D.br <= q.iloc[0]]; big_g = D[D.br >= q.iloc[1]]
    out["book extremes context"] = pd.DataFrame({"loss": [len(big_l), big_l.br.mean(), big_l.dist.mean(), big_l.vol20.mean(), big_l.p5.mean(), big_l.f5.mean()],
        "gain": [len(big_g), big_g.br.mean(), big_g.dist.mean(), big_g.vol20.mean(), big_g.p5.mean(), big_g.f5.mean()],
        "all_active": [int((D.alloc>0).sum()), D.loc[D.alloc.shift(1)>0, "br"].mean(), D.loc[D.alloc>0, "dist"].mean(), D.loc[D.alloc>0, "vol20"].mean(), np.nan, np.nan]},
        index=["n", "br", "dist", "vol20", "past5", "next5"])
    # drawdown by year of book
    out["book r by year"] = D.groupby("yr")["br"].apply(tt).unstack()
    return out
