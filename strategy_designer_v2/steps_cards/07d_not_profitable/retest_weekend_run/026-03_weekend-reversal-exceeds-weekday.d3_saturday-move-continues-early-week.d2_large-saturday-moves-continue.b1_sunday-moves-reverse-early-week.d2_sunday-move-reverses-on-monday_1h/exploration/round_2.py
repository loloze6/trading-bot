def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        vals = []
        for w, b in bars[coin].items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 24, 24)
            vals.append(c[idx + 24] / c[idx] - 1)
        dr24 = np.mean(np.concatenate(vals))
        vals = []
        for w, b in bars[coin].items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            vals.append(c[idx + 48] / c[idx] - 1)
        dr48 = np.mean(np.concatenate(vals))
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]
            r24 = c / c.shift(24) - 1
            hr = np.log(c).diff()
            vol = hr.rolling(720, min_periods=720).std()
            vrel = vol / vol.rolling(4320, min_periods=1440).median()
            nxt = ts + pd.Timedelta(hours=1)
            wd = nxt.dt.weekday.values; hh = nxt.dt.hour.values
            for i in np.where(hh == 0)[0]:
                if i < 24 or i + 48 >= len(c) or np.isnan(r24.iloc[i]) or r24.iloc[i] == 0:
                    continue
                s = -np.sign(r24.iloc[i])
                rows.append({"coin": coin, "win": w, "year": ts.iloc[i].year, "mon": wd[i] == 0,
                             "vol": vol.iloc[i], "vrel": vrel.iloc[i],
                             "alloc": abs(b["postRebalance_current_allocation"].iloc[i]),
                             "f24": s * (c.iloc[i + 24] / c.iloc[i] - 1 - dr24),
                             "f48": s * (c.iloc[i + 48] / c.iloc[i] - 1 - dr48),
                             "raw24": c.iloc[i + 24] / c.iloc[i] - 1 - dr24})
    df = pd.DataFrame(rows)
    def summ(g, col="f24"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    mon = df[df["mon"]].copy()
    oth = df[~df["mon"]].copy()
    mon["vq"] = pd.qcut(mon["vol"], 3, labels=False)  # pooled absolute vol level
    edges = mon["vol"].quantile([1/3, 2/3]).values
    oth["vq"] = np.digitize(oth["vol"], edges)
    mon["rq"] = pd.qcut(mon["vrel"], 3, labels=False)
    out["mon_by_pooled_vol"] = mon.groupby("vq").apply(lambda g: pd.concat([summ(g), summ(g, "f48").add_prefix("h48_"),
        pd.Series({"vol": g["vol"].mean(), "alloc": g["alloc"].mean(),
                   "alloc_w_mean": (g["f24"] * g["alloc"]).sum() / g["alloc"].sum()})]))
    out["mon_by_rel_vol"] = mon.groupby("rq").apply(summ)
    out["other_days_reversal_by_vol"] = oth.groupby("vq").apply(summ)
    out["mon_unsigned_drift_by_vol"] = mon.groupby("vq").apply(lambda g: summ(g, "raw24"))
    out["mon_by_coin_hi_vol"] = mon[mon["vq"] == 2].groupby("coin").apply(summ)
    out["mon_by_year_hi_vol"] = mon[mon["vq"] == 2].groupby("year").apply(summ)
    out["mon_vq_by_year_count"] = mon.groupby(["year", "vq"]).size().unstack()
    # book drawdown
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            x = d[["day", "book_return", "coin_return"]].copy(); x["win"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["wn"] = dd["win"].str[1:].astype(int)
    bk = dd.groupby(["wn", "day"])["book_return"].mean().dropna().reset_index().sort_values(["wn", "day"])
    v = (1 + bk["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); ddn = v / peak - 1
    j = ddn.argmin(); k = v[:j + 1].argmax()
    bk["year"] = pd.to_datetime(bk["day"]).dt.year
    out["deepest_fall"] = pd.Series({"depth": ddn[j], "days_long": j - k,
        "start_year": bk["year"].iloc[k], "end_year": bk["year"].iloc[j]})
    out["book_by_year"] = bk.groupby("year")["book_return"].agg(["mean", "sum"])
    return out
