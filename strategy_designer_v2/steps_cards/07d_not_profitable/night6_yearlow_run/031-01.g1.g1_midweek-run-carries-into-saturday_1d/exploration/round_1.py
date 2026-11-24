def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    dayrows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            b["ts"] = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float)
            b["r1"] = c.shift(-1) / c - 1
            b["rprev"] = c / c.shift(1) - 1
            b["r20"] = c / c.shift(20) - 1
            b["r60"] = c / c.shift(60) - 1
            dr = c.pct_change()
            b["vol20"] = dr.rolling(20).std()
            b["vol60"] = dr.rolling(60).std()
            b["hi365pos"] = (c - c.rolling(250, min_periods=60).min()) / (c.rolling(250, min_periods=60).max() - c.rolling(250, min_periods=60).min())
            b["monthu"] = c.shift(1) / c.shift(4) - 1
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["fc"] = b["forecast"].astype(float)
            b["wd"] = b["ts"].dt.weekday
            b["gain"] = b["alloc"] * b["r1"]
            b["coin"] = coin; b["w"] = w
            b["year"] = b["ts"].dt.year
            rows.append(b[["coin","w","year","wd","fc","alloc","r1","rprev","r20","r60","vol20","vol60","hi365pos","monthu","gain"]])
        for w, d in data["days"][coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w
            dayrows.append(d[["coin","w","day","book_return","coin_return"]])
    B = pd.concat(rows, ignore_index=True)
    D = pd.concat(dayrows, ignore_index=True)
    # coin mean daily return
    mu = B.groupby("coin")["r1"].mean()
    B["ex"] = B["r1"] - B["coin"].map(mu)
    F = B[(B.wd == 4) & (B.fc != 0) & B.r1.notna()].copy()
    F["side"] = np.where(F.fc > 0, "long", "short")
    F["sgn_ex"] = np.sign(F.fc) * F["ex"]
    def summ(g):
        n = len(g)
        return pd.Series({"n": n, "mean_signed_ex%": 100*g.sgn_ex.mean(), "t": g.sgn_ex.mean()/(g.sgn_ex.std()/np.sqrt(n)) if n>2 else np.nan,
                          "mean_gain%": 100*g.gain.mean(), "mean|alloc|": g.alloc.abs().mean()})
    out["by_side"] = F.groupby("side").apply(summ)
    F["fcq"] = pd.qcut(F.fc.abs(), 4, labels=False)
    out["by_side_fcq"] = F.groupby(["side","fcq"]).apply(summ)
    out["by_year"] = F.groupby("year").apply(summ)
    F["volq"] = pd.qcut(F.vol20/F.vol60, 3, labels=False)
    out["by_volratio"] = F.groupby(["volq","side"]).apply(summ)
    F["r60s"] = np.where(F.r60 > 0, "up60", "down60")
    out["by_trend60_side"] = F.groupby(["r60s","side"]).apply(summ)
    F["lowq"] = pd.qcut(F.hi365pos, 3, labels=False)
    out["by_rangepos_side"] = F.groupby(["lowq","side"]).apply(summ)
    F["agree"] = np.where(np.sign(F.rprev) == np.sign(F.fc), "fri_agrees", "fri_opposes")
    out["by_friday_agree"] = F.groupby("agree").apply(summ)
    # book daily and drawdown
    D = D.dropna(subset=["book_return"])
    bk = D.groupby(["w","day"])["book_return"].mean().reset_index()
    bk["wn"] = bk["w"].str[1:].astype(int)
    bk = bk.sort_values(["wn","day"])
    v = (1 + bk.book_return).cumprod()
    dd = v / v.cummax() - 1
    bk["dd"] = dd.values
    out["maxdd"] = float(dd.min())
    out["dd_by_window_min"] = bk.groupby("wn")["dd"].min()
    out["book_ret_by_window_%"] = bk.groupby("wn")["book_return"].sum()*100
    return out
