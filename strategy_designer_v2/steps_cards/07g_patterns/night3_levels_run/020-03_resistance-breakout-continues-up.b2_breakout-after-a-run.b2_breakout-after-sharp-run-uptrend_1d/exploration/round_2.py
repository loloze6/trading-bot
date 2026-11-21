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
            s = pd.Series(c)
            r1 = s.pct_change().values
            r10 = s.pct_change(10).values
            r30 = s.pct_change(30).values
            vol60 = s.pct_change().rolling(60, min_periods=30).std().values
            fc = b["forecast"].astype(float).values
            reg = (b["regime"] == "trending").values
            # days since the last trending (break) bar, and since forecast turned positive
            since_brk = np.full(n, np.nan); last = None
            since_on = np.full(n, np.nan); on = None
            for i in range(n):
                if reg[i]:
                    last = i
                if last is not None:
                    since_brk[i] = i - last
                if fc[i] > 0:
                    if on is None:
                        on = i
                    since_on[i] = i - on
                else:
                    on = None
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 half=0 if ts.iloc[i].year <= 2021 else 1,
                                 fwd=c[i+H]/c[i]-1, r1z=r1[i]/vol60[i] if vol60[i] else np.nan,
                                 r10z=r10[i]/(vol60[i]*np.sqrt(10)) if vol60[i] else np.nan,
                                 r30z=r30[i]/(vol60[i]*np.sqrt(30)) if vol60[i] else np.nan,
                                 r1=r1[i], fc=fc[i], sb=since_brk[i], so=since_on[i]))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    usual = df.groupby("coin")["fwd"].std()
    df["unus"] = df["fwd"] - df["coin"].map(drift)
    df["str"] = df["unus"] / df["coin"].map(usual)
    def summ(g):
        x = g["unus"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan, strength=g["str"].mean()))
    def slope(d, col):
        d = d.dropna(subset=[col, "str"])
        r = stats.linregress(d[col], d["str"])
        return pd.Series(dict(n=len(d), slope=r.slope, t=r.slope/r.stderr))
    # graded momentum: slope of strength on vol-scaled past returns, by coin and by half
    for col in ["r1z", "r10z", "r30z"]:
        d = df.copy(); d[col] = d[col].clip(-4, 4)
        out["slope_"+col+"_by_coin"] = d.groupby("coin").apply(lambda g: slope(g, col))
        out["slope_"+col+"_by_half"] = d.groupby("half").apply(lambda g: slope(g, col))
        out["slope_"+col+"_all"] = slope(d, col).to_frame().T
    # r1 quintile pattern by half
    d = df.dropna(subset=["r1"]).copy()
    d["q"] = d.groupby("coin")["r1"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["r1q_by_half"] = d.groupby(["half", "q"]).apply(summ)
    # r30 top vs rest by coin
    d = df.dropna(subset=["r30z"]).copy()
    d["top"] = d.groupby("coin")["r30z"].transform(lambda s: s >= s.quantile(0.8))
    out["r30top_by_coin"] = d[d["top"]].groupby("coin").apply(summ)
    # weekday by half
    df["monTue"] = df["wd"].isin([0, 1])
    out["monTue_by_half"] = df.groupby(["half", "monTue"]).apply(summ)
    out["monTue_by_coin"] = df[df["monTue"]].groupby("coin").apply(summ)
    # in position: by days since forecast turned on
    ip = df[df["fc"] > 0].copy()
    ip["soq"] = pd.cut(ip["so"], [-0.5, 2.5, 7.5, 15.5, 30.5, 1e4])
    out["inpos_by_days_since_on"] = ip.groupby("soq").apply(summ)
    out["inpos_by_coin"] = ip.groupby("coin").apply(summ)
    out["inpos_by_half"] = ip.groupby("half").apply(summ)
    # after a break, flat or not: by days since the last break bar
    d = df.dropna(subset=["sb"]).copy()
    d["sbq"] = pd.cut(d["sb"], [-0.5, 0.5, 5.5, 15.5, 40.5, 1e5])
    out["by_days_since_break"] = d.groupby("sbq").apply(summ)
    # book: deepest falls and what precedes
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    D = pd.concat(dd)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    out["book_window_stats"] = bk.groupby("w").agg(book=("book_return", "mean"), coin=("coin_return", "mean"),
        worst=("book_return", "min"), best=("book_return", "max")).describe().loc[["mean", "min", "max"]]
    q = bk["book_return"].quantile([0.01, 0.99])
    out["book_tails_coin_same_day"] = pd.DataFrame({
        "worst1pct_book": [bk.loc[bk.book_return <= q.iloc[0], "book_return"].mean(), bk.loc[bk.book_return <= q.iloc[0], "coin_return"].mean()],
        "best1pct_book": [bk.loc[bk.book_return >= q.iloc[1], "book_return"].mean(), bk.loc[bk.book_return >= q.iloc[1], "coin_return"].mean()]},
        index=["book", "coin"])
    return out
