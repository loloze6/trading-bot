def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    g24 = []; h2 = []; hh = []
    for coin, wins in bars.items():
        r = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            r.append(c[idx + 24] / c[idx] - 1)
        d24 = np.concatenate(r).mean()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; ts = pd.to_datetime(df["timestamp"])
            yr = ts.dt.year.values; hr = ((ts.dt.hour + 1) % 24).values
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=200).std()
            vol_rel = vol / vol.rolling(2160, min_periods=500).median()
            rp = c / c.shift(24) - 1
            sp = rp / rp.abs().rolling(720, min_periods=200).mean()
            f = c.shift(-24) / c - 1 - d24
            idx = np.arange(0, len(c), 24)
            g24.append(pd.DataFrame({"coin": coin, "w": w, "yr": yr[idx], "sp": sp.values[idx],
                                     "f": f.values[idx], "vol": vol.values[idx],
                                     "vrel": vol_rel.values[idx]}))
            r2 = c / c.shift(2) - 1
            s2 = r2 / r2.abs().rolling(720, min_periods=200).mean()
            m = np.isin(hr, [0, 1, 2])
            h2.append(pd.DataFrame({"coin": coin, "yr": yr[m], "hour": hr[m], "s2": s2.values[m],
                                    "f": f.values[m], "r24": sp.values[m]}))
            hh.append(pd.DataFrame({"coin": coin, "yr": yr, "hour": hr, "fwd1": r1.shift(-1).values}))
    out = {}
    G = pd.concat(g24).dropna()
    G["vt"] = G.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False))
    H = G[G["vt"] == 2]
    rows = []
    for k, g in H.groupby("coin"):
        sl = stats.linregress(g["sp"], g["f"]); fl = g[g["sp"] < 0]
        rows.append({"coin": k, "n": len(g), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr,
                     "fall_mean_pct": fl["f"].mean()*100, "n_fall": len(fl)})
    out["hivol_24h_rev_by_coin"] = pd.DataFrame(rows).round(3)
    rows = []
    for k, g in H.groupby("yr"):
        sl = stats.linregress(g["sp"], g["f"])
        rows.append({"yr": k, "n": len(g), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["hivol_24h_rev_by_year"] = pd.DataFrame(rows).round(3)
    F = H[H["sp"] < 0].copy()
    F["d"] = pd.qcut(F["sp"], 5, labels=False)
    out["hivol_falls_graded"] = F.groupby("d").agg(n=("f", "size"), sp=("sp", "mean"),
        f_pct=("f", lambda x: x.mean()*100), t=("f", lambda x: x.mean()/x.std()*np.sqrt(len(x)))).round(3)
    R = H[H["sp"] > 0].copy()
    R["d"] = pd.qcut(R["sp"], 5, labels=False)
    out["hivol_rises_graded"] = R.groupby("d").agg(n=("f", "size"), sp=("sp", "mean"),
        f_pct=("f", lambda x: x.mean()*100), t=("f", lambda x: x.mean()/x.std()*np.sqrt(len(x)))).round(3)
    # interaction: slope by vol relative (own-history) tercile
    G["vrt"] = pd.qcut(G["vrel"], 3, labels=False)
    rows = []
    for k, g in G.groupby("vrt"):
        sl = stats.linregress(g["sp"], g["f"])
        rows.append({"vrel_tercile": k, "n": len(g), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["24h_rev_by_relative_vol"] = pd.DataFrame(rows).round(3)
    # 2h fall at 00-02 UTC: by coin and year, and controlling for 24h move
    A = pd.concat(h2).dropna()
    rows = []
    for k, g in A.groupby("coin"):
        sl = stats.linregress(g["s2"], g["f"])
        rows.append({"coin": k, "n": len(g), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["2h_at_00_02_by_coin"] = pd.DataFrame(rows).round(3)
    rows = []
    for k, g in A.groupby("yr"):
        sl = stats.linregress(g["s2"], g["f"])
        rows.append({"yr": k, "n": len(g), "slope_bp": sl.slope*1e4, "t": sl.slope/sl.stderr})
    out["2h_at_00_02_by_year"] = pd.DataFrame(rows).round(3)
    X = np.column_stack([np.ones(len(A)), A["s2"], A["r24"]])
    b, *_ = np.linalg.lstsq(X, A["f"].values, rcond=None)
    res = A["f"].values - X @ b
    cov = np.linalg.inv(X.T @ X) * res.var(ddof=3)
    out["2h_at_00_02_with_24h_control"] = pd.DataFrame({"coef_bp": b*1e4, "t": b/np.sqrt(np.diag(cov))},
                                                      index=["const", "s2", "s24"]).round(3)
    Hh = pd.concat(hh).dropna()
    Hh = Hh[Hh["hour"].isin([21, 22])]
    out["hour21_22_next1h_by_year"] = Hh.groupby("yr").agg(n=("fwd1", "size"),
        bp=("fwd1", lambda x: x.mean()*1e4), t=("fwd1", lambda x: x.mean()/x.std()*np.sqrt(len(x)))).round(3)
    # book: daily returns by weekday
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.weekday; D.append(d)
    D = pd.concat(D).dropna(subset=["book_return", "coin_return"])
    out["book_by_weekday"] = D.groupby("wd").agg(book_bp=("book_return", lambda x: x.mean()*1e4),
        coin_bp=("coin_return", lambda x: x.mean()*1e4), n=("book_return", "size")).round(2)
    return out
