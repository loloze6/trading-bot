def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            if n < 220: continue
            r1 = c.pct_change()
            vol = r1.rolling(180).std()
            z1 = r1 / vol.shift(1)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "z1": z1, "vol": vol,
                               "f18": c.shift(-18) / c - 1, "f6": c.shift(-6) / c - 1,
                               "f36": c.shift(-36) / c - 1, "r1n": r1.shift(-1),
                               "hour": ts.dt.hour, "wd": ts.dt.weekday, "year": ts.dt.year,
                               "mom180": c / c.shift(180) - 1})
            df["pos"] = np.arange(n)
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    drifts = {}
    for h, col in [(6, "f6"), (18, "f18"), (36, "f36")]:
        drifts[col] = A[A.pos % h == 0].groupby("coin")[col].mean()
        A["ex" + col] = A[col] - A["coin"].map(drifts[col])
    usual = A[A.pos % H == 0].groupby("coin")["f18"].std()
    A["s18"] = A["exf18"] / A["coin"].map(usual)
    # event study: down bars z<=-2, de-overlapped (no event within 18 bars of previous kept event, per window)
    def events(mask):
        keep = []
        for (coin, w), g in A[mask].groupby(["coin", "w"]):
            last = -10**9
            for i, p in zip(g.index, g.pos):
                if p - last >= H:
                    keep.append(i); last = p
        return A.loc[keep]
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    E = events(A.z1 <= -2)
    E["zb"] = pd.cut(E["z1"], [-np.inf, -4, -3, -2.5, -2])
    out["down_z_bins_ex18"] = E.groupby("zb").apply(lambda g: summ(g, "exf18"))
    out["down_z_bins_ex6"] = E.groupby("zb").apply(lambda g: summ(g, "exf6"))
    out["down_z_bins_ex36"] = E.groupby("zb").apply(lambda g: summ(g, "exf36"))
    out["down_by_coin"] = E.groupby("coin").apply(lambda g: summ(g, "exf18"))
    out["down_by_year"] = E.groupby("year").apply(lambda g: summ(g, "exf18"))
    out["down_by_mom"] = E.groupby(np.sign(E["mom180"])).apply(lambda g: summ(g, "exf18"))
    out["down_strength"] = summ(E, "s18")
    sp = stats.spearmanr(-E["z1"], E["exf18"], nan_policy="omit")
    out["down_spearman_neg_z_vs_ex18"] = pd.Series({"rho": sp.correlation, "p": sp.pvalue, "n": E["exf18"].notna().sum()})
    U = events(A.z1 >= 2)
    U["zb"] = pd.cut(U["z1"], [2, 2.5, 3, 4, np.inf])
    out["up_z_bins_ex18"] = U.groupby("zb").apply(lambda g: summ(g, "exf18"))
    # hour 16 and friday per coin and year
    A["h16"] = A.hour == 16
    out["h16_by_coin"] = A[A.h16].groupby("coin").apply(lambda g: summ(g, "r1n"))
    out["h16_by_year"] = A[A.h16].groupby("year").apply(lambda g: summ(g, "r1n"))
    out["fri_by_coin"] = A[A.wd == 4].groupby("coin").apply(lambda g: summ(g, "r1n"))
    out["fri_hour"] = A[A.wd == 4].groupby("hour").apply(lambda g: summ(g, "r1n"))
    # book around largest losses/gains days
    D = pd.concat([d.assign(coin=c, w=w) for c, ws in data["days"].items() for w, d in ws.items()], ignore_index=True)
    D = D.dropna(subset=["book_return"])
    D["bq"] = D.groupby("coin")["book_return"].transform(lambda s: pd.qcut(s.rank(method="first"), 10, labels=False))
    out["book_decile_coinret"] = D.groupby("bq")[["book_return", "coin_return"]].mean()
    return out
