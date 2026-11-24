def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "pos": np.arange(len(b)),
                "fwd2": c.shift(-2)/c - 1,
                "fwd5": c.shift(-5)/c - 1,
                "r1": r1,
                "r3": c/c.shift(3)-1,
                "r14": c/c.shift(14)-1,
                "r30": c/c.shift(30)-1,
                "vol20": r1.rolling(20).std(),
                "fc": b["forecast"].astype(float),
                "regime": b["regime"],
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "dlow": c/ c.rolling(60, min_periods=40).min() - 1,
                "dhigh": c/ c.rolling(60, min_periods=40).max() - 1,
                "brk": (c < c.shift(1).rolling(59, min_periods=39).min()).astype(float),
                "rng": (b["high"]-b["low"]).astype(float)/c,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            df["vr"] = df["vol20"]/df["vol20"].rolling(60, min_periods=20).mean()
            df["rngz"] = df["rng"]/df["rng"].rolling(20).mean()
            df["volz"] = (b["volume"].astype(float)/b["volume"].astype(float).rolling(20).mean())
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g2 = A[A.pos % 2 == 0].copy()
    g2["m2"] = g2.groupby("coin")["fwd2"].transform("mean")
    g2["ex2"] = g2["fwd2"] - g2["m2"]
    g5 = A[A.pos % 5 == 0].copy()
    g5["ex5"] = g5["fwd5"] - g5.groupby("coin")["fwd5"].transform("mean")
    out = {}
    def slope(df, x, y):
        d = df[[x, y]].dropna()
        d = d[np.isfinite(d[x])]
        z = (d[x]-d[x].mean())/d[x].std()
        r = stats.linregress(z, d[y])
        return pd.Series({"slope_per_sd": r.slope, "t": r.slope/r.stderr, "n": len(d)})
    feats = ["r1","r3","r14","r30","vol20","vr","dlow","dhigh","rngz","volz","brk"]
    out["slopes_fwd2"] = pd.DataFrame({f: slope(g2, f, "ex2") for f in feats}).T
    out["slopes_fwd5"] = pd.DataFrame({f: slope(g5, f, "ex5") for f in feats}).T
    def q(df, f, y, k=5):
        d = df[[f, y]].dropna().copy()
        d["q"] = d.groupby(pd.qcut(d[f].rank(method="first"), k, labels=False)).ngroup()
        return d.groupby("q")[y].agg(["mean","count", lambda s: s.mean()/s.std()*np.sqrt(len(s))]).rename(columns={"<lambda_0>":"t"})
    for f in ["r1","r14","dlow","vr","rngz","volz"]:
        out["q_"+f+"_fwd2"] = q(g2, f, "ex2")
    out["q_dlow_fwd5"] = q(g5, "dlow", "ex5")
    out["brk_fwd5"] = g5.groupby("brk")["ex5"].agg(["mean","count","std"])
    # regime x r14 sign
    g2["side"] = np.sign(g2["r14"])
    g2["dirmove"] = g2["side"]*g2["ex2"]
    out["regime_dir"] = g2.groupby("regime")["dirmove"].agg(["mean","count"])
    # weekday on 1-day returns (grid 1)
    A["f1"] = A.groupby(["coin","win"])["r1"].shift(-1)
    A["ex1"] = A["f1"] - A.groupby("coin")["f1"].transform("mean")
    out["weekday_next1"] = A.groupby((A.wd+1)%7)["ex1"].agg(["mean","count", lambda s: s.mean()/s.std()*np.sqrt(len(s))])
    # book days
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["win"]=w; D.append(d)
    D = pd.concat(D)
    bk = D.groupby(["win","day"])[["book_return","coin_return"]].mean().dropna()
    out["book_corr_coin"] = bk.corr().iloc[0,1]
    big = bk["book_return"]
    out["book_top5pct_coinret"] = bk[big >= big.quantile(.95)]["coin_return"].describe()
    out["book_bot5pct_coinret"] = bk[big <= big.quantile(.05)]["coin_return"].describe()
    out["book_by_year"] = D.assign(yr=pd.to_datetime(D["day"]).dt.year).groupby("yr")[["book_return","coin_return"]].mean()
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean","count","median"])
    T["dur_d"] = T["duration_minutes"]/1440
    out["trades_dur"] = T.groupby(pd.cut(T["dur_d"],[0,2,4,8,16,1000]))["net_profit_loss_percent"].agg(["mean","count"])
    out["trades_coin"] = T.groupby(["coin","side"])["net_profit_loss_percent"].agg(["mean","count"])
    return out
