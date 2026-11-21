def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    hr = []; grid = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].values.astype(float); v = b["volume"].values.astype(float)
            ts = pd.to_datetime(b["timestamp"]); tc = ts + pd.Timedelta(hours=1)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            hc = tc.dt.hour.values; yr = tc.dt.year.values
            hr.append(pd.DataFrame({"coin": coin, "w": w, "yr": yr, "h": hc, "r": r1}))
            n = len(c)
            for t in range(24, n-24, 24):
                rr = r1[t-23:t+1]; vv = v[t-23:t+1]
                sa = np.nansum(np.abs(rr))
                vsh = np.nanmax(vv)/np.nansum(vv) if np.nansum(vv) > 0 else np.nan
                vol_rel = np.nansum(vv)/np.nanmean(v[max(0,t-24*30):t+1])/24 if t > 0 else np.nan
                grid.append((coin, w, yr[t], c[t]/c[t-24]-1, c[t+24]/c[t]-1, sa, vsh,
                             np.nanmax(np.abs(rr))/sa if sa > 0 else np.nan, vol_rel))
    H = pd.concat(hr).dropna()
    H["late"] = H["h"].isin([22, 23])
    a = H.groupby(["coin", "late"])["r"].mean().unstack()
    a["t_diff"] = [stats.ttest_ind(H[(H.coin==k)&H.late]["r"], H[(H.coin==k)&~H.late]["r"], equal_var=False).statistic for k in a.index]
    out["late(22-23 close) vs other hourly ret by coin"] = a
    b2 = H[H.late].groupby("yr")["r"].agg(["mean", "count"]); b2["other_mean"] = H[~H.late].groupby("yr")["r"].mean()
    out["late hours by year"] = b2
    G = pd.DataFrame(grid, columns=["coin","w","yr","past","fwd","sa","vsh","maxsh","volrel"]).dropna()
    G["exc"] = G["fwd"] - G.groupby("coin")["fwd"].transform("mean")
    G["volq"] = G.groupby("coin")["sa"].transform(lambda s: pd.qcut(s, 5, labels=False))
    top = G[G.volq == 4].copy()
    top["pq"] = pd.qcut(top["past"], 5, labels=False)
    t1 = top.groupby("pq").agg(past=("past","mean"), exc=("exc","mean"), n=("exc","size"))
    t1["t"] = top.groupby("pq")["exc"].apply(lambda s: s.mean()/(s.std()/np.sqrt(len(s))))
    out["top-vol quintile: fwd24 exc by past24 quintile"] = t1
    out["top-vol slope t per coin"] = top.groupby("coin").apply(lambda d: pd.Series({"t": stats.linregress(d.past, d.exc).slope/stats.linregress(d.past, d.exc).stderr, "n": len(d)}))
    out["top-vol slope t per year"] = top.groupby("yr").apply(lambda d: pd.Series({"t": stats.linregress(d.past, d.exc).slope/stats.linregress(d.past, d.exc).stderr, "n": len(d)}))
    G["vshq"] = G.groupby("coin")["vsh"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["slope of exc on past by volume-concentration tercile"] = G.groupby("vshq").apply(lambda d: pd.Series({"slope": stats.linregress(d.past, d.exc).slope, "t": stats.linregress(d.past, d.exc).slope/stats.linregress(d.past, d.exc).stderr, "n": len(d)}))
    G["mxq"] = G.groupby("coin")["maxsh"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["slope by max-hour-move share tercile"] = G.groupby("mxq").apply(lambda d: pd.Series({"slope": stats.linregress(d.past, d.exc).slope, "t": stats.linregress(d.past, d.exc).slope/stats.linregress(d.past, d.exc).stderr}))
    # book
    rows = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            rows.append(d.assign(coin=coin, w=w))
    D = pd.concat(rows).dropna(subset=["book_return"])
    bd = D.groupby(["w", "day"])["book_return"].mean()
    out["book daily mean, sharpe"] = f"{bd.mean():.6f}, {bd.mean()/bd.std()*np.sqrt(365):.2f}, n={len(bd)}"
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades: mean gross, mean net, mean dur min, mean comm"] = f"{T.profit_loss_percent.mean():.4f}, {T.net_profit_loss_percent.mean():.4f}, {T.duration_minutes.mean():.0f}, {T.total_commission.mean():.4f}, n={len(T)}"
    return out
