def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 36
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            if len(b) < 60:
                continue
            c, hi, lo = b["close"].astype(float), b["high"].astype(float), b["low"].astype(float)
            rng = (hi - lo)
            r180 = rng.rolling(180, min_periods=60).mean()
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b))})
            d["brk_up"] = (c - hi.shift(1).rolling(12).max()) / r180
            d["brk_dn"] = (lo.shift(1).rolling(12).min() - c) / r180
            d["quiet"] = rng.shift(1).rolling(12).mean() / r180
            d["r7"] = c / c.shift(42) - 1
            d["r30"] = c / c.shift(180) - 1
            lr = np.log(c).diff()
            d["vol30"] = lr.rolling(180, min_periods=60).std()
            d["fwd"] = c.shift(-H) / c - 1
            d["fwd6"] = c.shift(-6) / c - 1
            d["ret1"] = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            d["hour"] = ts.dt.hour.values
            d["wd"] = ts.dt.weekday.values
            d["cell"] = d["pos"] // H
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    g = D[D["pos"] % H == 0].dropna(subset=["fwd"])
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    D["unu"] = D["fwd"] - D["coin"].map(drift)
    D["str"] = D["unu"] / D["coin"].map(sd)
    out = {}

    def summ(x, col="unu"):
        x = x.dropna(subset=[col])
        n = len(x)
        m = x[col].mean()
        t = m / (x[col].std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": m, "t": t, "strength": x["str"].mean()})

    def events(mask):
        e = D[mask].dropna(subset=["fwd"])
        return e.groupby(["coin", "win", "cell"]).head(1)

    # up breaks by 7d sign and size tercile
    eu = events(D["brk_up"] > 0)
    eu = eu.assign(r7pos=eu["r7"] > 0, size_t=pd.qcut(eu["brk_up"], 3, labels=["s", "m", "l"]),
                   quiet_t=pd.qcut(eu["quiet"], 3, labels=["quiet", "mid", "wide"]))
    out["up_by_r7_size"] = eu.groupby(["r7pos", "size_t"]).apply(summ)
    out["up_by_r7_quiet"] = eu.groupby(["r7pos", "quiet_t"]).apply(summ)
    # down breaks
    ed = events(D["brk_dn"] > 0)
    ed = ed.assign(r7pos=ed["r7"] > 0, size_t=pd.qcut(ed["brk_dn"], 3, labels=["s", "m", "l"]),
                   quiet_t=pd.qcut(ed["quiet"], 3, labels=["quiet", "mid", "wide"]))
    out["dn_by_r7_size(long sign)"] = ed.groupby(["r7pos", "size_t"]).apply(summ)
    out["dn_by_r7_quiet(long sign)"] = ed.groupby(["r7pos", "quiet_t"]).apply(summ)
    # grid-start continuous features
    G = D[D["pos"] % H == 0].dropna(subset=["fwd", "r7", "quiet", "vol30", "r30"]).copy()
    G["absstr"] = (G["fwd"] - G["coin"].map(drift)).abs() / G["coin"].map(sd)
    for f in ["r7", "r30", "quiet", "vol30"]:
        G["q"] = G.groupby("coin")[f].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t1 = G.groupby("q").apply(summ)
        t1["abs_move_str"] = G.groupby("q")["absstr"].mean()
        out["grid_quintile_" + f] = t1
    # hour/weekday on one-bar returns
    B = D.dropna(subset=["ret1"]).copy()
    B["ret1u"] = B["ret1"] - B["coin"].map(B.groupby("coin")["ret1"].mean())
    hw = B.groupby("hour")["ret1u"].agg(["count", "mean", "std"])
    hw["t"] = hw["mean"] / (hw["std"] / np.sqrt(hw["count"]))
    out["hour_unusual_1bar"] = hw
    wd = B.groupby("wd")["ret1u"].agg(["count", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday_unusual_1bar"] = wd
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w
            x["yr"] = pd.to_datetime(x["day"]).dt.year
            dd.append(x)
    DD = pd.concat(dd).dropna(subset=["book_return"])
    bk = DD.groupby(["win", "day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean"), yr=("yr", "first")).reset_index()
    out["book_by_year"] = bk.groupby("yr").agg(n=("b", "size"), book=("b", "mean"), hold=("c", "mean"))
    s = bk["b"].sort_values()
    tot = bk["b"].sum()
    out["book_share_top10_days"] = float(s.tail(10).sum() / tot)
    out["book_share_worst10_days"] = float(s.head(10).sum() / tot)
    return out
