import numpy as np, pandas as pd

def tday(g, col):
    s = g.groupby("day")[col].sum()
    n = len(s)
    return pd.Series({"cases": len(g), "days": n, "mean%": g[col].mean()*100,
                      "t_day": s.mean()/(s.std()/np.sqrt(n)) if n > 2 else np.nan})

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            tr60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            pct = vol30.rolling(365, min_periods=60).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            hl = (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "nxt": nxt, "tr60": tr60, "pct": pct,
                                      "z": r / r.rolling(20).std(), "clpos": (c - b["low"]) / hl,
                                      "day": ts.dt.floor("D"), "yr": ts.dt.year}))
    d = pd.concat(rows, ignore_index=True)
    d["ex"] = d["nxt"] - d.groupby("coin")["nxt"].transform("mean")
    d = d.dropna(subset=["nxt", "tr60", "pct", "z"])
    d["trend"] = np.where(d.tr60 > 0.1, "rising", np.where(d.tr60 < -0.1, "falling", "choppy"))
    d["agit"] = np.where(d.pct > 0.5, "agitated", "calm")
    out = {}
    fa = d[(d.trend == "falling") & (d.agit == "agitated")].copy()
    fa["zb"] = pd.cut(fa.z, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["falling_agit_zbins"] = fa.groupby("zb", observed=True).apply(lambda g: tday(g, "ex"))
    fc = d[(d.trend == "falling") & (d.agit == "calm")].copy()
    fc["zb"] = pd.cut(fc.z, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["falling_calm_zbins"] = fc.groupby("zb", observed=True).apply(lambda g: tday(g, "ex"))
    fa2 = fa.dropna(subset=["clpos"]).copy()
    fa2["cb"] = pd.cut(fa2.clpos, [0, .2, .4, .6, .8, 1.0001], include_lowest=True)
    out["falling_agit_closeloc"] = fa2.groupby("cb", observed=True).apply(lambda g: tday(g, "ex"))
    fa["pay"] = -np.sign(fa.z) * fa.ex
    out["falling_agit_fade_by_window"] = fa.groupby("w").apply(lambda g: tday(g, "pay"))
    out["falling_agit_fade_by_side_year"] = fa.assign(side=np.where(fa.z > 0, "up", "down")).groupby(["side", "yr"]).apply(lambda g: tday(g, "pay"))
    ra = d[(d.trend == "rising") & (d.agit == "agitated")].copy()
    ra["zb"] = pd.cut(ra.z, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["rising_agit_zbins"] = ra.groupby("zb", observed=True).apply(lambda g: tday(g, "ex"))
    return out
