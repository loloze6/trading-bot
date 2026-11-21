def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    day_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "win": w,
                "regime": b["regime"].values,
                "fc": b["forecast"].astype(float).values,
                "pos": b["postRebalance_current_allocation"].astype(float).values,
                "ret1": r1.values,
                "ret3": (c / c.shift(3) - 1).values,
                "ret7": (c / c.shift(7) - 1).values,
                "ret20": (c / c.shift(20) - 1).values,
                "vol20": r1.rolling(20).std().values,
                "near20": (c / c.rolling(20).max() - 1).values,
                "fwd": (c.shift(-H) / c - 1).values,
                "fwd1": (c.shift(-1) / c - 1).values,
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values,
                "i": np.arange(len(b)),
            })
            rows.append(f)
    df = pd.concat(rows, ignore_index=True)
    g = df[df["i"] % H == 0].copy()
    drift = g.groupby("coin")["fwd"].mean()
    g["adj"] = g["fwd"] - g["coin"].map(drift)
    usual = g.groupby("coin")["fwd"].std()
    g["adjn"] = g["adj"] / g["coin"].map(usual)
    out = {}
    # regime split
    out["fwd5_by_regime"] = g.groupby("regime")["adj"].agg(["mean", "count", lambda s: s.mean()/s.std()*np.sqrt(len(s))]).rename(columns={"<lambda_0>": "t"})
    # feature slopes by regime
    res = []
    for feat in ["ret1", "ret3", "ret7", "ret20", "vol20", "near20", "fc"]:
        for reg in ["trending", "unknown", "all"]:
            s = g if reg == "all" else g[g["regime"] == reg]
            s = s[["coin", feat, "adjn"]].dropna()
            if len(s) < 50: continue
            z = s.groupby("coin")[feat].transform(lambda x: (x - x.mean()) / x.std())
            lr = stats.linregress(z, s["adjn"])
            res.append([feat, reg, lr.slope, lr.slope / lr.stderr, len(s)])
    out["slopes_std_feature_on_norm_fwd5"] = pd.DataFrame(res, columns=["feat", "regime", "slope", "t", "n"])
    # quintiles of ret20 in unknown regime, and vol20
    for feat, reg in [("ret20", "unknown"), ("vol20", "all"), ("ret3", "all"), ("near20", "trending")]:
        s = g if reg == "all" else g[g["regime"] == reg]
        s = s[["coin", feat, "adj"]].dropna().copy()
        s["q"] = s.groupby("coin")[feat].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
        out[f"q_{feat}_{reg}"] = s.groupby("q")["adj"].agg(["mean", "count"])
    # weekday on 1-day returns
    d = df.dropna(subset=["fwd1"]).copy()
    d["adj1"] = d["fwd1"] - d.groupby("coin")["fwd1"].transform("mean")
    wd = d.groupby((d["wd"] + 1) % 7)["adj1"].agg(["mean", "std", "count"])
    wd["t"] = wd["mean"] / wd["std"] * np.sqrt(wd["count"])
    out["next_day_by_weekday_of_close"] = wd
    # book by regime and position side
    df["gain"] = df["pos"] * df["fwd1"]
    df["side"] = np.sign(df["pos"]).fillna(0)
    out["gain_by_regime_side"] = df.groupby(["regime", "side"])["gain"].agg(["mean", "count", "sum"])
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"])
        out["trades_by_coin"] = T.groupby(["coin", "side"])["net_profit_loss_percent"].agg(["mean", "count"])
    # book days: before/after largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.reset_index(drop=True).copy()
            x["coin"] = coin; x["win"] = w
            x["nxt"] = x["book_return"].shift(-1)
            x["prv"] = x["book_return"].shift(1)
            dd.append(x)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["q"] = pd.qcut(D["book_return"].rank(method="first"), 10, labels=False)
    out["book_decile_next_prev"] = D.groupby("q")[["book_return", "nxt", "prv", "coin_return"]].mean()
    return out
