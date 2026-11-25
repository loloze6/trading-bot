def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = 5
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        g = []
        for w, df in wins.items():
            c = df.sort_values("timestamp")["close"].values
            for i in range(0, len(c) - H, H):
                g.append(c[i + H] / c[i] - 1)
        coin_mean[coin] = np.mean(g)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            n = len(df)
            lo, hi, cl = df["low"], df["high"], df["close"]
            r1 = cl / cl.shift(1) - 1
            vol30 = r1.rolling(30).std()
            plow = lo.shift(1).rolling(30).min()
            d = pd.DataFrame({
                "coin": coin, "win": w, "i": np.arange(n), "cell": np.arange(n) // H,
                "day": df["timestamp"].astype(str).str[:10],
                "fwd": cl.shift(-H) / cl - 1,
                "tr60": cl / cl.shift(60) - 1,
                "tr20": cl / cl.shift(20) - 1,
                "tr10": cl / cl.shift(10) - 1,
                "vol30": vol30, "volz": vol30 / vol30.expanding(20).median(),
                "lrec": (lo < plow) & (cl >= plow),
                "depth": (plow - lo) / plow,
            })
            d["exc"] = d.fwd - coin_mean[coin]
            d["z20"] = d.tr20 / (d.vol30 * np.sqrt(20))
            d["z10"] = d.tr10 / (d.vol30 * np.sqrt(10))
            d["trend"] = np.where(d.tr60 > 0.1, "rising", np.where(d.tr60 < -0.1, "falling", "choppy"))
            d.loc[d.tr60.isna(), "trend"] = np.nan
            d["agit"] = np.where(d.volz > 1, "agit", "calm")
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D.fwd.notna()]

    def grid(s):
        s = s.sort_values("i").groupby(["coin", "win", "cell"]).head(1)
        return s[s.exc.notna()]

    def summ(mask):
        s = grid(D[mask])
        if len(s) < 5:
            return pd.Series({"n": len(s)})
        g = s.groupby("day")["exc"].sum(); G = len(g); m = s.exc.mean()
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean": m, "t": m / se, "coins": s.coin.nunique()})

    out = {}
    ch = D[(D.trend == "choppy") & D.z20.notna()].copy()
    ch["q"] = pd.qcut(ch.z20, 4, labels=False)
    r = {}
    for ag in ["agit", "calm"]:
        for q in range(4):
            r[f"{ag} q{q}"] = summ(D.index.isin(ch[(ch.q == q) & (ch.agit == ag)].index))
    out["choppy: z20 quartile by agitation"] = pd.DataFrame(r).T
    r = {}
    for y in ["2018", "2019", "2020", "2021"]:
        r[y] = summ(D.index.isin(ch[(ch.q == 0) & (ch.day.str[:4] == y)].index))
    out["choppy z20 q0 by year"] = pd.DataFrame(r).T
    r = {}
    for c in D.coin.unique():
        r[c] = summ(D.index.isin(ch[(ch.q == 0) & (ch.coin == c)].index))
    out["choppy z20 q0 by coin"] = pd.DataFrame(r).T
    # graded: day-clustered regression slope of exc on z20 within choppy (grid)
    s = grid(ch)
    res = {}
    for nm, ss in [("choppy all", s), ("choppy agit", s[s.agit == "agit"]), ("choppy calm", s[s.agit == "calm"])]:
        sl, ic, rr, p, se = stats.linregress(ss.z20, ss.exc)
        res[nm] = pd.Series({"n": len(ss), "slope": sl, "t_ols": sl / se, "spearman": stats.spearmanr(ss.z20, ss.exc)[0]})
    s2 = grid(D[D.z20.notna() & (D.trend != "choppy")])
    for tr in ["rising", "falling"]:
        ss = s2[s2.trend == tr]
        sl, ic, rr, p, se = stats.linregress(ss.z20, ss.exc)
        res[tr] = pd.Series({"n": len(ss), "slope": sl, "t_ols": sl / se, "spearman": stats.spearmanr(ss.z20, ss.exc)[0]})
    out["slope of 5d excess on z20 by trend"] = pd.DataFrame(res).T
    # brief's situation in falling agit by depth halves
    fa = D[(D.trend == "falling") & (D.agit == "agit") & D.lrec].copy()
    if len(fa) > 6:
        fa["h"] = fa.depth > fa.depth.median()
        out["falling agit reclaim depth halves"] = pd.DataFrame({str(h): summ(D.index.isin(fa[fa.h == h].index)) for h in [False, True]}).T
    return out
