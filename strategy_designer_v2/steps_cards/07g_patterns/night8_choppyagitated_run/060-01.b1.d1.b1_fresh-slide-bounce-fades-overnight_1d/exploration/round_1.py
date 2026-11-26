def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "r": r, "z1": r / vol,
                "z5": (c / c.shift(5) - 1) / (vol * np.sqrt(5)),
                "z5l": (c.shift(1) / c.shift(6) - 1) / (vol * np.sqrt(5)),
                "tr60": c / c.shift(60) - 1,
                "volrel": vol / vol.rolling(60, min_periods=30).median(),
                "clv": (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "fc": b["forecast"].astype(float),
                "pos": b["postRebalance_current_allocation"].astype(float),
                "f1": c.shift(-1) / c - 1,
                "f2": c.shift(-2) / c - 1,
                "f3": c.shift(-3) / c - 1,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r"].mean()
    d["mu"] = d["coin"].map(mu)
    for h in (1, 2, 3):
        d[f"x{h}"] = d[f"f{h}"] - h * d["mu"]

    def tday(sub, col):
        s = sub.dropna(subset=[col])
        g = (s[col]).groupby(s["day"]).sum()
        n = s.groupby("day").size()
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s) if len(s) > 1 else np.nan
        return pd.Series({"n": len(s), "days": s["day"].nunique(), "mean%": 100 * m, "t": m / se if se else np.nan})

    out = {}
    # 1. next-day excess by z1 bucket, all bars
    d["z1b"] = pd.cut(d["z1"], [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out["x1 by z1 all"] = d.groupby("z1b", observed=True).apply(lambda s: tday(s, "x1"))
    # 2. by trend sign x z1 bucket (falling vs other), next 1 and 3 days
    d["trb"] = pd.cut(d["tr60"], [-np.inf, -0.1, 0.1, np.inf], labels=["fall", "chop", "rise"])
    d["z1c"] = pd.cut(d["z1"], [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["x1 by trend,z1"] = d.groupby(["trb", "z1c"], observed=True).apply(lambda s: tday(s, "x1"))
    # non-overlap 3d: use rows at grid positions
    d["pos_in_w"] = d.groupby(["coin", "win"]).cumcount()
    g3 = d[d["pos_in_w"] % 3 == 0]
    out["x3 by trend,z1 (grid)"] = g3.groupby(["trb", "z1c"], observed=True).apply(lambda s: tday(s, "x3"))
    # 3. active bars: forecast quintile
    a = d[d["fc"] < 0].copy()
    a["q"] = pd.qcut(-a["fc"], 4, labels=False, duplicates="drop")
    a["sx1"] = -a["x1"]; a["sx2"] = -a["x2"]; a["sx3"] = -a["x3"]
    out["active short-signed by fc quartile"] = a.groupby("q").apply(lambda s: pd.concat([tday(s, "sx1"), tday(s, "sx2").add_prefix("h2_")]))
    a["clvb"] = pd.cut(a["clv"], [0, 0.33, 0.66, 1.0001])
    out["active sx1 by close location"] = a.groupby("clvb", observed=True).apply(lambda s: tday(s, "sx1"))
    a["vrb"] = pd.qcut(a["volrel"], 3, labels=False, duplicates="drop")
    out["active sx1 by volrel tercile"] = a.groupby("vrb").apply(lambda s: tday(s, "sx1"))
    out["active sx1 by weekday"] = a.groupby("wd").apply(lambda s: tday(s, "sx1"))
    # 4. weekday all bars
    out["x1 by weekday all"] = d.groupby("wd").apply(lambda s: tday(s, "x1"))
    # 5. all up days in falling trend by close location
    u = d[(d["trb"] == "fall") & (d["z1"] > 0.5)].copy()
    u["clvb"] = pd.cut(u["clv"], [0, 0.33, 0.66, 1.0001])
    out["fall up-days x1 by clv"] = u.groupby("clvb", observed=True).apply(lambda s: tday(s, "x1"))
    dn = d[(d["trb"] == "fall") & (d["z1"] < -0.5)].copy()
    dn["clvb"] = pd.cut(dn["clv"], [0, 0.33, 0.66, 1.0001])
    out["fall down-days x1 by clv"] = dn.groupby("clvb", observed=True).apply(lambda s: tday(s, "x1"))
    return out
