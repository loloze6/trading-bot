def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    H = [6, 18, 36]
    feats = {}
    drift = {}
    for coin, wins in bars.items():
        for w, df in wins.items():
            d = df[["timestamp","open","high","low","close"]].copy().reset_index(drop=True)
            c = d["close"]; rng = d["high"] - d["low"]
            d["low12"] = d["low"].shift(1).rolling(12).min()
            d["high12"] = d["high"].shift(1).rolling(12).max()
            mr = rng.shift(1).rolling(180, min_periods=90).mean()
            d["width"] = (d["high12"] - d["low12"]) / mr
            d["depth"] = (d["low12"] - c) / mr
            d["height"] = (c - d["high12"]) / mr
            d["r180"] = c / c.shift(180) - 1
            d["r6"] = c / c.shift(6) - 1
            d["r18"] = c / c.shift(18) - 1
            r1 = c.pct_change()
            sd = r1.rolling(180, min_periods=90).std()
            d["z1"] = r1 / sd
            d["vol"] = sd
            d["pos"] = np.arange(len(d))
            for h in H:
                d[f"f{h}"] = c.shift(-h) / c - 1
            ts = pd.to_datetime(d["timestamp"])
            d["hour"] = ts.dt.hour; d["wd"] = ts.dt.weekday; d["year"] = ts.dt.year
            d["coin"] = coin; d["win"] = w
            feats.setdefault(coin, []).append(d)
    for coin, lst in feats.items():
        for h in H:
            vals = []
            for d in lst:
                g = d[d["pos"] % h == 0][f"f{h}"].dropna()
                vals.append(g)
            drift[(coin, h)] = pd.concat(vals).mean()
    allb = pd.concat([d for lst in feats.values() for d in lst], ignore_index=True)
    # vol tercile per coin
    allb["volq"] = allb.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False) if s.notna().sum() > 10 else np.nan)
    for h in H:
        allb[f"u{h}"] = allb[f"f{h}"] - allb["coin"].map({k[0]: v for k, v in drift.items() if k[1] == h})

    def cases(mask, h):
        sub = allb[mask & allb[f"u{h}"].notna()].copy()
        sub["cell"] = sub["pos"] // h
        return sub.groupby(["coin", "win", "cell"], sort=False).head(1)

    def summ(x):
        x = x.dropna(); n = len(x)
        if n < 5: return pd.Series({"n": n, "mean": np.nan, "t": np.nan})
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})

    brk = allb["close"] < allb["low12"]; bup = allb["close"] > allb["high12"]
    up = allb["r180"] > 0; dn = allb["r180"] <= 0
    sig = {"breakdown_up30": brk & up, "breakdown_dn30": brk & dn, "breakout_up30": bup & up, "breakout_dn30": bup & dn}
    t1 = []
    for nm, m in sig.items():
        for h in H:
            s = summ(cases(m, h)[f"u{h}"]); s["sig"] = nm; s["h"] = h; t1.append(s)
    out = {"signals_by_horizon_long_unusual": pd.DataFrame(t1)}

    def quint(nm, m, col, h=18, q=5):
        cs = cases(m, h)
        cs = cs[cs[col].notna()]
        cs["q"] = pd.qcut(cs[col].rank(method="first"), q, labels=False)
        r = cs.groupby("q")[f"u{h}"].apply(summ).unstack()
        r["col_mean"] = cs.groupby("q")[col].mean()
        return r
    out["bd_up_by_width"] = quint("a", sig["breakdown_up30"], "width")
    out["bd_up_by_depth"] = quint("a", sig["breakdown_up30"], "depth")
    out["bd_up_by_r180"] = quint("a", sig["breakdown_up30"], "r180")
    out["bd_dn_by_r180"] = quint("b", sig["breakdown_dn30"], "r180")
    out["bd_up_by_volq"] = cases(sig["breakdown_up30"], 18).groupby("volq")["u18"].apply(summ).unstack()
    out["bd_up_by_year"] = cases(sig["breakdown_up30"], 18).groupby("year")["u18"].apply(summ).unstack()
    out["bd_up_by_hour"] = cases(sig["breakdown_up30"], 18).groupby("hour")["u18"].apply(summ).unstack()
    # all-bar grid: graded features
    g = allb[(allb["pos"] % 18 == 0) & allb["u18"].notna()].copy()
    rows = []
    for col in ["z1", "r6", "r18", "r180", "width"]:
        x = g[[col, "u18"]].dropna()
        x["q"] = pd.qcut(x[col].rank(method="first"), 5, labels=False)
        m = x.groupby("q")["u18"].mean()
        rho, p = stats.spearmanr(x[col], x["u18"])
        rows.append(pd.Series({"feat": col, "n": len(x), "rho": rho, "p": p, "q0": m[0], "q2": m[2], "q4": m[4]}))
    out["grid18_feature_quintiles"] = pd.DataFrame(rows)
    g6 = allb[(allb["pos"] % 6 == 0) & allb["u6"].notna()].copy()
    out["grid6_by_weekday"] = g6.groupby("wd")["u6"].apply(summ).unstack()
    out["grid6_by_hour"] = g6.groupby("hour")["u6"].apply(summ).unstack()
    # book
    dd = pd.concat([df.assign(coin=c, win=w) for c, ws in days.items() for w, df in ws.items()], ignore_index=True)
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["book_by_year"] = dd.groupby("year")[["book_return", "coin_return"]].mean()
    out["book_by_coin"] = dd.groupby("coin")[["book_return", "coin_return"]].mean()
    return out
