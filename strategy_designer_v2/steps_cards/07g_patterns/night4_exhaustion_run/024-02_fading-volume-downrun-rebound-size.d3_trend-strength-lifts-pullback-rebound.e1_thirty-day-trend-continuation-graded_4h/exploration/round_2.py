import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 18
    rows = []; hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(180, min_periods=60).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({
                "coin": coin, "w": w,
                "fwd": c.shift(-H) / c - 1,
                "fwd6": c.shift(-6) / c - 1,
                "r30": c / c.shift(180) - 1,
                "r1dz": (c / c.shift(6) - 1) / (vol30 * np.sqrt(6)),
                "r7z": (c / c.shift(42) - 1) / (vol30 * np.sqrt(42)),
                "lvr": np.log(v.rolling(6).mean() / v.rolling(60).mean()),
                "lvr3": np.log(v.rolling(18).mean() / v.rolling(120).mean()),
                "year": ts.dt.year,
            })
            rows.append(df.iloc[::H])
            hb = pd.DataFrame({"coin": coin, "w": w, "hour": ts.shift(-1).dt.hour,
                               "wd": ts.shift(-1).dt.weekday, "year": ts.dt.year,
                               "fwd1": r1.shift(-1)})
            hourly.append(hb)
    g = pd.concat(rows, ignore_index=True).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def st(d, x, y="ex"):
        d = d.dropna(subset=[x, y])
        if len(d) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(d)})
        s = stats.linregress(d[x], d[y])
        return pd.Series({"slope": s.slope, "t": s.slope / s.stderr, "n": len(d)})
    out["lvr_pooled"] = pd.DataFrame({"lvr": st(g, "lvr"), "lvr3": st(g, "lvr3")}).T
    out["lvr_by_coin"] = g.groupby("coin").apply(lambda d: st(d, "lvr"))
    out["lvr_by_year"] = g.groupby("year").apply(lambda d: st(d, "lvr"))
    # direction split: volume surge on up vs down day
    g["up1d"] = np.sign(g["r1dz"])
    out["lvr_by_1d_sign"] = g.groupby("up1d").apply(lambda d: st(d, "lvr"))
    out["lvr_by_r30_sign"] = g.groupby(np.sign(g["r30"])).apply(lambda d: st(d, "lvr"))
    # multivariate: ex on lvr, r30 rank, r7z
    d = g.dropna(subset=["lvr", "r30", "r7z", "ex"]).copy()
    d["r30rk"] = d.groupby("coin")["r30"].rank(pct=True)
    X = np.column_stack([np.ones(len(d)), d["lvr"], d["r30rk"], d["r7z"]])
    beta, *_ = np.linalg.lstsq(X, d["ex"].values, rcond=None)
    res = d["ex"].values - X @ beta
    s2 = res @ res / (len(d) - 4)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["multi_lvr_r30rk_r7z"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["c", "lvr", "r30rk", "r7z"])
    # lvr on 1-day horizon
    g["ex6"] = g["fwd6"] - g.groupby("coin")["fwd6"].transform("mean")
    out["lvr_1day_horizon"] = st(g, "lvr", "ex6").to_frame().T
    # lvr quintiles mean ex
    d = g.dropna(subset=["lvr"]).copy()
    d["bin"] = np.minimum((d.groupby("coin")["lvr"].rank(pct=True) * 5).astype(int), 4)
    out["lvr_quintile_by_coin_mean_ex"] = d.pivot_table(index="bin", columns="coin", values="ex", aggfunc="mean").round(4)
    # hour effect robustness
    hb = pd.concat(hourly).dropna(subset=["fwd1", "hour"])
    hb["ex1"] = hb["fwd1"] - hb.groupby("coin")["fwd1"].transform("mean")
    def tt(x): return x.mean() / (x.std() / np.sqrt(len(x)))
    out["hour_t_by_coin"] = hb.pivot_table(index="hour", columns="coin", values="ex1", aggfunc=tt).round(2)
    out["hour_t_by_year"] = hb.pivot_table(index="hour", columns="year", values="ex1", aggfunc=tt).round(2)
    out["fri_t_by_year"] = hb[hb.wd == 4].groupby("year")["ex1"].apply(tt).round(2)
    return out
