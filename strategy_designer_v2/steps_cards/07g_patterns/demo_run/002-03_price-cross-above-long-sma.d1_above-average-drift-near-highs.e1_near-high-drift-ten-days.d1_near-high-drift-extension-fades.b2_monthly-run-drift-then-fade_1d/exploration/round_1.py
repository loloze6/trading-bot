def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, ws in bars.items():
        # coin mean 10-bar return on grid over all windows
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            fwd10 = np.r_[c[10:]/c[:-10]-1, [np.nan]*10] if n > 10 else np.full(n, np.nan)
            fwd5 = np.r_[c[5:]/c[:-5]-1, [np.nan]*5] if n > 5 else np.full(n, np.nan)
            past30 = pd.Series(c).pct_change(30).values
            past10 = pd.Series(c).pct_change(10).values
            vol20 = pd.Series(r1).rolling(20).std().values
            dd = c/pd.Series(c).cummax().values-1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n, 10):
                rows.append(dict(coin=coin, w=w, i=i, fwd10=fwd10[i], fwd5=fwd5[i],
                    fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i], p30=past30[i], p10=past10[i],
                    r1=r1[i], vol=vol20[i], wd=ts.iloc[i].weekday(), yr=ts.iloc[i].year,
                    alloc=df["postRebalance_current_allocation"].iloc[i]))
    g = pd.DataFrame(rows)
    g["ex"] = g["fwd10"] - g.groupby("coin")["fwd10"].transform("mean")
    out = {}
    def summ(x, by):
        x = x.dropna(subset=["ex", by])
        r = x.groupby(by)["ex"].agg(["count", "mean", "std"])
        r["t"] = r["mean"]/(r["std"]/np.sqrt(r["count"]))
        return r.round(4)
    out["regime"] = summ(g, "reg")
    tr = g[g.reg == "trending"].copy()
    tr["fcq"] = pd.qcut(tr["fc"], 5, labels=False, duplicates="drop")
    out["trend_fc_quintile"] = summ(tr, "fcq")
    un = g[g.reg != "trending"].copy()
    un["p30q"] = pd.qcut(un["p30"], 5, labels=False)
    out["below200_p30_quintile"] = summ(un, "p30q")
    tr["p30q"] = pd.qcut(tr["p30"], 5, labels=False)
    out["above200_raw_p30_quintile"] = summ(tr, "p30q")
    g["p10q"] = pd.qcut(g["p10"], 5, labels=False)
    out["all_p10_quintile"] = summ(g, "p10q")
    g["volq"] = pd.qcut(g["vol"], 5, labels=False)
    out["vol_quintile"] = summ(g, "volq")
    g["r1q"] = pd.qcut(g["r1"], 5, labels=False)
    out["r1_quintile"] = summ(g, "r1q")
    out["by_year"] = summ(g, "yr")
    out["coin_trend"] = tr.dropna(subset=["ex","fc"]).groupby("coin").apply(
        lambda d: pd.Series({"n": len(d), "corr": np.corrcoef(d.fc, d.ex)[0,1]})).round(3)
    # book daily
    D = []
    for coin, ws in days.items():
        for w, d in ws.items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    b = D.dropna(subset=["book_return"]).groupby("wd")["book_return"].agg(["count","mean","std"])
    b["t"] = b["mean"]/(b["std"]/np.sqrt(b["count"]))
    out["book_weekday"] = b.round(5)
    c = D.dropna(subset=["coin_return"]).groupby("wd")["coin_return"].agg(["count","mean","std"])
    c["t"] = c["mean"]/(c["std"]/np.sqrt(c["count"]))
    out["coin_weekday"] = c.round(5)
    return out
