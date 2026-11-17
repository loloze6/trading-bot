def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = cl.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            mom20 = cl / cl.shift(20) - 1
            dist = cl / cl.cummax() - 1  # distance to in-window running high
            dist60 = cl / cl.rolling(60, min_periods=30).max() - 1
            vr = v / v.rolling(30, min_periods=20).mean()
            z1 = r1 / vol20
            for h in (1, 5, 10):
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(b), h)
                for i in idx:
                    if i + h >= len(b): break
                    rows.append(dict(coin=c, w=w, h=h, fwd=fwd.iloc[i], mom20=mom20.iloc[i],
                                     dist60=dist60.iloc[i], vr=vr.iloc[i], z1=z1.iloc[i],
                                     vol20=vol20.iloc[i], fc=b["forecast"].iloc[i],
                                     wd=pd.Timestamp(b["timestamp"].iloc[i]).dayofweek, r1=r1.iloc[i]))
    df = pd.DataFrame(rows)
    # demean by coin mean per h
    df["ex"] = df["fwd"] - df.groupby(["coin", "h"])["fwd"].transform("mean")
    res = []
    for h in (1, 5, 10):
        d = df[df.h == h]
        for var in ("mom20", "dist60", "vr", "z1", "vol20"):
            dd = d.dropna(subset=[var, "ex"])
            dd = dd.assign(q=dd.groupby("coin")[var].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False)))
            m = dd.groupby("q")["ex"].mean()
            hi = dd[dd.q == 4]["ex"]; lo = dd[dd.q == 0]["ex"]
            t = stats.ttest_ind(hi, lo, equal_var=False).statistic
            rho = stats.spearmanr(dd[var], dd["ex"]).correlation
            res.append(dict(h=h, var=var, q0=m.get(0), q2=m.get(2), q4=m.get(4), t_hi_lo=t, rho=rho, n=len(dd)))
    out["quintiles_all_bars"] = pd.DataFrame(res).round(4)
    d1 = df[df.h == 1].dropna(subset=["ex"])
    g = d1.groupby("wd")["ex"].agg(["mean", "count", "std"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["weekday_1d"] = g.round(4)
    # per coin: mom20 effect at h=10
    d10 = df[df.h == 10].dropna(subset=["mom20", "ex"])
    pc = d10.groupby("coin").apply(lambda x: pd.Series({"rho": stats.spearmanr(x.mom20, x.ex).correlation, "n": len(x)}))
    out["mom20_h10_by_coin"] = pc.round(3)
    pc2 = d10.dropna(subset=["dist60"]).groupby("coin").apply(lambda x: pd.Series({"rho": stats.spearmanr(x.dist60, x.ex).correlation, "n": len(x)}))
    out["dist60_h10_by_coin"] = pc2.round(3)
    # book: daily returns, positions
    bk = []
    for c in days:
        for w, d in days[c].items():
            bk.append(d.assign(coin=c, w=w))
    B = pd.concat(bk)
    B["year"] = pd.to_datetime(B["day"]).dt.year
    by = B.groupby("year")[["book_return", "coin_return"]].mean()
    by["n"] = B.groupby("year").size()
    out["book_by_year"] = by
    act = []
    for c in bars:
        for w, b in bars[c].items():
            a = b["postRebalance_current_allocation"].astype(float)
            g1 = a * (b["close"].shift(-1) / b["close"] - 1)
            act.append(pd.DataFrame({"coin": c, "a": a, "g": g1, "fc": b["forecast"]}))
    A = pd.concat(act)
    out["position_stats"] = pd.Series({"share_bars_in_pos": (A.a.abs() > 1e-6).mean(),
                                        "share_forecast_pos": (A.fc > 0).mean(),
                                        "mean_alloc_when_in": A.a[A.a.abs() > 1e-6].mean(),
                                        "mean_gain_in": A.g[A.a.abs() > 1e-6].mean(),
                                        "n_in": (A.a.abs() > 1e-6).sum()})
    tr = pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()])
    tr["dur_d"] = tr["duration_minutes"] / 1440
    out["trades"] = tr.groupby("coin").agg(n=("dur_d", "size"), dur=("dur_d", "median"),
                                          pl=("net_profit_loss_percent", "mean"),
                                          win=("net_profit_loss_percent", lambda s: (s > 0).mean())).round(3)
    return out
