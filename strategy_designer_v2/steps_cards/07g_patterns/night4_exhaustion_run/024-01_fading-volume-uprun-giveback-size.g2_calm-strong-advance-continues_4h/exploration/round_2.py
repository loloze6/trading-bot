def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r1 = c.pct_change()
            past = c / c.shift(H) - 1
            mabs = past.abs().rolling(180, min_periods=90).mean()
            past6 = c / c.shift(6) - 1
            m6 = past6.abs().rolling(180, min_periods=90).mean()
            vrel = np.log(v.rolling(6).sum() / v.shift(6).rolling(30).mean().mul(6) if False else v.rolling(6).sum() / (v.rolling(180, min_periods=90).mean() * 6))
            vfade = np.log(v.rolling(9).sum() / v.shift(9).rolling(9).sum())
            fwd = c.shift(-H) / c - 1
            fwd6 = c.shift(-6) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            idx = np.arange(0, len(b), H)
            rows.append(pd.DataFrame({"coin": coin, "w": int(w[1:]),
                "s18": (past / mabs).values[idx], "s6": (past6 / m6).values[idx],
                "vrel": vrel.values[idx], "vfade": vfade.values[idx],
                "fwd": fwd.values[idx], "fwd6": fwd6.values[idx], "year": ts.dt.year.values[idx]}))
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def reg(x, col, y="ex"):
        x = x.dropna(subset=[col, y])
        r = stats.linregress(x[col], x[y])
        return pd.Series({"slope": r.slope, "t": r.slope / r.stderr, "n": len(x)})
    # 1) one-day fall bounce: slope of ex on -s6 when s6<0
    neg = g[g["s6"] < 0].copy(); neg["mag"] = -neg["s6"]
    out["fall6_all"] = reg(neg, "mag").round(5).to_frame().T
    out["fall6_by_coin"] = neg.groupby("coin").apply(lambda x: reg(x, "mag")).round(5)
    neg["half"] = np.where(neg["w"] <= 12, "w1-12", "w13-24")
    out["fall6_by_half"] = neg.groupby("half").apply(lambda x: reg(x, "mag")).round(5)
    out["fall6_by_year"] = neg.groupby("year").apply(lambda x: reg(x, "mag")).round(5)
    # fall bounce graded by volume of the fall
    neg2 = neg.dropna(subset=["vrel"]).copy()
    neg2["vb"] = np.where(neg2["vrel"] > neg2.groupby("coin")["vrel"].transform("median"), "highvol", "lowvol")
    out["fall6_by_volume"] = neg2.groupby("vb").apply(lambda x: reg(x, "mag")).round(5)
    pos = g[g["s6"] > 0].copy(); pos["mag"] = pos["s6"]
    out["rise6_all"] = reg(pos, "mag").round(5).to_frame().T
    # 2) |s18| U-shape
    g["abs18"] = g["s18"].abs()
    out["abs18_all"] = reg(g, "abs18").round(5).to_frame().T
    out["abs18_by_coin"] = g.groupby("coin").apply(lambda x: reg(x, "abs18")).round(5)
    neg18 = g[g["s18"] < 0].copy(); neg18["mag"] = -neg18["s18"]
    out["fall18_all"] = reg(neg18, "mag").round(5).to_frame().T
    # 3) volume rising -> ex
    out["vfade_all"] = reg(g, "vfade").round(5).to_frame().T
    out["vrel_all"] = reg(g, "vrel").round(5).to_frame().T
    out["vrel_by_coin"] = g.groupby("coin").apply(lambda x: reg(x, "vrel")).round(5)
    g["half"] = np.where(g["w"] <= 12, "w1-12", "w13-24")
    out["vrel_by_half"] = g.groupby("half").apply(lambda x: reg(x, "vrel")).round(5)
    # 4) book weekday t
    dd = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()]).dropna(subset=["book_return"])
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    day = dd.groupby(["day"]).agg(b=("book_return", "mean"), c=("coin_return", "mean"))
    day["wd"] = pd.to_datetime(day.index).weekday
    t = day.groupby("wd")["b"].agg(["mean", "std", "count"]); t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    out["book_wd_t"] = t.round(5)
    return out
