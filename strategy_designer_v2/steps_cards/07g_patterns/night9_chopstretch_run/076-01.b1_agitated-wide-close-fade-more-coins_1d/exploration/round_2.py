def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].astype(float)
            allr.append((c.shift(-1)/c - 1).dropna())
        mu = pd.concat(allr).mean()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = (h - l); mr = rng.rolling(20, min_periods=20).mean(); rm = rng / mr
            clv = ((c - l) / rng.replace(0, np.nan))
            r1 = c.shift(-1)/c - 1; r2 = c.shift(-2)/c - 1
            tr = c/c.shift(60) - 1
            d = pd.DataFrame({"coin": coin, "win": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "rm": rm, "clv": clv, "u1": r1 - mu, "u2": r2 - 2*mu, "g2": (np.arange(len(b)) % 2 == 0),
                              "agit": (b["regime"] != "chop"), "trend": tr,
                              "alloc": b["postRebalance_current_allocation"].astype(float)})
            rows.append(d)
    df = pd.concat(rows, ignore_index=True).dropna(subset=["rm","clv"])
    def stat(g, col="u1"):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "days": np.nan, "mean%": np.nan, "t_day": np.nan})
        s = g.groupby("day")[col].apply(lambda x: (x - g[col].mean()).sum())
        dd = len(s); se = np.sqrt((s**2).sum() * dd/(dd-1)) / len(g)
        return pd.Series({"n": len(g), "days": dd, "mean%": 100*g[col].mean(), "t_day": g[col].mean()/se})
    df["tb"] = pd.cut(df["trend"], [-9, -0.1, 0.1, 99], labels=["falling","choppy","rising"])
    df["clvb"] = pd.cut(df["clv"], [-0.01, 0.33, 0.67, 1.01], labels=["low","mid","high"])
    wide = df[df.rm >= 1.5]
    out = {}
    out["agitated wide by trend x close"] = wide[wide.agit].groupby(["tb","clvb"], observed=True).apply(stat).reset_index()
    # graded: product rm*clv vs rm*(1-clv) as predictors, agitated, all days with rm>=1
    a = df[(df.agit)].dropna(subset=["u1"]).copy()
    a["hi_push"] = a.rm * a.clv; a["lo_push"] = a.rm * (1 - a.clv)
    from scipy import stats
    out["agit spearman u1 vs hi_push, lo_push"] = pd.Series({
        "hi_push rho": stats.spearmanr(a.hi_push, a.u1)[0], "lo_push rho": stats.spearmanr(a.lo_push, a.u1)[0], "n": len(a)})
    c_ = df[(~df.agit)].dropna(subset=["u1"]).copy()
    c_["hi_push"] = c_.rm * c_.clv; c_["lo_push"] = c_.rm*(1-c_.clv)
    out["calm spearman"] = pd.Series({"hi_push rho": stats.spearmanr(c_.hi_push, c_.u1)[0], "lo_push rho": stats.spearmanr(c_.lo_push, c_.u1)[0], "n": len(c_)})
    # wide high close calm choppy by window
    sub = wide[(~wide.agit) & (wide.tb=="choppy") & (wide.clvb=="high")].dropna(subset=["u1"])
    out["calm choppy wide high close by window"] = sub.groupby("win")["u1"].agg(["count","mean"])
    # wide high close (all profiles) quintiles of rm, u1 and u2 grid
    wh = df[(df.clv > 0.67)].dropna(subset=["u1"]).copy()
    wh["rmq"] = pd.qcut(wh.rm, 5, labels=False)
    out["high close by rm quintile, agit"] = wh[wh.agit].groupby("rmq").apply(stat)
    out["high close by rm quintile, calm"] = wh[~wh.agit].groupby("rmq").apply(stat)
    # book: short positions days, u1 by clv band
    pos = df[df.alloc < 0].dropna(subset=["u1"])
    out["held shorts by close band"] = pos.groupby("clvb", observed=True).apply(stat)
    return out
