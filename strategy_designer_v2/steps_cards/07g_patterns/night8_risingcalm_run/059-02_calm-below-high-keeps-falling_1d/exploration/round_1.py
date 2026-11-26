def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30, min_periods=20).std()
            hi14 = c.rolling(14, min_periods=10).max()
            depth = (c - hi14) / hi14 / vol30
            ret14 = (c / c.shift(14) - 1) / (vol30 * np.sqrt(14))
            ret1s = r1 / vol30
            tr60 = c / c.shift(60) - 1
            rng = (b["high"] - b["low"]) / c / vol30
            clpos = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                "depth": depth, "ret14": ret14, "ret1s": ret1s, "tr60": tr60, "rng": rng,
                "clpos": clpos, "fwd": fwd, "fwd1": fwd1, "calm": (b["regime"] == "unknown"),
                "fc": b["forecast"], "alloc": b["postRebalance_current_allocation"],
                "gain": b["postRebalance_current_allocation"] * fwd1,
                "year": ts.dt.year, "wd": ts.dt.weekday, "vol30": vol30})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[A["pos"] % H == 0].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    usual = g.groupby("coin")["fwd"].std()
    g["ex"] = g["fwd"] - g["coin"].map(drift)
    g["exs"] = g["ex"] / g["coin"].map(usual)
    g["trend"] = np.where(g["tr60"] > 0.1, "rising", np.where(g["tr60"] < -0.1, "falling", np.where(g["tr60"].notna(), "choppy", "na")))
    g["agit"] = np.where(g["calm"], "calm", "agit")
    out = {}
    def tab(df, key, q=5):
        d = df.dropna(subset=[key, "ex"]).copy()
        d["q"] = pd.qcut(d[key].rank(method="first"), q, labels=False)
        t = d.groupby("q").agg(n=("ex", "size"), mean_key=(key, "mean"), ex_mean=("ex", "mean"), exs=("exs", "mean"))
        t["t"] = d.groupby("q")["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))))
        return t.round(4)
    for ag in ["calm", "agit"]:
        out[f"depth_q_{ag}"] = tab(g[g.agit == ag], "depth")
        out[f"ret14_q_{ag}"] = tab(g[g.agit == ag], "ret14")
        out[f"ret1s_q_{ag}"] = tab(g[g.agit == ag], "ret1s")
    # by profile, slope of exs on depth
    res = []
    for (tr, ag), d in g.dropna(subset=["depth"]).groupby(["trend", "agit"]):
        if len(d) > 30:
            s = stats.linregress(d["depth"], d["exs"])
            res.append({"trend": tr, "agit": ag, "n": len(d), "slope": s.slope, "t": s.slope / s.stderr, "ex_mean": d["ex"].mean()})
    out["depth_slope_by_profile"] = pd.DataFrame(res).round(4)
    res = []
    for (tr, ag), d in g.dropna(subset=["ret1s"]).groupby(["trend", "agit"]):
        if len(d) > 30:
            s = stats.linregress(d["ret1s"], d["exs"])
            res.append({"trend": tr, "agit": ag, "n": len(d), "slope": s.slope, "t": s.slope / s.stderr})
    out["ret1s_slope_by_profile"] = pd.DataFrame(res).round(4)
    out["range_q_all"] = tab(g, "rng")
    out["clpos_q_all"] = tab(g, "clpos")
    # weekday 1-day returns, all bars
    a = A.dropna(subset=["fwd1"]).copy()
    a["ex1"] = a["fwd1"] - a["coin"].map(a.groupby("coin")["fwd1"].mean())
    wd = a.groupby("wd")["ex1"].agg(["size", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["size"]))
    out["weekday_next_day_ex"] = wd.round(5)
    # book by year
    by = A.dropna(subset=["gain"]).groupby(["year"]).agg(gain=("gain", "mean"), inpos=("alloc", lambda x: (x != 0).mean()))
    out["book_gain_by_year"] = by.round(5)
    return out
