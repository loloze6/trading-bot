def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "day": pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r1": r1, "sd30": sd30,
                "z1": r1 / sd30,
                "z5": (c / c.shift(5) - 1) / sd30,
                "f1": c.shift(-1) / c - 1,
                "f3": c.shift(-3) / c - 1,
                "f5": c.shift(-5) / c - 1,
                "chop": (b["regime"] == "unknown").astype(int),
                "rng": (b["high"] - b["low"]) / c,
                "cl": (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
            })
            d["vq"] = sd30.rolling(90, min_periods=30).rank(pct=True)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    # drift per coin per horizon (all windows)
    for h in (1, 3, 5):
        g = D[D["pos"] % h == 0]
        m = g.groupby("coin")["f%d" % h].mean()
        D["a%d" % h] = D["f%d" % h] - D["coin"].map(m)

    def dayt(df, col):
        df = df.dropna(subset=[col])
        s = df.groupby("day")[col].sum()
        n = len(s)
        if n < 5: return (np.nan, np.nan, len(df), n)
        mean_case = df[col].mean()
        t = s.mean() / (s.std(ddof=1) / np.sqrt(n))
        return (mean_case, t, len(df), n)

    out = {}
    # 1. signed follow-through of 1-day z and 5-day z, by regime, horizon
    res = []
    for sitcol in ("z1", "z5"):
        for h in (1, 3, 5):
            g = D[(D["pos"] % h == 0)].dropna(subset=[sitcol, "a%d" % h]).copy()
            g["x"] = np.sign(g[sitcol]) * g["a%d" % h]
            for ch in (0, 1):
                gg = g[g["chop"] == ch]
                q = gg[sitcol].abs().quantile([1/3, 2/3]).values
                for lab, sub in (("all", gg), ("top3", gg[gg[sitcol].abs() > q[1]]),
                                 ("bot3", gg[gg[sitcol].abs() <= q[0]])):
                    m, t, n, nd = dayt(sub, "x")
                    res.append([sitcol, h, "chop" if ch else "outside", lab, m, t, n])
    out["follow_through_sign_x_adj"] = pd.DataFrame(res, columns=["sit", "h", "reg", "grp", "mean", "t_day", "n"])
    # 2. close location in range -> next day, by regime
    res = []
    g = D.dropna(subset=["cl", "a1"]).copy()
    g["clq"] = pd.qcut(g["cl"], 5, labels=False)
    for ch in (0, 1):
        for q in range(5):
            m, t, n, nd = dayt(g[(g["chop"] == ch) & (g["clq"] == q)], "a1")
            res.append([ch, q, m, t, n])
    out["closeloc_next1"] = pd.DataFrame(res, columns=["chop", "clq", "mean", "t", "n"])
    # 3. weekday
    res = []
    for wd in range(7):
        m, t, n, nd = dayt(D[D["wd"] == wd], "a1")
        res.append([wd, m, t, n])
    out["weekday_adj1"] = pd.DataFrame(res, columns=["wd", "mean", "t", "n"])
    # 4. vol quantile -> fwd 5 (raw, not signed)
    res = []
    g = D[D["pos"] % 5 == 0].dropna(subset=["vq", "a5"]).copy()
    g["vb"] = pd.cut(g["vq"], [0, .33, .66, 1.0], labels=False, include_lowest=True)
    for ch in (0, 1):
        for vb in range(3):
            m, t, n, nd = dayt(g[(g["chop"] == ch) & (g["vb"] == vb)], "a5")
            res.append([ch, vb, m, t, n])
    out["volq_fwd5"] = pd.DataFrame(res, columns=["chop", "vb", "mean", "t", "n"])
    # 5. large down/up day (z1) next 3d unsigned, by regime
    res = []
    g = D[D["pos"] % 3 == 0].dropna(subset=["z1", "a3"]).copy()
    g["zb"] = pd.cut(g["z1"], [-99, -2, -1, 0, 1, 2, 99], labels=False)
    for ch in (0, 1):
        for zb in range(6):
            m, t, n, nd = dayt(g[(g["chop"] == ch) & (g["zb"] == zb)], "a3")
            res.append([ch, zb, m, t, n])
    out["z1bin_fwd3"] = pd.DataFrame(res, columns=["chop", "zbin", "mean", "t", "n"])
    # 6. book: daily returns by side and regime
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["win"] = w; dd.append(x)
    DD = pd.concat(dd, ignore_index=True)
    pos = D.groupby(["coin", "win", "day"])["alloc"].last().reset_index()
    pos["day"] = pos["day"]
    DD["day"] = pd.to_datetime(DD["day"]).dt.floor("D")
    if DD["day"].dt.tz is not None and pos["day"].dt.tz is None:
        DD["day"] = DD["day"].dt.tz_localize(None)
    if pos["day"].dt.tz is not None:
        pos["day"] = pos["day"].dt.tz_localize(None); DD["day"] = DD["day"].dt.tz_localize(None) if DD["day"].dt.tz is not None else DD["day"]
    DD = DD.merge(pos, on=["coin", "win", "day"], how="left")
    DD["prev_alloc"] = DD.groupby(["coin", "win"])["alloc"].shift(1)
    DD["side"] = np.sign(DD["prev_alloc"]).fillna(0)
    out["book_by_side"] = DD.groupby("side")["book_return"].agg(["mean", "count", "std"])
    out["book_by_win"] = DD.groupby("win")["book_return"].mean()
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    out["trades_by_side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean", "median", "count"])
    out["trades_by_coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["mean", "count"])
    out["share_chop_bars"] = D["chop"].mean()
    return out
