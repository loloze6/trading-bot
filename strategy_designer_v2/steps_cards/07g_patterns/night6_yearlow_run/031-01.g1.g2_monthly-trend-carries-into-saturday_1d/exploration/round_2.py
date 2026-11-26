def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            r1 = c / c.shift(1) - 1
            df = pd.DataFrame({
                "coin": coin, "win": w, "wd": ts.dt.weekday.values,
                "year": ts.dt.year.values, "day": ts.dt.floor("D").values,
                "r1": r1.values, "r5": (c / c.shift(5) - 1).values,
                "r20": (c / c.shift(20) - 1).values,
                "vol20": r1.rolling(20).std().values,
                "nxt": (c.shift(-1) / c - 1).values,
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["mu"] = d.groupby("coin")["nxt"].transform("mean")
    d["ex"] = d["nxt"] - d["mu"]
    d["z20"] = d["r20"] / (d["vol20"] * np.sqrt(20))
    d["z5"] = d["r5"] / (d["vol20"] * np.sqrt(5))
    d["z1"] = d["r1"] / d["vol20"]
    d["s"] = d["ex"] / d["vol20"]  # strength-like

    def tc(sub, val):
        s = sub.dropna(subset=[val])
        x = s.groupby("day")[val].sum()
        n = len(x)
        return pd.Series({"mean_bp": 1e4 * s[val].mean(), "t_day": x.mean() / (x.std() / np.sqrt(n)), "days": n, "cases": len(s)})

    out = {}
    out["excess by signal weekday, day-clustered"] = d.dropna(subset=["ex"]).groupby("wd").apply(lambda x: tc(x, "ex")).round(2)
    # weekday by year for Fri and Wed
    tmp = d.dropna(subset=["ex"])
    out["Fri->Sat excess t by year"] = tmp[tmp.wd == 4].groupby("year").apply(lambda x: tc(x, "ex"))[["mean_bp", "t_day"]].round(2)
    # prior-day reversal: z1 * ex, day-clustered, overall and by year
    d["z1ex"] = -d["z1"].clip(-4, 4) * d["ex"]
    out["reversal -z1*ex overall"] = tc(d.dropna(subset=["z1ex"]), "z1ex").round(2).to_frame("all")
    out["reversal -z1*ex by year"] = d.dropna(subset=["z1ex"]).groupby("year").apply(lambda x: tc(x, "z1ex"))[["mean_bp", "t_day"]].round(2)
    out["reversal -z1*ex by weekday"] = d.dropna(subset=["z1ex"]).groupby("wd").apply(lambda x: tc(x, "z1ex"))[["mean_bp", "t_day"]].round(2)
    # Friday z5 quintiles, day clustered
    f = d[d.wd == 4].dropna(subset=["z5", "z20", "ex"]).copy()
    f["q5"] = pd.qcut(f["z5"], 5, labels=False)
    out["Fri z5 quintile -> Sat excess"] = f.groupby("q5").apply(lambda x: tc(x, "ex"))[["mean_bp", "t_day", "cases"]].round(2)
    f["q20"] = pd.qcut(f["z20"], 5, labels=False)
    out["Fri z20 quintile -> Sat excess"] = f.groupby("q20").apply(lambda x: tc(x, "ex"))[["mean_bp", "t_day", "cases"]].round(2)
    # strength of Fri z5 product, by year, and correlation z5 z20
    f["p5"] = f["z5"].clip(-4, 4) * f["ex"]
    out["Fri z5*ex by year"] = f.groupby("year").apply(lambda x: tc(x, "p5"))[["mean_bp", "t_day"]].round(2)
    out["corr z5 z20 Fri"] = round(f[["z5", "z20"]].corr().iloc[0, 1], 3)
    # z5 on other weekdays day-clustered
    d["p5"] = d["z5"].clip(-4, 4) * d["ex"]
    out["z5*ex by weekday, day-clustered"] = d.dropna(subset=["p5"]).groupby("wd").apply(lambda x: tc(x, "p5"))[["mean_bp", "t_day"]].round(2)
    # Fri excess strength in usual-move units
    out["Fri->Sat excess / vol20 mean"] = round(float(d[d.wd == 4]["s"].mean()), 4)
    return out
