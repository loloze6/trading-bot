def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hrs = []
    for coin, wins in data["bars"].items():
        # drift per horizon over all windows
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            mabs = r1.abs().rolling(720, min_periods=240).mean().shift(1)
            z = r1 / mabs
            vr = v / v.rolling(720, min_periods=240).mean().shift(1)
            vol30 = r1.rolling(720, min_periods=240).std()
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "z": z, "vr": vr,
                               "vol": vol30, "ts": pd.to_datetime(b["timestamp"])})
            for h in (1, 2, 4, 6):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    for h in (1, 2, 4, 6):
        A[f"u{h}"] = A[f"f{h}"] - A.groupby("coin")[f"f{h}"].transform(lambda s: s[A.loc[s.index, "pos"] % h == 0].mean())
    A["zb"] = pd.cut(A["z"], [-np.inf, -5, -3, -1.5, 1.5, 3, 5, np.inf])
    A["vb"] = pd.cut(A["vr"], [0, 0.67, 1.5, 3, np.inf])
    res = []
    for h in (2, 4, 6):
        g = A[(A["pos"] % h == 0) & A[f"u{h}"].notna() & A["zb"].notna() & A["vb"].notna()]
        for (zb, vb), s in g.groupby(["zb", "vb"], observed=True)[f"u{h}"]:
            if len(s) < 20: continue
            res.append({"h": h, "z": str(zb), "vr": str(vb), "n": len(s), "mean_bp": s.mean()*1e4,
                        "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    R = pd.DataFrame(res)
    out["unusual fwd by z x volratio, h=2"] = R[R.h == 2].drop(columns="h").round(2)
    out["unusual fwd by z x volratio, h=6"] = R[R.h == 6].drop(columns="h").round(2)
    # signed continuation slope by vol bucket: regress u6 on z (clipped)
    sl = []
    for h in (2, 6):
        g = A[(A["pos"] % h == 0)].dropna(subset=[f"u{h}", "z", "vb"])
        for vb, s in g.groupby("vb", observed=True):
            x = s["z"].clip(-10, 10); y = s[f"u{h}"]
            r = stats.linregress(x, y)
            sl.append({"h": h, "vr": str(vb), "n": len(s), "slope_bp_per_z": r.slope*1e4, "t": r.slope/r.stderr})
    out["slope u on z by volratio"] = pd.DataFrame(sl).round(3)
    # hour-of-day 1h unusual return
    g = A.dropna(subset=["u1"])
    g = g.assign(hour=g["ts"].dt.hour, wd=g["ts"].dt.weekday)
    hh = g.groupby(["hour"])["u1"].agg(["count", "mean", "std"])
    hh["mean_bp"] = hh["mean"]*1e4; hh["t"] = hh["mean"]/(hh["std"]/np.sqrt(hh["count"]))
    out["hour of day u1"] = hh[["count", "mean_bp", "t"]].round(2)
    wd = g.groupby("wd")["u1"].agg(["count", "mean", "std"])
    wd["mean_bp"] = wd["mean"]*1e4; wd["t"] = wd["mean"]/(wd["std"]/np.sqrt(wd["count"]))
    out["weekday u1"] = wd[["count", "mean_bp", "t"]].round(2)
    # volatility level vs 6h abs-move continuation
    g6 = A[(A.pos % 6 == 0)].dropna(subset=["u6", "z", "vol"])
    g6 = g6.assign(volq=g6.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 4, labels=False)))
    vq = []
    for q, s in g6.groupby("volq"):
        r = stats.linregress(s["z"].clip(-10, 10), s["u6"])
        vq.append({"volq": q, "n": len(s), "slope_bp": r.slope*1e4, "t": r.slope/r.stderr})
    out["vol quartile slope u6 on z"] = pd.DataFrame(vq).round(3)
    # book: daily by year, trades
    d = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            d.append(x.assign(coin=coin, win=w))
    D = pd.concat(d); D["year"] = pd.to_datetime(D["day"]).dt.year
    out["book by year"] = D.groupby("year")[["book_return", "coin_return"]].mean().mul(1e4).round(2)
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    T["fb"] = pd.qcut(T["entry_forecast"].abs(), 4, duplicates="drop")
    out["trades by |entry forecast|"] = T.groupby("fb", observed=True)[["profit_loss_percent", "net_profit_loss_percent"]].agg(["count", "mean"]).round(4)
    return out
