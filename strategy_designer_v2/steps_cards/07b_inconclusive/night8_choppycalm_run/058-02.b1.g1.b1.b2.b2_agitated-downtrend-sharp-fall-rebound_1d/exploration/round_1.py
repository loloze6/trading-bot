def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        # coin mean daily return over all windows
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allr.append(c[1:] / c[:-1] - 1)
        mu = np.nanmean(np.concatenate(allr)) if allr else np.nan
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            nxt = np.append(c[1:] / c[:-1] - 1, np.nan)
            r1 = np.insert(c[1:] / c[:-1] - 1, 0, np.nan)
            sd = pd.Series(r1).rolling(20).std().values
            z = r1 / sd
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "f": b["forecast"].astype(float).values,
                               "reg": b["regime"].values, "nx": nxt - mu, "z": z,
                               "day": ts.dt.floor("D").astype(str).values, "year": ts.dt.year.values,
                               "wd": ts.dt.weekday.values})
            rows.append(df)
    d = pd.concat(rows)
    a = d[(d.f > 0) & d.nx.notna()].copy()

    def slope_t(g):
        if len(g) < 10:
            return pd.Series({"n": len(g), "slope": np.nan, "t": np.nan, "mean_ex": g.nx.mean()})
        x = g.f.values; y = g.nx.values
        xm = x - x.mean(); b1 = (xm * (y - y.mean())).sum() / (xm ** 2).sum()
        e = y - y.mean() - b1 * xm
        s = pd.Series(xm * e).groupby(g.day.values).sum()
        se = np.sqrt((s ** 2).sum()) / (xm ** 2).sum()
        m = pd.Series(y).groupby(g.day.values).sum()
        tm = y.mean() / (np.sqrt(((m - m.mean() * 0 - (pd.Series(np.ones(len(y))).groupby(g.day.values).sum() * y.mean())) ** 2).sum()) / len(y))
        return pd.Series({"n": len(g), "days": g.day.nunique(), "slope": b1, "t": b1 / se,
                          "mean_ex": y.mean(), "t_mean": tm})

    out = {}
    out["all"] = slope_t(a).to_frame().T
    out["by_coin"] = a.groupby("coin").apply(slope_t)
    out["by_window"] = a.groupby("w").apply(slope_t)
    a["fq"] = pd.qcut(a.f, 5, labels=False, duplicates="drop")
    out["by_fq"] = a.groupby("fq").apply(lambda g: pd.Series({"n": len(g), "fmean": g.f.mean(), "zmean": g.z.mean(), "mean_ex": g.nx.mean(), "t": g.nx.mean() / (g.nx.std() / np.sqrt(len(g)))}))
    # by number of coins falling that day (market-wide fall vs idiosyncratic)
    cnt = a.groupby("day").coin.transform("count")
    a["ncoins"] = pd.cut(cnt, [0, 1, 3, 6, 20])
    out["by_ncoins_same_day"] = a.groupby("ncoins").apply(slope_t)
    # positive-forecast bars outside the profile? and z bins on all falls in-profile
    inp = d[(d.reg == "unknown") & (d.z < 0) & d.nx.notna()].copy()
    inp["zb"] = pd.cut(inp.z, [-20, -3, -2, -1.5, -1, -0.5, 0])
    out["in_profile_by_z"] = inp.groupby("zb").nx.agg(["count", "mean", "std"])
    out_ = d[(d.reg != "unknown") & (d.z < 0) & d.nx.notna()].copy()
    out_["zb"] = pd.cut(out_.z, [-20, -3, -2, -1.5, -1, -0.5, 0])
    out["out_profile_by_z"] = out_.groupby("zb").nx.agg(["count", "mean", "std"])
    out["share_unknown_among_pos"] = float((a.reg == "unknown").mean())
    return out
