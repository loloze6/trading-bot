def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().rolling(720, min_periods=240).mean().shift(1)
            z = r1 / mabs
            vr = v / v.rolling(720, min_periods=240).mean().shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "vr": vr,
                               "ts": ts, "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "r1": r1})
            for h in (1, 2, 3, 4, 6):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 3, 4, 6):
        dr = A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = A[f"f{h}"] - A["coin"].map(dr)
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean_bp": s.mean()*1e4, "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    # 1) hour 20-21 drift: per coin, per year; next-hour return from close of bar opening at 19 (covers 20) etc
    g = A.dropna(subset=["u1"])
    hz = g[g.hour.isin([20, 21])]
    out["h20-21 u1 by coin"] = hz.groupby("coin")["u1"].apply(tt).unstack().round(2)
    out["h20-21 u1 by year"] = hz.groupby("year")["u1"].apply(tt).unstack().round(2)
    out["h20-21 u1 by weekday"] = hz.groupby("wd")["u1"].apply(tt).unstack().round(2)
    h02 = g[g.hour.isin([0, 1, 2])]
    out["h0-2 u1 by year"] = h02.groupby("year")["u1"].apply(tt).unstack().round(2)
    out["thursday u1 by year"] = g[g.wd == 3].groupby("year")["u1"].apply(tt).unstack().round(2)
    # 2) high-volume reversal: slope of u_h on z among vr>3, by coin, by year, by horizon; sign by direction
    sl = []
    for h in (1, 2, 3, 4, 6):
        s = A[(A.pos % h == 0) & (A.vr > 3)].dropna(subset=[f"u{h}", "z"])
        for coin, q in s.groupby("coin"):
            r = stats.linregress(q["z"].clip(-10, 10), q[f"u{h}"])
            sl.append({"h": h, "coin": coin, "n": len(q), "slope_bp": r.slope*1e4, "t": r.slope/r.stderr})
    out["vr>3 slope u on z by h, coin"] = pd.DataFrame(sl).round(3)
    s = A[(A.pos % 2 == 0) & (A.vr > 3)].dropna(subset=["u2", "z"])
    yy = []
    for y, q in s.groupby("year"):
        r = stats.linregress(q["z"].clip(-10, 10), q["u2"])
        yy.append({"year": y, "n": len(q), "slope_bp": r.slope*1e4, "t": r.slope/r.stderr})
    out["vr>3 slope u2 on z by year"] = pd.DataFrame(yy).round(3)
    # graded by volume among |z|>2: reversal signed move
    s = A[(A.pos % 2 == 0)].dropna(subset=["u2", "z", "vr"])
    s = s[s.z.abs() > 2].copy()
    s["rev"] = -np.sign(s.z) * s.u2
    s["vb"] = pd.cut(s.vr, [0, 1, 1.5, 2, 3, 5, np.inf])
    out["|z|>2 reversal u2 by volratio"] = s.groupby(["vb"], observed=True)["rev"].apply(tt).unstack().round(2)
    s["dir"] = np.where(s.z > 0, "up", "down")
    out["|z|>2 & vr>3 reversal by dir"] = s[s.vr > 3].groupby("dir")["rev"].apply(tt).unstack().round(2)
    # 3) book's worst/best days: coin moves
    d = pd.concat([x.assign(coin=c, win=w) for c, ws in data["days"].items() for w, x in ws.items()])
    d = d.dropna(subset=["book_return"])
    d["bq"] = pd.qcut(d.book_return, 5, labels=False)
    out["book quintile vs coin day"] = d.groupby("bq")[["book_return", "coin_return"]].agg(["mean"]).mul(1e4).round(1)
    return out
