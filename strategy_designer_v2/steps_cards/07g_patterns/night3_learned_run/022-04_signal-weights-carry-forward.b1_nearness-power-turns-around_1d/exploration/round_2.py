def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.extend(list(c[idx + H] / c[idx] - 1))
        mu = np.nanmean(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            vol365 = r1.rolling(365, min_periods=60).std()
            idx = np.arange(0, len(c) - H, H)
            for i in idx:
                fr = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, win=w, f=b["forecast"].iloc[i], ex=fr - mu,
                                 r1z=r1.iloc[i] / vol20.iloc[i] if vol20.iloc[i] else np.nan,
                                 vlev=vol20.iloc[i] / vol365.iloc[i] if vol365.iloc[i] else np.nan,
                                 vol20=vol20.iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    d = pd.DataFrame(rows)
    d["g"] = d["f"] / 10 * d["ex"]
    out = {}
    def tt(s):
        s = s.dropna(); return pd.Series({"mean": s.mean(), "n": len(s), "t": s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan})
    d["side"] = np.sign(d["f"])
    out["gain_by_side"] = d.groupby("side")["g"].apply(tt).unstack()
    out["ex_by_side"] = d.groupby("side")["ex"].apply(tt).unstack()
    x = d.dropna(subset=["vlev"]).copy()
    x["vq"] = x.groupby("coin")["vlev"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["gain_by_vol_tercile"] = x.groupby("vq")["g"].apply(tt).unstack()
    out["ex_by_vol_tercile"] = x.groupby("vq")["ex"].apply(tt).unstack()
    # r1z top quintile per coin consistency
    y = d.dropna(subset=["r1z"]).copy()
    y["q"] = y.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["r1z_top_minus_rest_by_coin"] = y.groupby("coin").apply(lambda z: pd.Series({
        "top": z.loc[z.q == 4, "ex"].mean(), "rest": z.loc[z.q < 4, "ex"].mean(),
        "t": stats.ttest_ind(z.loc[z.q == 4, "ex"], z.loc[z.q < 4, "ex"], equal_var=False).statistic}))
    # book: timing vs market, drawdowns
    dd = []
    for coin, wins in data["days"].items():
        cm = pd.concat([x_["coin_return"] for x_ in wins.values()]).mean()
        for w, x_ in wins.items():
            x_ = x_.copy(); x_["coin"] = coin; x_["win"] = w; x_["cm"] = cm
            dd.append(x_)
    D = pd.concat(dd)
    # position at end of previous day from bars
    pos = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            p = pd.DataFrame({"day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                              "pos": b["postRebalance_current_allocation"].shift(1)})
            p["coin"] = coin; p["win"] = w
            pos.append(p)
    P = pd.concat(pos)
    D["day"] = pd.to_datetime(D["day"]).dt.floor("D")
    if getattr(D["day"].dt, "tz", None) is not None: D["day"] = D["day"].dt.tz_localize(None)
    if getattr(P["day"].dt, "tz", None) is not None: P["day"] = P["day"].dt.tz_localize(None)
    D = D.merge(P, on=["coin", "win", "day"], how="left")
    D["mkt"] = D["pos"] * D["cm"]
    out["book_mean_vs_market_part"] = pd.Series({"book": D["book_return"].mean(), "market_part": D["mkt"].mean(),
                                                 "mean_abs_pos": D["pos"].abs().mean(), "mean_pos": D["pos"].mean()})
    # book daily (mean over coins) and its worst days, coin return those days
    B = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_tail"] = pd.Series({"n_days": len(B), "corr_book_coin": B["book_return"].corr(B["coin_return"]),
        "coin_ret_on_worst5pct_book": B.loc[B.book_return <= B.book_return.quantile(.05), "coin_return"].mean(),
        "coin_ret_on_best5pct_book": B.loc[B.book_return >= B.book_return.quantile(.95), "coin_return"].mean(),
        "book_std": B.book_return.std()})
    # book return by sign of coin daily return magnitude bucket
    B["cq"] = pd.qcut(B["coin_return"], 5, labels=False)
    out["book_by_coin_quintile"] = B.groupby("cq")[["book_return", "coin_return"]].mean()
    # drawdown per window
    def mdd(s):
        v = (1 + s).cumprod(); return (v / v.cummax() - 1).min()
    out["window_mdd"] = B.groupby("win")["book_return"].apply(mdd).sort_values().head(8)
    return out
