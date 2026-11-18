def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin in bars:
        for w, b in bars[coin].items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            ph = c.shift(1).rolling(30, min_periods=30).max()
            pl = c.shift(1).rolling(30, min_periods=30).min()
            ph90 = c.shift(1).rolling(90, min_periods=90).max()
            fwd20 = c.shift(-20)/c - 1
            fwd10 = c.shift(-10)/c - 1
            past30 = c/c.shift(30) - 1
            vol20 = np.log(c).diff().rolling(20).std()
            wi = int(w[1:])
            for t in range(n):
                rows.append(dict(coin=coin, w=w, wi=wi, t=t, grid20=(t % 20 == 0), grid10=(t % 10 == 0),
                                 fwd20=fwd20.iloc[t], fwd10=fwd10.iloc[t], past30=past30.iloc[t],
                                 vol20=vol20.iloc[t],
                                 newhigh=bool(c.iloc[t] > ph.iloc[t]) if not np.isnan(ph.iloc[t]) else False,
                                 newlow=bool(c.iloc[t] < pl.iloc[t]) if not np.isnan(pl.iloc[t]) else False,
                                 brk=c.iloc[t]/ph.iloc[t]-1 if not np.isnan(ph.iloc[t]) else np.nan,
                                 dd=c.iloc[t]/pl.iloc[t]-1 if not np.isnan(pl.iloc[t]) else np.nan,
                                 high90=bool(c.iloc[t] > ph90.iloc[t]) if not np.isnan(ph90.iloc[t]) else False,
                                 yr=pd.Timestamp(b["timestamp"].iloc[t]).year))
    df = pd.DataFrame(rows)
    for h in (20, 10):
        m = df[df[f"grid{h}"]].groupby("coin")[f"fwd{h}"].mean()
        df[f"x{h}"] = df[f"fwd{h}"] - df["coin"].map(m)

    def events(mask, span=20, col="x20"):
        sel = []
        for (coin, w), g in df[mask].groupby(["coin", "w"]):
            last = -999
            for i, t in zip(g.index, g.t):
                if t - last >= span:
                    sel.append(i); last = t
        return df.loc[sel].dropna(subset=[col])
    def tt(x):
        x = x.dropna(); return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan))

    eh = events(df.newhigh)
    out["newhigh_by_coin"] = eh.groupby("coin")["x20"].apply(tt).unstack()
    eh["half"] = np.where(eh.wi <= 12, "w1-w12", "w13-w24")
    out["newhigh_by_half"] = eh.groupby("half")["x20"].apply(tt).unstack()
    out["newhigh_by_year"] = eh.groupby("yr")["x20"].agg(["count", "mean"])
    eh10 = events(df.newhigh, 10, "x10")
    out["newhigh_x10"] = tt(eh10["x10"])
    e = eh.dropna(subset=["past30"])
    out["newhigh_x20_vs_past30"] = pd.Series(dict(r=stats.pearsonr(e.past30, e.x20)[0], n=len(e),
                                                  slope=stats.linregress(e.past30, e.x20).slope))
    e90 = events(df.high90)
    out["high90_x20"] = tt(e90["x20"])
    # non-event grid baseline: grid20 bars with no new high
    g = df[df.grid20 & ~df.newhigh]
    out["grid_nohigh_x20"] = tt(g["x20"])
    # graded: grid20 bars by past30 quintile, each coin
    g20 = df[df.grid20].dropna(subset=["past30", "x20"]).copy()
    g20["q"] = g20.groupby("coin")["past30"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["x20_by_past30_quint"] = g20.groupby("q")["x20"].apply(tt).unstack()
    out["grid_past30_corr"] = pd.Series(dict(r=stats.pearsonr(g20.past30, g20.x20)[0], n=len(g20)))
    # lows: depth relation by coin, half
    el = events(df.newlow).dropna(subset=["past30"])
    el["half"] = np.where(el.wi <= 12, "a", "b")
    out["newlow_corr_by_coin_half"] = el.groupby(["coin", "half"]).apply(
        lambda s: pd.Series(dict(n=len(s), r=stats.pearsonr(s.past30, s.x20)[0] if len(s) > 3 else np.nan)))
    el["q"] = pd.qcut(el.past30, 3, labels=False)
    out["newlow_x20_by_depth_tercile"] = el.groupby("q")["x20"].apply(tt).unstack()

    # book's largest days: coin returns after
    dd = []
    for coin in days:
        for w, d in days[coin].items():
            d = d.copy().reset_index(drop=True); d["coin"] = coin; d["w"] = w
            d["next5"] = d["close"].shift(-5)/d["close"] - 1
            d["prev5"] = d["close"]/d["close"].shift(5) - 1
            dd.append(d)
    D = pd.concat(dd).dropna(subset=["book_return"])
    D["wd"] = pd.to_datetime(D["day"]).dt.dayofweek
    lo, hi = D.book_return.quantile([0.02, 0.98])
    out["book_extremes"] = pd.DataFrame({
        "big_loss": D[D.book_return <= lo][["coin_return", "prev5", "next5"]].mean(),
        "big_gain": D[D.book_return >= hi][["coin_return", "prev5", "next5"]].mean(),
        "all": D[["coin_return", "prev5", "next5"]].mean()})
    out["sat_by_coin_half"] = D[D.wd == 5].assign(half=lambda x: np.where(x.w.str[1:].astype(int) <= 12, "a", "b")).groupby(["coin", "half"])["coin_return"].apply(tt).unstack()
    return out
