def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 48
    drift = {}
    for c in bars:
        g = []
        for w, df in bars[c].items():
            cl = df["close"].values
            idx = np.arange(0, len(cl) - H, H)
            g.append(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.concatenate(g).mean()
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            cl = pd.Series(df["close"].values)
            r24 = cl.pct_change(24).values
            r168 = cl.pct_change(168).values
            r720 = cl.pct_change(720).values
            mabs = pd.Series(r24).abs().rolling(720).mean().values
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            f = df["forecast"].fillna(0).values
            al = df["postRebalance_current_allocation"].fillna(0).values
            clv = cl.values
            sel = np.where((hr == 23) & (np.arange(len(clv)) + H < len(clv)))[0]
            for i in sel:
                if np.isnan(r24[i]) or np.isnan(r168[i]) or np.isnan(mabs[i]) or r24[i] == 0:
                    continue
                tot = clv[i + H] / clv[i] - 1
                s = -np.sign(r24[i])
                rows.append({"coin": c, "w": w, "wd": wd[i], "sun": wd[i] == 6, "sig": f[i] != 0,
                             "s": s, "z": abs(r24[i]) / mabs[i],
                             "rev": s * tot, "rev_unu": s * (tot - drift[c]),
                             "tr7": np.sign(r168[i]) * (tot - drift[c]),
                             "tr30": np.sign(r720[i]) * (tot - drift[c]) if not np.isnan(r720[i]) else np.nan,
                             "with7": s == np.sign(r168[i]),
                             "with30": s == np.sign(r720[i]) if not np.isnan(r720[i]) else np.nan,
                             "r168up": r168[i] > 0,
                             "rel24_7": abs(r24[i]) / (abs(r168[i]) + 1e-9)})
    a = pd.DataFrame(rows)
    def m(x, col):
        x = x[col].dropna()
        return pd.Series({"n": len(x), "mean%": 100 * x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    res = {}
    # reversal by weekday x with-7d-trend (falsifier + control)
    res["rev_by_weekday_with7"] = a.groupby(["wd", "with7"]).apply(lambda x: m(x, "rev_unu")).unstack()
    # condition alone: 7d trend-following 48h from 23:00, Sunday vs other days
    res["trend7_alone_by_sun"] = a.groupby("sun").apply(lambda x: m(x, "tr7"))
    res["trend30_alone_by_sun"] = a.groupby("sun").apply(lambda x: m(x, "tr30"))
    s = a[a["sun"]].copy()
    # Sunday: with-trend split by size of Sunday move
    s["zq"] = pd.qcut(s["z"], 4, labels=False)
    res["sun_with7_by_zq"] = s.groupby(["zq", "with7"]).apply(lambda x: m(x, "rev_unu")).unstack()
    res["sun_with7_by_side"] = s.groupby(["with7", "s"]).apply(lambda x: m(x, "rev_unu"))
    res["sun_with30_with7"] = s.dropna(subset=["with30"]).groupby(["with30", "with7"]).apply(lambda x: m(x, "rev_unu"))
    # book: per-day returns split by allocation side, deepest fall windows
    out = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            al = df["postRebalance_current_allocation"].fillna(0).values
            cl = df["close"].values
            g = al[:-1] * (cl[1:] / cl[:-1] - 1)
            wn = int(w[1:])
            out.append({"wn": wn, "long_gain": g[al[:-1] > 0].sum(), "short_gain": g[al[:-1] < 0].sum(),
                        "coin_ret": cl[-1] / cl[0] - 1})
    o = pd.DataFrame(out).groupby("wn").mean()
    res["gain_by_side_window"] = o
    res["gain_by_side_total"] = o.sum().to_frame()
    return res
