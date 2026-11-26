def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            ret7 = c / c.shift(7) - 1
            ret30 = c / c.shift(30) - 1
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            vol30 = r1.rolling(30).std()
            vol90 = r1.rolling(90).std()
            s7 = ret7 / (vol30 * np.sqrt(7))
            r1s = r1 / vol30.shift(1)
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "ret7": ret7, "ret30": ret30, "er": er, "vol30": vol30,
                               "volratio": vol30 / vol90, "s7": s7, "r1s": r1s,
                               "fwd": fwd, "fc": b["forecast"].astype(float),
                               "alloc": b["postRebalance_current_allocation"].astype(float),
                               "wd": ts.dt.weekday, "yr": ts.dt.year})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    g = A[(A["pos"] % H == 0)].dropna(subset=["fwd"]).copy()
    drift = g.groupby("coin")["fwd"].mean()
    sd = g.groupby("coin")["fwd"].std()
    g["un"] = g["fwd"] - g["coin"].map(drift)
    g["z"] = g["un"] / g["coin"].map(sd)

    def summ(x):
        n = len(x)
        m = x.mean()
        t = m / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean_un": m, "t": t})

    out = {}
    gg = g.dropna(subset=["er", "s7", "ret30"]).copy()
    gg["chop"] = np.where(gg["er"] <= 0.3, "chop", "trend")
    gg["s7q"] = pd.qcut(gg["s7"], 5, labels=False)
    out["un by chop x s7 quintile"] = gg.groupby(["chop", "s7q"])["un"].apply(summ).unstack()
    gg["r30sign"] = np.where(gg["ret30"] > 0, "up30", "dn30")
    out["un by chop x r30sign x s7sign"] = gg.groupby(["chop", "r30sign", np.sign(gg["s7"])])["un"].apply(summ).unstack()
    gg["erq"] = pd.qcut(gg["er"], 5, labels=False)
    out["un by ER quintile"] = gg.groupby("erq")["un"].apply(summ).unstack()
    gg["vrq"] = pd.qcut(gg["volratio"], 4, labels=False)
    out["un by vol30/vol90 quartile"] = gg.groupby("vrq")["un"].apply(summ).unstack()
    gg["r30q"] = pd.qcut(gg["ret30"] / (gg["vol30"] * np.sqrt(30)), 5, labels=False)
    out["un by scaled ret30 quintile"] = gg.groupby("r30q")["un"].apply(summ).unstack()
    out["corr s7 vs z by chop and coin"] = gg.groupby(["chop", "coin"]).apply(lambda d: pd.Series({"n": len(d), "corr": d["s7"].corr(d["z"])})).unstack(0)
    # daily: next-day after large scaled 1d moves
    A["nd"] = A.groupby(["coin", "w"])["r1s"].shift(-1)
    d1 = A.dropna(subset=["r1s", "nd"]).copy()
    d1["q"] = pd.qcut(d1["r1s"], 5, labels=False)
    out["next day scaled ret by today scaled ret quintile"] = d1.groupby("q")["nd"].apply(summ).unstack()
    out["next day scaled ret by weekday"] = d1.groupby("wd")["nd"].apply(summ).unstack()
    # book: daily returns by position / regime
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book ret by weekday"] = D.dropna(subset=["book_return"]).groupby("wd")["book_return"].apply(summ).unstack()
    out["book ret by window"] = D.dropna(subset=["book_return"]).groupby("w")["book_return"].apply(summ).unstack()
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values() if len(t)])
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 3, labels=False)
    out["trades by entry fc tercile"] = tr.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades by coin"] = tr.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    return out
