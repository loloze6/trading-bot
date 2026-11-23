def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.set_index("timestamp")
            c = b["close"]
            r24 = c / c.shift(24) - 1
            scale = r24.abs().rolling(720, min_periods=360).mean()
            z = r24 / scale
            r1 = c.pct_change()
            vol = r1.rolling(720, min_periods=360).std()
            f24 = c.shift(-24) / c - 1
            f48 = c.shift(-48) / c - 1
            f24b = c.shift(-48) / c.shift(-24) - 1
            df = pd.DataFrame({"z": z, "r24": r24, "f24": f24, "f48": f48, "f24b": f24b, "vol": vol})
            df = df[df.index.hour == 23].dropna()
            df["wd"] = df.index.weekday
            df["year"] = df.index.year
            df["coin"] = coin
            df["w"] = w
            rows.append(df)
    d = pd.concat(rows)
    # remove drift per coin
    for col in ["f24", "f48", "f24b"]:
        d[col + "x"] = d[col] - d.groupby("coin")[col].transform("mean")
    def slope(g, y):
        g = g.dropna(subset=["z", y])
        if len(g) < 30: return pd.Series({"n": len(g), "slope%": np.nan, "t": np.nan})
        s = stats.linregress(g["z"], g[y] * 100)
        return pd.Series({"n": len(g), "slope%": s.slope, "t": s.slope / s.stderr})
    res = {}
    wdtab = []
    for wd, g in d.groupby("wd"):
        a = slope(g, "f24x"); b = slope(g, "f48x"); c2 = slope(g, "f24bx")
        wdtab.append({"wd": wd, "n": a["n"], "next24_slope": a["slope%"], "next24_t": a["t"],
                      "next48_slope": b["slope%"], "next48_t": b["t"], "day2_slope": c2["slope%"], "day2_t": c2["t"]})
    res["day_end_z_vs_forward_by_weekday(0=Mon)"] = pd.DataFrame(wdtab)
    sun = d[d["wd"] == 6].copy()
    sun["volq"] = sun.groupby("coin")["vol"].transform(lambda x: pd.qcut(x.rank(method="first"), 3, labels=False))
    vt = []
    for q, g in sun.groupby("volq"):
        b = slope(g, "f48x"); vt.append({"volq": q, **b.to_dict()})
    res["sunday_by_vol_third"] = pd.DataFrame(vt)
    sun["zq"] = pd.qcut(sun["z"], 5, labels=False)
    res["sunday_z_quintile_mean_f48x%"] = sun.groupby("zq").agg(n=("z","size"), z=("z","mean"), f24x=("f24x", lambda x: x.mean()*100), f48x=("f48x", lambda x: x.mean()*100))
    ct = []
    for coin, g in sun.groupby("coin"):
        b = slope(g, "f48x"); ct.append({"coin": coin, **b.to_dict()})
    res["sunday_by_coin"] = pd.DataFrame(ct)
    yt = []
    for y, g in sun.groupby("year"):
        b = slope(g, "f48x"); yt.append({"year": y, **b.to_dict()})
    res["sunday_by_year"] = pd.DataFrame(yt)
    # weekend 48h (Fri23 -> Sun23) move vs next 48h
    sat = d[d["wd"] == 5]
    res["saturday_slope_next48"] = slope(sat, "f48x")
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["year"] = pd.to_datetime(tr["entry_time"], utc=True).dt.year
    res["trades_by_year"] = tr.groupby("year").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    res["trades_by_side"] = tr.groupby("side").agg(n=("net_profit_loss_percent","size"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), hours=("duration_minutes", lambda x: x.mean()/60))
    return res
