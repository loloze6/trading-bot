def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    trades = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f20 = c.shift(-20) / c - 1
            f5 = c.shift(-5) / c - 1
            f1n = c.shift(-1) / c - 1
            past20 = c / c.shift(20) - 1
            vol20 = r1.rolling(20).std()
            dist = b["debug_info.components.above_ma.last_history_value"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "w": w, "fc": b["forecast"].astype(float),
                              "alloc": b["postRebalance_current_allocation"].astype(float),
                              "dist": dist, "r1": r1, "f1": f1n, "f5": f5, "f20": f20,
                              "past20": past20, "vol20": vol20, "wd": ts.dt.weekday,
                              "yr": ts.dt.year})
            rows.append(d)
        for w, t in data["trades"][coin].items():
            if len(t):
                t = t.copy(); t["coin"] = coin; t["w"] = w; trades.append(t)
    D = pd.concat(rows, ignore_index=True)
    T = pd.concat(trades, ignore_index=True)
    out = {}
    # forecast buckets
    D["fcb"] = pd.cut(D["fc"], [-0.01, 0.0001, 5, 10, 15, 20.01], labels=["0", "0-5", "5-10", "10-15", "15-20"])
    out["fwd by forecast bucket"] = D.groupby("fcb", observed=True).agg(n=("f20", "count"), f1=("f1", "mean"), f5=("f5", "mean"), f20=("f20", "mean"), f20med=("f20", "median"), hit20=("f20", lambda x: (x > 0).mean()))
    # raw distance buckets (including below)
    D["db"] = pd.cut(D["dist"], [-np.inf, -30, -15, -5, 0, 5, 15, 30, 60, np.inf])
    out["fwd by raw distance (pct?)"] = D.groupby("db", observed=True).agg(n=("f20", "count"), dist=("dist", "mean"), f5=("f5", "mean"), f20=("f20", "mean"), hit20=("f20", lambda x: (x > 0).mean()), vol=("vol20", "mean"))
    out["dist describe"] = D["dist"].describe()
    # past 20 return quintile
    D["pq"] = D.groupby("coin")["past20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    g = D.groupby("pq").agg(n=("f20", "count"), past=("past20", "mean"), f1=("f1", "mean"), f5=("f5", "mean"), f20=("f20", "mean"))
    out["fwd by past20 quintile"] = g
    # vol quintile
    D["vq"] = D.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 5, labels=False, duplicates="drop"))
    out["fwd by vol quintile"] = D.groupby("vq").agg(n=("f20", "count"), f1=("f1", "mean"), f20=("f20", "mean"), active=("fc", lambda x: (x > 0).mean()))
    # large daily moves
    D["z"] = D["r1"] / D["vol20"].shift(1) if False else D["r1"] / D.groupby(["coin", "w"])["vol20"].shift(1)
    D["zb"] = pd.cut(D["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    out["fwd after daily z move"] = D.groupby("zb", observed=True).agg(n=("f1", "count"), f1=("f1", "mean"), f5=("f5", "mean"), f20=("f20", "mean"))
    # weekday
    wdg = D.groupby("wd")["r1"].agg(["count", "mean", "std"])
    wdg["t"] = wdg["mean"] / wdg["std"] * np.sqrt(wdg["count"])
    out["weekday r1"] = wdg
    out["year: active share, f20 active vs inactive"] = D.groupby("yr").apply(lambda x: pd.Series({"n": len(x), "active": (x.fc > 0).mean(), "r1": x.r1.mean(), "f20_act": x.loc[x.fc > 0, "f20"].mean(), "f20_inact": x.loc[x.fc == 0, "f20"].mean()}))
    out["coin: active vs inactive daily r1"] = D.groupby("coin").apply(lambda x: pd.Series({"act_share": (x.alloc.shift(1) > 0).mean(), "r1_when_held": x.loc[x.alloc.shift(1).fillna(0) > 0, "r1"].mean(), "r1_flat": x.loc[x.alloc.shift(1).fillna(0) == 0, "r1"].mean(), "f20_act": x.loc[x.fc > 0, "f20"].mean(), "f20_all": x.f20.mean()}))
    # trades
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.cut(T["dur_d"], [0, 2, 5, 15, 40, 100, 1e5])
    out["trades by duration"] = T.groupby("db", observed=True).agg(n=("net_profit_loss_percent", "count"), mean=("net_profit_loss_percent", "mean"), med=("net_profit_loss_percent", "median"), win=("net_profit_loss_percent", lambda x: (x > 0).mean()), sum=("net_profit_loss_percent", "sum"))
    out["trades summary"] = pd.Series({"n": len(T), "mean": T.net_profit_loss_percent.mean(), "median": T.net_profit_loss_percent.median(), "win": (T.net_profit_loss_percent > 0).mean(), "top10share": T.net_profit_loss_percent.nlargest(10).sum() / T.net_profit_loss_percent[T.net_profit_loss_percent > 0].sum(), "mean_commission": T.total_commission.mean()})
    # allocation changes
    D["achg"] = D.groupby(["coin", "w"])["alloc"].diff().abs()
    out["alloc stats"] = pd.Series({"mean_alloc_active": D.loc[D.alloc > 0, "alloc"].mean(), "max_alloc": D.alloc.max(), "mean_abs_change": D.achg.mean(), "share_bars_change": (D.achg > 1e-6).mean()})
    return out
