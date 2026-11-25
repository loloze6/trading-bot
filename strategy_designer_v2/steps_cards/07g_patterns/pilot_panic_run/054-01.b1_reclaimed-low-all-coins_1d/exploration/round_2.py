def explore(data):
    import numpy as np, pandas as pd
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
            plow = lo.shift(1).rolling(30).min()
            phigh = hi.shift(1).rolling(30).max()
            r1 = cl / cl.shift(1) - 1
            vol30 = r1.rolling(30).std()
            d = pd.DataFrame({
                "coin": coin, "win": w, "i": np.arange(n), "cell": np.arange(n) // H,
                "day": df["timestamp"].astype(str).str[:10],
                "fwd": cl.shift(-H) / cl - 1,
                "r1": r1, "tr60": cl / cl.shift(60) - 1, "tr20": cl / cl.shift(20) - 1,
                "vol30": vol30, "volz": vol30 / vol30.expanding(20).median(),
                "rng": (hi - lo) / cl.shift(1), "pos": (cl - lo) / (hi - lo),
                "plow": plow, "phigh": phigh, "lo": lo, "hi": hi, "cl": cl,
                "alloc": df["postRebalance_current_allocation"],
                "bv": df["postRebalance_total_value"],
            })
            d["exc"] = d.fwd - coin_mean[coin]
            d["hbreak"] = d.hi > d.phigh
            d["hdepth_v"] = (d.cl / d.phigh - 1) / d.vol30
            d["lbreak_rec"] = (d.lo < d.plow) & (d.cl >= d.plow)
            d["depth_v"] = ((d.plow - d.lo) / d.plow) / d.vol30
            d["trend"] = np.where(d.tr60 > 0.1, "rising", np.where(d.tr60 < -0.1, "falling", "choppy"))
            d.loc[d.tr60.isna(), "trend"] = np.nan
            d["agit"] = np.where(d.volz > 1, "agit", "calm")
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D = D[D.fwd.notna()]

    def summ(mask):
        s = D[mask].sort_values("i").groupby(["coin", "win", "cell"]).head(1)
        s = s[s.exc.notna()]
        if len(s) < 5:
            return pd.Series({"n": len(s)})
        g = s.groupby("day")["exc"].sum(); G = len(g); m = s.exc.mean()
        se = np.sqrt((g ** 2).sum() * G / (G - 1)) / len(s)
        return pd.Series({"n": len(s), "days": G, "mean": m, "t": m / se, "coins": s.coin.nunique()})

    out = {}
    res = {}
    for tr in ["rising", "choppy", "falling"]:
        for ag in ["agit", "calm"]:
            m = (D.trend == tr) & (D.agit == ag)
            res[f"{tr} {ag} all"] = summ(m)
            res[f"{tr} {ag} hbreak"] = summ(m & D.hbreak)
            res[f"{tr} {ag} lreclaim"] = summ(m & D.lbreak_rec)
            res[f"{tr} {ag} up>2vol"] = summ(m & (D.r1 > 2 * D.vol30))
    out["by profile"] = pd.DataFrame(res).T
    # high break graded by close distance above old high (in vol units), non-rising
    hb = D[D.hbreak & D.hdepth_v.notna()].copy()
    hb["q"] = pd.qcut(hb.hdepth_v, 4, labels=False)
    r2 = {}
    for tr in ["rising", "choppy", "falling"]:
        for q in range(4):
            r2[f"{tr} q{q}"] = summ(D.index.isin(hb[(hb.q == q) & (hb.trend == tr)].index))
    out["hbreak by close-vs-high quartile and trend"] = pd.DataFrame(r2).T
    out["hbreak quartile edges"] = pd.Series(hb.hdepth_v.quantile([0.25, 0.5, 0.75]).values)
    # by year for hbreak (all)
    r3 = {}
    for y in ["2018", "2019", "2020", "2021"]:
        r3[y] = summ(D.hbreak & (D.day.str[:4] == y))
    out["hbreak by year"] = pd.DataFrame(r3).T
    r4 = {}
    for c in D.coin.unique():
        r4[c] = summ(D.hbreak & (D.coin == c))
    out["hbreak by coin"] = pd.DataFrame(r4).T
    # 20-day trend graded inside choppy
    ch = D[(D.trend == "choppy") & D.tr20.notna()].copy()
    ch["q"] = pd.qcut(ch.tr20, 4, labels=False)
    out["choppy: 20d return quartile"] = pd.DataFrame({f"q{q}": summ(D.index.isin(ch[ch.q == q].index)) for q in range(4)}).T
    return out
