def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            z = r1 / r1.rolling(20).std()
            tr20 = c / c.shift(20) - 1
            z5 = (c / c.shift(5) - 1) / (r1.rolling(20).std() * np.sqrt(5))
            z20 = tr20 / (r1.rolling(60).std() * np.sqrt(20))
            tr60 = c / c.shift(60) - 1
            f3 = c.shift(-3) / c - 1
            idx = np.arange(0, len(b), 3)
            rows.append(pd.DataFrame({
                "coin": coin, "w": w, "z": z.values[idx], "z5": z5.values[idx], "z20": z20.values[idx],
                "tr60": tr60.values[idx], "f3": f3.values[idx],
                "inprof": (b["regime"].values[idx] == "unknown"),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values[idx]}))
    df = pd.concat(rows)
    df["u3"] = df["f3"] - df.groupby("coin")["f3"].transform("mean")
    df = df.dropna(subset=["u3", "z"])
    out = {}
    def daytest(g, col):
        s = g.groupby("day")[col].sum()
        return pd.Series({"n_cases": len(g), "n_days": len(s), "mean%": 100 * g[col].mean(),
                          "t_day": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    # Idea A: falling calm down days continue, graded by down size
    p = df[df.inprof].copy()
    p["dn"] = (-p["z"]).clip(lower=0)
    pd_ = p[p.dn > 0].copy()
    pd_["cont"] = -pd_["u3"] * pd_["dn"]   # signed: positive if fall continues, weighted
    pd_["cont1"] = -pd_["u3"]
    out["prof_down_weighted"] = daytest(pd_, "cont")
    out["prof_down_unweighted"] = daytest(pd_, "cont1")
    sl = stats.linregress(pd_["dn"], pd_["cont1"])
    out["prof_down_slope"] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "n": len(pd_)})
    out["prof_down_by_window"] = pd_.groupby("w").apply(lambda g: daytest(g, "cont"))
    out["prof_down_by_coin"] = pd_.groupby("coin").apply(lambda g: daytest(g, "cont"))
    # same with tr60 instead of regime (falling only, any agitation) to compare
    f = df[df.tr60 < -0.1].copy()
    f["dn"] = (-f["z"]).clip(lower=0); f = f[f.dn > 0]
    f["cont"] = -f["u3"] * f["dn"]
    out["falling_any_down_weighted"] = f.groupby("inprof").apply(lambda g: daytest(g, "cont"))
    # outside profile down days rebound, by trend bucket
    o = df[~df.inprof].copy()
    o["dn"] = (-o["z"]).clip(lower=0); o = o[o.dn > 0]
    o["reb"] = o["u3"] * o["dn"]
    o["trb"] = pd.cut(o["tr60"], [-9, -0.1, 0.1, 9])
    out["outside_down_rebound_by_trend"] = o.groupby("trb").apply(lambda g: daytest(g, "reb"))
    # Idea B: 20-day scaled move momentum, all bars
    df["mom"] = df["u3"] * df["z20"]
    out["mom20_all"] = daytest(df.dropna(subset=["z20"]), "mom")
    out["mom20_by_window"] = df.dropna(subset=["z20"]).groupby("w").apply(lambda g: daytest(g, "mom"))
    df["mom5"] = df["u3"] * df["z5"]
    out["mom5_all"] = daytest(df.dropna(subset=["z5"]), "mom5")
    out["mom20_inprof"] = df.dropna(subset=["z20"]).groupby("inprof").apply(lambda g: daytest(g, "mom"))
    return out
