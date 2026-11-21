def explore(data):
    import numpy as np, pandas as pd
    out = {}
    recs = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values; hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(c)
            rng = (hi - lo)
            mr180 = rng.rolling(180, min_periods=45).mean().values
            hh12 = hi.shift(1).rolling(12).max().values
            ll12 = lo.shift(1).rolling(12).min().values
            cs = pd.Series(c)
            ret42 = (cs / cs.shift(42) - 1).values
            ret6 = (cs / cs.shift(6) - 1).values
            ret1 = (cs / cs.shift(1) - 1)
            vol = ret1.rolling(180, min_periods=45).std().values
            ts = pd.to_datetime(b["timestamp"])
            for H in (6, 18, 36):
                f = np.full(n, np.nan); f[:n-H] = c[H:] / c[:n-H] - 1
                recs.append(pd.DataFrame({"coin": coin, "win": w, "H": H, "pos": np.arange(n),
                    "cell": np.arange(n) // H, "fwd": f,
                    "up": (c - hh12) / mr180, "dn": (ll12 - c) / mr180,
                    "ret42": ret42, "ret6s": ret6 / (vol * np.sqrt(6)), "r1s": ret1.values / vol,
                    "hour": ts.dt.hour.values, "wd": ts.dt.weekday.values}))
    A = pd.concat(recs, ignore_index=True)
    A = A[A.fwd.notna()]
    # coin drift and sd on grid
    grid = A[A.pos % A.H == 0]
    st = grid.groupby(["coin", "H"]).fwd.agg(["mean", "std"])
    A = A.join(st, on=["coin", "H"])
    A["unp"] = A.fwd - A["mean"]; A["un"] = A.unp / A["std"]
    def first_case(mask, H):
        d = A[(A.H == H) & mask]
        return d.sort_values("pos").groupby(["coin", "win", "cell"]).head(1)
    def summ(d):
        if len(d) < 5: return pd.Series({"n": len(d)})
        return pd.Series({"n": len(d), "unusual_pct": d.unp.mean() * 100, "strength": d.un.mean(),
                          "t": d.un.mean() / (d.un.std() / np.sqrt(len(d)))})
    res = {}
    for H in (6, 18, 36):
        res[f"dnbreak_H{H}"] = summ(first_case(A.dn > 0, H))
        res[f"dnbreak_neg7d_H{H}"] = summ(first_case((A.dn > 0) & (A.ret42 < 0), H))
        res[f"dnbreak_pos7d_H{H}"] = summ(first_case((A.dn > 0) & (A.ret42 > 0), H))
        res[f"upbreak_pos7d_H{H}"] = summ(first_case((A.up > 0) & (A.ret42 > 0), H))
        res[f"upbreak_neg7d_H{H}"] = summ(first_case((A.up > 0) & (A.ret42 <= 0), H))
    out["break_cases"] = pd.DataFrame(res).T.round(4)
    # graded: down break size quartiles, H=36 and 18
    for H in (18, 36):
        d = first_case(A.dn > 0, H)
        k = pd.qcut(d.dn.rank(method="first"), 4, labels=False)
        out[f"dn_size_q_H{H}"] = d.groupby(k).apply(summ).round(4)
        d = first_case(A.up > 0, H)
        k = pd.qcut(d.up.rank(method="first"), 4, labels=False)
        out[f"up_size_q_H{H}"] = d.groupby(k).apply(summ).round(4)
    # per coin down break H36
    d = first_case(A.dn > 0, 36)
    out["dnbreak_by_coin_H36"] = d.groupby("coin").apply(summ).round(4)
    d = grid[(grid.H == 36)].join(st, on=["coin", "H"])
    d["unp"] = d.fwd - d["mean"]; d["un"] = d.unp / d["std"]
    d = d.dropna(subset=["ret42"])
    d["q"] = d.groupby("coin").ret42.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["ret42_top_by_coin"] = d[d.q == 4].groupby("coin").apply(summ).round(4)
    # 1-day reversal after large 1-day move (6 bars) on 6-bar grid
    d = A[(A.H == 6) & (A.pos % 6 == 0)].dropna(subset=["ret6s"])
    k = pd.qcut(d.ret6s.rank(method="first"), 5, labels=False)
    out["ret1d_quint_H1d"] = d.groupby(k).apply(summ).round(4)
    # hour of next 4h bar (H=1 effect) via r1s next bar
    B = A[A.H == 6].copy()
    B = B.sort_values(["coin", "win", "pos"])
    B["next_r"] = B.groupby(["coin", "win"]).r1s.shift(-1)
    out["next_bar_by_hour"] = B.groupby("hour").next_r.agg(["mean", "count"]).assign(
        t=lambda x: x["mean"] / (B.groupby("hour").next_r.std() / np.sqrt(x["count"]))).round(4)
    out["next_bar_by_wd"] = B.groupby("wd").next_r.agg(["mean", "count"]).assign(
        t=lambda x: x["mean"] / (B.groupby("wd").next_r.std() / np.sqrt(x["count"]))).round(4)
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): T.append(t.assign(coin=coin))
    T = pd.concat(T)
    T["dur_d"] = T.duration_minutes / 1440
    k = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc"] = T.groupby(k).agg(n=("net_profit_loss_percent", "size"),
        fc_lo=("entry_forecast", "min"), net=("net_profit_loss_percent", "mean"),
        win=("net_profit_loss_percent", lambda s: (s > 0).mean()), dur=("dur_d", "median")).round(3)
    out["trades_summary"] = pd.Series({"n": len(T), "net_mean": T.net_profit_loss_percent.mean(),
        "net_median": T.net_profit_loss_percent.median(), "dur_med_d": T.dur_d.median(),
        "share_loss_gt10": (T.net_profit_loss_percent < -10).mean()}).round(3)
    return out
