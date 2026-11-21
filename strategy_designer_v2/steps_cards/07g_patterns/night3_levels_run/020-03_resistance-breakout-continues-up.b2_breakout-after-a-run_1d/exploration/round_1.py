def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            f = pd.DataFrame({
                "coin": coin, "w": w,
                "ret1": r1,
                "ret5p": c / c.shift(5) - 1,
                "ret20p": c / c.shift(20) - 1,
                "vol20": r1.rolling(20).std(),
                "dist30h": c / c.rolling(30).max() - 1,
                "dist30l": c / c.rolling(30).min() - 1,
                "fwd5": c.shift(-5) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "yr": pd.to_datetime(b["timestamp"]).dt.year,
            })
            f["vol_ratio"] = r1.rolling(5).std() / r1.rolling(30).std()
            f = f.iloc[::5]
            rows.append(f)
    g = pd.concat(rows, ignore_index=True)
    g = g.dropna(subset=["fwd5"])
    g["drift"] = g.groupby("coin")["fwd5"].transform("mean")
    g["unus"] = g["fwd5"] - g["drift"]
    g["usual"] = g.groupby("coin")["fwd5"].transform("std")
    g["strength"] = g["unus"] / g["usual"]
    out["n_grid"] = len(g)

    def bucket(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = d.groupby("q").agg(n=("unus", "size"), mean_unus=("unus", "mean"), sd=("unus", "std"),
                               strength=("strength", "mean"), feat=(col, "median"))
        t["t"] = t["mean_unus"] / (t["sd"] / np.sqrt(t["n"]))
        top, bot = d[d.q == q - 1]["unus"], d[d.q == 0]["unus"]
        t.loc["top-bot", "t"] = stats.ttest_ind(top, bot, equal_var=False).statistic
        t.loc["top-bot", "mean_unus"] = top.mean() - bot.mean()
        return t.drop(columns="sd").round(4)

    for col in ["ret1", "ret5p", "ret20p", "vol20", "dist30h", "dist30l", "vol_ratio"]:
        out["q_" + col] = bucket(col)
    d = g.copy()
    out["by_weekday"] = d.groupby("wd")["unus"].agg(["size", "mean", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))]).round(4)
    out["by_year"] = d.groupby("yr")["unus"].agg(["size", "mean"]).round(4)
    out["by_coin_ret20p_corr"] = d.dropna(subset=["ret20p"]).groupby("coin").apply(lambda x: pd.Series({
        "rho_ret20": stats.spearmanr(x["ret20p"], x["unus"]).correlation,
        "rho_dist30h": stats.spearmanr(x["dist30h"], x["unus"], nan_policy="omit").correlation,
        "rho_ret1": stats.spearmanr(x["ret1"], x["unus"], nan_policy="omit").correlation,
        "n": len(x)})).round(3)
    # forecast on vs off
    d["on"] = d["fc"] > 0
    out["fc_on_off"] = d.groupby("on")["unus"].agg(["size", "mean", "std"]).round(4)
    # strongest dist30h within off bars
    off = d[~d["on"]].dropna(subset=["dist30h"]).copy()
    off["q"] = off.groupby("coin")["dist30h"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["off_dist30h"] = off.groupby("q")["unus"].agg(["size", "mean"]).round(4)
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["days"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_fc"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"), fc=("entry_forecast", "median"), days=("days", "median")).round(3)
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean())).round(3)
    # book days
    dl = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w
            x["coin_prev5"] = x["close"] / x["close"].shift(5) - 1
            x["coin_next5"] = x["close"].shift(-5) / x["close"] - 1
            dl.append(x)
    D = pd.concat(dl, ignore_index=True).dropna(subset=["book_return"])
    act = D[D["book_return"].abs() > 1e-9]
    lo, hi = act["book_return"].quantile([0.02, 0.98])
    out["book_extremes"] = pd.DataFrame({
        "top2pct": act[act.book_return >= hi][["book_return", "coin_return", "coin_prev5", "coin_next5"]].mean(),
        "bot2pct": act[act.book_return <= lo][["book_return", "coin_return", "coin_prev5", "coin_next5"]].mean(),
        "all_active": act[["book_return", "coin_return", "coin_prev5", "coin_next5"]].mean()}).round(4)
    return out
