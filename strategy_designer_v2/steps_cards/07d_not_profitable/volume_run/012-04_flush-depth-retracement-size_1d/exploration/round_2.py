def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    rec = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl, op, hi, lo, v = b["close"], b["open"], b["high"], b["low"], b["volume"]
            r1 = cl.pct_change()
            z = r1 / r1.rolling(20).std()
            vr = v / v.shift(1).rolling(20).mean()
            rng = (hi - lo).replace(0, np.nan)
            wick = (np.minimum(op, cl) - lo) / rng
            drop = (op - lo) / op
            r5 = cl / cl.shift(5) - 1
            r20 = cl / cl.shift(20) - 1
            df = pd.DataFrame(dict(z=z, vr=vr, wick=wick, drop=drop, r5=r5, r20=r20, coin=c, win=w,
                                   pos=np.arange(len(b))))
            for h in [1, 3, 5]:
                df[f"f{h}"] = cl.shift(-h) / cl - 1
            rec.append(df)
    D = pd.concat(rec, ignore_index=True)
    for h in [1, 3, 5]:
        g = D[D.pos % h == 0]
        mu = g.groupby("coin")[f"f{h}"].mean()
        D[f"x{h}"] = D[f"f{h}"] - D.coin.map(mu)
    E = D[(D.z <= -1.5) & (D.vr >= 1.5)].copy()
    out["n_event"] = len(E)
    def tb(df, col, q=4):
        df = df.copy()
        df["b"] = pd.qcut(df[col], q, duplicates="drop")
        gg = df.groupby("b")
        res = gg[["x1", "x3", "x5"]].mean().assign(n=gg.size())
        res["t3"] = gg["x3"].apply(lambda x: x.mean() / (x.std() / np.sqrt(x.count())))
        return res
    out["by_vr"] = tb(E, "vr")
    out["by_z"] = tb(E, "z")
    out["by_drop"] = tb(E, "drop")
    out["by_wick"] = tb(E, "wick")
    out["by_r20"] = tb(E, "r20")
    # correlations / slopes on x3 with vr (graded)
    sl = {}
    for col in ["vr", "z", "drop", "wick", "r20", "r5"]:
        e = E[[col, "x3"]].dropna()
        r = stats.linregress(e[col], e["x3"])
        sl[col] = pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(e)))
    out["slopes_x3"] = pd.DataFrame(sl).T
    # by coin and year-ish via window for event
    E2 = E.copy()
    out["event_by_coin"] = E2.groupby("coin")[["x1", "x3", "x5"]].mean().assign(n=E2.groupby("coin").size())
    return out
