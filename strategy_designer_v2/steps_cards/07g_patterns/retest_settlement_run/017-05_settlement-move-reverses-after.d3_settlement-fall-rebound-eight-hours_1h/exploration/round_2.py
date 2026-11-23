def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    recs = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            if n < 900: continue
            ts = pd.to_datetime(df["timestamp"]) + pd.Timedelta(hours=1)
            s = pd.Series(c)
            d = pd.DataFrame({"coin": coin, "win": w, "hour": ts.dt.hour.values, "year": ts.dt.year.values,
                              "tkey": ts.astype("int64").values // 10**9, "pos": np.arange(n)})
            r24 = s / s.shift(24) - 1
            d["p24"] = (r24 / r24.abs().rolling(720, min_periods=360).mean()).values
            d["f24"] = (s.shift(-24) / s - 1).values
            d["f8"] = (s.shift(-8) / s - 1).values
            d["vol"] = s.pct_change().rolling(720, min_periods=360).std().values
            d["vol_ratio"] = (s.pct_change().rolling(72).std() / s.pct_change().rolling(720, min_periods=360).std()).values
            recs.append(d)
    D = pd.concat(recs, ignore_index=True)
    for H in (8, 24):
        g = D[D["pos"] % H == 0]
        mu = g.groupby("coin")[f"f{H}"].mean()
        D[f"e{H}"] = D[f"f{H}"] - D["coin"].map(mu)
    g = D[D["pos"] % 24 == 0].dropna(subset=["p24", "e24", "vol"]).copy()
    g["vt"] = g.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    g["q"] = g.groupby("coin")["p24"].transform(lambda x: pd.qcut(x, 5, labels=False))
    # grading by quintile, all and high vol
    out["A_quintile_p24_e24_all"] = g.groupby("q").agg(n=("e24", "size"), e_pct=("e24", lambda x: 100 * x.mean()),
                                                     tot_pct=("f24", lambda x: 100 * x.mean()),
                                                     t=("e24", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    hv = g[g["vt"] == 2]
    out["B_quintile_p24_e24_highvol"] = hv.groupby("q").agg(n=("e24", "size"), e_pct=("e24", lambda x: 100 * x.mean()),
                                                         tot_pct=("f24", lambda x: 100 * x.mean()),
                                                         t=("e24", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    # stability by year: slope t of p24 -> e24 ; and clustered by time (mean across coins per tkey)
    rows = []
    for y, gg in g.groupby("year"):
        sl = stats.linregress(gg["p24"], gg["e24"])
        rows.append({"year": y, "n": len(gg), "slope_t": sl.slope / sl.stderr,
                     "fall_lowq_e_pct": 100 * gg.loc[gg["q"] == 0, "e24"].mean(),
                     "rise_topq_e_pct": 100 * gg.loc[gg["q"] == 4, "e24"].mean()})
    out["C_by_year"] = pd.DataFrame(rows)
    # clustered: product -p24*e24 averaged over coins per timestamp
    g["sig"] = -g["p24"].clip(-3, 3) * g["e24"]
    cl = g.groupby("tkey")["sig"].mean()
    out["D_clustered_t_signal_pnl"] = pd.Series({"n_times": len(cl), "mean": cl.mean(),
                                                 "t": cl.mean() / cl.std() * np.sqrt(len(cl))})
    # vol_ratio interaction: recent vol vs long vol
    g2 = g.dropna(subset=["vol_ratio"]).copy()
    g2["vr"] = g2.groupby("coin")["vol_ratio"].transform(lambda x: pd.qcut(x, 3, labels=False))
    rows = []
    for v, gg in g2.groupby("vr"):
        sl = stats.linregress(gg["p24"], gg["e24"])
        rows.append({"recent_vol_tercile": v, "n": len(gg), "slope": sl.slope, "slope_t": sl.slope / sl.stderr,
                     "lowq_e_pct": 100 * gg.loc[gg["q"] == 0, "e24"].mean()})
    out["E_by_recent_vol_ratio"] = pd.DataFrame(rows)
    # hour-of-day drift: 8h excess from close hour 15 and 23, by year, clustered by time
    rows = []
    for h in (15, 16, 23, 0, 1):
        gg = D[D["hour"] == h].dropna(subset=["e8"])
        for y, gy in gg.groupby("year"):
            cm = gy.groupby("tkey")["e8"].mean()
            rows.append({"hour": h, "year": y, "n": len(cm), "e8_pct": 100 * cm.mean(),
                         "t_cl": cm.mean() / cm.std() * np.sqrt(len(cm))})
    hd = pd.DataFrame(rows)
    out["F_hour_drift_by_year"] = hd.pivot(index="year", columns="hour", values="t_cl")
    rows = []
    for h in range(24):
        gg = D[D["hour"] == h].dropna(subset=["e8"])
        cm = gg.groupby("tkey")["e8"].mean()
        rows.append({"hour": h, "e8_pct": 100 * cm.mean(), "t_clustered": cm.mean() / cm.std() * np.sqrt(len(cm)), "n_days": len(cm)})
    out["G_hour_drift_clustered"] = pd.DataFrame(rows)
    # book by hour of entry (trades)
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    T = pd.concat(tr, ignore_index=True)
    T["eh"] = (pd.to_datetime(T["entry_time"])).dt.hour
    out["H_trades_by_entry_hour"] = T.groupby("eh").agg(n=("net_profit_loss_percent", "size"),
                                                       gross=("profit_loss_percent", "mean"),
                                                       net=("net_profit_loss_percent", "mean"),
                                                       dur_h=("duration_minutes", lambda x: x.mean() / 60))
    return out
