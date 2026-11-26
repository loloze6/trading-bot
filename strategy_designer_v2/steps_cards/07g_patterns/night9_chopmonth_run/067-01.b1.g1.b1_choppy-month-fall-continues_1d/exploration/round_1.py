def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(b)
            r30 = c / c.shift(30) - 1
            raw = b.get("debug_info.components.month_fall.last_history_value")
            r60 = c / c.shift(60) - 1
            r7 = c / c.shift(7) - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            hi30 = c.rolling(30).max(); lo30 = c.rolling(30).min()
            pos30 = (c - lo30) / (hi30 - lo30)
            fwd = c.shift(-10) / c - 1
            for i in range(0, n, 10):
                if i + 10 >= n: continue
                rows.append(dict(coin=coin, w=w, i=i, ts=b["timestamp"].iloc[i],
                                 chop=b["regime"].iloc[i] == "unknown",
                                 raw=raw.iloc[i] if raw is not None else np.nan,
                                 r30=r30.iloc[i], r60=r60.iloc[i], r7=r7.iloc[i], r1=r1.iloc[i],
                                 vol=vol20.iloc[i], pos=pos30.iloc[i],
                                 fc=b["forecast"].iloc[i], fwd=fwd.iloc[i]))
    d = pd.DataFrame(rows)
    drift = d.groupby("coin")["fwd"].mean()
    d["ex"] = d["fwd"] - d["coin"].map(drift)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["year"] = pd.to_datetime(d["ts"]).dt.year
    d["wd"] = pd.to_datetime(d["ts"]).dt.dayofweek
    out = {}
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean() / (x.std(ddof=1) / np.sqrt(len(x))) if len(x) > 2 else np.nan))
    out["raw_debug_vs_r30_corr"] = float(d[["raw", "r30"]].dropna().corr().iloc[0, 1]) if d["raw"].notna().sum() > 5 else "na"
    ch = d[d.chop].copy()
    ch["r30q"] = pd.qcut(ch["r30"], 5, labels=False, duplicates="drop")
    out["chop_by_r30_quintile"] = ch.groupby("r30q").apply(summ).join(ch.groupby("r30q")["r30"].mean().rename("r30mean"))
    nc = d[~d.chop & d.r60.notna()].copy()
    nc["trend"] = np.where(nc.r60 > 0.1, "rising", np.where(nc.r60 < -0.1, "falling", "choppy?"))
    nc["r30q"] = pd.qcut(nc["r30"], 5, labels=False, duplicates="drop")
    out["nonchop_trend_x_r30q"] = nc.groupby(["trend", "r30q"]).apply(summ)
    # chop: other predictors
    for col in ["r7", "r1", "pos", "vol"]:
        s = ch[[col, "ex"]].dropna()
        s["q"] = pd.qcut(s[col], 5, labels=False, duplicates="drop")
        out["chop_by_" + col] = s.groupby("q").apply(summ).join(s.groupby("q")[col].mean().rename(col + "mean"))
    out["chop_by_year"] = ch.groupby("year").apply(summ)
    out["all_by_weekday"] = d.groupby("wd").apply(summ)
    # chop cases with r30<0: by year, short direction
    sh = ch[ch.r30 < 0]
    out["chop_fall_by_year"] = sh.groupby("year").apply(summ)
    out["chop_fall_by_coin"] = sh.groupby("coin").apply(summ)
    # book
    br = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w
            br.append(x)
    br = pd.concat(br)
    out["book_by_window"] = br.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "count"))
    out["book_by_coin"] = br.groupby("coin").agg(book=("book_return", "mean"), sumbook=("book_return", "sum"), n=("book_return", "count"))
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): tt = t.copy(); tt["coin"] = coin; tr.append(tt)
    tr = pd.concat(tr)
    tr["dur_d"] = tr["duration_minutes"] / 1440
    tr["efq"] = pd.qcut(tr["entry_forecast"], 4, labels=False, duplicates="drop")
    out["trades_by_entry_fc_q"] = tr.groupby("efq").agg(n=("net_profit_loss_percent", "count"), net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"), dur=("dur_d", "mean"), fc=("entry_forecast", "mean"))
    out["trades_side"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "count"), net=("net_profit_loss_percent", "mean"), dur=("dur_d", "median"))
    return out
