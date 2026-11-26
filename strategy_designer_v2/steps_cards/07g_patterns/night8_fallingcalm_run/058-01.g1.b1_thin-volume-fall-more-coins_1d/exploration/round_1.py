def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            ret30 = c / c.shift(30) - 1
            ret60 = c / c.shift(60) - 1
            ret5p = c / c.shift(5) - 1
            vr = v.rolling(30).mean().shift(30) / v.rolling(30).mean()
            sd30 = r1.rolling(30).std()
            z1 = r1 / sd30.shift(1)
            z5 = ret5p / (sd30 * np.sqrt(5))
            vz = v / v.rolling(30).mean().shift(1)
            fwd5 = c.shift(-5) / c - 1
            fwd1 = c.shift(-1) / c - 1
            rng = (df["high"] - df["low"]) / c
            clpos = (c - df["low"]) / (df["high"] - df["low"]).replace(0, np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), 5):
                if i + 5 >= len(df):
                    break
                rows.append(dict(coin=coin, w=w, regime=df["regime"].iloc[i],
                                 fc=df["forecast"].iloc[i], ret30=ret30.iloc[i], ret60=ret60.iloc[i],
                                 vr=vr.iloc[i], z1=z1.iloc[i], z5=z5.iloc[i], vz=vz.iloc[i], clpos=clpos.iloc[i],
                                 sd30=sd30.iloc[i], fwd5=fwd5.iloc[i], wd=ts.iloc[i].weekday(),
                                 year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
    g = pd.DataFrame(rows)
    g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    g["sex5"] = g["ex5"] / (g.groupby("coin")["fwd5"].transform("std"))
    out = {}

    def summ(sub, col="ex5"):
        x = sub[col].dropna()
        n = len(x)
        if n < 3:
            return pd.Series(dict(n=n))
        return pd.Series(dict(n=n, mean=x.mean(), t=x.mean() / (x.std() / np.sqrt(n)), days=sub.loc[x.index, "day"].nunique()))

    out["by_regime"] = g.groupby("regime").apply(summ).round(4)
    # ret30 quintiles inside and outside profile
    for reg, lab in [("unknown", "prof"), ("chop", "out")]:
        s = g[(g.regime == reg) & g.ret30.notna()].copy()
        if len(s) > 20:
            s["q"] = pd.qcut(s.ret30, 5, labels=False, duplicates="drop")
            out[f"ret30_q_{lab}"] = s.groupby("q").apply(lambda x: pd.concat([summ(x), pd.Series(dict(r30=x.ret30.mean()))])).round(4)
    # 60d trend groups (computable part), all regimes
    s = g[g.ret60.notna()].copy()
    s["trend"] = np.where(s.ret60 > 0.1, "rising", np.where(s.ret60 < -0.1, "falling", "choppy"))
    s["q30"] = pd.qcut(s.ret30, 3, labels=["lo", "mid", "hi"])
    out["trend_x_ret30"] = s.groupby(["trend", "q30"]).apply(summ).round(4)
    # volume ratio terciles in falling calm
    s = g[(g.regime == "unknown") & g.vr.notna() & (g.ret30 < 0)].copy()
    if len(s) > 20:
        s["q"] = pd.qcut(s.vr, 3, labels=False, duplicates="drop")
        out["vr_terc_prof_fall"] = s.groupby("q").apply(lambda x: pd.concat([summ(x), pd.Series(dict(vr=x.vr.mean()))])).round(4)
    # large 1-day moves and 5-day moves
    s = g[g.z1.notna()].copy()
    s["z1b"] = pd.cut(s.z1, [-np.inf, -2, -1, 1, 2, np.inf])
    out["z1_all"] = s.groupby("z1b").apply(summ).round(4)
    s["z5b"] = pd.cut(s.z5, [-np.inf, -1.5, -0.5, 0.5, 1.5, np.inf])
    out["z5_all"] = s.groupby("z5b").apply(summ).round(4)
    out["z5_by_regime"] = s.groupby(["regime", "z5b"]).apply(summ).round(4)
    s2 = s[s.vz.notna()].copy()
    s2["vzb"] = pd.qcut(s2.vz, 4, labels=False, duplicates="drop")
    out["volspike_q"] = s2.groupby("vzb").apply(summ).round(4)
    s3 = s[s.clpos.notna()].copy()
    s3["cp"] = pd.cut(s3.clpos, [0, 0.2, 0.8, 1.0001], include_lowest=True)
    out["closepos"] = s3.groupby("cp").apply(summ).round(4)
    # volatility level
    s4 = g[g.sd30.notna()].copy()
    s4["vq"] = s4.groupby("coin")["sd30"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["vol_terc"] = s4.groupby("vq").apply(summ).round(4)
    # weekday of daily returns
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            d = df.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["cx"] = D.coin_return - D.groupby("coin")["coin_return"].transform("mean")
    out["weekday_coin"] = D.groupby("wd")["cx"].agg(["count", "mean", lambda x: x.mean() / (x.std() / np.sqrt(len(x)))]).round(5)
    # book by window
    out["book_by_window"] = D.groupby("w")["book_return"].agg(["count", "mean", "sum"]).round(5)
    # trades
    T = []
    for coin, wins in trades.items():
        for w, df in wins.items():
            if df is not None and len(df):
                t = df.copy(); t["coin"] = coin; t["w"] = w; T.append(t)
    if T:
        T = pd.concat(T)
        T["fq"] = pd.qcut(T.entry_forecast.abs(), 3, labels=False, duplicates="drop")
        out["trades_by_fc"] = T.groupby("fq")["net_profit_loss_percent"].agg(["count", "mean", "median", lambda x: (x > 0).mean()]).round(3)
        out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean"]).round(3)
        out["trade_dur_days"] = (T.duration_minutes / 1440).describe().round(2)
    return out
