def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    H_rows, D_rows = [], []
    for coin, ws in bars.items():
        g = {}
        for H in (1, 3, 10, 20):
            arr = []
            for w, df in ws.items():
                ts = pd.to_datetime(df["timestamp"]); c = df["close"].astype(float).values
                ch = (ts + pd.Timedelta(hours=1)).dt.hour.values
                cc = c[ch == 0]
                if len(cc) > H:
                    idx = np.arange(0, len(cc) - H, H); arr.append(cc[idx + H] / cc[idx] - 1)
            g[H] = np.concatenate(arr).mean() if arr else 0
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"]); c = df["close"].astype(float)
            ch = (ts + pd.Timedelta(hours=1)).dt.hour.values
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            d = pd.DataFrame({"h": ch, "r1": r1.values, "yr": ts.dt.year.values,
                              "wd": (ts + pd.Timedelta(hours=1)).dt.weekday.values, "coin": coin,
                              "x2": ((c / c.shift(2) - 1) / (vol * np.sqrt(2))).values,
                              "x3": ((c / c.shift(3) - 1) / (vol * np.sqrt(3))).values,
                              "y24": (c.shift(-24) / c - 1).values,
                              "y72": (c.shift(-72) / c - 1).values})
            H_rows.append(d)
            m = ch == 0
            cc = pd.Series(c.values[m]); yrs = ts.dt.year.values[m]
            wdd = (ts + pd.Timedelta(hours=1)).dt.weekday.values[m]
            dr = cc.pct_change(); dvol = dr.rolling(20).std()
            for H in (1, 3, 10, 20):
                D_rows.append(pd.DataFrame({"coin": coin, "H": H, "yr": yrs, "wd": wdd,
                    "x1": (dr / dvol).values,
                    "x5": ((cc / cc.shift(5) - 1) / (dvol * np.sqrt(5))).values,
                    "x20": ((cc / cc.shift(20) - 1) / (dvol * np.sqrt(20))).values,
                    "dvol": dvol.values, "dvolrank": (dvol / dvol.rolling(120, min_periods=40).median()).values,
                    "dr": dr.values,
                    "y": (cc.shift(-H) / cc - 1 - g[H]).values, "pos": np.arange(len(cc))}))
    D = pd.concat(H_rows, ignore_index=True)
    # evening drift: bars closing 22 and 23 summed per day
    ev = D[D.h.isin([22, 23])].dropna(subset=["r1"])
    out["evening_drift_22_23_by_year"] = ev.groupby("yr").r1.agg(mean_bps=lambda z: z.mean() * 1e4,
        t=lambda z: z.mean() / z.std() * np.sqrt(len(z)), n="count")
    out["evening_drift_by_coin"] = ev.groupby("coin").r1.agg(mean_bps=lambda z: z.mean() * 1e4,
        t=lambda z: z.mean() / z.std() * np.sqrt(len(z)))
    # 2h/3h move into 01:00 close vs next 24h and 72h
    res = []
    for hh, xc in ((1, "x2"), (1, "x3"), (0, "x2")):
        s = D[D.h == hh].dropna(subset=[xc, "y24"]); s = s[np.isfinite(s[xc])]
        for yc in ("y24", "y72"):
            ss = s.dropna(subset=[yc])
            if yc == "y72":
                ss = ss.groupby("coin", group_keys=False).apply(lambda z: z.iloc[::3])
            y = ss[yc] - ss.groupby("coin")[yc].transform("mean")
            xv = ss[xc].clip(-6, 6)
            lr = stats.linregress(xv, y)
            top = xv.abs() >= xv.abs().quantile(2/3)
            rv = (-np.sign(xv) * y)[top]
            res.append({"close_h": hh, "x": xc, "y": yc, "n": len(ss), "t": lr.slope / lr.stderr,
                        "top3_rev_bps": rv.mean() * 1e4, "top3_t": rv.mean() / rv.std() * np.sqrt(len(rv))})
    out["night_move_reversal"] = pd.DataFrame(res)
    s = D[D.h == 1].dropna(subset=["x2", "y24"]); s = s[np.isfinite(s.x2)]
    s["y"] = s.y24 - s.groupby("coin").y24.transform("mean"); xv = s.x2.clip(-6, 6)
    s["rv"] = -np.sign(xv) * s.y; s["top"] = xv.abs() >= xv.abs().quantile(2/3)
    out["night01_top3_rev_by_year"] = s[s.top].groupby("yr").rv.agg(bps=lambda z: z.mean() * 1e4,
        t=lambda z: z.mean() / z.std() * np.sqrt(len(z)), n="count")
    # daily
    R = pd.concat(D_rows, ignore_index=True)
    res = []; yrres = []
    for H, s in R.groupby("H"):
        s = s[s.pos % H == 0].dropna(subset=["x1", "x5", "x20", "y"])
        s = s[np.isfinite(s.x1) & np.isfinite(s.x5) & np.isfinite(s.x20)]
        for xc in ("x1", "x5", "x20"):
            xv = s[xc].clip(-6, 6); lr = stats.linregress(xv, s.y)
            top = xv.abs() >= xv.abs().quantile(2/3); sg = (np.sign(xv) * s.y)[top]
            res.append({"H": H, "x": xc, "n": len(s), "t": lr.slope / lr.stderr,
                        "top3_signed_bps": sg.mean() * 1e4, "top3_t": sg.mean() / sg.std() * np.sqrt(len(sg))})
            if (H, xc) in ((10, "x5"), (20, "x20"), (1, "x1")):
                tmp = s[top].assign(sg=sg)
                k = tmp.groupby("yr").sg.agg(bps=lambda z: z.mean() * 1e4, n="count")
                k.index = [f"H{H}_{xc}_{i}" for i in k.index]; yrres.append(k)
        if H == 1:
            s2 = s.dropna(subset=["dvolrank"]).copy()
            s2["vq"] = pd.qcut(s2.dvolrank, 3, labels=["lowvol", "mid", "highvol"])
            s2["rv"] = -np.sign(s2.x1) * s2.y
            s2["big"] = s2.x1.abs() >= s2.x1.abs().quantile(2/3)
            out["daily1_reversal_by_volregime"] = s2[s2.big].groupby("vq").rv.agg(
                bps=lambda z: z.mean() * 1e4, t=lambda z: z.mean() / z.std() * np.sqrt(len(z)), n="count")
            out["daily_excess_by_weekday_of_close"] = s.groupby("wd").y.agg(bps=lambda z: z.mean() * 1e4,
                t=lambda z: z.mean() / z.std() * np.sqrt(len(z)), n="count")
    out["daily_signals"] = pd.DataFrame(res)
    out["daily_top3_by_year"] = pd.concat(yrres)
    return out
