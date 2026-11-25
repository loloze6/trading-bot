def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol30 = r1.rolling(30).std()
            er = (c - c.shift(30)).abs() / c.diff().abs().rolling(30).sum()
            r7 = c / c.shift(7) - 1
            r30 = c / c.shift(30) - 1
            vol90 = r1.rolling(90, min_periods=60).std()
            df = pd.DataFrame({
                "coin": coin, "w": w, "pos": np.arange(len(b)),
                "ts": pd.to_datetime(b["timestamp"]),
                "r1": r1, "r1z": r1 / vol30.shift(1), "vol30": vol30, "volratio": vol30 / vol90,
                "er": er, "r7s": r7 / (vol30 * np.sqrt(7)), "r30": r30,
                "r30s": r30 / (vol30 * np.sqrt(30)),
                "f1": c.shift(-1) / c - 1, "f7": c.shift(-7) / c - 1,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "regime": b["regime"].astype(str),
            })
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    d["wd"] = d["ts"].dt.weekday
    d["day"] = d["ts"].dt.floor("D")
    for h in (1, 7):
        m = d.groupby("coin")["f%d" % h].transform(lambda s: s.iloc[::1].mean())
        d["x%d" % h] = d["f%d" % h] - m
    g7 = d[d["pos"] % 7 == 0]
    out = {}

    def tday(sub, col):
        s = sub.dropna(subset=[col]).groupby("day")[col].mean()
        if len(s) < 3:
            return (np.nan, np.nan, len(s))
        return (s.mean(), s.mean() / (s.std() / np.sqrt(len(s))), len(s))

    def slope_tab(sub, xcol, ycol, bycol):
        res = []
        for k, s in sub.dropna(subset=[xcol, ycol, bycol]).groupby(bycol):
            if len(s) < 30:
                continue
            lr = stats.linregress(s[xcol], s[ycol])
            res.append({bycol: k, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr})
        return pd.DataFrame(res)

    # 1. weekly scaled move -> next week, by ER tercile (non-overlapping grid)
    g7 = g7.copy()
    g7["erb"] = pd.qcut(g7["er"], 3, labels=["chop", "mid", "trend"])
    g7["vb"] = pd.qcut(g7["volratio"], 3, labels=["calmer", "mid", "agitated"])
    out["r7s->x7 by ER tercile"] = slope_tab(g7, "r7s", "x7", "erb")
    out["r7s->x7 by volratio tercile"] = slope_tab(g7, "r7s", "x7", "vb")
    out["r30s->x7 by ER tercile"] = slope_tab(g7, "r30s", "x7", "erb")
    out["r30s->x7 all"] = slope_tab(g7.assign(a=1), "r30s", "x7", "a")
    # 2. daily: after large daily moves
    d2 = d.copy()
    d2["zb"] = pd.qcut(d2["r1z"], 5, labels=False)
    t = d2.dropna(subset=["x1", "zb"]).groupby("zb").agg(n=("x1", "size"), mean_x1=("x1", "mean"), mean_z=("r1z", "mean"))
    t["t"] = [tday(d2[d2["zb"] == k], "x1")[1] for k in t.index]
    out["next-day excess by today's scaled move quintile"] = t
    # 3. weekday
    w = []
    for k in range(7):
        m_, t_, n_ = tday(d[d["wd"] == k], "x1")
        w.append({"wd_of_bar": k, "mean_next_x1": m_, "t": t_, "days": n_})
    out["next-day excess by weekday of signal bar"] = pd.DataFrame(w)
    # 4. vol level -> next week mean (drift premium?)
    g7["vlev"] = g7.groupby("coin")["vol30"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["x7 by own vol30 tercile"] = g7.groupby("vlev")["x7"].agg(["size", "mean", lambda s: s.mean() / s.std() * np.sqrt(len(s))])
    # 5. book: active vs inactive, by forecast size
    act = d[d["fc"] != 0].copy()
    act["fb"] = pd.qcut(act["fc"].abs(), 4, labels=False)
    act["sx1"] = np.sign(act["fc"]) * act["x1"]
    act["sx7"] = np.sign(act["fc"]) * act["x7"]
    out["active: signed next-day / next-week excess by |forecast| quartile"] = act.groupby("fb").agg(
        n=("sx1", "size"), sx1=("sx1", "mean"), sx7=("sx7", "mean"))
    act["side"] = np.where(act["fc"] > 0, "long", "short")
    out["active by side"] = act.groupby("side").agg(n=("sx1", "size"), sx1=("sx1", "mean"), sx7=("sx7", "mean"))
    out["active by year"] = act.assign(y=act["ts"].dt.year).groupby("y").agg(n=("sx1", "size"), sx1=("sx1", "mean"))
    # 6. book days around largest losses
    dd = []
    for coin, wins in data["days"].items():
        for wk, t_ in wins.items():
            dd.append(t_.assign(coin=coin, w=wk))
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"]).agg(br=("book_return", "mean"), cr=("coin_return", "mean")).dropna()
    q = bk["br"].quantile([0.02, 0.98])
    out["book worst/best 2% days: mean coin return same day"] = pd.Series({
        "worst_book": bk.loc[bk.br <= q.iloc[0], "br"].mean(), "worst_coin": bk.loc[bk.br <= q.iloc[0], "cr"].mean(),
        "best_book": bk.loc[bk.br >= q.iloc[1], "br"].mean(), "best_coin": bk.loc[bk.br >= q.iloc[1], "cr"].mean(),
        "corr_book_coin": bk["br"].corr(bk["cr"])})
    return out
