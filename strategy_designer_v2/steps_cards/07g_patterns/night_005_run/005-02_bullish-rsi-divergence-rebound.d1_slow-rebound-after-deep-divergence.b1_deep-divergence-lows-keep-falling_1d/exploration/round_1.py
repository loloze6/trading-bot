def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]

    def rsi(c, n=14):
        d = c.diff()
        up = d.clip(lower=0).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
        dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False, min_periods=n).mean()
        return 100 - 100/(1+up/dn)

    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = rsi(c)
            n = len(c)
            prior_low = c.shift(1).rolling(30, min_periods=30).min()
            fwd20 = c.shift(-20)/c - 1
            fwd5 = c.shift(-5)/c - 1
            past20 = c/c.shift(20) - 1
            past5 = c/c.shift(5) - 1
            past30 = c/c.shift(30) - 1
            vol20 = np.log(c).diff().rolling(20).std()
            prior_high = c.shift(1).rolling(30, min_periods=30).max()
            for t in range(n):
                newlow = (not np.isnan(prior_low.iloc[t])) and c.iloc[t] < prior_low.iloc[t]
                newhigh = (not np.isnan(prior_high.iloc[t])) and c.iloc[t] > prior_high.iloc[t]
                div = np.nan
                if newlow and t >= 30:
                    seg = c.iloc[t-30:t-3]
                    j = seg.idxmin()
                    if not np.isnan(r.iloc[j]) and not np.isnan(r.iloc[t]):
                        div = r.iloc[t] - r.iloc[j]
                rows.append(dict(coin=coin, w=w, t=t, grid20=(t % 20 == 0), grid5=(t % 5 == 0),
                                 fwd20=fwd20.iloc[t], fwd5=fwd5.iloc[t], past20=past20.iloc[t],
                                 past5=past5.iloc[t], past30=past30.iloc[t], vol20=vol20.iloc[t],
                                 newlow=newlow, newhigh=newhigh, div=div,
                                 wd=pd.Timestamp(b["timestamp"].iloc[t]).dayofweek,
                                 yr=pd.Timestamp(b["timestamp"].iloc[t]).year))
    df = pd.DataFrame(rows)
    m20 = df[df.grid20].groupby("coin")["fwd20"].mean()
    m5 = df[df.grid5].groupby("coin")["fwd5"].mean()
    df["x20"] = df["fwd20"] - df["coin"].map(m20)
    df["x5"] = df["fwd5"] - df["coin"].map(m5)

    # event spacing: first event in any 20-bar span, per kind
    def events(mask):
        sel = []
        for (coin, w), g in df[mask].groupby(["coin", "w"]):
            last = -999
            for i, t in zip(g.index, g.t):
                if t - last >= 20:
                    sel.append(i); last = t
        return df.loc[sel].dropna(subset=["x20"])
    def summ(e, col="x20"):
        x = e[col].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              share_up=(e["fwd20"] > 0).mean()))
    ev = {}
    ev["divlow"] = events(df.newlow & (df["div"] > 0))
    ev["low_nodiv"] = events(df.newlow & (df["div"] <= 0))
    ev["anylow"] = events(df.newlow)
    ev["newhigh"] = events(df.newhigh)
    out["events_x20"] = pd.DataFrame({k: summ(v) for k, v in ev.items()}).T
    a, b_ = ev["divlow"]["x20"], ev["low_nodiv"]["x20"]
    out["div_minus_nodiv_welch_t"] = float(stats.ttest_ind(a, b_, equal_var=False).statistic)
    e = ev["anylow"].dropna(subset=["past30"])
    out["anylow_x20_vs_past30_corr"] = pd.Series(dict(r=stats.pearsonr(e.past30, e.x20)[0], n=len(e)))

    # forward 5d after past 5d moves, grid5
    g5 = df[df.grid5].dropna(subset=["past5", "x5"]).copy()
    g5["q"] = g5.groupby("coin")["past5"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["x5_by_past5_quint"] = g5.groupby("q")["x5"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    g5["vq"] = g5.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["x5_by_vol_quint"] = g5.groupby("vq")["x5"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    g20 = df[df.grid20].dropna(subset=["past20", "x20"]).copy()
    g20["q"] = g20.groupby("coin")["past20"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["x20_by_past20_quint"] = g20.groupby("q")["x20"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])

    # weekday daily returns
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    out["coin_ret_by_weekday"] = D.groupby("wd")["coin_return"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["book_by_year"] = D.groupby("yr")[["book_return", "coin_return"]].mean()
    out["book_by_coin"] = D.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std"])
    return out
