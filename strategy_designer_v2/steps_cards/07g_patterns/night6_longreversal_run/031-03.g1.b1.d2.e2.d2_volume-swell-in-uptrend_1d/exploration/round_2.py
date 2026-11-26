import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            ma50 = c.rolling(50).mean(); dist = c / ma50 - 1
            r30 = c / c.shift(30) - 1; r14 = c / c.shift(14) - 1
            swell = v.rolling(14).mean() / v.rolling(30).mean() - 1
            swell7 = v.rolling(7).mean() / v.rolling(30).mean() - 1
            lr = np.log(c).diff(); vol30 = lr.rolling(30).std()
            for H in (7, 14, 28):
                fwd = c.shift(-H) / c - 1
                for i in np.arange(0, len(b), H):
                    if np.isnan(fwd.iloc[i]): continue
                    rows.append(dict(H=H, coin=coin, w=w, ts=b["timestamp"].iloc[i], fwd=fwd.iloc[i],
                        dist=dist.iloc[i], r30=r30.iloc[i], r14=r14.iloc[i], swell=swell.iloc[i], swell7=swell7.iloc[i],
                        vol30=vol30.iloc[i], year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    G = pd.DataFrame(rows)
    G["ex"] = G["fwd"] - G.groupby(["H", "coin"])["fwd"].transform("mean")
    G["day"] = pd.to_datetime(G["ts"]).dt.floor("D")

    def ct(x, days):
        x = np.asarray(x, float); n = len(x)
        if n < 5: return np.nan
        m = x.mean(); S = pd.Series(x - m).groupby(np.asarray(days)).sum()
        return m * n / np.sqrt((S ** 2).sum())

    def zc(df, col):
        return df.groupby("coin")[col].transform(lambda s: (s.rank(pct=True) - 0.5))

    def ols_cl(df, xs):
        df = df.dropna(subset=xs + ["ex"]).copy()
        X = np.column_stack([np.ones(len(df))] + [zc(df, x).values for x in xs])
        y = df.ex.values
        XtX = np.linalg.inv(X.T @ X); beta = XtX @ X.T @ y; e = y - X @ beta
        g = df.day.values; meat = np.zeros((X.shape[1],) * 2)
        for k, idx in pd.Series(np.arange(len(df))).groupby(g):
            s = (X[idx.values] * e[idx.values, None]).sum(0); meat += np.outer(s, s)
        Gn = len(np.unique(g)); n, K = X.shape
        V = XtX @ meat @ XtX * Gn / (Gn - 1) * (n - 1) / (n - K)
        return pd.Series(beta / np.sqrt(np.diag(V)), index=["const"] + xs).round(2)

    res = {}
    g14 = G[G.H == 14]
    for H in (7, 14, 28):
        gh = G[G.H == H]
        res[f"t_H{H}"] = pd.DataFrame({"swell": ols_cl(gh, ["swell"]), "swell+r30+vol+dist": ols_cl(gh, ["swell", "r30", "vol30", "dist"]),
                                       "swell7": ols_cl(gh, ["swell7"])})
    # swell rank slope by year (14d)
    g14 = g14.dropna(subset=["swell"]).copy()
    g14["sr"] = zc(g14, "swell")
    res["year_swell"] = g14.groupby("year").apply(lambda s: pd.Series(dict(n=len(s),
        hi=s[s.sr > 0.3].ex.mean(), lo=s[s.sr < -0.3].ex.mean(),
        t=stats.ttest_ind(s[s.sr > 0.3].ex, s[s.sr < -0.3].ex, equal_var=False).statistic)))
    # swell quintile by sign of r14
    g14["q"] = g14.groupby("coin")["swell"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    g14["up14"] = np.where(g14.r14 > 0, "up", "down")
    res["swell_q_by_r14sign"] = g14.dropna(subset=["r14"]).groupby(["up14", "q"]).apply(
        lambda s: pd.Series(dict(n=len(s), mean=s.ex.mean(), t=ct(s.ex, s.day)))).round(4)
    # leave-one-coin-out hi-lo
    out = {}
    for cn in g14.coin.unique():
        s = g14[g14.coin != cn]
        out[cn] = stats.ttest_ind(s[s.q == 4].ex, s[s.q == 0].ex, equal_var=False).statistic
    res["loco_hilo_t"] = pd.Series(out).describe()
    res["coin_hilo"] = g14.groupby("coin").apply(lambda s: s[s.q == 4].ex.mean() - s[s.q == 0].ex.mean()).describe()
    return res
