def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 10
    rows = []
    drift = {}
    usual = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(allr); usual[coin] = np.std(allr)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; lr = np.log(c).diff()
            ret1 = c.pct_change()
            ret10 = c / c.shift(10) - 1
            ret30 = c / c.shift(30) - 1
            ret60 = c / c.shift(60) - 1
            vol20 = lr.rolling(20).std()
            volrel = vol20 / lr.rolling(60, min_periods=40).std()
            hi = c.rolling(60, min_periods=30).max(); lo = c.rolling(60, min_periods=30).min()
            pos = (c - lo) / (hi - lo)
            fc = b["forecast"]
            wd = pd.to_datetime(b["timestamp"]).dt.dayofweek
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for i in range(0, len(c) - H, H):
                fr = c.iloc[i + H] / c.iloc[i] - 1
                rows.append(dict(coin=coin, win=w, yr=yr.iloc[i], wd=wd.iloc[i], fwd=fr,
                                 ex=fr - drift[coin], z=(fr - drift[coin]) / usual[coin],
                                 ret1=ret1.iloc[i], ret10=ret10.iloc[i], ret30=ret30.iloc[i], ret60=ret60.iloc[i],
                                 vol20=vol20.iloc[i], volrel=volrel.iloc[i], pos=pos.iloc[i], fc=fc.iloc[i]))
    df = pd.DataFrame(rows)
    def grp(col, q=5):
        d = df.dropna(subset=[col, "z"]).copy()
        d["b"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        g = d.groupby("b")["z"].agg(["mean", "count", "std"])
        g["t"] = g["mean"] / (g["std"] / np.sqrt(g["count"]))
        g["ex_mean"] = d.groupby("b")["ex"].mean()
        return g.drop(columns="std")
    def corr(col):
        out = {}
        for coin, d in df.dropna(subset=[col]).groupby("coin"):
            r, p = stats.spearmanr(d[col], d["z"]); out[coin] = (round(r, 3), len(d))
        return pd.Series(out).astype(str)
    res = {}
    for col in ["ret1", "ret10", "ret30", "ret60", "vol20", "volrel", "pos"]:
        res["q_" + col] = grp(col)
        res["rho_" + col] = corr(col)
    d = df.copy(); d["fcb"] = np.where(d.fc < 0, "short", "flat")
    res["by_forecast"] = d.groupby(["fcb"])["z"].agg(["mean", "count"])
    res["by_wd"] = df.groupby("wd")["z"].agg(["mean", "count"])
    res["by_year"] = df.groupby("yr")["ex"].agg(["mean", "count"])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            x["yr"] = pd.to_datetime(dd["day"]).dt.year
            bk.append(x)
    bk = pd.concat(bk)
    res["book_by_coin"] = bk.groupby("coin")[["book_return", "coin_return"]].mean() * 1e4
    res["book_by_year"] = bk.groupby("yr")[["book_return", "coin_return"]].mean() * 1e4
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    tr = pd.concat(tr)
    res["trades"] = tr.groupby("side")[["profit_loss_percent", "net_profit_loss_percent", "duration_minutes"]].agg(["mean", "count"])
    return res
