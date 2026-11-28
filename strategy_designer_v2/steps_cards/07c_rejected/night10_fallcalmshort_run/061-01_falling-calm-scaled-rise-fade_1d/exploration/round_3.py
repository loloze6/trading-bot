def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std(ddof=1)
            df = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)),
                               "fc": b["regime"].astype(str) != "chop",
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            df["z1"] = r / sd
            df["z3"] = (c / c.shift(3) - 1) / (sd * np.sqrt(3))
            df["z5"] = (c / c.shift(5) - 1) / (sd * np.sqrt(5))
            df["z10"] = (c / c.shift(10) - 1) / (sd * np.sqrt(10))
            df["clv"] = (c - lo) / (hi - lo).replace(0, np.nan)
            for h in (1, 2, 3, 5):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["usd"] = {1: 1}.get(1) * sd
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    drift = d.groupby("coin")["f1"].mean()
    def tt(s):
        s = s.dropna(); return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    for h in (1, 2, 3, 5):
        d[f"u{h}"] = d[f"f{h}"] - h * d["coin"].map(drift)
    fc = d[d["fc"]]
    res = {}
    out = []
    for feat in ("z1", "z3", "z5", "z10"):
        for h in (2, 3, 5):
            g = fc[(fc["pos"] % h == 0)][[feat, f"u{h}", "coin", "year"]].dropna()
            neg = g[g[feat] < 0]
            pos = g[g[feat] >= 0]
            out.append({"feat": feat, "h": h, "n_neg": len(neg), "u_neg": neg[f"u{h}"].mean(), "t_neg": tt(neg[f"u{h}"]),
                        "n_pos": len(pos), "u_pos": pos[f"u{h}"].mean(), "t_pos": tt(pos[f"u{h}"]),
                        "spear_neg": neg[[feat, f"u{h}"]].corr("spearman").iloc[0, 1],
                        "strength_neg": (neg[f"u{h}"] / (fc[f"u{h}"].std())).mean()})
    res["fc past-return sign split (unusual, long dir)"] = pd.DataFrame(out)
    g3 = fc[(fc["pos"] % 3 == 0)].dropna(subset=["z5", "u3"])
    n3 = g3[g3["z5"] < 0]
    res["fc z5<0 u3 by coin"] = n3.groupby("coin")["u3"].agg(["count", "mean", tt])
    res["fc z5<0 u3 by year"] = n3.groupby("year")["u3"].agg(["count", "mean"])
    res["fc z5<0 u3 by z5 size"] = n3.groupby(pd.cut(n3["z5"], [-np.inf, -1.5, -0.75, 0]), observed=True)["u3"].agg(["count", "mean", tt])
    p3 = g3[g3["z5"] >= 0]
    res["fc z5>=0 u3 by z5 size"] = p3.groupby(pd.cut(p3["z5"], [0, 0.75, 1.5, np.inf]), observed=True)["u3"].agg(["count", "mean", tt])
    g5 = fc[(fc["pos"] % 5 == 0)].dropna(subset=["clv", "u5"])
    res["fc clv u5 by tercile and coin"] = g5.groupby([pd.qcut(g5["clv"], 3, labels=["low", "mid", "high"]), "coin"], observed=True)["u5"].mean().unstack()
    res["fc usual 3-day move sd"] = float(fc[fc["pos"] % 3 == 0]["f3"].std())
    return res
