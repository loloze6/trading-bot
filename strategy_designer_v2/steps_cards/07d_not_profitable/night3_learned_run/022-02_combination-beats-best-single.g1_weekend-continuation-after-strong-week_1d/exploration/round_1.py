def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    act = []
    bk = []
    for coin, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            c = b["close"].astype(float).values
            allr.append(pd.Series(c).pct_change().dropna())
        mu = pd.concat(allr).mean()
        for w, b in ws.items():
            b = b.copy()
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].astype(float)
            b["nwd"] = (ts + pd.Timedelta(days=1)).dt.weekday.values
            b["r7"] = c / c.shift(7) - 1
            b["r3"] = c / c.shift(3) - 1
            b["r28"] = c / c.shift(28) - 1
            b["n1"] = c.shift(-1) / c - 1 - mu
            b["n2"] = c.shift(-2) / c - 1 - 2 * mu
            b["n3"] = c.shift(-3) / c - 1 - 3 * mu
            b["coin"] = coin
            b["win"] = w
            a = b["postRebalance_current_allocation"].astype(float)
            b["alloc"] = a
            b["gain"] = a * (c.shift(-1) / c - 1)
            rows.append(b[["coin", "win", "nwd", "r7", "r3", "r28", "n1", "n2", "n3", "alloc", "gain", "regime"]])
        for w, d in data["days"][coin].items():
            bk.append(d["book_return"].dropna())
    df = pd.concat(rows, ignore_index=True)
    out["book_daily_mean_all"] = float(pd.concat(bk).mean())
    out["share_bars_long"] = float((df["alloc"] > 1e-9).mean())
    out["mean_alloc_when_long"] = float(df.loc[df["alloc"] > 1e-9, "alloc"].mean())
    out["gain_by_nextweekday"] = df.groupby("nwd")["gain"].agg(["mean", "count"])
    # continuation by next-day weekday
    g = []
    for wd, s in df.dropna(subset=["r7", "n1"]).groupby("nwd"):
        pos = s[s["r7"] > 0]["n1"]; neg = s[s["r7"] <= 0]["n1"]
        t = stats.ttest_ind(pos, neg, equal_var=False).statistic
        g.append([wd, s["r7"].corr(s["n1"]), pos.mean(), neg.mean(), t, len(pos)])
    out["r7_vs_next1_by_nwd"] = pd.DataFrame(g, columns=["nwd", "corr", "mean_pos", "mean_neg", "t", "npos"])
    fr = df[df["nwd"] == 5].dropna(subset=["r7", "n1"]).copy()
    fr["q"] = fr.groupby("coin")["r7"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["fri_quintile"] = fr.groupby("q")[["n1", "n2", "n3", "r7"]].mean()
    # other lookbacks on Friday
    out["fri_corrs"] = pd.Series({k: fr[k].corr(fr["n1"]) for k in ["r3", "r7", "r28"]})
    # all days quintile of r7 -> n1
    al = df.dropna(subset=["r7", "n1"]).copy()
    al["q"] = al.groupby("coin")["r7"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["all_days_quintile_n1"] = al.groupby("q")["n1"].agg(["mean", "count"])
    out["sat_gain_by_coin"] = df[df["alloc"] > 1e-9].groupby("coin")[["gain", "alloc"]].mean()
    return out
