def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            vm = v.rolling(720, min_periods=240).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "z": r/sd, "vr": v/vm,
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "i": np.arange(len(b))})
            for h in [1, 2, 4, 8, 12, 24]:
                df[f"f{h}"] = c.shift(-h)/c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def tt(x):
        x = pd.Series(x).dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    # drift per coin per horizon (grid)
    drift = {}
    for h in [1, 2, 4, 8, 12, 24]:
        g = A[A.i % h == 0]
        drift[h] = g.groupby("coin")[f"f{h}"].mean()
        A[f"x{h}"] = A[f"f{h}"] - A.coin.map(drift[h])
    # events: |z|>2.5, de-overlapped per window (spacing >= 24 bars)
    ev = []
    for (coin, w), g in A[A.z.abs() > 2.5].groupby(["coin", "w"]):
        last = -10**9
        for idx, row in g.iterrows():
            if row.i - last >= 24:
                ev.append(idx); last = row.i
    E = A.loc[ev].copy()
    E["s"] = np.sign(E.z)
    E["vb"] = pd.cut(E.vr, [0, 2, 4, 8, np.inf])
    res = {}
    for h in [1, 2, 4, 8, 12, 24]:
        res[h] = E.groupby("vb", observed=True).apply(lambda g: tt(g.s*g[f"x{h}"]))["mean_bp"]
    out["events_dirret_bp_by_vol_x_horizon"] = pd.DataFrame(res)
    out["events_n_by_vol"] = E.groupby("vb", observed=True).size()
    out["events_dir4_by_sign_vol"] = E.groupby(["s", "vb"], observed=True).apply(lambda g: tt(g.s*g.x4))
    out["events_dir12_by_sign_vol"] = E.groupby(["s", "vb"], observed=True).apply(lambda g: tt(g.s*g.x12))
    E["prod"] = E.z.abs()*E.vr
    E["pq"] = pd.qcut(E["prod"], 4)
    out["events_dir12_by_prod_q"] = E.groupby("pq", observed=True).apply(lambda g: tt(g.s*g.x12))
    out["events_dir12_by_year"] = E.groupby("yr").apply(lambda g: tt(g.s*g.x12))
    out["events_dir12_by_coin"] = E.groupby("coin").apply(lambda g: tt(g.s*g.x12))
    out["corr_s_x12_spearman_prod"] = stats.spearmanr(E["prod"], E.s*E.x12, nan_policy="omit")[0]
    # hour: 4h fwd from each hour, sampled once a day -> non-overlapping
    out["hour_x4_daily_samples"] = A.groupby("hour").apply(lambda g: tt(g.x4))
    H0 = A[A.hour == 0]
    out["hour0_x4_by_year"] = H0.groupby("yr").apply(lambda g: tt(g.x4))
    out["hour0_x4_by_coin"] = H0.groupby("coin").apply(lambda g: tt(g.x4))
    # weekday: daily returns
    D = pd.concat([x.assign(coin=c, w=w) for c, ws in data["days"].items() for w, x in ws.items()])
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    D["cx"] = D.coin_return - D.groupby("coin").coin_return.transform("mean")
    out["weekday_coin_daily"] = D.groupby("wd").apply(lambda g: tt(g.cx))
    out["thursday_by_year"] = D[D.wd == 3].groupby("yr").apply(lambda g: tt(g.cx))
    out["thursday_by_coin"] = D[D.wd == 3].groupby("coin").apply(lambda g: tt(g.cx))
    return out
