def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            for i in range(0, n - 14, 14):
                d = dict(coin=coin, win=w, i=i)
                d["fwd14"] = c[i+14]/c[i]-1
                d["fwd7"] = c[i+7]/c[i]-1
                for L in (7, 14, 30, 60):
                    d[f"ret{L}"] = c[i]/c[i-L]-1 if i >= L else np.nan
                d["vr"] = v[i-13:i+1].mean()/v[i-29:i+1].mean() if i >= 29 else np.nan
                d["vol14"] = r1[i-13:i+1].std() if i >= 14 else np.nan
                d["fc"] = b["forecast"].iloc[i]
                d["alloc"] = b["postRebalance_current_allocation"].iloc[i]
                d["regime"] = b["regime"].iloc[i]
                d["ts"] = pd.Timestamp(b["timestamp"].iloc[i])
                rows.append(d)
    g = pd.DataFrame(rows)
    g["cm"] = g.groupby("coin")["fwd14"].transform("mean")
    g["ex"] = g["fwd14"] - g["cm"]
    out = {}
    def tab(col, q=5):
        s = g.dropna(subset=[col])
        s = s.assign(bin=pd.qcut(s[col].rank(method="first"), q, labels=False))
        # per-coin quantile instead
        s["bin"] = s.groupby("coin")[col].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False) if len(x) >= q else np.nan)
        t = s.groupby("bin")["ex"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
        t.columns = ["mean_ex14", "n", "t"]
        return t
    for col in ["ret7", "ret14", "ret30", "ret60", "vr", "vol14", "fc"]:
        out[f"ex14 by coin-quintile of {col}"] = tab(col)
    # correlations
    cr = {}
    for col in ["ret7", "ret14", "ret30", "ret60", "vr", "vol14", "fc"]:
        s = g.dropna(subset=[col, "ex"])
        rho, p = stats.spearmanr(s[col], s["ex"])
        cr[col] = (rho, len(s), p)
    out["spearman with ex14"] = pd.DataFrame(cr, index=["rho", "n", "p"]).T
    # interaction ret14 sign x vr
    s = g.dropna(subset=["ret14", "vr"]).copy()
    s["sgn"] = np.sign(s["ret14"])
    s["vrb"] = pd.qcut(s["vr"], 3, labels=["low", "mid", "high"])
    s["sx"] = s["ex"] * s["sgn"]
    out["continuation(ex*sign ret14) by vr tercile"] = s.groupby("vrb")["sx"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    s2 = g.dropna(subset=["ret60"]).copy()
    s2["sx"] = s2["ex"] * np.sign(s2["ret60"])
    s2["ab"] = s2.groupby("coin")["ret60"].transform(lambda x: pd.qcut(x.abs().rank(method="first"), 3, labels=False))
    out["continuation ret60 by |ret60| coin-tercile"] = s2.groupby("ab")["sx"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    # daily: weekday, book
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["win"] = w; dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    out["coin_return by weekday"] = D.groupby("wd")["coin_return"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["book_return by weekday"] = D.groupby("wd")["book_return"].agg(["mean", "count"])
    # previous-day return effects
    D = D.sort_values(["coin", "win", "day"])
    D["prev"] = D.groupby(["coin", "win"])["coin_return"].shift(1)
    D["pb"] = D.groupby("coin")["prev"].transform(lambda x: pd.qcut(x.rank(method="first"), 5, labels=False))
    out["next-day coin return by prev-day quintile"] = D.groupby("pb")["coin_return"].agg(["mean", "count", lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    out["regime share"] = g["regime"].value_counts(normalize=True)
    return out
