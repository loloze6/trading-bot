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
            t["next2"] = (1 + t["coin_return"]).rolling(2).apply(np.prod, raw=True).shift(-1) - 1
            dd.append(t)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    ts = pd.to_datetime(D["day"])
    D["wd"] = ts.dt.dayofweek; D["yr"] = ts.dt.year
    drift = D.groupby("coin")["coin_return"].mean()
    D["u"] = D["coin_return"] - D["coin"].map(drift)
    N = D.dropna(subset=["prev", "vol20"]).copy()
    N["pz"] = N["prev"] / N["vol20"]
    # down-day rebound: graded within negative prev days
    neg = N[N.pz < 0].copy()
    neg["q"] = pd.qcut(neg["pz"], 5, labels=False)
    out["neg_prev_quintiles_unusual"] = neg.groupby("q").agg(n=("u", "size"), pz=("pz", "mean"), u=("u", "mean"), t=("u", tt))
    r = stats.linregress(-neg["pz"], neg["u"] / neg["vol20"])
    out["neg_slope"] = pd.Series(dict(slope=r.slope, t=r.slope / r.stderr, n=len(neg)))
    out["neg_slope_by_coin_t"] = neg.groupby("coin").apply(lambda d: (lambda r: r.slope / r.stderr)(stats.linregress(-d["pz"], d["u"] / d["vol20"])))
    out["neg_slope_by_year_t"] = neg.groupby("yr").apply(lambda d: (lambda r: r.slope / r.stderr)(stats.linregress(-d["pz"], d["u"] / d["vol20"])))
    big = N[N.pz < N.pz.quantile(0.2)]
    out["bigdown_by_coin"] = big.groupby("coin")["u"].agg(["size", "mean", tt])
    out["bigdown_by_year"] = big.groupby("yr")["u"].agg(["size", "mean", tt])
    # prior-7 grading: all weekdays vs Fri/Sat
    S = D.dropna(subset=["ret7", "vol20"]).copy()
    S["r7z"] = S["ret7"] / (S["vol20"] * np.sqrt(7))
    sl = {}
    for name, sub in [("all", S), ("frisat", S[S.wd.isin([4, 5])]), ("other", S[~S.wd.isin([4, 5])])]:
        r = stats.linregress(sub["r7z"], sub["u"] / sub["vol20"])
        sl[name] = dict(slope=r.slope, t=r.slope / r.stderr, n=len(sub))
    out["prior7_slope"] = pd.DataFrame(sl).T
    fs = S[S.wd.isin([4, 5])]
    out["frisat_prior7_by_coin_t"] = fs.groupby("coin").apply(lambda d: (lambda r: r.slope / r.stderr)(stats.linregress(d["r7z"], d["u"] / d["vol20"])))
    out["frisat_prior7_by_year_t"] = fs.groupby("yr").apply(lambda d: (lambda r: r.slope / r.stderr)(stats.linregress(d["r7z"], d["u"] / d["vol20"])))
    return out
