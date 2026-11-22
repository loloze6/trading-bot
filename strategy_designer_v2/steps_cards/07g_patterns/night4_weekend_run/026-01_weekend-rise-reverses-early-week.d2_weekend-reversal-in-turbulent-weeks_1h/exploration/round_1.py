def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []      # 48h grid at 00:00: prior 48h ret, next 48h ret, weekday of grid point
    hrs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True) + pd.Timedelta(hours=1)  # close time
            b = b.set_index("ts")
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=200).std()
            # hourly
            h = pd.DataFrame({"r": r1, "rnext": r1.shift(-1), "hour": c.index.hour, "wd": c.index.weekday,
                              "vol": vol, "coin": coin})
            hrs.append(h.dropna(subset=["r"]))
            # 00:00 closes
            z = c[c.index.hour == 0]
            z = z[~z.index.duplicated()]
            full = z.reindex(pd.date_range(z.index.min(), z.index.max(), freq="1D", tz="UTC"))
            prev = full / full.shift(2) - 1
            nxt = full.shift(-2) / full - 1
            nxt1 = full.shift(-1) / full - 1
            df = pd.DataFrame({"prev": prev, "next": nxt, "next1": nxt1, "wd": full.index.weekday,
                               "vol": vol.reindex(full.index), "coin": coin, "win": w})
            # regime at the Monday bar
            reg = b["regime"].reindex(full.index)
            df["reg"] = reg.values
            # weekday ret (Fri00 -> Sat00) etc
            rows.append(df.dropna(subset=["prev", "next"]))
    D = pd.concat(rows)
    D["vstd48"] = D["vol"] * np.sqrt(48)
    D["z"] = D["prev"] / D["vstd48"]
    D["nz"] = D["next"] / D["vstd48"]
    D = D.dropna(subset=["z", "nz"])
    # per weekday of grid point: slope of next on prev (standardised), on non-overlapping? each weekday is its own grid of 1 per week
    res = []
    for wd, g in D.groupby("wd"):
        sl = stats.linregress(g["z"], g["nz"])
        res.append({"wd": wd, "n": len(g), "slope": sl.slope, "t": sl.slope / sl.stderr,
                    "corr": sl.rvalue, "mean_next_after_up": g.loc[g.z > 0, "next"].mean(),
                    "mean_next_after_dn": g.loc[g.z < 0, "next"].mean()})
    out["48h_reversal_by_weekday_of_point"] = pd.DataFrame(res)
    # Monday only, by regime and sign
    M = D[D.wd == 0].copy()
    M["vterc"] = M.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    res = []
    for (vt, up), g in M.groupby(["vterc", M.z > 0]):
        res.append({"vol_tercile": vt, "weekend_up": up, "n": len(g), "mean_next": g["next"].mean(),
                    "t": g["next"].mean() / (g["next"].std() / np.sqrt(len(g))),
                    "mean_next1": g["next1"].mean(), "slope_nz_on_z": stats.linregress(g["z"], g["nz"]).slope})
    out["monday_by_voltercile_sign"] = pd.DataFrame(res)
    # Monday by z quintile
    M["zq"] = pd.qcut(M["z"], 5, labels=False)
    out["monday_by_weekend_z_quintile"] = M.groupby("zq").agg(n=("next", "size"), z=("z", "mean"),
        next=("next", "mean"), next1=("next1", "mean"), nz=("nz", "mean"))
    out["monday_by_coin_slope"] = M.groupby("coin").apply(lambda g: pd.Series({
        "n": len(g), "slope": stats.linregress(g.z, g.nz).slope,
        "t": stats.linregress(g.z, g.nz).slope / stats.linregress(g.z, g.nz).stderr}))
    # hourly by hour and weekday
    H = pd.concat(hrs)
    H["rs"] = H["r"] / H["vol"]
    hh = H.groupby("hour")["r"].agg(["mean", "std", "count"])
    hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["hourly_mean_by_hour"] = hh[["mean", "t", "count"]]
    ww = H.groupby("wd")["r"].agg(["mean", "std", "count"])
    ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["count"]))
    out["hourly_mean_by_weekday"] = ww[["mean", "t"]]
    # 1h after large 1h moves
    H2 = H.dropna(subset=["rs", "rnext"])
    H2["q"] = pd.qcut(H2["rs"], 10, labels=False)
    g = H2.groupby("q")["rnext"].agg(["mean", "std", "count"])
    g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
    out["next1h_by_decile_of_1h_move"] = g[["mean", "t", "count"]]
    # book: trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_h"] = T["duration_minutes"] / 60
    out["trades_summary"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"),
        gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"),
        dur_h=("dur_h", "mean"), dur_h_max=("dur_h", "max"))
    out["trades_dur_quantiles"] = T["dur_h"].describe()
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"))
    return out
