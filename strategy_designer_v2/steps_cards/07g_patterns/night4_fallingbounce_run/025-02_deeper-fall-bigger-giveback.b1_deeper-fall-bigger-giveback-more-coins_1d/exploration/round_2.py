def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "win": w, "z": r1 / vol20.shift(1),
                               "ret30": c / c.shift(30) - 1, "ret90": c / c.shift(90) - 1,
                               "fwd5": c.shift(-5) / c - 1, "fwd1": c.shift(-1) / c - 1,
                               "rng": (b["high"] - b["low"]) / c, "rng20": ((b["high"] - b["low"]) / c).rolling(20, min_periods=15).mean(),
                               "wd": ts.dt.weekday, "yr": ts.dt.year, "day": ts.dt.floor("D"),
                               "pos": np.arange(len(b))})
            daily.append(df); rows.append(df[df["pos"] % 5 == 0])
    g = pd.concat(rows).dropna(subset=["fwd5"]); d = pd.concat(daily)
    st = g.groupby("coin")["fwd5"].agg(["mean", "std"]); g = g.join(st, on="coin")
    g["exs"] = (g["fwd5"] - g["mean"]) / g["std"]
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean() / s.std() * np.sqrt(len(s))})
    # weekday: cross-coin mean per day first (clustered), then by year halves
    dd = d.dropna(subset=["fwd1"])
    dm = dd.groupby(["day", "wd", "yr"])["fwd1"].mean().reset_index()
    out["next-day ret by weekday, per-day coin mean"] = dm.groupby("wd")["fwd1"].apply(tt).unstack()
    dm["half"] = np.where(dm["yr"] <= 2021, "<=2021", ">=2022")
    out["Fri-close next-day t by half"] = dm[dm["wd"] == 4].groupby("half")["fwd1"].apply(tt).unstack()
    out["Tue+Thu next-day t by half"] = dm[dm["wd"].isin([1, 3])].groupby("half")["fwd1"].apply(tt).unstack()
    # shock x trend, clustered by grid day: date-level mean of exs within cell
    gg = g.dropna(subset=["z", "ret30"]).copy()
    gg["tr"] = np.where(gg["ret30"] < 0, "down30", "up30")
    gg["sz"] = gg["z"] * np.where(gg["tr"] == "up30", 1, -1)  # shock in trend direction sign
    # graded regression within trend: exs on z
    res = {}
    for k, v in gg.groupby("tr"):
        r = stats.linregress(v["z"].clip(-5, 5), v["exs"]); res[k] = pd.Series({"n": len(v), "slope": r.slope, "t": r.slope / r.stderr})
        vm = v.groupby("day").apply(lambda x: pd.Series({"z": x["z"].clip(-5, 5).mean(), "e": x["exs"].mean()}))
        r = stats.linregress(vm["z"], vm["e"]); res[k + "_daymean"] = pd.Series({"n": len(vm), "slope": r.slope, "t": r.slope / r.stderr})
    out["exs on z by 30d trend"] = pd.DataFrame(res).T
    gg["half"] = np.where(gg["yr"] <= 2021, "<=2021", ">=2022")
    res = {}
    for (k, h), v in gg.groupby(["tr", "half"]):
        r = stats.linregress(v["z"].clip(-5, 5), v["exs"]); res[k + h] = pd.Series({"n": len(v), "slope": r.slope, "t": r.slope / r.stderr})
    out["exs on z by trend x half"] = pd.DataFrame(res).T
    # ret30 by trend clustered
    res = {}
    for k, v in gg.groupby("tr"):
        x = v.assign(rr=v.groupby("coin")["ret30"].rank(pct=True))
        vm = x.groupby("day").apply(lambda q: pd.Series({"r": q["rr"].mean(), "e": q["exs"].mean()}))
        r = stats.linregress(vm["r"], vm["e"]); res[k] = pd.Series({"n": len(vm), "slope": r.slope, "t": r.slope / r.stderr})
    out["exs on ret30 rank by trend, daymean"] = pd.DataFrame(res).T
    # range relative to its 20d average
    gg2 = g.dropna(subset=["rng", "rng20"]).copy()
    gg2["rr"] = np.log(gg2["rng"] / gg2["rng20"])
    r = stats.linregress(gg2["rr"].clip(-2, 2), gg2["exs"])
    out["exs on log range/20d range"] = pd.Series({"n": len(gg2), "slope": r.slope, "t": r.slope / r.stderr})
    gg2["q"] = pd.qcut(gg2["rr"], 5, labels=False)
    out["exs by relative range quintile"] = gg2.groupby("q")["exs"].apply(tt).unstack()
    pc = {}
    for coin, v in gg2.groupby("coin"):
        if len(v) > 50:
            r = stats.linregress(v["rr"].clip(-2, 2), v["exs"]); pc[coin] = r.slope
    pc = pd.Series(pc); out["range slope per coin: share positive"] = pd.Series({"coins": len(pc), "share_pos": (pc > 0).mean()})
    return out
