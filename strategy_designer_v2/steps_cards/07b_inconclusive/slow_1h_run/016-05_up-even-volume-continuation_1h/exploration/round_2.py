def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        allg = []
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            idx = np.arange(0, n - 72, 72)
            allg.extend(list(c[idx + 72] / c[idx] - 1))
        coin_mean[coin] = np.mean(allg)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df)
            cs = pd.Series(c)
            past = cs.pct_change(72).values
            r1 = np.abs(cs.pct_change().values)
            top3 = pd.Series(r1).rolling(72).apply(lambda x: np.sort(x)[-3:].sum() / x.sum() if x.sum() > 0 else np.nan, raw=True).values
            # efficiency ratio: net move / sum abs moves
            er = (np.abs(cs.diff(72)) / pd.Series(np.abs(cs.diff().values)).rolling(72).sum()).values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - 72, 72):
                if not (past[i] > 0):
                    continue
                rows.append(dict(coin=coin, year=ts.iat[i].year, f=df["forecast"].iat[i],
                                 trend=df["regime"].iat[i] == "trending",
                                 past=past[i], g=-top3[i], er=er[i],
                                 x72=c[i + 72] / c[i] - 1 - coin_mean[coin]))
    d = pd.DataFrame(rows)
    def tb(sub, col="g", y="x72"):
        sub = sub.dropna(subset=[col, y]); k = len(sub) // 3
        if k < 5: return pd.Series(dict(n=len(sub), diff=np.nan, t=np.nan, top=np.nan, bot=np.nan))
        s = sub.sort_values(col, kind="stable"); b, t = s[y].iloc[:k], s[y].iloc[-k:]
        return pd.Series(dict(n=len(sub), diff=t.mean() - b.mean(), t=stats.ttest_ind(t, b, equal_var=False)[0], top=t.mean(), bot=b.mean()))
    out = {}
    d["pastq"] = pd.qcut(d["past"], 3, labels=["small", "mid", "large"])
    sm = d[d["pastq"] != "large"]
    out["grind_all_up"] = tb(d).to_frame().T
    out["er_all_up"] = tb(d, "er").to_frame().T
    out["grind_small_mid"] = tb(sm).to_frame().T
    out["grind_small_mid_by_coin"] = sm.groupby("coin").apply(tb)
    out["grind_small_mid_by_year"] = sm.groupby("year").apply(tb)
    out["even_f_small_mid"] = tb(sm[sm.f > 0], "f").to_frame().T
    out["er_by_pastq"] = d.groupby("pastq").apply(lambda s: tb(s, "er"))
    return out
