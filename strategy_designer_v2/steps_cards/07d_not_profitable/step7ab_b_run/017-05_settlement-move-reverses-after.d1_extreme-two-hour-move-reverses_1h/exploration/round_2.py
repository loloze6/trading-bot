def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    cases = []; pos = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            vol = r1.rolling(20).std()
            z = (c / c.shift(2) - 1) / (vol * np.sqrt(2))
            ts = pd.to_datetime(df["timestamp"], utc=True)
            closeh = ((ts.dt.hour + 1) % 24).values
            fwd = c.shift(-24) / c - 1
            vol30 = r1.rolling(720, min_periods=240).std()
            ret24 = c / c.shift(24) - 1
            trendz = ret24 / (vol * np.sqrt(24))
            cases.append(pd.DataFrame({"coin": coin, "z": z.values, "fwd": fwd.values, "ch": closeh,
                                       "vol30": vol30.values, "trz": trendz.values}))
            alloc = df["postRebalance_current_allocation"].astype(float)
            g = alloc * (c.shift(-1) / c - 1)
            fc = df["forecast"].astype(float)
            pos.append(pd.DataFrame({"coin": coin, "g": g.values, "alloc": alloc.values, "fc": fc.values,
                                     "z": z.values, "ch": closeh}))
    C = pd.concat(cases, ignore_index=True).dropna()
    C["drift"] = C.groupby("coin")["fwd"].transform("mean")
    C["unus"] = -np.sign(C["z"]) * (C["fwd"] - C["drift"])
    C["az"] = C["z"].abs()
    C["q"] = pd.qcut(C["az"], 5, labels=False)
    # non-overlap: each close-hour series is spaced 24 bars apart already (per hour ~ once per day)
    def summ(g):
        n = len(g); m = g["unus"].mean(); s = g["unus"].std()
        return pd.Series({"n": n, "unus_bps": m*1e4, "t": m/(s/np.sqrt(n))})
    top = C[C.q == 4]
    out = {}
    out["top_by_close_hour"] = top.groupby("ch").apply(summ)
    top = top.copy()
    top["vt"] = pd.qcut(top["vol30"], 3, labels=False)
    top["settle"] = top["ch"].isin([0, 8, 16])
    out["top_settle_x_vol"] = top.groupby(["settle", "vt"]).apply(summ)
    # move against 24h trend vs with
    top["against"] = np.sign(top["z"]) != np.sign(top["trz"])
    out["top_settle_x_against_trend"] = top.groupby(["settle", "against"]).apply(summ)
    P = pd.concat(pos, ignore_index=True).dropna()
    P["agree"] = np.sign(P["alloc"]) == np.sign(P["fc"])
    P["fcb"] = pd.cut(P["fc"].abs(), [-0.01, 0.5, 2.5, 7, 14, 20.01])
    out["book_by_absfc"] = P.groupby("fcb").agg(n=("g", "size"), gain_bps=("g", lambda x: x.mean()*1e4),
                                                 absalloc=("alloc", lambda x: x.abs().mean()),
                                                 agree=("agree", "mean"))
    P["sgn_fade_now"] = np.sign(P["alloc"]) == -np.sign(P["z"])
    out["book_overall"] = pd.Series({"gain_bps_per_bar": P["g"].mean()*1e4,
                                     "share_pos_with_forecast": P["agree"].mean(),
                                     "share_pos_fading_current_2h": P["sgn_fade_now"].mean(),
                                     "corr_alloc_fc": P["alloc"].corr(P["fc"])})
    return out
