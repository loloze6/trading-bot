def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        drift = np.nanmean(np.concatenate(allr))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c / c.shift(1) - 1
            sd = r.rolling(30, min_periods=20).std()
            z = r / sd
            n1 = c.shift(-1) / c - 1 - drift
            pos = b["postRebalance_current_allocation"].astype(float)
            prev = b["previous_allocation"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "regime": b["regime"].astype(str),
                               "z": z, "n1": n1, "pos": pos, "prev": prev,
                               "fc": b["forecast"].astype(float), "day": ts.dt.floor("D")})
            df["prev_regime"] = df["regime"].shift(1)
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["gain"] = d["pos"] * d["n1"]
    d["short_move"] = -d["n1"]
    out = {}
    act = d[d.pos.abs() > 0].copy()
    act["is_mr"] = act.regime == "mean_reversion"
    def s(g):
        return pd.Series({"n": len(g), "mean|pos|": g.pos.abs().mean(), "share short": (g.pos < 0).mean(),
                          "gain%": 100 * g.gain.mean(), "t gain": g.gain.mean() / (g.gain.std() / np.sqrt(len(g))),
                          "short move%": 100 * g.short_move.mean(),
                          "t move": g.short_move.mean() / (g.short_move.std() / np.sqrt(len(g)))})
    out["active bars: MR vs other regime"] = act.groupby("is_mr").apply(s)
    out["active non-MR bars by regime"] = act[~act.is_mr].groupby("regime").apply(s)
    mr = d[d.regime == "mean_reversion"].dropna(subset=["n1"])
    out["MR bars: pos zero vs not"] = mr.groupby(mr.pos.abs() > 0).apply(s)
    mr2 = mr.copy()
    mr2["fcb"] = pd.qcut(mr2.fc.abs(), 4, duplicates="drop")
    out["MR by |forecast| quartile"] = mr2.groupby("fcb", observed=True).apply(s)
    mr2["zq"] = pd.qcut(mr2.z, 4, duplicates="drop")
    out["MR by z quartile"] = mr2.groupby("zq", observed=True).apply(s)
    out["MR share forecast>0 (long)"] = float((mr.fc > 0).mean())
    # gain if held unit short on every MR bar, day-clustered
    g = mr.groupby("day")["short_move"].agg(["sum", "count"])
    m = mr.short_move.mean()
    dev = mr.short_move - m
    dsum = dev.groupby(mr["day"]).sum()
    out["MR unit short, day-clustered"] = pd.Series({"mean%": 100 * m, "t": m / (np.sqrt((dsum ** 2).sum()) / len(mr)),
                                                     "cases": len(mr), "days": len(dsum)})
    # whole in-profile: graded reversal on z in [-2,2]
    ip = d[d.regime.isin(["mean_reversion", "unknown"])].dropna(subset=["z", "n1"])
    ip = ip[ip.z.abs() <= 2]
    sl = stats.linregress(ip.z, ip.n1)
    out["in-profile slope n1 on z, |z|<=2"] = pd.Series({"slope%": 100 * sl.slope, "t": sl.slope / sl.stderr, "n": len(ip)})
    ch = d[d.regime == "chop"].dropna(subset=["z", "n1"])
    ch = ch[ch.z.abs() <= 2]
    sl = stats.linregress(ch.z, ch.n1)
    out["out-of-profile slope n1 on z, |z|<=2"] = pd.Series({"slope%": 100 * sl.slope, "t": sl.slope / sl.stderr, "n": len(ch)})
    return out
