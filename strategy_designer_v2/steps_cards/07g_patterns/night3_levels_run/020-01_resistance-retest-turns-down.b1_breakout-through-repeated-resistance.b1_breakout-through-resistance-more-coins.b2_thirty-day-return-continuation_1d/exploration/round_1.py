def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    H = 10
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=15).std()
            ret7 = c / c.shift(7) - 1
            ret3 = c / c.shift(3) - 1
            hi30 = c.rolling(30, min_periods=20).max()
            lo30 = c.rolling(30, min_periods=20).min()
            pos30 = (c - lo30) / (hi30 - lo30)
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, f=b["forecast"].iloc[i],
                                 fwd=c.iloc[i + H] / c.iloc[i] - 1,
                                 r1=r1.iloc[i], r3=ret3.iloc[i], r7=ret7.iloc[i], vol=vol20.iloc[i],
                                 pos=pos30.iloc[i], wd=ts.iloc[i].dayofweek, year=ts.iloc[i].year,
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    out = {}
    def tab(col, q=5):
        d = g.dropna(subset=[col, "ex"]).copy()
        d["b"] = pd.qcut(d[col].rank(method="first"), q, labels=False)
        t = d.groupby("b").agg(lo=(col, "min"), hi=(col, "max"), n=("ex", "size"),
                               mean_ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["mean_ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.drop(columns="sd").round(4)
    out["by_forecast_quintile"] = tab("f")
    out["by_r1_quintile"] = tab("r1")
    out["by_r7_quintile"] = tab("r7")
    out["by_vol_quintile"] = tab("vol")
    out["by_pos30_quintile"] = tab("pos")
    # slope of ex on forecast within vol terciles
    d = g.dropna(subset=["f", "ex", "vol"]).copy()
    d["vt"] = pd.qcut(d["vol"].rank(method="first"), 3, labels=False)
    res = []
    for k, s in d.groupby("vt"):
        lr = stats.linregress(s["f"], s["ex"])
        res.append(dict(vt=k, n=len(s), slope=lr.slope, t=lr.slope / lr.stderr))
    out["slope_by_vol_tercile"] = pd.DataFrame(res).round(5)
    # slope by forecast sign
    res = []
    for k, s in d.groupby(d["f"] > 0):
        lr = stats.linregress(s["f"], s["ex"])
        res.append(dict(pos=k, n=len(s), mean_ex_signed=(np.sign(s["f"]) * s["ex"]).mean(), slope=lr.slope, t=lr.slope / lr.stderr))
    out["by_side"] = pd.DataFrame(res).round(5)
    # interaction: forecast x r7 residual (short-term reversal inside momentum)
    d2 = g.dropna(subset=["f", "ex", "r7", "vol"]).copy()
    d2["r7z"] = d2["r7"] / (d2["vol"] * np.sqrt(7))
    X = np.column_stack([np.ones(len(d2)), d2["f"], d2["r7z"]])
    beta, *_ = np.linalg.lstsq(X, d2["ex"], rcond=None)
    resid = d2["ex"] - X @ beta
    s2 = resid.var(ddof=3)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    out["ols_f_and_r7z"] = pd.DataFrame({"beta": beta, "t": beta / se}, index=["const", "f", "r7z"]).round(5)
    # weekday of grid bar
    out["by_weekday_signed"] = g.assign(se=np.sign(g["f"]) * g["ex"]).groupby("wd")["se"].agg(["size", "mean"]).round(4)
    # book: daily returns, worst days and window/year
    dd = []
    for coin, wins in data["days"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; t["win"] = w; dd.append(t)
    D = pd.concat(dd)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby(["win", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean"), nc=("coin", "size")).reset_index()
    bk = bk.dropna()
    bk["year"] = bk["day"].dt.year
    yt = bk.groupby("year").agg(n=("br", "size"), book=("br", "mean"), hold=("cr", "mean"), bsd=("br", "std"))
    yt["book_sharpe"] = yt["book"] / yt["bsd"] * np.sqrt(365)
    out["book_by_year"] = yt.round(5)
    wt = []
    for w, s in bk.sort_values("day").groupby("win"):
        v = (1 + s["br"]).cumprod()
        wt.append(dict(win=w, n=len(s), chain=v.iloc[-1] - 1, maxdd=(v / v.cummax() - 1).min(), hold=(1 + s["cr"]).prod() - 1))
    out["book_by_window"] = pd.DataFrame(wt).set_index("win").round(4)
    # book return vs market return on the day: worst book days
    q = bk["br"].quantile([0.02, 0.98])
    out["book_worst2pct_market"] = pd.Series({"n": (bk["br"] <= q.iloc[0]).sum(),
                                             "book_mean": bk.loc[bk["br"] <= q.iloc[0], "br"].mean(),
                                             "coins_mean": bk.loc[bk["br"] <= q.iloc[0], "cr"].mean(),
                                             "best_book_mean": bk.loc[bk["br"] >= q.iloc[1], "br"].mean(),
                                             "best_coins_mean": bk.loc[bk["br"] >= q.iloc[1], "cr"].mean()}).round(4)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades_by_side"] = tr.groupby("side")["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
    return out
