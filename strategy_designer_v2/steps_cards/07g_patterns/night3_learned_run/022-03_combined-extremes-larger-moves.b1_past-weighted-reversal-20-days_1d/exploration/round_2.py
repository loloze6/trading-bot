def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    recs = []
    for coin, wins in bars.items():
        for H in [5, 10, 20, 40]:
            fr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                fr += list(c[idx + H] / c[idx] - 1)
            fr = np.array(fr); drift, usual = fr.mean(), fr.std()
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"]; r1 = c.pct_change()
                sd = r1.rolling(60, min_periods=30).std().shift(1)
                lv = np.log(b["volume"].replace(0, np.nan))
                vz = (lv - lv.rolling(60, min_periods=30).mean().shift(1)) / lv.rolling(60, min_periods=30).std().shift(1)
                df = pd.DataFrame({"coin": coin, "win": w, "H": H,
                                   "z1": r1 / sd, "r1": r1, "vz": vz,
                                   "r5z": (c / c.shift(5) - 1) / (sd * np.sqrt(5)),
                                   "fwd": c.shift(-H) / c - 1,
                                   "yr": pd.to_datetime(b["timestamp"]).dt.year,
                                   "pos": np.arange(len(b))})
                df["str"] = (df["fwd"] - drift) / usual
                df["ex"] = df["fwd"] - drift
                recs.append(df.dropna(subset=["fwd", "z1"]))
    A = pd.concat(recs)
    # grid offsets: offset 0 grid (official) and the mean of t over offsets
    res = []
    for H in [5, 10, 20, 40]:
        d = A[A.H == H]
        g = d[d.pos % H == 0]
        rho = stats.spearmanr(g["z1"], g["str"]).correlation
        # slope of str on -z1 clipped
        x = -g["z1"].clip(-4, 4)
        sl = stats.linregress(x, g["str"])
        ts = []
        for o in range(H):
            gg = d[d.pos % H == o]
            ts.append(stats.linregress(-gg["z1"].clip(-4, 4), gg["str"]).rvalue * np.sqrt(len(gg)))
        res.append([H, len(g), round(rho, 3), round(sl.slope, 4), round(sl.rvalue * np.sqrt(len(g)), 2),
                    round(np.mean(ts), 2), round(np.min(ts), 2), round(np.max(ts), 2)])
    out["rev_by_horizon"] = pd.DataFrame(res, columns=["H", "n", "spearman", "slope_str_per_negz", "t", "t_mean_offsets", "t_min", "t_max"])
    g = A[(A.H == 20) & (A.pos % 20 == 0)].copy()
    g["q"] = pd.qcut(g["z1"], 5, labels=False)
    out["z1_quintile_20d"] = g.groupby("q").agg(z=("z1", "mean"), strength=("str", "mean"), excess=("ex", "mean"), n=("str", "size")).round(4)
    g["sig"] = -np.sign(g["z1"]) * np.minimum(g["z1"].abs(), 4)
    def tt(x):
        r = stats.linregress(x["sig"], x["str"]); return pd.Series({"slope": round(r.slope, 4), "t": round(r.rvalue * np.sqrt(len(x)), 2), "n": len(x)})
    out["rev20_by_year"] = g.groupby("yr").apply(tt)
    out["rev20_by_coin"] = g.groupby("coin").apply(tt)
    g["vq"] = pd.qcut(g["vz"], 3, labels=False)
    out["rev20_by_volz_tercile"] = g.dropna(subset=["vq"]).groupby("vq").apply(tt)
    g["big"] = g["z1"].abs() > 1
    out["vol_signed_by_bigmove"] = g.dropna(subset=["vz"]).assign(vqq=lambda x: pd.qcut(x["vz"], 3, labels=False)).groupby(["vqq"])["str"].agg(["mean", "count"]).round(3)
    # book: what carries its loss
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            b = bars[coin][w].copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            p = b.groupby("day")["postRebalance_current_allocation"].last()
            x = x.copy(); x["day"] = pd.to_datetime(x["day"])
            x = x.merge(p.rename("pos").reset_index(), on="day", how="left")
            x["posprev"] = x["pos"].shift(1)
            x["coin"] = coin
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return", "posprev"])
    out["book_long_vs_short"] = D.assign(side=np.sign(D["posprev"])).groupby("side").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"), abspos=("posprev", lambda s: s.abs().mean()))
    out["book_mean_daily"] = round(D["book_return"].mean(), 6)
    return out
