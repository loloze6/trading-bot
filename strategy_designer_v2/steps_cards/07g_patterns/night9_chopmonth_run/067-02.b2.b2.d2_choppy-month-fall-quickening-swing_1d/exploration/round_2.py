def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def tstat(x):
        x = pd.Series(x).dropna()
        if len(x) < 3 or x.std() == 0: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].reset_index(drop=True).astype(float)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r = c.pct_change()
            r30 = c / c.shift(30) - 1
            r60 = c / c.shift(60) - 1
            r5 = c / c.shift(5) - 1
            r10 = c / c.shift(10) - 1
            sd30 = r.rolling(30).std()
            sd365 = r.rolling(30).std().rolling(len(c), min_periods=60).median()
            rng = (df["high"].values - df["low"].values) / c.values
            for h in (5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(c) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=fwd[i], r30=r30[i], r60=r60[i], r5=r5[i], r10=r10[i],
                                     sd30=sd30[i], agi=sd30[i] > sd365[i] if pd.notna(sd365[i]) else np.nan,
                                     rng=rng[i]/sd30[i] if sd30[i] > 0 else np.nan, yr=ts[i].year,
                                     wn=int(str(w)[1:])))
    g = pd.DataFrame(rows)
    g["drift"] = g.groupby(["coin", "h"])["fwd"].transform("mean")
    g["ex"] = g["fwd"] - g["drift"]
    g["prof"] = np.where(g.r60 > 0.1, "rising", np.where(g.r60 < -0.1, "falling", "choppy"))
    g["z30"] = g.r30 / (g.sd30 * np.sqrt(30))
    g["z5"] = g.r5 / (g.sd30 * np.sqrt(5))
    g["z10"] = g.r10 / (g.sd30 * np.sqrt(10))
    s = g[(g.h == 10) & (g.prof == "choppy")].dropna(subset=["z5", "z30", "ex"]).copy()
    s["q"] = pd.qcut(s.z5, 5, labels=False)
    out["choppy h10 z5 quintiles"] = s.groupby("q").agg(n=("ex", "count"), z5=("z5", "mean"), ex=("ex", "mean"), t=("ex", tstat))
    s["side"] = np.where(s.z5 > 0, "up", "down")
    out["choppy h10 z5 side"] = s.groupby("side")["ex"].agg(["count", "mean", tstat])
    s["sig"] = np.sign(s.z5) * s.ex
    out["choppy h10 signed ex by year"] = s.groupby("yr")["sig"].agg(["count", "mean", tstat])
    out["choppy h10 signed ex by window"] = s.groupby("wn")["sig"].agg(["count", "mean", tstat])
    out["choppy h10 signed ex by agitation"] = s.groupby("agi")["sig"].agg(["count", "mean", tstat])
    # partial: regress ex on z5 and z30
    X = np.column_stack([np.ones(len(s)), s.z5, s.z30]); y = s.ex.values
    b, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X @ b
    cov = np.linalg.inv(X.T @ X) * (res @ res) / (len(y) - 3)
    out["choppy h10 ols ex~z5+z30"] = pd.DataFrame({"b": b, "t": b / np.sqrt(np.diag(cov))}, index=["c", "z5", "z30"])
    rr = []
    for h in (5, 10):
        for lag in ("z5", "z10", "z30"):
            for prof in ("choppy", "rising", "falling"):
                q = g[(g.h == h) & (g.prof == prof)].dropna(subset=[lag, "ex"])
                rho, p = stats.spearmanr(q[lag], q.ex)
                rr.append(dict(h=h, lag=lag, prof=prof, n=len(q), rho=rho, p=p))
    out["lookback x profile spearman"] = pd.DataFrame(rr)
    s2 = g[(g.h == 10) & (g.prof == "rising")].dropna(subset=["rng", "ex"]).copy()
    s2["q"] = pd.qcut(s2.rng, 4, labels=False)
    out["rising h10 range quartiles"] = s2.groupby("q")["ex"].agg(["count", "mean", tstat])
    return out
