def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(30, min_periods=20).std()
            z = r1 / vol
            r5p = c / c.shift(5) - 1
            r30p = c / c.shift(30) - 1
            volrank = vol.rolling(180, min_periods=60).apply(lambda x: (x[-1] > x[:-1]).mean(), raw=True)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "r1": r1,
                               "z5": r5p / (vol * np.sqrt(5)), "r30": r30p, "volrank": volrank,
                               "wd": ts.dt.weekday, "year": ts.dt.year,
                               "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float)})
            for h in [1, 2, 3, 5, 10]:
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    out = {}
    # coin drift per horizon and usual move, on grid
    for h in [1, 2, 3, 5, 10]:
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")[f"f{h}"].mean()
        s = g.groupby("coin")[f"f{h}"].std()
        D[f"x{h}"] = D[f"f{h}"] - D["coin"].map(m)
        D[f"s{h}"] = D[f"x{h}"] / D["coin"].map(s)
    D["zq"] = pd.qcut(D["z"], 10, labels=False)
    # 1. next-h excess by decile of z (non-overlap grid per h)
    res = {}
    for h in [1, 2, 3, 5, 10]:
        g = D[D["pos"] % h == 0]
        res[f"x{h}_bps"] = g.groupby("zq")[f"x{h}"].mean() * 1e4
        res[f"str{h}"] = g.groupby("zq")[f"s{h}"].mean()
    res["n_h1"] = D.groupby("zq")["x1"].count()
    res["zmean"] = D.groupby("zq")["z"].mean()
    out["by_z_decile"] = pd.DataFrame(res).round(3)
    # 2. multi-day horizon after falls: slope of x_h on -z clipped, t
    t = []
    for h in [1, 2, 3, 5, 10]:
        g = D[(D["pos"] % h == 0) & (D["z"] < 0)].dropna(subset=["z", f"x{h}"])
        sl = stats.linregress(-g["z"], g[f"x{h}"])
        t.append({"h": h, "n": len(g), "slope_bps": sl.slope * 1e4, "t": sl.slope / sl.stderr,
                  "mean_x_bps_z<-1.5": g.loc[g["z"] < -1.5, f"x{h}"].mean() * 1e4,
                  "mean_total_bps_z<-1.5": g.loc[g["z"] < -1.5, f"f{h}"].mean() * 1e4,
                  "n_z<-1.5": (g["z"] < -1.5).sum()})
    out["fall_horizons"] = pd.DataFrame(t).round(3)
    # 3. rise side: same for z>0
    t = []
    for h in [1, 3, 5, 10]:
        g = D[(D["pos"] % h == 0) & (D["z"] > 0)].dropna(subset=["z", f"x{h}"])
        sl = stats.linregress(g["z"], g[f"x{h}"])
        t.append({"h": h, "n": len(g), "slope_bps": sl.slope * 1e4, "t": sl.slope / sl.stderr,
                  "mean_x_bps_z>1.5": g.loc[g["z"] > 1.5, f"x{h}"].mean() * 1e4, "n": (g["z"] > 1.5).sum()})
    out["rise_horizons"] = pd.DataFrame(t).round(3)
    # 4. 5-day move scaled, decile -> next 5 day
    g = D[D["pos"] % 5 == 0].dropna(subset=["z5", "x5"])
    g = g.assign(q=pd.qcut(g["z5"], 5, labels=False))
    out["z5_quint_next5"] = g.groupby("q").agg(z5=("z5", "mean"), x5_bps=("x5", lambda s: s.mean() * 1e4),
                                                str5=("s5", "mean"), n=("x5", "count")).round(3)
    # 5. falls by regime: trend (30d return sign) and vol rank
    f = D[(D["z"] < -1)].dropna(subset=["x1", "r30"])
    f = f.assign(trend=np.where(f["r30"] > 0, "up30", "down30"),
                 vr=pd.cut(f["volrank"], [-0.01, 0.33, 0.66, 1.01], labels=["lowvol", "midvol", "highvol"]))
    agg = lambda s: pd.Series({"n": len(s), "x1_bps": s.mean() * 1e4, "t": s.mean() / s.std() * np.sqrt(len(s))})
    out["falls_by_trend"] = f.groupby("trend")["x1"].apply(agg).unstack().round(2)
    out["falls_by_vol"] = f.groupby("vr")["x1"].apply(agg).unstack().round(2)
    out["falls_by_coin"] = f.groupby("coin")["x1"].apply(agg).unstack().round(2)
    out["falls_by_year"] = f.groupby("year")["x1"].apply(agg).unstack().round(2)
    out["falls_by_wd"] = f.groupby("wd")["x1"].apply(agg).unstack().round(2)
    # 6. all bars by weekday
    out["all_by_wd"] = D.dropna(subset=["x1"]).groupby("wd")["x1"].apply(agg).unstack().round(2)
    # 7. book: daily returns, largest gains/losses context
    dd = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd.append(d.assign(coin=coin, w=w))
    Dd = pd.concat(dd, ignore_index=True)
    br = Dd.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book_daily"] = pd.Series({"mean_bps": br.mean() * 1e4, "std_bps": br.std() * 1e4,
                                   "share_gain_top5pct_days": br[br > br.quantile(.95)].sum() / br.sum(),
                                   "share_loss_bottom5pct": br[br < br.quantile(.05)].sum() / br.sum()}).round(3)
    # 8. trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()], ignore_index=True)
    tr["dur_d"] = tr["duration_minutes"] / 1440
    out["trades"] = pd.Series({"n": len(tr), "mean_dur_d": tr["dur_d"].mean(), "med_dur_d": tr["dur_d"].median(),
                               "mean_net_pct": tr["net_profit_loss_percent"].mean(),
                               "mean_gross_pct": tr["profit_loss_percent"].mean(),
                               "win": (tr["net_profit_loss_percent"] > 0).mean()}).round(3)
    return out
