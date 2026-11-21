def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    # per-hour reversal: 2h vol-scaled return at close hour H vs next 24h excess return
    rows = []
    daily_rows = []
    hour_rows = []
    for coin, ws in bars.items():
        # coin mean 24h return on grid
        g24 = []
        for w, df in ws.items():
            c = df["close"].values
            if len(c) > 24:
                idx = np.arange(0, len(c) - 24, 24)
                g24.append(c[idx + 24] / c[idx] - 1)
        mu24 = np.concatenate(g24).mean() if g24 else 0
        for w, df in ws.items():
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std() * np.sqrt(2)
            x = (c / c.shift(2) - 1) / vol
            f24 = c.shift(-24) / c - 1 - mu24
            ch = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            d = pd.DataFrame({"x": x.values, "y": f24.values, "h": ch, "coin": coin,
                              "r1": r1.values, "v": df["volume"].astype(float).values,
                              "wd": (ts + pd.Timedelta(hours=1)).dt.weekday.values,
                              "yr": ts.dt.year.values})
            rows.append(d)
            # daily grid: close at 00 UTC
            dd = d[d.h == 0].copy()
            cc = c[d.h.values == 0].values
            if len(cc) > 12:
                dr = pd.Series(cc).pct_change()
                dvol = dr.rolling(20).std()
                for H in (1, 3, 5, 10):
                    fw = pd.Series(cc).shift(-H) / pd.Series(cc) - 1
                    daily_rows.append(pd.DataFrame({"coin": coin, "H": H, "x1": (dr / dvol).values,
                                                    "x5": ((pd.Series(cc) / pd.Series(cc).shift(5) - 1) / (dvol * np.sqrt(5))).values,
                                                    "y": fw.values, "dvol": dvol.values,
                                                    "pos": np.arange(len(cc))}))
    D = pd.concat(rows, ignore_index=True)
    # per hour slope
    res = []
    for h in range(24):
        s = D[(D.h == h)].dropna(subset=["x", "y"])
        s = s[np.isfinite(s.x)]
        lr = stats.linregress(s.x.clip(-6, 6), s.y)
        xs = s.x.clip(-6, 6)
        top = s[xs.abs() >= xs.abs().quantile(2/3)]
        res.append({"hour": h, "n": len(s), "slope_bps": lr.slope * 1e4, "t": lr.slope / lr.stderr,
                    "top3_rev_bps": (-np.sign(top.x) * top.y).mean() * 1e4})
    out["per_hour_2h_vs_24h"] = pd.DataFrame(res)
    # hour of day mean return and volume share
    D["vrel"] = D.v / D.groupby("coin").v.transform("median")
    hr = D.dropna(subset=["r1"]).groupby("h").agg(mean_r_bps=("r1", lambda z: z.mean() * 1e4),
                                                  t=("r1", lambda z: z.mean() / z.std() * np.sqrt(len(z))),
                                                  vol_rel=("vrel", "median"))
    out["hour_of_day"] = hr
    out["weekday_hourly_ret"] = D.dropna(subset=["r1"]).groupby("wd").r1.agg(
        mean_bps=lambda z: z.mean() * 1e4, t=lambda z: z.mean() / z.std() * np.sqrt(len(z)), n="count")
    # daily reversal / continuation, non-overlapping grid per H
    R = pd.concat(daily_rows, ignore_index=True)
    dres = []
    for H, s in R.groupby("H"):
        s = s[s.pos % H == 0].dropna()
        s = s[np.isfinite(s.x1) & np.isfinite(s.x5)]
        for xc in ("x1", "x5"):
            xv = s[xc].clip(-6, 6)
            mu = s.groupby("coin").y.transform("mean")
            y = s.y - mu
            lr = stats.linregress(xv, y)
            top = xv.abs() >= xv.abs().quantile(2/3)
            sgn = (np.sign(xv) * y)[top]
            dres.append({"H_days": H, "x": xc, "n": len(s), "slope_bps": lr.slope * 1e4,
                         "t": lr.slope / lr.stderr, "top3_signed_excess_bps": sgn.mean() * 1e4,
                         "top3_t": sgn.mean() / sgn.std() * np.sqrt(len(sgn)),
                         "usual_move_pct": s.y.std() * 100})
    out["daily_signal_vs_next"] = pd.DataFrame(dres)
    # book
    bk = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            t = df.copy(); t["coin"] = coin; t["w"] = w
            t["yr"] = pd.to_datetime(t["day"]).dt.year
            bk.append(t)
    B = pd.concat(bk, ignore_index=True)
    bd = B.dropna(subset=["book_return"])
    out["book_by_year"] = bd.groupby("yr").agg(book_bps=("book_return", lambda z: z.mean() * 1e4),
                                              coin_bps=("coin_return", lambda z: z.mean() * 1e4), n=("book_return", "count"))
    out["book_by_coin"] = bd.groupby("coin").agg(book_bps=("book_return", lambda z: z.mean() * 1e4),
                                                coin_bps=("coin_return", lambda z: z.mean() * 1e4))
    return out
