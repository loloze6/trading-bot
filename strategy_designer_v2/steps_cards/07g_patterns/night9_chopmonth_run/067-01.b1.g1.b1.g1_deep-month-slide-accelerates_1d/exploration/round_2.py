def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r1": r1, "r60": c / c.shift(60) - 1,
                               "vol30": r1.rolling(30).std(),
                               "f1": c.shift(-1) / c - 1, "f3": c.shift(-3) / c - 1,
                               "f5": c.shift(-5) / c - 1, "pos": np.arange(len(b))})
            df["vol_rel"] = df["vol30"] / df["vol30"].rolling(120, min_periods=60).median()
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A.ts.dt.floor("D"); A["year"] = A.ts.dt.year; A["wd"] = A.ts.dt.weekday
    A["trend"] = np.where(A.r60 > 0.1, "rising", np.where(A.r60 < -0.1, "falling", "choppy"))
    A["agit"] = np.where(A.vol_rel > 1, "agit", "calm")
    A["z1"] = A.r1 / A.vol30
    A = A.dropna(subset=["z1", "r60"])
    for h in [1, 3, 5]:
        dr = A[A.pos % h == 0].groupby("coin")[f"f{h}"].mean()
        A[f"u{h}"] = (A[f"f{h}"] - A.coin.map(dr)) / (A.vol30 * np.sqrt(h))

    def ct(v, d):
        v = np.asarray(v, float); m = ~np.isnan(v); v = v[m]; d = np.asarray(d)[m]
        if len(v) < 5: return np.nan, len(v), 0
        dd = pd.Series(v - v.mean()).groupby(d).sum()
        return v.mean() / (np.sqrt((dd ** 2).sum()) / len(v)), len(v), dd.size

    res = {}
    A["zq"] = pd.cut(A.z1, [-99, -2, -1, -0.3, 0.3, 1, 2, 99])
    out = []
    for (tr, ag, zq), x in A.groupby(["trend", "agit", "zq"], observed=True):
        rec = {"trend": tr, "agit": ag, "zq": str(zq)}
        for h in [1, 3, 5]:
            g = x[x.pos % h == 0]
            t, n, nd = ct(g[f"u{h}"], g.day)
            rec[f"m{h}"] = g[f"u{h}"].mean(); rec[f"t{h}"] = t; rec[f"n{h}"] = n
        out.append(rec)
    res["scaled_move_by_profile_z1"] = pd.DataFrame(out)
    # grading inside falling: correlation of z1 with u1, u3 for z1>0
    out = []
    for (tr), x in A.groupby("trend"):
        for sgn in ["up", "down"]:
            y = x[x.z1 > 0] if sgn == "up" else x[x.z1 < 0]
            for h in [1, 3]:
                g = y[y.pos % h == 0].dropna(subset=[f"u{h}"])
                out.append({"trend": tr, "side": sgn, "h": h, "n": len(g),
                            "corr": g[["z1", f"u{h}"]].corr().iloc[0, 1]})
    res["grading_corr"] = pd.DataFrame(out)
    # weekday by year and by trend (raw next-day return, day clustered)
    out = []
    for (yr, wd), x in A.groupby(["year", "wd"]):
        t, n, nd = ct(x.f1, x.day)
        out.append({"year": yr, "wd": wd, "mean": x.f1.mean(), "t": t, "days": nd})
    res["weekday_by_year"] = pd.DataFrame(out).pivot(index="wd", columns="year", values="t")
    out = []
    for (tr, wd), x in A.groupby(["trend", "wd"]):
        t, n, nd = ct(x.f1, x.day)
        out.append({"trend": tr, "wd": wd, "mean": x.f1.mean(), "t": t, "days": nd})
    res["weekday_by_trend"] = pd.DataFrame(out).pivot(index="wd", columns="trend", values="t")
    res["weekday_by_trend_mean"] = pd.DataFrame(out).pivot(index="wd", columns="trend", values="mean")
    return res
