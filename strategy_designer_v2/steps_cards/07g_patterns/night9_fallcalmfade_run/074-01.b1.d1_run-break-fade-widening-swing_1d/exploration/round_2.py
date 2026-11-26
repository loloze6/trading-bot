import pandas as pd, numpy as np
from scipy import stats

def build(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            up = r > 0; dn = r < 0
            run = np.zeros(len(b), dtype=int); cnt = 0
            for i in range(len(b)):
                run[i] = cnt if up.iloc[i] else 0
                cnt = cnt + 1 if dn.iloc[i] else 0
            urun = np.zeros(len(b), dtype=int); cnt = 0
            for i in range(len(b)):
                urun[i] = cnt if dn.iloc[i] else 0
                cnt = cnt + 1 if up.iloc[i] else 0
            prevup = up.shift(1).fillna(False)
            sd30 = r.rolling(30).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "year": ts.dt.year, "wd": ts.dt.weekday, "day": ts.dt.floor("D"),
                "r": r, "nxt": nxt, "run": run, "urun": urun, "prevup": prevup,
                "tr60": c / c.shift(60) - 1, "rz": r / sd30, "sd30": sd30,
                "r3": c / c.shift(3) - 1}))
    D = pd.concat(rows, ignore_index=True).dropna(subset=["nxt"])
    D["un"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    D["trend"] = np.where(D.tr60 < -0.10, "falling", np.where(D.tr60 > 0.10, "rising", np.where(D.tr60.notna(), "choppy", "na")))
    D["agit"] = np.where(D.sd30 > D.groupby("coin")["sd30"].transform("median"), "agit", "calm")
    return D

def ct(x, day):
    s = pd.Series(x.values, index=day.values).groupby(level=0).sum()
    n = len(x); m = x.mean()
    se = np.sqrt(((s - 0) ** 2).sum() - 0) if False else None
    dev = pd.Series((x - m).values, index=day.values).groupby(level=0).sum()
    se = np.sqrt((dev ** 2).sum()) / n
    return m / se if se > 0 else np.nan

def summ(g, sign=1):
    x = sign * g["un"]
    return pd.Series({"n": len(x), "days": g["day"].nunique(), "mean%": 100 * x.mean(), "t_day": ct(x, g["day"])})

def slope(g, xcol):
    g = g.dropna(subset=[xcol, "un"])
    sl = stats.linregress(g[xcol], g["un"])
    return pd.Series({"n": len(g), "slope%": 100 * sl.slope, "t": sl.slope / sl.stderr, "corr": sl.rvalue})

def explore(data):
    D = build(data)
    out = {}
    upd = D[D.r > 0].copy()
    upd["kind"] = np.where(upd.run > 0, "runbreak", "up_after_up")
    upd["rzt"] = upd.groupby("coin")["rz"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["upday_fade_trend_kind_agit (short-signed)"] = upd.groupby(["trend", "kind", "agit"]).apply(summ, sign=-1)
    out["upday_fade_falling_rz_tercile_agit"] = upd[upd.trend == "falling"].groupby(["agit", "rzt"]).apply(summ, sign=-1)
    out["slope_un_on_rz_by_trend_all_days"] = D.groupby("trend").apply(slope, xcol="rz")
    out["slope_un_on_rz_falling_by_agit"] = D[D.trend == "falling"].groupby("agit").apply(slope, xcol="rz")
    out["slope_un_on_rz_falling_by_year"] = D[D.trend == "falling"].groupby("year").apply(slope, xcol="rz")
    out["slope_un_on_rz_falling_up_only_by_kind"] = upd[upd.trend == "falling"].groupby("kind").apply(slope, xcol="rz")
    # mirror: first down day after up run in falling market
    m = D[(D.urun > 0)].assign(urb=lambda x: x.urun.clip(upper=4))
    out["mirror_falling_by_agit_urb (long)"] = m[m.trend == "falling"].groupby(["agit", "urb"]).apply(summ)
    out["mirror_slope_on_urun_by_trend"] = m.groupby("trend").apply(slope, xcol="urun")
    # weekday in falling by year
    f = D[D.trend == "falling"]
    out["falling_sat_vs_other_by_year (long)"] = f.assign(sat=f.wd == 5).groupby(["year", "sat"]).apply(summ)
    out["all_trends_sat (long)"] = D.assign(sat=D.wd == 5).groupby(["trend", "sat"]).apply(summ)
    return out
