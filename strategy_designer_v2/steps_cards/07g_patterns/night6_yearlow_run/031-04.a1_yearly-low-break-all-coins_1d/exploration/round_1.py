def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; H = 10
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            d = df.reset_index(drop=True)
            c = d["close"].astype(float)
            n = len(c)
            ret1 = c.pct_change()
            feat = pd.DataFrame({
                "lo30": c / c.shift(1).rolling(30).min() - 1,
                "lo60": c / c.shift(1).rolling(60).min() - 1,
                "hi30": c / c.shift(1).rolling(30).max() - 1,
                "r10": c / c.shift(10) - 1,
                "r1": ret1,
                "vol20": ret1.rolling(20).std(),
                "fc": d["forecast"].astype(float),
            })
            ts = pd.to_datetime(d["timestamp"])
            for p in range(0, n - H, H):
                r = c.iloc[p + H] / c.iloc[p] - 1
                row = feat.iloc[p].to_dict()
                row.update(coin=coin, win=w, fwd=r, day=ts.iloc[p].normalize(), year=ts.iloc[p].year)
                rows.append(row)
    X = pd.DataFrame(rows)
    drift = X.groupby("coin")["fwd"].mean()
    usual = X.groupby("coin")["fwd"].std()
    X["un"] = X["fwd"] - X["coin"].map(drift)
    X["str"] = X["un"] / X["coin"].map(usual)
    X["vol_rank"] = X.groupby("coin")["vol20"].rank(pct=True)

    def ct(s, days):
        s = s.dropna(); days = days.loc[s.index]
        N = len(s); m = s.mean()
        S = (s - m).groupby(days).sum(); G = len(S)
        se = np.sqrt(G / (G - 1) * (S ** 2).sum()) / N
        return m, m / se, N, G

    out = {}
    for f in ["lo30", "lo60", "hi30", "r10", "r1", "vol_rank"]:
        sub = X.dropna(subset=[f]).copy()
        sub["q"] = sub.groupby("coin")[f].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        res = []
        for q, g in sub.groupby("q"):
            m, t, N, G = ct(g["un"], g["day"])
            res.append({"q": q, "feat_mean": g[f].mean(), "unusual": m, "t": t, "strength": g["str"].mean(), "N": N, "days": G})
        out["quintile_" + f] = pd.DataFrame(res)
    # top-minus-bottom by year for lo30 and r10
    for f in ["lo30", "r10"]:
        sub = X.dropna(subset=[f]).copy()
        sub["q"] = sub.groupby("coin")[f].transform(lambda v: pd.qcut(v.rank(method="first"), 5, labels=False))
        yy = sub[sub.q.isin([0, 4])].groupby(["year", "q"])["un"].mean().unstack()
        yy["bottom_minus_top"] = yy[0] - yy[4]
        out["by_year_" + f] = yy
    # trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        T = pd.concat(tr)
        out["trades"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), entry_fc=("entry_forecast", "mean"))
    # weekday on daily returns
    D = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            D.append(d.assign(coin=coin))
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["cu"] = D["coin_return"] - D.groupby("coin")["coin_return"].transform("mean")
    out["weekday"] = D.groupby("wd")["cu"].agg(["mean", "count", lambda v: v.mean() / v.std() * np.sqrt(len(v))])
    return out
