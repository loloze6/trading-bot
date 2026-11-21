def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]; trades = data["trades"]

    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))

    rows120, rows24, rowsh = [], [], []
    for coin, wins in bars.items():
        recs120, recs24 = [], []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"]).reset_index(drop=True)
            r1 = c.pct_change()
            ret24 = c / c.shift(24) - 1
            scale = ret24.abs().rolling(720, min_periods=120).mean()
            m = ret24 / scale
            vol = r1.rolling(720, min_periods=240).std()
            ret720 = c / c.shift(720) - 1
            near = c / c.rolling(720, min_periods=240).max() - 1
            ret120p = c / c.shift(120) - 1
            mult120 = ret120p / (r1.rolling(720, min_periods=240).std() * np.sqrt(120))
            for h, recs in ((120, recs120), (24, recs24)):
                fwd = c.shift(-h) / c - 1
                idx = np.arange(0, len(c), h)
                d = pd.DataFrame({"coin": coin, "w": w, "fwd": fwd.iloc[idx].values, "m": m.iloc[idx].values,
                                  "vol": vol.iloc[idx].values, "ret720": ret720.iloc[idx].values,
                                  "near": near.iloc[idx].values, "mult120": mult120.iloc[idx].values})
                recs.append(d)
            rowsh.append(pd.DataFrame({"coin": coin, "hour": ts.dt.hour, "r1": r1}))
        for recs, lst in ((recs120, rows120), (recs24, rows24)):
            d = pd.concat(recs)
            d = d.dropna(subset=["fwd"])
            d["unus"] = d["fwd"] - d["fwd"].mean()
            d["str"] = d["unus"] / d["fwd"].std()
            for col in ["vol", "ret720", "near"]:
                d[col + "_q"] = pd.qcut(d[col].rank(method="first"), 5, labels=False) if d[col].notna().sum() > 10 else np.nan
            lst.append(d)
    g120 = pd.concat(rows120); g24 = pd.concat(rows24)

    def binned(d, col, bins=None, qcol=None):
        if qcol is None:
            b = pd.cut(d[col], bins)
        else:
            b = d[qcol]
        res = d.groupby(b, observed=True).agg(n=("unus", "size"), mean_unus_pct=("unus", lambda x: 100 * x.mean()),
                                              strength=("str", "mean"))
        res["t"] = d.groupby(b, observed=True)["unus"].apply(tstat)
        return res.round(4)

    mb = [-np.inf, -3, -2, -1, -0.5, 0, 0.5, 1, 2, 3, np.inf]
    out["120h fwd by 24h multiple"] = binned(g120, "m", mb)
    out["24h fwd by 24h multiple"] = binned(g24, "m", mb)
    out["120h fwd by vol quintile"] = binned(g120, None, qcol="vol_q")
    out["120h fwd by 30d return quintile"] = binned(g120, None, qcol="ret720_q")
    out["120h fwd by nearness to 30d high quintile"] = binned(g120, None, qcol="near_q")
    out["120h fwd by 5d-return multiple"] = binned(g120, "mult120", [-np.inf, -2, -1, -0.5, 0, 0.5, 1, 2, np.inf])
    out["24h fwd by vol quintile"] = binned(g24, None, qcol="vol_q")

    h = pd.concat(rowsh).dropna()
    hh = h.groupby("hour")["r1"].agg(["mean", "size"])
    hh["mean_bps"] = hh["mean"] * 1e4
    hh["t"] = h.groupby("hour")["r1"].apply(tstat)
    out["1h return by hour"] = hh[["size", "mean_bps", "t"]].round(3)

    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            x = df.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    wk = dd.groupby("wd").agg(n=("coin_return", "count"), coin_bps=("coin_return", lambda x: 1e4 * x.mean()),
                              book_bps=("book_return", lambda x: 1e4 * x.mean()))
    wk["t_coin"] = dd.groupby("wd")["coin_return"].apply(tstat)
    out["daily by weekday"] = wk.round(3)
    pw = dd.groupby("w").agg(book_bps=("book_return", lambda x: 1e4 * x.mean()),
                             coin_bps=("coin_return", lambda x: 1e4 * x.mean()))
    out["daily by window"] = pw.round(2)
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    out["daily by year"] = dd.groupby("year").agg(book_bps=("book_return", lambda x: 1e4 * x.mean()),
                                                  coin_bps=("coin_return", lambda x: 1e4 * x.mean()),
                                                  n=("book_return", "count")).round(2)

    # book: market vs timing per coin
    bt = []
    for coin, wins in bars.items():
        allr = []
        for w, df in wins.items():
            c = df["close"].astype(float).reset_index(drop=True)
            a = df["postRebalance_current_allocation"].astype(float).reset_index(drop=True)
            r = c.shift(-1) / c - 1
            allr.append(pd.DataFrame({"a": a, "r": r}))
        x = pd.concat(allr).dropna()
        mu = x["r"].mean()
        bt.append({"coin": coin, "gain_bps_day": 24e4 * (x.a * x.r).mean(), "market_bps_day": 24e4 * (x.a * mu).mean(),
                   "mean_alloc": x.a.mean(), "share_in": (x.a.abs() > 1e-6).mean()})
    out["book gain split"] = pd.DataFrame(bt).set_index("coin").round(3)

    tr = []
    for coin, wins in trades.items():
        for w, df in wins.items():
            if len(df): x = df.copy(); x["coin"] = coin; tr.append(x)
    tr = pd.concat(tr)
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 5, labels=False)
    tt = tr.groupby("fq").agg(n=("net_profit_loss_percent", "size"), fc=("entry_forecast", "mean"),
                              net_pct=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda x: x.median() / 60))
    tt["t"] = tr.groupby("fq")["net_profit_loss_percent"].apply(tstat)
    out["trades by entry forecast quintile"] = tt.round(3)
    return out
