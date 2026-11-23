def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        nn8 = []; nn3 = []
        for w, b in wins.items():
            c = b["close"].values
            i8 = np.arange(0, len(c) - 8, 8); nn8.append(c[i8 + 8] / c[i8] - 1)
            i3 = np.arange(0, len(c) - 3, 3); nn3.append(c[i3 + 3] / c[i3] - 1)
        nn8 = np.concatenate(nn8); nn3 = np.concatenate(nn3)
        d8, u8 = nn8.mean(), nn8.std(); d3, u3 = nn3.mean(), nn3.std()
        for w, b in wins.items():
            ts = pd.to_datetime(b["timestamp"])
            ch = ((ts + pd.Timedelta(hours=1)).dt.hour).values
            c = b["close"]
            r2 = c / c.shift(2) - 1
            z = r2 / r2.abs().rolling(720, min_periods=240).mean()
            r24 = c / c.shift(24) - 1
            z24 = r24 / r24.abs().rolling(720, min_periods=240).mean()
            f8 = c.shift(-8) / c - 1
            f3 = c.shift(-3) / c - 1
            rows.append(pd.DataFrame({"coin": coin, "w": w, "ch": ch, "z": z.values, "z24": z24.values,
                "f8s": ((f8 - d8) / u8).values, "f8": (f8 - d8).values,
                "f3s": ((f3 - d3) / u3).values, "f3": (f3 - d3).values,
                "yr": ts.dt.year.values}))
    D = pd.concat(rows, ignore_index=True)
    # 1) midnight 2h reversal: close hours 0,1,2 ; signed product -sign... use -z*f8s
    M = D[D.ch.isin([0, 1, 2])].dropna(subset=["z", "f8s"]).copy()
    M["p"] = -M.z * M.f8s
    M["dec"] = pd.qcut(M.z, 10, labels=False)
    out["midnight_f8_by_z_decile"] = M.groupby("dec").agg(z=("z", "mean"), f8s=("f8s", "mean"),
        f8_bp=("f8", lambda s: s.mean() * 1e4), n=("f8s", "size")).round(4)
    def tt(s): return s.mean() / s.std() * np.sqrt(len(s))
    M1 = M[M.ch == 1]
    out["h1_rev_by_coin"] = M1.groupby("coin")["p"].agg(["mean", tt, "size"]).round(4)
    out["h1_rev_by_year"] = M1.groupby("yr")["p"].agg(["mean", tt, "size"]).round(4)
    # 2) 24h momentum at 16: by coin, year; and at other hours
    S = D.dropna(subset=["z24", "f8s"]).copy()
    S["p"] = S.z24 * S.f8s
    out["z24_mom_t_by_close_hour"] = S.groupby("ch")["p"].agg(["mean", tt, "size"]).round(4)
    S16 = S[S.ch == 16].copy()
    S16["q"] = pd.qcut(S16.z24, 5, labels=False)
    out["at16_f8_by_z24_quintile"] = S16.groupby("q").agg(z24=("z24", "mean"), f8s=("f8s", "mean"),
        f8_bp=("f8", lambda s: s.mean() * 1e4), n=("f8s", "size")).round(4)
    out["at16_z24mom_by_coin"] = S16.groupby("coin")["p"].agg(["mean", tt, "size"]).round(4)
    out["at16_z24mom_by_year"] = S16.groupby("yr")["p"].agg(["mean", tt, "size"]).round(4)
    # 3) evening 3h drift from close hour 20 (hours 21,22,23 returns): by coin/year, graded by z24
    E = D[D.ch == 20].dropna(subset=["f3", "z24"]).copy()
    out["eve3h_by_coin_bp"] = E.groupby("coin")["f3"].agg(lambda s: s.mean() * 1e4).round(2)
    out["eve3h_by_year"] = E.groupby("yr")["f3"].agg(mean_bp=lambda s: s.mean() * 1e4, t=tt, n="size").round(2)
    E["q"] = pd.qcut(E.z24, 5, labels=False)
    out["eve3h_by_z24_quintile"] = E.groupby("q").agg(z24=("z24", "mean"), f3_bp=("f3", lambda s: s.mean() * 1e4),
        f3s=("f3s", "mean"), n=("f3", "size")).round(4)
    return out
