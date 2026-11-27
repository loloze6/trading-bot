def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True).copy()
            c = b["close"]
            b["coin"] = coin; b["win"] = w; b["pos"] = np.arange(len(b))
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["r1"] = c.pct_change()
            for k in [3, 7, 14, 21, 30]:
                b["r%d" % k] = c.pct_change(k)
            b["vol30"] = b["r1"].rolling(30, min_periods=20).std()
            b["z14"] = b["r14"] / (b["vol30"] * np.sqrt(14))
            b["z30"] = b["r30"] / (b["vol30"] * np.sqrt(30))
            b["z3"] = b["r3"] / (b["vol30"] * np.sqrt(3))
            b["r60"] = c.pct_change(60)
            b["volu"] = b["volume"] / b["volume"].rolling(30, min_periods=20).mean()
            for h in [1, 3, 5, 7]:
                b["f%d" % h] = c.shift(-h) / c - 1
            b["fc"] = b["regime"] == "unknown"
            rows.append(b)
    df = pd.concat(rows, ignore_index=True)
    out = {}
    def clust_t(x, d):
        s = pd.DataFrame({"x": x - x.mean(), "d": d}).groupby("d")["x"].sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(x)
        return x.mean() / se, G
    res = {}
    for h in [3, 5, 7]:
        grid = df[df.pos % h == 0].copy()
        drift = grid.groupby("coin")["f%d" % h].mean()
        grid["x"] = grid["f%d" % h] - grid["coin"].map(drift)
        for regname, sub in [("fc", grid[grid.fc]), ("all", grid)]:
            for col in ["r3", "r7", "r14", "r21", "r30", "z3", "z14", "z30", "volu"]:
                s = sub.dropna(subset=[col, "x"])
                if len(s) < 30: continue
                rho, p = stats.spearmanr(s[col], s.x)
                # top tercile minus bottom tercile
                q = pd.qcut(s[col], 3, labels=False, duplicates="drop")
                hi = s.x[q == q.max()]; lo = s.x[q == 0]
                tw = stats.ttest_ind(hi, lo, equal_var=False).statistic
                # long-side graded: positive values only, weighted mean
                pos = s[s[col] > 0]
                if len(pos) > 20:
                    wv = pos[col] / pos[col].mean()
                    wx = pos.x * wv
                    tt, G = clust_t(wx, pos.day)
                    wm = wx.mean()
                else:
                    wm, tt, G = np.nan, np.nan, np.nan
                res[(regname, h, col)] = dict(n=len(s), rho=rho, p=p, hi_lo=hi.mean() - lo.mean(), t_hilo=tw,
                                              pos_n=len(pos), pos_wmean=wm, pos_t=tt, days=G)
    r = pd.DataFrame(res).T
    out["fc horizons"] = r.loc["fc"].round(4)
    out["all horizons (subset)"] = r.loc["all"].loc[[3, 5]].round(4) if "all" in r.index.get_level_values(0) else r
    # r14 by window among fc cases, h=3
    grid = df[(df.pos % 3 == 0) & df.fc].copy()
    drift = df[df.pos % 3 == 0].groupby("coin")["f3"].mean()
    grid["x"] = grid["f3"] - grid["coin"].map(drift)
    grid = grid.dropna(subset=["r14", "x"])
    grid["up14"] = grid["r14"] > 0
    out["fc x3 by r14 sign and window"] = grid.groupby(["win", "up14"])["x"].agg(["size", "mean"]).unstack()
    # book days: largest gains/losses
    dd = pd.concat([d.assign(coin=c) for c, ws in data["days"].items() for d in ws.values()], ignore_index=True)
    dd = dd.dropna(subset=["book_return"])
    act = dd[dd.book_return != 0]
    out["book active days"] = pd.Series({"n": len(act), "mean": act.book_return.mean(), "share up": (act.book_return > 0).mean(),
                                         "coin mean same days": act.coin_return.mean(),
                                         "top10 share of sum": act.book_return.nlargest(10).sum() / act.book_return.sum()})
    return out
