def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def tt(s):
        s = s.dropna()
        return s.mean() / (s.std() / np.sqrt(len(s))) if len(s) > 2 else np.nan
    dd = []
    for coin, wins in data["days"].items():
        for w, dy in wins.items():
            t = dy.copy(); t["coin"] = coin; t["win"] = w
            t["vol20"] = t["coin_return"].rolling(20, min_periods=10).std().shift(1)
            t["prev"] = t["coin_return"].shift(1)
            t["ret7"] = (1 + t["coin_return"]).rolling(7, min_periods=7).apply(np.prod, raw=True).shift(1) - 1
            dd.append(t)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    ts = pd.to_datetime(D["day"])
    D["wd"] = ts.dt.dayofweek; D["yr"] = ts.dt.year
    D["z"] = D["coin_return"] / D["vol20"]
    # weekday by coin (Fri, Sat) and by year
    piv = {}
    for wd in [2, 4, 5]:
        piv[f"wd{wd}_by_coin_mean"] = D[D.wd == wd].groupby("coin")["coin_return"].mean()
        piv[f"wd{wd}_by_coin_t"] = D[D.wd == wd].groupby("coin")["coin_return"].apply(tt)
    out["wd_by_coin"] = pd.DataFrame(piv)
    yy = {}
    for wd in [4, 5]:
        yy[f"wd{wd}_mean"] = D[D.wd == wd].groupby("yr")["coin_return"].mean()
        yy[f"wd{wd}_t"] = D[D.wd == wd].groupby("yr")["coin_return"].apply(tt)
        yy[f"other_mean"] = D[~D.wd.isin([4, 5])].groupby("yr")["coin_return"].mean()
    out["wd_by_year"] = pd.DataFrame(yy)
    # Saturday minus other days, standardised by vol, and share of windows positive
    D["sat"] = D.wd == 5
    out["sat_minus_rest"] = pd.Series(dict(
        diff=D[D.sat]["coin_return"].mean() - D[~D.sat]["coin_return"].mean(),
        welch_t=stats.ttest_ind(D[D.sat]["coin_return"], D[~D.sat]["coin_return"], equal_var=False).statistic,
        zdiff=D[D.sat]["z"].mean() - D[~D.sat]["z"].mean(),
        share_win_coin_sat_pos=D[D.sat].groupby(["coin", "win"])["coin_return"].mean().gt(0).mean(),
        n_win_coin=D[D.sat].groupby(["coin", "win"]).ngroups))
    # Saturday graded by prior week return? (Fri/Sat after a strong week)
    S = D[D.wd.isin([4, 5])].dropna(subset=["ret7", "vol20"])
    S["r7z"] = S["ret7"] / (S["vol20"] * np.sqrt(7))
    S["q"] = pd.qcut(S["r7z"], 5, labels=False)
    out["frisat_by_prior7"] = S.groupby("q").agg(n=("coin_return", "size"), r7z=("r7z", "mean"),
                                                y=("coin_return", "mean"), t=("coin_return", tt))
    # next-day continuation after a large standardised day
    N = D.dropna(subset=["prev", "vol20"]).copy()
    N["pz"] = N["prev"] / N["vol20"]
    N["q"] = pd.qcut(N["pz"], 5, labels=False)
    out["next_day_by_prev_z"] = N.groupby("q").agg(n=("coin_return", "size"), pz=("pz", "mean"),
                                                   y=("coin_return", "mean"), t=("coin_return", tt))
    r = stats.linregress(N["pz"], N["coin_return"] / N["vol20"])
    out["cont_slope"] = pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(N)))
    out["cont_by_coin_t"] = N.groupby("coin").apply(lambda d: (lambda r: r.slope / r.stderr)(stats.linregress(d["pz"], d["coin_return"] / d["vol20"])))
    out["cont_by_year_t"] = N.groupby("yr").apply(lambda d: (lambda r: r.slope / r.stderr)(stats.linregress(d["pz"], d["coin_return"] / d["vol20"])))
    # book: long vs short share of gain
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            a = b["postRebalance_current_allocation"]
            g = a * (b["close"].shift(-1) / b["close"] - 1)
            rows.append(pd.DataFrame(dict(a=a, g=g)))
    B = pd.concat(rows).dropna()
    B["side"] = np.sign(B["a"])
    out["gain_by_side"] = B.groupby("side").agg(n=("g", "size"), mean=("g", "mean"), total=("g", "sum"), t=("g", tt))
    # trades: net by year of entry and side
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); tr.append(t)
    T = pd.concat(tr)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    out["short_trades_by_year"] = T[T.side == "SHORT"].groupby("yr")["net_profit_loss_percent"].agg(["size", "mean"])
    out["long_trades_by_year"] = T[T.side == "LONG"].groupby("yr")["net_profit_loss_percent"].agg(["size", "mean"])
    return out
