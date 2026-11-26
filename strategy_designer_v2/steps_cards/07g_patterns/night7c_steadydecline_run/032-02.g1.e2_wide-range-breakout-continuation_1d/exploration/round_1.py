def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); hi = b["high"].astype(float); lo = b["low"].astype(float)
            v = b["volume"].astype(float)
            r1 = c.pct_change()
            rng = (hi - lo) / c
            df = pd.DataFrame({
                "coin": coin, "win": w,
                "ret28": c / c.shift(28) - 1,
                "ret5p": c / c.shift(5) - 1,
                "ret1": r1,
                "rr": rng / rng.rolling(28).mean(),
                "prox": c / c.rolling(28).max(),
                "proxlow": c / c.rolling(28).min(),
                "vol28": r1.rolling(28).std(),
                "volr": v / v.rolling(28).mean(),
                "clv": (c - lo) / (hi - lo).replace(0, np.nan),
                "fc": b["forecast"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "fwd": c.shift(-H) / c - 1,
            })
            df["vollvl"] = df["vol28"] / df["vol28"].rolling(60, min_periods=20).median()
            df = df.iloc[::H]
            rows.append(df)
    g = pd.concat(rows).dropna(subset=["fwd"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def summ(s):
        s = s.dropna()
        n = len(s); m = s.mean(); t = m / (s.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_ex_%": 100 * m, "t": t})
    out = {}
    reg = (g["ret28"] > 0) & (g["rr"] >= 1)
    out["regime_vs_not"] = g.groupby(reg)["ex"].apply(summ).unstack()
    for f in ["ret28", "ret5p", "ret1", "rr", "prox", "proxlow", "vollvl", "volr", "clv"]:
        q = pd.qcut(g[f], 5, labels=False, duplicates="drop")
        out["all_q_" + f] = g.groupby(q)["ex"].apply(summ).unstack()
    gi = g[reg]
    for f in ["rr", "ret28", "clv", "volr", "prox"]:
        q = pd.qcut(gi[f], 4, labels=False, duplicates="drop")
        out["inreg_q_" + f] = gi.groupby(q)["ex"].apply(summ).unstack()
    out["weekday"] = g.groupby("wd")["ex"].apply(summ).unstack()
    # down-trend calm (the brief) : ret28<0 and rr<1
    calm_down = (g["ret28"] < 0) & (g["vollvl"] < 1)
    gd = g[calm_down]
    q = pd.qcut(gd["ret28"], 4, labels=False, duplicates="drop")
    out["calmdown_q_ret28"] = gd.groupby(q)["ex"].apply(summ).unstack()
    # book largest days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd)
    bk = D.groupby(["win", "day"])["book_return"].mean().dropna()
    out["book_by_window"] = bk.groupby(level=0).agg(["count", "mean", "std"]).assign(sh=lambda x: x["mean"] / x["std"] * np.sqrt(365))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["dur_d"] = T["duration_minutes"] / 1440
    out["trades"] = pd.Series({"n": len(T), "mean_net%": T["net_profit_loss_percent"].mean(),
                               "win_share": (T["net_profit_loss_percent"] > 0).mean(),
                               "mean_dur_d": T["dur_d"].mean(),
                               "top10pct_share_of_sum": T["net_profit_loss_percent"].nlargest(max(1, len(T)//10)).sum() / T["net_profit_loss_percent"].sum()})
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
