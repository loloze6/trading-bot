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
            r1 = c / c.shift(1) - 1
            vol30 = r1.rolling(30).std()
            cp = (b["close"] - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            cp7 = (c - b["low"].rolling(7).min()) / (b["high"].rolling(7).max() - b["low"].rolling(7).min()).replace(0, np.nan)
            fwd7 = c.shift(-7) / c - 1
            alloc = b["postRebalance_current_allocation"].astype(float)
            pos_gain7 = pd.Series([np.nan]*n)
            # book position gain over 7 bars from bar i (before costs)
            pr = (c.shift(-1) / c - 1) * alloc
            pg7 = pr[::-1].rolling(7, min_periods=7).sum()[::-1]
            for i in range(0, n, 7):
                rows.append(dict(coin=coin, w=w, ts=b["timestamp"].iloc[i],
                                 regime=b["regime"].iloc[i], fc=b["forecast"].iloc[i],
                                 r30=r30.iloc[i], vol30=vol30.iloc[i], cp=cp.iloc[i], cp7=cp7.iloc[i],
                                 fwd7=fwd7.iloc[i], alloc=alloc.iloc[i], pg7=pg7.iloc[i]))
    g = pd.DataFrame(rows)
    g["ts"] = pd.to_datetime(g["ts"])
    drift = g.groupby("coin")["fwd7"].mean()
    g["ex7"] = g["fwd7"] - g["coin"].map(drift)
    g["day"] = g["ts"].dt.floor("D")
    g["year"] = g["ts"].dt.year
    g["chop"] = g["regime"] == "unknown"
    vmed = g.groupby("coin")["vol30"].median()
    g["agit"] = g["vol30"] > g["coin"].map(vmed)
    out = {}
    def summ(df, key, col="ex7"):
        d = df.dropna(subset=[col, key])
        res = d.groupby(key)[col].agg(["mean", "count", "std"])
        res["t"] = res["mean"] / (res["std"] / np.sqrt(res["count"]))
        res["days"] = d.groupby(key)["day"].nunique()
        return res
    def dayt(s, col="ex7"):
        d = s.dropna(subset=[col])
        p = d.groupby("day")[col].sum()
        n = len(d)
        m = d[col].mean()
        se = np.sqrt(((d.groupby("day")[col].apply(lambda x: (x - m).sum()))**2).sum()) / n
        return pd.Series(dict(mean=m, t_day=m / se, n=n, days=d["day"].nunique()))
    ch = g[g.chop].dropna(subset=["r30", "ex7"]).copy()
    cells = {}
    for side in ["fall", "rise"]:
        for ag in [True, False]:
            s = ch[(ch.r30 < 0) == (side == "fall")]
            s = s[s.agit == ag]
            cells[f"{side}_{'agit' if ag else 'calm'}"] = dayt(s)
    out["chop cells, day-clustered t"] = pd.DataFrame(cells).T
    # chop agitated: graded by r30 across all (both sides)
    ca = ch[ch.agit].copy()
    ca["q"] = pd.qcut(ca["r30"], 4, labels=False)
    out["chop agitated r30 quartile"] = summ(ca, "q")
    ca2 = ch[ch.agit].copy()
    ca2["vq"] = pd.qcut(ca2["vol30"] / ca2["coin"].map(vmed), 3, labels=False)
    out["chop agitated: vol ratio tercile -> ex7"] = summ(ca2, "vq")
    out["chop agitated by year"] = summ(ca, "year")
    out["chop agitated by window"] = summ(ca, "w")
    # forecast vs r30 among chop falls
    cf = ch[ch.r30 < 0].copy()
    cf["fq"] = pd.qcut(cf["fc"].rank(method="first"), 3, labels=False)
    out["chop fall: forecast tercile (0 most negative) -> ex7"] = summ(cf, "fq")
    out["chop fall: share with forecast<0, corr fc~r30"] = pd.Series(dict(share_fc_neg=(cf.fc < 0).mean(),
                                                                      corr=cf[["fc", "r30"]].corr().iloc[0, 1]))
    # book's 7-bar position gain by cell
    ch["cell"] = np.where(ch.r30 < 0, "fall", "rise") + "_" + np.where(ch.agit, "agit", "calm")
    out["book pos gain 7 by cell, chop"] = summ(ch, "cell", "pg7")
    # close position of the day, by chop / agitation
    a = g.dropna(subset=["cp", "ex7"]).copy()
    a["cpq"] = pd.qcut(a["cp"], 5, labels=False)
    a["grp"] = np.where(a.chop, "chop", "trend") + "_" + np.where(a.agit, "agit", "calm")
    out["close pos top minus bottom quintile, by group"] = pd.DataFrame({k: pd.Series(dict(
        top=s[s.cpq == 4].ex7.mean(), bot=s[s.cpq == 0].ex7.mean(),
        t=stats.ttest_ind(s[s.cpq == 4].ex7, s[s.cpq == 0].ex7, equal_var=False).statistic,
        n=len(s))) for k, s in a.groupby("grp")}).T
    out["close pos quintile by year (top-bot)"] = pd.DataFrame({k: pd.Series(dict(
        diff=s[s.cpq == 4].ex7.mean() - s[s.cpq == 0].ex7.mean(),
        t=stats.ttest_ind(s[s.cpq == 4].ex7, s[s.cpq == 0].ex7, equal_var=False).statistic))
        for k, s in a.groupby("year")}).T
    b7 = g.dropna(subset=["cp7", "ex7"]).copy()
    b7["q"] = pd.qcut(b7["cp7"], 5, labels=False)
    out["7-day close position quintile -> ex7 all"] = summ(b7, "q")
    out["top quintile close pos day-clustered"] = pd.DataFrame({"top": dayt(a[a.cpq == 4]), "bot": dayt(a[a.cpq == 0])}).T
    return out
