def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    D = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            D.append(d.assign(coin=c, w=w))
    D = pd.concat(D, ignore_index=True)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    def sh(x):
        x = x.dropna(); return x.mean() / x.std() * np.sqrt(365) if len(x) > 2 else np.nan
    g = D.groupby("coin")
    out["daily_by_coin"] = pd.DataFrame({"book_bps": g["book_return"].mean()*1e4, "hold_bps": g["coin_return"].mean()*1e4,
        "book_sh": g["book_return"].apply(sh), "hold_sh": g["coin_return"].apply(sh)})
    P = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    loo = {}
    for c in D.coin.unique():
        Q = D[D.coin != c].groupby(["w", "day"])["book_return"].mean()
        loo[c] = sh(Q)
    loo["all"] = sh(P["book_return"])
    out["pf_sharpe_leave_coin_out"] = pd.Series(loo)
    # beta of book to coin on daily
    X = D.dropna(subset=["book_return", "coin_return"])
    b, a, r, p, se = stats.linregress(X["coin_return"], X["book_return"])
    out["beta_book_on_coin"] = pd.Series({"beta": b, "alpha_bps": a*1e4, "alpha_ann_pct": a*365*100, "r2": r*r})
    # grid 20-bar non-overlapping
    rows = []
    for c in data["bars"]:
        for w, bb in data["bars"][c].items():
            bb = bb.reset_index(drop=True)
            cl = bb["close"].values
            hi20 = bb["close"].rolling(20).max(); lo20 = bb["close"].rolling(20).min()
            rng = ((bb["close"] - lo20) / (hi20 - lo20)).values
            r20p = (bb["close"] / bb["close"].shift(20) - 1).values
            vol = bb["close"].pct_change().rolling(30).std().values
            for i in range(0, len(bb) - 20, 20):
                rows.append(dict(coin=c, w=w, fc=bb["forecast"].fillna(0).iloc[i], reg=bb["regime"].iloc[i],
                                 f20=cl[i+20]/cl[i]-1, rng=rng[i], r20p=r20p[i], vol=vol[i]))
    G = pd.DataFrame(rows)
    G["f20x"] = G["f20"] - G.groupby("coin")["f20"].transform("mean")
    def tt(x):
        x = x.dropna(); return pd.Series({"mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    out["grid_by_regime"] = G.groupby("reg")["f20x"].apply(tt).unstack()
    T = G[G.reg == "trending"].copy()
    T["fcb"] = pd.cut(T["fc"], [-0.1, 0, 5, 10, 15, 21])
    out["grid_trending_fc_bucket"] = T.groupby("fcb", observed=True)["f20x"].apply(tt).unstack()
    T["r20b"] = pd.qcut(T["r20p"], 4)
    out["grid_trending_r20past_q"] = T.groupby("r20b", observed=True)["f20x"].apply(tt).unstack()
    N = G[G.reg != "trending"].copy()
    N["r20b"] = pd.qcut(N["r20p"], 4)
    out["grid_below_r20past_q"] = N.groupby("r20b", observed=True)["f20x"].apply(tt).unstack()
    G["volq"] = G.groupby("coin")["vol"].transform(lambda v: pd.qcut(v, 3, labels=False))
    out["grid_trend_by_volq"] = G[G.reg=="trending"].groupby("volq")["f20x"].apply(tt).unstack()
    out["grid_below_by_volq"] = G[G.reg!="trending"].groupby("volq")["f20x"].apply(tt).unstack()
    out["corr_r20p_f20_trend"] = pd.Series({"spearman": stats.spearmanr(T["r20p"], T["f20x"], nan_policy="omit")[0],
        "spearman_below": stats.spearmanr(N["r20p"], N["f20x"], nan_policy="omit")[0]})
    return out
