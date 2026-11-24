def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            r1 = c.pct_change()
            past10 = c / c.shift(10) - 1
            past20 = c / c.shift(20) - 1
            low30 = c.rolling(30, min_periods=30).min()
            high30 = c.rolling(30, min_periods=30).max()
            dlow = c / low30 - 1
            dhigh = c / high30 - 1
            vol20 = r1.rolling(20, min_periods=20).std()
            vol60 = r1.rolling(60, min_periods=40).std()
            rng = (b["high"] - b["low"]) / c
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, ts=pd.Timestamp(b["timestamp"].iloc[i]),
                                 fwd=c.iloc[i + H] / c.iloc[i] - 1,
                                 past10=past10.iloc[i], past20=past20.iloc[i],
                                 dlow=dlow.iloc[i], dhigh=dhigh.iloc[i],
                                 vol20=vol20.iloc[i], volratio=vol20.iloc[i] / vol60.iloc[i] if vol60.iloc[i] else np.nan,
                                 r1=r1.iloc[i], rng=rng.iloc[i],
                                 fc=float(b["forecast"].iloc[i]) if pd.notna(b["forecast"].iloc[i]) else 0.0))
    g = pd.DataFrame(rows)
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["un"] = g["fwd"] - g["coin"].map(drift)
    g["str"] = g["un"] / g["coin"].map(sd)
    g["day"] = g["ts"].dt.floor("D")
    out = {"drift_sd": pd.DataFrame({"drift": drift, "sd": sd, "n": g.groupby("coin").size()})}

    def qtab(col, q=5):
        d = g.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        res = []
        for k, s in d.groupby("q"):
            dd = s.groupby("day")["un"].sum()
            nd = len(dd)
            m = s["un"].mean()
            t = dd.mean() / (dd.std(ddof=1) / np.sqrt(nd)) if nd > 2 else np.nan
            res.append(dict(q=k, n=len(s), days=nd, mean_un=m, strength=s["str"].mean(), t_day=t,
                            feat_mean=s[col].mean()))
        r = pd.DataFrame(res).set_index("q")
        # top minus bottom
        top = d[d.q == q - 1]["un"]; bot = d[d.q == 0]["un"]
        r.loc["top-bot", "mean_un"] = top.mean() - bot.mean()
        r.loc["top-bot", "t_day"] = stats.ttest_ind(top, bot, equal_var=False).statistic
        sp = stats.spearmanr(d[col], d["str"])
        r.loc["spearman", "mean_un"] = sp.correlation
        r.loc["spearman", "t_day"] = sp.pvalue
        return r
    for col in ["past10", "past20", "dlow", "dhigh", "vol20", "volratio", "r1", "rng"]:
        out["q_" + col] = qtab(col)
    # weekday / year of grid start
    for key in ["wd", "yr"]:
        g[key] = g["ts"].dt.weekday if key == "wd" else g["ts"].dt.year
        out["by_" + key] = g.groupby(key)["un"].agg(["count", "mean", "std"])
    # daily coin returns by weekday (non-overlapping 1-day)
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dl.append(d)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    cm = D.groupby("coin")["coin_return"].transform("mean")
    D["cun"] = D["coin_return"] - cm
    wd = D.groupby("wd")["cun"].agg(["count", "mean", "std"])
    wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["daily_by_weekday"] = wd
    # book: active days stats
    act = D[D["book_return"].abs() > 1e-9]
    out["book_active_days"] = pd.DataFrame({"n": [len(act)], "mean": [act["book_return"].mean()],
                                           "coins": [act["coin"].nunique()]})
    out["book_active_by_coin"] = act.groupby("coin")["book_return"].agg(["count", "mean", "sum"])
    # trades
    tl = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tl.append(t)
    if tl:
        T = pd.concat(tl)
        out["trades"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "min", "max"])
    return out
