def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 5
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        rs = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs += list(c[idx + H] / c[idx] - 1)
        drift[coin] = (np.mean(rs), np.std(rs))
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            vr = np.log(v.rolling(30).mean() / v.shift(30).rolling(30).mean())
            vr7 = np.log(v.rolling(7).mean() / v.shift(7).rolling(30).mean())
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            z1 = r1 / sd30.shift(1)
            rng = (b["high"] - b["low"]) / c
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, day=ts.iloc[i].normalize(), regime=b["regime"].iloc[i],
                    fc=b["forecast"].iloc[i], vr=vr.iloc[i], vr7=vr7.iloc[i], ret20=ret20.iloc[i], ret60=ret60.iloc[i],
                    z1=z1.iloc[i], sd30=sd30.iloc[i], rng=rng.iloc[i]/sd30.iloc[i] if sd30.iloc[i] else np.nan, clv=clv.iloc[i],
                    wd=ts.iloc[i].weekday(), fwd=fwd.iloc[i], un=fwd.iloc[i]-drift[coin][0], st=(fwd.iloc[i]-drift[coin][0])/drift[coin][1]))
    g = pd.DataFrame(rows)
    def summ(df, key):
        a = df.dropna(subset=[key, "un"]).groupby(key)["un"]
        r = a.agg(["count", "mean"])
        r["t"] = a.mean() / (a.std() / np.sqrt(a.count()))
        return r.round(4)
    out["regime counts / fwd5 unusual"] = summ(g, "regime")
    tr = g[g.regime == "trending"].copy()
    tr["fcq"] = pd.qcut(tr.fc.rank(method="first"), 5, labels=False)
    out["trending: by forecast quintile"] = summ(tr, "fcq")
    fall = g[g.ret60 < -0.10].copy()
    fall["vrq"] = pd.qcut(fall.vr, 5, labels=False)
    out["falling(ret60<-10%): by 30d vol ratio quintile"] = summ(fall, "vrq")
    fall["vr7q"] = pd.qcut(fall.vr7, 5, labels=False)
    out["falling: by 7d vol ratio quintile"] = summ(fall, "vr7q")
    fall["r20s"] = np.where(fall.ret20 < 0, "r20neg", "r20pos")
    out["falling: by ret20 sign"] = summ(fall, "r20s")
    for nm, sub in [("all", g), ("rising", g[g.ret60 > 0.10]), ("choppy", g[(g.ret60 >= -0.1) & (g.ret60 <= 0.1)]), ("falling", fall)]:
        s = sub.dropna(subset=["z1"]).copy()
        s["zq"] = pd.qcut(s.z1, 5, labels=False)
        out[f"{nm}: fwd5 by 1d z-move quintile"] = summ(s, "zq")
    s = g.dropna(subset=["sd30"]).copy(); s["vq"] = pd.qcut(s.sd30, 4, labels=False)
    out["all: by 30d vol quartile"] = summ(s, "vq")
    s = g.dropna(subset=["vr"]).copy(); s["vrq"] = pd.qcut(s.vr, 5, labels=False)
    out["all: by 30d vol ratio quintile"] = summ(s, "vrq")
    s = g.dropna(subset=["ret60"]).copy(); s["r60q"] = pd.qcut(s.ret60, 5, labels=False)
    out["all: by ret60 quintile"] = summ(s, "r60q")
    # daily coin returns by weekday
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    a = D.dropna(subset=["coin_return"]).groupby("wd")["coin_return"]
    r = a.agg(["count", "mean"]); r["t"] = a.mean() / (a.std() / np.sqrt(a.count()))
    out["coin daily return by weekday"] = r.round(5)
    # book
    bk = D.groupby(["w", "day"])["book_return"].mean().dropna()
    out["book: by window mean/sum"] = D.groupby("w")["book_return"].agg(["mean", "sum"]).round(5)
    big = bk.abs().sort_values(ascending=False).index[:20]
    cm = D.groupby(["w", "day"])["coin_return"].mean()
    out["book top20 abs days: book vs coin mean"] = pd.Series({"book_mean": bk.loc[big].mean(), "coin_mean": cm.loc[big].mean(),
        "corr_book_coin_all": np.corrcoef(bk.values, cm.loc[bk.index].values)[0, 1], "n_pos_book": (bk.loc[big] > 0).sum()})
    # trades
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["dur_d"] = T.duration_minutes / 1440
    T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), mean_fc=("entry_forecast", "mean"), dur=("dur_d", "mean")).round(3)
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean")).round(3)
    return out
