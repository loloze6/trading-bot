def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    coin_mean = {}
    for coin, wins in bars.items():
        allg = {24: [], 72: [], 144: []}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in allg:
                idx = np.arange(0, n - h, h)
                allg[h].extend(list(c[idx + h] / c[idx] - 1))
        coin_mean[coin] = {h: np.mean(v) for h, v in allg.items()}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; v = df["volume"].values.astype(float)
            n = len(df)
            vs = pd.Series(v)
            raw = (vs.rolling(72).median() / vs.rolling(72).mean()).values
            past = pd.Series(c).pct_change(72).values
            # concentration: share of 72h abs move from top 3 hours
            r1 = np.abs(pd.Series(c).pct_change().values)
            top3 = pd.Series(r1).rolling(72).apply(lambda x: np.sort(x)[-3:].sum() / x.sum() if x.sum() > 0 else np.nan, raw=True).values
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - 72, 72):
                if df["regime"].iat[i] != "trending" or not (df["forecast"].iat[i] > 0):
                    continue
                rec = dict(coin=coin, window=w, year=ts.iat[i].year, f=df["forecast"].iat[i],
                           raw=raw[i], past=past[i], top3=top3[i])
                for h in (24, 72, 144):
                    if i + h < n:
                        rec["x%d" % h] = c[i + h] / c[i] - 1 - coin_mean[coin][h]
                rows.append(rec)
    d = pd.DataFrame(rows)
    def tb(sub, col="f", y="x72"):
        sub = sub.dropna(subset=[col, y])
        k = len(sub) // 3
        if k < 5: return pd.Series(dict(n=len(sub), diff=np.nan, t=np.nan, top=np.nan, bot=np.nan))
        s = sub.sort_values(col, kind="stable")
        b, t = s[y].iloc[:k], s[y].iloc[-k:]
        return pd.Series(dict(n=len(sub), diff=t.mean() - b.mean(), t=stats.ttest_ind(t, b, equal_var=False)[0], top=t.mean(), bot=b.mean()))
    out = {}
    out["overall"] = pd.DataFrame({y: tb(d, "f", y) for y in ["x24", "x72", "x144"]}).T
    out["raw_evenness"] = pd.DataFrame({y: tb(d, "raw", y) for y in ["x24", "x72", "x144"]}).T
    out["top3_conc (neg=grind)"] = pd.DataFrame({y: tb(d.assign(g=-d["top3"]), "g", y) for y in ["x24", "x72", "x144"]}).T
    out["by_coin"] = d.groupby("coin").apply(tb)
    out["by_year"] = d.groupby("year").apply(tb)
    d["pastq"] = pd.qcut(d["past"], 3, labels=["small", "mid", "large"])
    out["by_past_rise"] = d.groupby("pastq").apply(tb)
    out["by_past_rise_top3"] = d.assign(g=-d["top3"]).groupby("pastq").apply(lambda s: tb(s, "g"))
    out["corr"] = d[["f", "raw", "top3", "past", "x72"]].corr(method="spearman")
    return out
