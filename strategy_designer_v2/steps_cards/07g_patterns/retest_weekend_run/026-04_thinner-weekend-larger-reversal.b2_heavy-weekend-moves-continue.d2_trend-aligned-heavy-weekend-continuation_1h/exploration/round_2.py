def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    ev = []   # 20:00-22:00 close-to-close window per day
    mon = []  # Monday 23h anchors
    grid = [] # non-overlapping 48h grid cases
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values; n = len(c)
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values; yr = ts.dt.year.values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sd1 = pd.Series(r1).rolling(720, min_periods=240).std().values
            # bar with hour 19 starting -> close at 20:00; return over hours 20,21 = c[i+2]/c[i]-1
            for i in np.where(hr == 19)[0]:
                if i - 24 < 0 or i + 2 >= n or np.isnan(sd1[i]):
                    continue
                f = c[i + 2] / c[i] - 1
                p24 = c[i] / c[i - 24] - 1
                p7 = c[i] / c[i - 7] - 1  # 13:00..19:00 bars
                ev.append((coin, w, yr[i], wd[i], f, f / sd1[i], p24 / (sd1[i] * np.sqrt(24)), p7 / (sd1[i] * np.sqrt(7)), sd1[i]))
            for i in np.where((hr == 23) & (wd == 0))[0]:
                if i - 720 < 0 or i + 48 >= n:
                    continue
                s48 = sd1[i] * np.sqrt(48)
                if np.isnan(s48):
                    continue
                mon.append((coin, w, yr[i], (c[i] / c[i - 48] - 1) / s48, (c[i + 48] / c[i] - 1) / s48,
                            (c[i] / c[i - 24] - 1) / (sd1[i] * np.sqrt(24)), (c[i - 24] / c[i - 48] - 1) / (sd1[i] * np.sqrt(24))))
            for i in range(720, n - 48, 48):
                s48 = sd1[i] * np.sqrt(48)
                if np.isnan(s48):
                    continue
                grid.append((coin, w, yr[i], (c[i] / c[i - 48] - 1) / s48, np.sign(c[i - 48] / c[i - 720] - 1),
                             (c[i + 48] / c[i] - 1) / s48))
    E = pd.DataFrame(ev, columns=["coin", "win", "year", "wd", "f", "fz", "p24z", "p7z", "sd"])
    def mt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean_bp": x.mean() * 1e4, "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["h20_21_by_year"] = E.groupby("year")["f"].apply(mt).unstack()
    out["h20_21_by_coin"] = E.groupby("coin")["f"].apply(mt).unstack()
    out["h20_21_by_weekday"] = E.groupby("wd")["f"].apply(mt).unstack()
    E["volq"] = E.groupby("coin")["sd"].transform(lambda s: pd.qcut(s, 4, labels=False))
    out["h20_21_by_volq"] = E.groupby("volq")["f"].apply(mt).unstack()
    E["p24q"] = pd.qcut(E["p24z"], 5, labels=False)
    out["h20_21_by_prior24z_quint"] = E.groupby("p24q")["f"].apply(mt).unstack()
    E["p7q"] = pd.qcut(E["p7z"], 5, labels=False)
    out["h20_21_by_prior13_19z_quint"] = E.groupby("p7q")["f"].apply(mt).unstack()
    for k in ["p24z", "p7z"]:
        g = E[[k, "fz"]].dropna(); s = stats.linregress(g[k], g["fz"])
        out["slope_fz_on_" + k] = f"slope {s.slope:.4f} t {s.slope/s.stderr:.2f} n {len(g)}"
    M = pd.DataFrame(mon, columns=["coin", "win", "year", "p48", "f48", "pmon", "psun"])
    def sl(g, x):
        g = g.dropna()
        s = stats.linregress(g[x], g["f48"])
        return pd.Series({"n": len(g), "slope": s.slope, "t": s.slope / s.stderr})
    out["mon23_slope_by_year"] = M.groupby("year").apply(lambda g: sl(g, "p48"))
    out["mon23_slope_by_coin"] = M.groupby("coin").apply(lambda g: sl(g, "p48"))
    out["mon23_on_monday24h"] = sl(M, "pmon")
    out["mon23_on_sunday24h"] = sl(M, "psun")
    G = pd.DataFrame(grid, columns=["coin", "win", "year", "p", "trs", "f"])
    G["al"] = np.sign(G["p"]) == G["trs"]
    G["sf"] = np.sign(G["p"]) * G["f"]
    out["grid48_aligned"] = G.groupby("al")["sf"].apply(lambda x: pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})).unstack()
    out["grid48_aligned_by_year"] = G[G.al].groupby("year")["sf"].apply(lambda x: pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})).unstack()
    return out
