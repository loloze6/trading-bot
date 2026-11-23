def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 24
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            p24 = c / c.shift(24) - 1
            s24 = p24 / p24.abs().rolling(720, min_periods=200).mean()
            p72 = c / c.shift(72) - 1
            s72 = p72 / p72.abs().rolling(720, min_periods=200).mean()
            vol = r1.rolling(720, min_periods=200).std()
            vol24 = r1.rolling(24, min_periods=20).std()
            fwd = c.shift(-H) / c - 1
            idx = np.arange(0, len(b), H)
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.iloc[idx].values,
                "s24": s24.iloc[idx].values, "s72": s72.iloc[idx].values,
                "vol": vol.iloc[idx].values, "vr": (vol24 / vol).iloc[idx].values,
                "year": ts.dt.year.iloc[idx].values, "wd": ts.dt.weekday.iloc[idx].values,
                "hour": ts.dt.hour.iloc[idx].values}))
            hourly.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour.values,
                                        "year": ts.dt.year.values, "r": r1.shift(-1).values}))
    g = pd.concat(rows, ignore_index=True)
    g["drift"] = g.groupby("coin")["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["usual"] = g.groupby("coin")["fwd"].transform("std")
    g["str"] = g["ex"] / g["usual"]
    x = g.dropna(subset=["s24", "ex", "vol", "vr", "s72"]).copy()
    rk = lambda s, q: pd.qcut(s.rank(method="first"), q, labels=False)
    x["vt"] = x.groupby("coin")["vol"].transform(lambda s: rk(s, 3))
    x["vrt"] = x.groupby("coin")["vr"].transform(lambda s: rk(s, 3))
    x["q24"] = x.groupby("coin")["s24"].transform(lambda s: rk(s, 5))
    x["q72"] = x.groupby("coin")["s72"].transform(lambda s: rk(s, 5))
    tt = lambda s: s.mean() / (s.std() / np.sqrt(len(s)))
    agg = dict(n=("ex", "size"), total=("fwd", "mean"), mean_ex=("ex", "mean"), strength=("str", "mean"), t=("ex", tt))
    out["s24 quintile within high 30d-vol tercile"] = x[x.vt == 2].groupby("q24").agg(**agg)
    out["s24 quintile within high 24h/30d vol-ratio tercile"] = x[x.vrt == 2].groupby("q24").agg(**agg)
    out["s24 quintile within low vol-ratio tercile"] = x[x.vrt == 0].groupby("q24").agg(**agg)
    out["s72 quintiles"] = x.groupby("q72").agg(**agg)
    res = []
    for k, gg in x.groupby("vrt"):
        sl = stats.linregress(gg["s24"], gg["str"])
        res.append({"vr_tercile": k, "n": len(gg), "slope": sl.slope, "t": sl.slope / sl.stderr})
    out["s24 slope by vol-ratio tercile"] = pd.DataFrame(res)
    # vol-scaled interaction: s24 * vr
    x["int"] = x["s24"] * x["vr"]
    res = []
    for yr, gg in x.groupby("year"):
        sl = stats.linregress(gg["s24"], gg["str"])
        sl2 = stats.linregress(gg["int"], gg["str"])
        res.append({"year": yr, "n": len(gg), "slope_s24": sl.slope, "t": sl.slope / sl.stderr,
                    "slope_s24xvr": sl2.slope, "t_int": sl2.slope / sl2.stderr})
    out["slopes by year"] = pd.DataFrame(res)
    res = []
    for w, gg in x.groupby("win"):
        sl = stats.linregress(gg["s24"], gg["str"])
        res.append({"win": w, "slope": sl.slope})
    ws = pd.DataFrame(res)
    out["windows with negative s24 slope (share, count)"] = f"{(ws.slope<0).mean():.3f} of {len(ws)}"
    out["fwd24 excess, weekday 4, by year"] = g[g.wd == 4].groupby("year").agg(n=("ex", "size"), mean_ex=("ex", "mean"), t=("ex", tt))
    h = pd.concat(hourly, ignore_index=True).dropna(subset=["r"])
    hh = h[h.hour.isin([20, 21])]
    out["next-hour return, hours 20-21, by year"] = hh.groupby("year").agg(n=("r", "size"), mean=("r", "mean"), t=("r", tt))
    out["next-hour return, hours 20-21, by coin"] = hh.groupby("coin").agg(n=("r", "size"), mean=("r", "mean"), t=("r", tt))
    return out
