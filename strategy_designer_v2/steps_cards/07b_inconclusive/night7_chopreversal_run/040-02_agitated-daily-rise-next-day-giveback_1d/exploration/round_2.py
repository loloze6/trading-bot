def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            mabs = r.abs().rolling(60, min_periods=20).mean()
            tr = c / c.shift(60) - 1
            df = pd.DataFrame({"coin": coin, "win": w, "r": r, "z": r / mabs,
                               "agit": (b["regime"] != "chop").values,
                               "tr": tr, "f1": c.shift(-1) / c - 1,
                               "year": pd.to_datetime(b["timestamp"]).dt.year,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            rows.append(df)
    d = pd.concat(rows, ignore_index=True).dropna(subset=["r", "f1", "z"])
    drift = d.groupby("coin")["f1"].mean()
    d["x1"] = d["f1"] - d["coin"].map(drift)
    d["trend"] = np.where(d["tr"] > 0.10, "rising", np.where(d["tr"] < -0.10, "falling", np.where(d["tr"].isna(), "na", "choppy")))
    out = {}
    def slope(s):
        if len(s) < 30:
            return pd.Series({"n": len(s), "slope_bp": np.nan, "t": np.nan})
        sl = stats.linregress(s["z"], s["x1"])
        return pd.Series({"n": len(s), "slope_bp": 1e4 * sl.slope, "t": sl.slope / sl.stderr})
    dn = d[(d["agit"]) & (d["r"] < 0)]
    up = d[(d["agit"]) & (d["r"] > 0)]
    out["agit down slope by coin"] = dn.groupby("coin").apply(slope)
    out["agit down slope by window"] = dn.groupby("win").apply(slope)
    out["agit down slope by trend"] = dn.groupby("trend").apply(slope)
    out["agit up slope by trend"] = up.groupby("trend").apply(slope)
    # grading of rebound on agitated down days: gain = +x1, day-summed t, by size tercile
    dn = dn.copy()
    dn["q"] = pd.qcut(-dn["z"], 3, labels=["small", "mid", "large"])
    def daytt(s):
        g = s.groupby("day")["x1"].sum()
        return pd.Series({"cases": len(s), "days": len(g), "mean%": 100 * s["x1"].mean(),
                          "t_days": g.mean() / (g.std() / np.sqrt(len(g)))})
    out["agit down rebound by fall size tercile"] = dn.groupby("q", observed=True).apply(daytt)
    out["agit down all rebound"] = daytt(dn).to_frame().T
    # calm comparison
    cdn = d[(~d["agit"]) & (d["r"] < 0)].copy()
    cdn["q"] = pd.qcut(-cdn["z"], 3, labels=["small", "mid", "large"])
    out["calm down rebound by fall size tercile"] = cdn.groupby("q", observed=True).apply(daytt)
    return out
