def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            rng = h - l
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "cl": np.where(rng > 0, (c - l) / rng, np.nan),
                "rangepct": rng / c,
                "r0": c.pct_change(),
                "r1": c.shift(-1) / c - 1,
                "vol20": c.pct_change().rolling(20, min_periods=10).std(),
                "ret60": c / c.shift(60) - 1,
                "ts": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "alloc": b["postRebalance_current_allocation"].astype(float),
            })
            df["rngrel"] = df["rangepct"] / df["rangepct"].rolling(20, min_periods=10).median()
            df["vrel"] = df["vol20"] / df["vol20"].rolling(60, min_periods=20).median()
            df["gain"] = df["alloc"] * df["r1"]
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    mu = d.groupby("coin")["r1"].mean()
    d["x1"] = d["r1"] - d["coin"].map(mu)
    d["near_low"] = 1 - d["cl"]          # 1 at low, 0 at high
    d["dl"] = d["rangepct"] * d["near_low"]   # distance close-to-low pull, in % of price: range * nearness to low
    d["drop_from_high"] = d["rangepct"] * d["near_low"]  # (high-close)/close approx
    out = {}
    def cl_t(sub, xcol, ycol="x1"):
        s = sub[[xcol, ycol, "ts"]].dropna()
        if len(s) < 30: return pd.Series({"n": len(s), "slope": np.nan, "t_day": np.nan})
        x = s[xcol] - s[xcol].mean(); y = s[ycol] - s[ycol].mean()
        b = (x*y).sum()/(x*x).sum(); e = y - b*x
        g = (x*e).groupby(s["ts"]).sum()
        se = np.sqrt((g**2).sum())/(x*x).sum()
        return pd.Series({"n": len(s), "days": s["ts"].nunique(), "slope": b, "t_day": b/se})
    # graded: which measure predicts better, nearness to low or the pull (high-close)/close
    low = d[d["cl"] < 0.5]
    out["low half: slope on near_low"] = cl_t(low, "near_low")
    out["low half: slope on (high-close)/close"] = cl_t(low, "drop_from_high")
    out["all bars: slope on (high-close)/close"] = cl_t(d, "drop_from_high")
    out["all bars: slope on day return"] = cl_t(d, "r0")
    # within vol terciles: slope on near_low, all bars
    d["vq"] = pd.qcut(d["vrel"], 3, labels=["calm", "mid", "agit"])
    out["slope x1 on near_low by rel-vol tercile"] = d.groupby("vq", observed=True).apply(lambda s: cl_t(s, "near_low"))
    d["tr"] = pd.cut(d["ret60"], [-10, -0.1, 0.1, 100], labels=["falling", "choppy", "rising"])
    out["slope x1 on near_low by trend"] = d.groupby("tr", observed=True).apply(lambda s: cl_t(s, "near_low"))
    # interaction near_low * range: product as predictor, and residual after day return
    d["nl_x_rng"] = d["near_low"] * d["rngrel"]
    out["all: slope on near_low*rngrel"] = cl_t(d, "nl_x_rng")
    # residualise x1 on r0 then test near_low and drop_from_high
    s = d[["r0", "x1"]].dropna()
    bb = np.polyfit(s["r0"], s["x1"], 1)
    d["x1r"] = d["x1"] - np.polyval(bb, d["r0"])
    out["x1 resid of day return: slope on near_low"] = cl_t(d, "near_low", "x1r")
    out["x1 resid of day return: slope on (high-close)/close"] = cl_t(d, "drop_from_high", "x1r")
    # 2-way table: near_low half x day return sign
    d["half"] = np.where(d["cl"] < 0.5, "lowhalf", "highhalf")
    d["dsign"] = np.where(d["r0"] < 0, "down", "up")
    out["x1 mean% by half x day sign"] = d.groupby(["half", "dsign"])["x1"].agg(lambda s: s.mean()*100)
    out["n by half x day sign"] = d.groupby(["half", "dsign"])["x1"].count()
    # book: gains by vol tercile, by trend
    book = d[d["alloc"].abs() > 1e-9]
    out["book gain% per pos-bar by vol tercile"] = book.groupby("vq", observed=True)["gain"].agg(["count", lambda s: s.mean()*100, lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["book gain% per pos-bar by trend"] = book.groupby("tr", observed=True)["gain"].agg(["count", lambda s: s.mean()*100, lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # high closes: slope on cl in high half by vol tercile (short side)
    hi = d[d["cl"] >= 0.5]
    out["high half: slope x1 on cl by vol tercile"] = hi.groupby("vq", observed=True).apply(lambda s: cl_t(s, "cl"))
    return out
