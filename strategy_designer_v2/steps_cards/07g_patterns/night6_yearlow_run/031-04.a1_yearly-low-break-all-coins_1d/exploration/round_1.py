def explore(data):
    import numpy as np, pandas as pd
    H = 10
    rows = []
    for coin, ws in data["bars"].items():
        for w, df in ws.items():
            df = df.sort_values("timestamp")
            s = pd.Series(df["close"].astype(float).values)
            n = len(s)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1 = s.pct_change()
            vol = pd.Series(df["volume"].astype(float).values)
            f = pd.DataFrame({
                "ret1": r1,
                "ret5": s / s.shift(5) - 1,
                "ret30": s / s.shift(30) - 1,
                "vol20": r1.rolling(20).std(),
                "dlow60": s / s.rolling(60).min().shift(1) - 1,
                "dhigh60": s / s.rolling(60).max().shift(1) - 1,
                "relvol": vol / vol.rolling(20).mean().shift(1),
                "rng": (pd.Series(df["high"].astype(float).values) - pd.Series(df["low"].astype(float).values)) / s,
                "brk": (df["regime"].values == "mean_reversion").astype(int),
            })
            f["clv"] = (s - pd.Series(df["low"].astype(float).values)) / (pd.Series(df["high"].astype(float).values) - pd.Series(df["low"].astype(float).values))
            for i in range(0, n - H, H):
                d = f.iloc[i].to_dict()
                d.update(coin=coin, w=w, wn=int(w[1:]), day=ts[i].normalize(), wd=ts[i].weekday(),
                         fwd=s[i + H] / s[i] - 1)
                rows.append(d)
    g = pd.DataFrame(rows)
    st = g.groupby("coin")["fwd"].agg(["mean", "std"])
    g["un"] = g["fwd"] - g["coin"].map(st["mean"])
    g["strg"] = g["un"] / g["coin"].map(st["std"])

    def ct(x, days):
        x = np.asarray(x, float); m = x.mean(); e = x - m
        S = pd.Series(e).groupby(np.asarray(days)).sum()
        G = len(S)
        if G < 2: return np.nan
        se = np.sqrt((S ** 2).sum()) / len(x) * np.sqrt(G / (G - 1))
        return m / se

    def quint(col):
        x = g.dropna(subset=[col]).copy()
        x["q"] = x.groupby("coin")[col].rank(pct=True)
        x["q"] = pd.cut(x["q"], [0, .2, .4, .6, .8, 1], labels=[1, 2, 3, 4, 5])
        out = []
        for q, y in x.groupby("q", observed=True):
            e = y[y.wn <= 12]; l = y[y.wn > 12]
            out.append(dict(q=q, feat_mean=y[col].mean(), un=y.un.mean(), strength=y.strg.mean(),
                            t=ct(y.un, y.day), n=len(y), days=y.day.nunique(),
                            un_w1_12=e.un.mean(), un_w13_24=l.un.mean()))
        return pd.DataFrame(out)

    res = {}
    for c in ["ret1", "ret5", "ret30", "vol20", "dlow60", "dhigh60", "relvol", "rng", "clv"]:
        res["q_" + c] = quint(c)
    b = g.groupby("brk").apply(lambda y: pd.Series(dict(un=y.un.mean(), t=ct(y.un, y.day), n=len(y), days=y.day.nunique())))
    res["break_vs_not"] = b
    # weekday of daily returns
    dd = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            x = df[["day", "coin_return"]].dropna().copy(); x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd); dd["day"] = pd.to_datetime(dd["day"])
    dd["un"] = dd["coin_return"] - dd.groupby("coin")["coin_return"].transform("mean")
    dd["wd"] = dd["day"].dt.weekday
    res["weekday_daily"] = dd.groupby("wd").apply(lambda y: pd.Series(dict(un=y.un.mean(), t=ct(y.un, y.day), n=len(y))))
    res["coin_drift_10d"] = st
    tr = []
    for coin, ws in data["trades"].items():
        for w, t in ws.items():
            if len(t): tr.append(t.assign(coin=coin))
    if tr:
        tr = pd.concat(tr)
        res["trades"] = pd.Series(dict(n=len(tr), mean_net=tr.net_profit_loss_percent.mean(),
                                       share_pos=(tr.net_profit_loss_percent > 0).mean(),
                                       mean_days=tr.duration_minutes.mean() / 1440))
    return res
