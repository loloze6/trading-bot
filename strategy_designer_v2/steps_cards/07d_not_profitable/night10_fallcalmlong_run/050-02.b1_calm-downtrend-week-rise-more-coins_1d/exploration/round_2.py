def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    tr = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"]; r = cl.pct_change()
            b["r7"] = cl / cl.shift(7) - 1
            b["sd30"] = r.rolling(30).std()
            b["z7"] = b["r7"] / (b["sd30"] * np.sqrt(7))
            b["dist_hi30"] = cl / cl.rolling(30).max() - 1
            b["r60"] = cl / cl.shift(60) - 1
            b["inprof"] = b["regime"] == "unknown"
            b["sig"] = b["forecast"] > 0
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"] * (cl.shift(-1) / cl - 1)
            b["coin"] = c; b["w"] = w; b["i"] = np.arange(len(b))
            b["ts"] = pd.to_datetime(b["timestamp"])
            for h in [3, 5, 7, 10, 14]:
                b[f"f{h}"] = cl.shift(-h) / cl - 1
            tr.append(b)
    A = pd.concat(tr, ignore_index=True)
    # horizon test: signal vs no-signal in profile, by z7 half, per horizon grid
    rows = []
    for h in [3, 5, 7, 10, 14]:
        g = A[(A.i % h) == 0].dropna(subset=[f"f{h}"])
        drift = g.groupby("coin")[f"f{h}"].mean()
        sd = g.groupby("coin")[f"f{h}"].std()
        g = g.assign(u=g[f"f{h}"] - g.coin.map(drift), s=(g[f"f{h}"] - g.coin.map(drift)) / g.coin.map(sd))
        gi = g[g.inprof]
        S = gi[gi.sig]; N = gi[~gi.sig]
        med = S.z7.median()
        hi = S[S.z7 > med]; lo = S[S.z7 <= med]
        t = stats.ttest_1samp(S.u, 0).statistic if len(S) > 2 else np.nan
        rows.append({"h": h, "sig_u": S.u.mean(), "sig_tot": S[f"f{h}"].mean(), "sig_str": S.s.mean(),
                     "t": t, "n": len(S), "hi_u": hi.u.mean(), "lo_u": lo.u.mean(),
                     "nosig_u": N.u.mean(), "n_nosig": len(N)})
    out["horizon"] = pd.DataFrame(rows).set_index("h")
    # trades with entry features
    T = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            t = t.copy(); t["coin"] = c; t["w"] = w; T.append(t)
    T = pd.concat(T, ignore_index=True)
    T["et"] = pd.to_datetime(T.entry_time)
    key = A[["coin", "w", "ts", "z7", "dist_hi30", "r60"]]
    T = T.merge(key, left_on=["coin", "w", "et"], right_on=["coin", "w", "ts"], how="left")
    out["trades_matched"] = pd.Series({"n": len(T), "matched": T.z7.notna().sum()})
    Tm = T.dropna(subset=["z7"])
    Tm = Tm.assign(zb=pd.qcut(Tm.z7, 3, labels=False, duplicates="drop"))
    out["trades_by_entry_z7"] = Tm.groupby("zb").agg(lo=("z7", "min"), hi=("z7", "max"),
        net=("net_profit_loss_percent", "mean"), sum=("net_profit_loss_percent", "sum"),
        n=("z7", "count"), dur=("duration_minutes", lambda s: s.median() / 1440),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    Tm = Tm.assign(db=pd.qcut(Tm.dist_hi30, 3, labels=False, duplicates="drop"))
    out["trades_by_entry_disthi"] = Tm.groupby("db").agg(lo=("dist_hi30", "min"), hi=("dist_hi30", "max"),
        net=("net_profit_loss_percent", "mean"), n=("z7", "count"))
    out["trades_by_window"] = T.groupby("w").agg(net_sum=("net_profit_loss_percent", "sum"),
        n=("coin", "count"), worst=("net_profit_loss_percent", "min"),
        short_trades_sum=("net_profit_loss_percent", lambda s: s[T.loc[s.index, "duration_minutes"] <= 3.5 * 1440].sum()))
    # gain in book by bar in losing windows: per window, gain from bars by z7 of held bar
    H = A[A.pos != 0].copy()
    H["zb"] = pd.cut(H.z7, [-10, 0, 0.4, 1.0, 10])
    out["held_gain_by_z7"] = H.groupby("zb").agg(gain=("gain", "sum"), mean=("gain", "mean"), n=("gain", "count"))
    out["held_gain_inprof_vs_out"] = H.groupby("inprof").agg(gain=("gain", "sum"), mean=("gain", "mean"), n=("gain", "count"))
    # whole-book chain with filter: drop trades with entry z7 below 0.4 (approx by bar gains of positions opened in them)
    return out
