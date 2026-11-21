def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []      # grid-bar rows
    one = []       # 1-bar rows
    for coin, wins in data["bars"].items():
        # per coin drift/usual from grid
        per = []
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]; hi = b["high"]; lo = b["low"]
            b["r42"] = c / c.shift(42) - 1
            b["r6"] = c / c.shift(6) - 1
            b["up"] = c > hi.shift(1).rolling(12).max()
            b["dn"] = c < lo.shift(1).rolling(12).min()
            rng = (hi.rolling(12).max() - lo.rolling(12).min()) / c
            b["narrow"] = np.log(rng / rng.rolling(120, min_periods=60).mean())
            lr = np.log(c).diff()
            b["vol"] = lr.rolling(42).std()
            b["volrel"] = np.log(b["vol"] / lr.rolling(360, min_periods=180).std())
            b["f18"] = c.shift(-H) / c - 1
            b["f1"] = c.shift(-1) / c - 1
            b["pos"] = np.arange(len(b))
            b["cell"] = b["pos"] // H
            b["coin"] = coin; b["win"] = w
            ts = pd.to_datetime(b["timestamp"])
            b["year"] = ts.dt.year; b["hour"] = ts.dt.hour; b["wd"] = ts.dt.weekday
            per.append(b)
        allb = pd.concat(per)
        g = allb[allb["pos"] % H == 0]["f18"].dropna()
        drift, usual = g.mean(), g.std()
        s1 = allb["f1"].std(); m1 = allb["f1"].mean()
        allb["adj"] = allb["f18"] - drift
        allb["z"] = allb["adj"] / usual
        allb["z1"] = (allb["f1"] - m1) / s1
        rows.append(allb)
    A = pd.concat(rows, ignore_index=True)
    out = {}
    def summ(x, col="adj"):
        v = x[col].dropna()
        n = len(v)
        return pd.Series({"n": n, "mean_adj": v.mean(), "t": v.mean() / (v.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": x["z"].mean(), "coins_pos": x.groupby("coin")[col].mean().gt(0).sum(),
                          "coins": x["coin"].nunique()})
    # A: signal groups, first signal per cell
    groups = {
        "up_fallweek": (A["up"]) & (A["r42"] < 0),
        "up_riseweek": (A["up"]) & (A["r42"] > 0),
        "dn_fallweek": (A["dn"]) & (A["r42"] < 0),
        "dn_riseweek": (A["dn"]) & (A["r42"] > 0),
    }
    res = {}
    firsts = {}
    for k, m in groups.items():
        f = A[m & A["f18"].notna()].groupby(["coin", "win", "cell"]).head(1)
        firsts[k] = f
        res[k] = summ(f)
    out["A_signal_groups_raw_adj18"] = pd.DataFrame(res).T
    # B: grading by r42 quintile within each group
    for k in ["up_fallweek", "dn_riseweek", "up_riseweek", "dn_fallweek"]:
        f = firsts[k].copy()
        f["q"] = pd.qcut(f["r42"], 5, labels=False)
        out["B_" + k + "_by_r42_q"] = f.groupby("q").apply(summ)
    G = A[(A["pos"] % H == 0) & A["f18"].notna()].copy()
    for col in ["r42", "r6", "narrow", "volrel"]:
        x = G.dropna(subset=[col]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        t = x.groupby("q").apply(summ)
        t["abs_z"] = x.groupby("q")["z"].apply(lambda s: s.abs().mean())
        out["C_grid_by_" + col + "_q"] = t
    # up_fallweek by year and by narrowness
    f = firsts["up_fallweek"].copy()
    out["D_upfall_by_year"] = f.groupby("year").apply(summ)
    f2 = f.dropna(subset=["narrow"]).copy()
    f2["nq"] = pd.qcut(f2["narrow"], 3, labels=False)
    out["D_upfall_by_narrow_tercile"] = f2.groupby("nq").apply(summ)
    f3 = f.dropna(subset=["volrel"]).copy()
    f3["vq"] = pd.qcut(f3["volrel"], 3, labels=False)
    out["D_upfall_by_volrel_tercile"] = f3.groupby("vq").apply(summ)
    # hours / weekday, 1-bar
    o = A.dropna(subset=["z1"])
    hh = o.groupby("hour")["z1"].agg(["mean", "count", "std"]); hh["t"] = hh["mean"] / (hh["std"] / np.sqrt(hh["count"]))
    out["E_hour_1bar_z"] = hh
    ww = o.groupby("wd")["z1"].agg(["mean", "count", "std"]); ww["t"] = ww["mean"] / (ww["std"] / np.sqrt(ww["count"]))
    out["E_weekday_1bar_z"] = ww
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w
            d["year"] = pd.to_datetime(d["day"]).dt.year
            D.append(d)
    D = pd.concat(D)
    out["F_book_by_year"] = D.groupby("year")[["book_return", "coin_return"]].mean()
    bc = D.groupby("coin")["book_return"].agg(["mean", "std"]); bc["sharpe"] = bc["mean"] / bc["std"] * np.sqrt(365)
    out["F_book_by_coin"] = bc
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_h"] = T["duration_minutes"] / 60
    T["dq"] = pd.qcut(T["dur_h"].rank(method="first"), 4, labels=False)
    out["G_trades_by_duration_q"] = T.groupby("dq")[["dur_h", "profit_loss_percent", "net_profit_loss_percent"]].agg(["mean", "count"])
    return out
