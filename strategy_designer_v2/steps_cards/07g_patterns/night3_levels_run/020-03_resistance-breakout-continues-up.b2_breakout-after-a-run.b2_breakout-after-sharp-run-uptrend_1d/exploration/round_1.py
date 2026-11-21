def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            n = len(c)
            ts = pd.to_datetime(b["timestamp"])
            r1 = pd.Series(c).pct_change().values
            r10 = pd.Series(c).pct_change(10).values
            r60 = pd.Series(c).pct_change(60).values
            r30 = pd.Series(c).pct_change(30).values
            vol20 = pd.Series(r1).rolling(20).std().values
            vol90 = pd.Series(r1).rolling(90, min_periods=40).std().values
            hi90 = pd.Series(c).rolling(90, min_periods=30).max().values
            lo90 = pd.Series(c).rolling(90, min_periods=30).min().values
            fc = b["forecast"].astype(float).values
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 fwd=c[i+H]/c[i]-1, r1=r1[i], r10=r10[i], r30=r30[i], r60=r60[i],
                                 vrat=vol20[i]/vol90[i] if vol90[i] else np.nan,
                                 vol20=vol20[i],
                                 nearhi=c[i]/hi90[i]-1, pos=(c[i]-lo90[i])/(hi90[i]-lo90[i]) if hi90[i]>lo90[i] else np.nan,
                                 fc=fc[i], reg=b["regime"].iloc[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    usual = df.groupby("coin")["fwd"].std()
    df["unus"] = df["fwd"] - df["coin"].map(drift)
    df["str"] = df["unus"] / df["coin"].map(usual)
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, strength=g["str"].mean()))
    for col in ["r1", "r10", "r30", "r60", "vrat", "vol20", "nearhi", "pos"]:
        d = df.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["by_"+col+"_quintile"] = d.groupby("q").apply(summ)
    df["absr1"] = df["r1"].abs()
    d = df.dropna(subset=["r1"]).copy()
    d["big"] = d.groupby("coin")["absr1"].transform(lambda s: s >= s.quantile(0.9))
    d["dir"] = np.sign(d["r1"])
    out["after_big_day_by_dir"] = d[d["big"]].groupby("dir").apply(summ)
    out["by_fc_state"] = df.assign(s=pd.cut(df["fc"], [-0.1, 0.01, 5, 10, 20.1])).groupby("s").apply(summ)
    out["by_weekday"] = df.groupby("wd").apply(summ)
    out["by_year"] = df.groupby("year").apply(summ)
    d = df.dropna(subset=["r60", "r10"]).copy()
    d["up60"] = d["r60"] > 0
    d["q10"] = d.groupby("coin")["r10"].transform(lambda s: pd.qcut(s.rank(method="first"), 3, labels=False))
    out["r60sign_x_r10tercile"] = d.groupby(["up60", "q10"]).apply(summ)
    # book
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    D["year"] = pd.to_datetime(D["day"]).dt.year
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["book_by_year"] = bk.groupby("year").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"),
                                                 bsd=("book_return", "std"))
    out["book_by_coin"] = D.groupby("coin").agg(book=("book_return", "mean"), bsd=("book_return", "std"), coin=("coin_return", "mean"))
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t):
                t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr)
    T["days"] = T["duration_minutes"] / 1440
    T["fq"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades_by_entry_fc_q"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"), fc=("entry_forecast", "mean"),
                                                      net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"),
                                                      days=("days", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean()))
    T["dq"] = pd.cut(T["days"], [0, 5.5, 10, 20, 1e4])
    out["trades_by_duration"] = T.groupby("dq").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"))
    return out
