def explore(data):
    import numpy as np, pandas as pd
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            cl = (b["close"] - b["low"]) / rng
            r1 = c.pct_change()
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            past60 = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            vol_rel = vol20 / r1.rolling(60, min_periods=40).std()
            rngrel = (rng / c) / ((rng / c).rolling(20).mean())
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(b) - H, H):
                rows.append(dict(coin=coin, w=w, fwd=fwd[i], cl=cl[i], p5=past5[i], p20=past20[i],
                                 p60=past60[i], vol_rel=vol_rel[i], rngrel=rngrel[i], r1=r1[i],
                                 fc=b["forecast"][i], wd=ts[i].dayofweek, yr=ts[i].year))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd"].mean()
    d["unus"] = d["fwd"] - d["coin"].map(drift)
    def summ(g):
        x = g["unus"].dropna()
        n = len(x)
        return pd.Series(dict(n=n, mean_long_unusual=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan))
    out = {}
    out["all_grid"] = summ(d)
    out["by_cl_quint"] = d.groupby(pd.qcut(d["cl"], 5, labels=False)).apply(summ)
    out["by_p5_quint"] = d.groupby(pd.qcut(d["p5"], 5, labels=False)).apply(summ)
    out["by_p20_quint"] = d.groupby(pd.qcut(d["p20"], 5, labels=False)).apply(summ)
    out["by_r1_quint"] = d.groupby(pd.qcut(d["r1"], 5, labels=False)).apply(summ)
    out["by_volrel_tercile"] = d.groupby(pd.qcut(d["vol_rel"], 3, labels=False)).apply(summ)
    out["by_rngrel_quint"] = d.groupby(pd.qcut(d["rngrel"], 5, labels=False)).apply(summ)
    d["trend"] = pd.cut(d["p60"], [-10, -0.1, 0.1, 100], labels=["fall", "chop", "rise"])
    out["by_trend60"] = d.groupby("trend").apply(summ)
    d["hc"] = d["cl"] >= 0.8
    d["dn5"] = d["p5"] < 0
    out["hc_x_dn5"] = d.groupby(["hc", "dn5"]).apply(summ)
    d["lc"] = d["cl"] <= 0.2
    out["lowclose_x_dn5"] = d.groupby(["lc", "dn5"]).apply(summ)
    out["hc_dn5_by_trend"] = d[d.hc & d.dn5].groupby("trend").apply(summ)
    out["hc_dn5_by_volrel"] = d[d.hc & d.dn5].groupby(pd.qcut(d["vol_rel"], 3, labels=False)).apply(summ)
    out["hc_by_p20_tercile"] = d[d.hc].groupby(pd.qcut(d["p20"], 3, labels=False)).apply(summ)
    out["by_weekday"] = d.groupby("wd").apply(summ)
    out["by_year"] = d.groupby("yr").apply(summ)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd.copy(); x["coin"] = coin; x["w"] = w; br.append(x)
    br = pd.concat(br)
    br["yr"] = pd.to_datetime(br["day"]).dt.year
    out["book_by_window"] = br.groupby("w").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "count"))
    out["book_by_coin"] = br.groupby("coin").agg(book_mean=("book_return", "mean"), coin_mean=("coin_return", "mean"), n=("book_return", "count"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; tr.append(t)
    tr = pd.concat(tr)
    tr["fcq"] = pd.qcut(tr["entry_forecast"].abs().rank(method="first"), 4, labels=False)
    out["trades_by_fc_quart"] = tr.groupby("fcq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades_summary"] = tr["net_profit_loss_percent"].describe()
    return out
