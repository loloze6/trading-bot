def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 26
    rows = []
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            hi = b["high"].astype(float); lo = b["low"].astype(float)
            n = len(c)
            if n < 30:
                continue
            cs = pd.Series(c)
            lr = np.log(cs).diff()
            vol20 = lr.rolling(20).std()
            past26 = cs / cs.shift(26) - 1
            past10 = cs / cs.shift(10) - 1
            past5 = cs / cs.shift(5) - 1
            mid26 = (hi.rolling(26).max() + lo.rolling(26).min()) / 2
            pos26 = cs / mid26 - 1
            rng26 = (hi.rolling(26).max() - lo.rolling(26).min()) / cs
            nearhi = cs / hi.rolling(26).max() - 1
            ma26 = cs.rolling(26).mean()
            trend = cs / ma26 - 1
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, fwd=c[i + H] / c[i] - 1,
                                 past26=past26[i], past10=past10[i], past5=past5[i],
                                 vol20=vol20[i], pos26=pos26[i], rng26=rng26[i],
                                 nearhi=nearhi[i], trend=trend[i],
                                 reg=b["regime"].iloc[i], fc=b["forecast"].iloc[i]))
            ts = pd.to_datetime(b["timestamp"])
            r1 = cs.pct_change()
            for i in range(1, n - 1):
                drows.append(dict(coin=coin, w=w, r=r1[i], nxt=c[i + 1] / c[i] - 1,
                                  vol=vol20[i], wd=ts.iloc[i + 1].dayofweek,
                                  nxt5=(c[i + 5] / c[i] - 1) if i + 5 < n else np.nan,
                                  i5=i % 5))
    df = pd.DataFrame(rows)
    df["ex"] = df["fwd"] - df.groupby("coin")["fwd"].transform("mean")
    out["n_cases_by_regime"] = df.groupby("reg")["ex"].agg(["count", "mean"])
    feats = ["past26", "past10", "past5", "vol20", "pos26", "rng26", "nearhi", "trend"]
    res = []
    for f in feats:
        d = df.dropna(subset=[f, "ex"]).copy()
        d["z"] = d.groupby("coin")[f].transform(lambda x: (x - x.mean()) / x.std())
        d = d.dropna(subset=["z"])
        if len(d) < 30:
            continue
        s = stats.linregress(d["z"], d["ex"])
        q = pd.qcut(d["z"], 5, labels=False, duplicates="drop")
        qm = d.groupby(q)["ex"].mean()
        # per-coin slope signs
        signs = sum(1 for _, g in d.groupby("coin") if len(g) > 10 and stats.linregress(g["z"], g["ex"]).slope > 0)
        res.append(dict(feat=f, n=len(d), slope=s.slope, t=s.slope / s.stderr,
                        q1=qm.iloc[0], q5=qm.iloc[-1], coins_pos=signs))
    out["fwd26_on_features"] = pd.DataFrame(res)
    # in-regime only
    d = df[df.reg == "trending"].dropna(subset=["past26"]).copy()
    res = []
    for f in ["past26", "vol20", "rng26", "trend", "fc"]:
        dd = d.dropna(subset=[f])
        if len(dd) > 20 and dd[f].std() > 0:
            s = stats.linregress(dd[f], dd["ex"]); res.append(dict(feat=f, n=len(dd), t=s.slope / s.stderr))
    out["in_regime_features"] = pd.DataFrame(res)
    dd = pd.DataFrame(drows).dropna(subset=["r", "nxt", "vol"])
    dd["zr"] = dd["r"] / dd["vol"]
    dd["exn"] = dd["nxt"] - dd.groupby("coin")["nxt"].transform("mean")
    dd["zb"] = pd.cut(dd["zr"], [-99, -2, -1, 0, 1, 2, 99])
    out["next_day_after_move"] = dd.groupby("zb")["exn"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    g5 = dd[dd.i5 == 0].dropna(subset=["nxt5"]).copy()
    g5["ex5"] = g5["nxt5"] - g5.groupby("coin")["nxt5"].transform("mean")
    g5["zb"] = pd.cut(g5["zr"], [-99, -2, -1, 0, 1, 2, 99])
    out["next5d_after_move"] = g5.groupby("zb")["ex5"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["weekday_next_day"] = dd.groupby("wd")["exn"].agg(["count", "mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    dd["vq"] = dd.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 4, labels=False))
    out["next_day_by_volq"] = dd.groupby("vq")["nxt"].agg(["count", "mean", "std"])
    # book by regime share
    bk = []
    for coin, wins in data["days"].items():
        for w, d2 in wins.items():
            bk.append(d2.assign(coin=coin, w=w))
    bk = pd.concat(bk)
    out["book_vs_coin"] = bk[["book_return", "coin_return"]].describe().T
    return out
