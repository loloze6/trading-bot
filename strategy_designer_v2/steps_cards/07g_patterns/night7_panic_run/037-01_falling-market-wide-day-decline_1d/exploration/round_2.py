def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            sd = r.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w,
                "rng": ((b["high"] - b["low"]) / c) / sd,
                "z1": r / sd,
                "tr60": c / c.shift(60) - 1,
                "f3": c.shift(-3) / c - 1,
                "f1": c.shift(-1) / c - 1,
                "day": ts.dt.floor("D"),
                "wd": ts.dt.weekday,
                "pos": np.arange(len(b)),
            })
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    for h, col in [(3, "f3"), (1, "f1")]:
        g = D[D.pos % h == 0].copy()
        drift = g.groupby("coin")[col].transform("mean")
        D.loc[g.index, "u%d" % h] = g[col] - drift
    D["trend"] = np.where(D.tr60 < -0.10, "fall", np.where(D.tr60 > 0.10, "rise", "chop"))
    D.loc[D.tr60.isna(), "trend"] = np.nan

    def ct(x, col):
        x = x.dropna(subset=[col])
        n = len(x)
        if n < 5: return (np.nan, n, np.nan, 0)
        m = x[col].mean()
        gd = x.groupby("day")[col].agg(["sum", "count"])
        Dn = len(gd)
        se = np.sqrt(Dn / (Dn - 1) * ((gd["sum"] - gd["count"] * m) ** 2).sum()) / n
        return (round(m, 5), n, round(m / se, 3), Dn)

    def tab(df, col, by):
        res = {}
        for k, x in df.groupby(by):
            res[k] = ct(x, col)
        return pd.DataFrame(res, index=["mean", "n", "t_day", "days"]).T

    def bywin(df, col):
        g = df.dropna(subset=[col]).groupby("win")[col].agg(["mean", "count"])
        return f"pos {int((g['mean']>0).sum())} / neg {int((g['mean']<0).sum())} windows"

    out = {}
    # A: rising market, graded by range
    rise = D[D.trend == "rise"].copy()
    rise["rq"] = pd.qcut(rise.rng, 5, labels=False)
    out["rise: u3 by range quintile (day t)"] = tab(rise, "u3", "rq")
    rw = rise[rise.rng >= 2].copy()
    rw["dn"] = np.where(rw.z1 < 0, "down", "up")
    out["rise wide: u3 by close dir"] = tab(rw, "u3", "dn")
    out["rise wide windows"] = bywin(rw, "u3")
    # B: falling market, graded by 1-day z
    fall = D[D.trend == "fall"].copy()
    fall["zq"] = pd.qcut(fall.z1, 5, labels=False)
    out["fall: u3 by z1 quintile (day t)"] = tab(fall, "u3", "zq")
    fup = fall[fall.z1 > 0]
    out["fall up-days: corr z1 vs u3"] = float(fup[["z1", "u3"]].dropna().corr().iloc[0, 1])
    fall["zbin"] = pd.cut(fall.z1, [-99, -1, 0, 0.5, 1, 1.5, 2, 99])
    out["fall: u3 by z1 bin"] = tab(fall, "u3", "zbin")
    out["fall top z quintile windows"] = bywin(fall[fall.zq == 4], "u3")
    # C: falling market narrow days
    fall["rq"] = pd.qcut(fall.rng, 5, labels=False)
    out["fall: u3 by range quintile (day t)"] = tab(fall, "u3", "rq")
    out["fall narrow windows"] = bywin(fall[fall.rq == 0], "u3")
    out["fall narrow: mean z1, mean rng"] = fall[fall.rq == 0][["z1", "rng"]].mean().round(3)
    # D: weekday, day-clustered
    out["all: u1 by weekday (day t)"] = tab(D, "u1", "wd")
    # E: by year, the falling up-day effect
    fall["yr"] = fall.day.dt.year
    out["fall z1>1: u3 by year"] = tab(fall[fall.z1 > 1], "u3", "yr")
    out["rise rng>=2: u3 by year"] = tab(rise.assign(yr=rise.day.dt.year)[rise.rng >= 2], "u3", "yr")
    return out
