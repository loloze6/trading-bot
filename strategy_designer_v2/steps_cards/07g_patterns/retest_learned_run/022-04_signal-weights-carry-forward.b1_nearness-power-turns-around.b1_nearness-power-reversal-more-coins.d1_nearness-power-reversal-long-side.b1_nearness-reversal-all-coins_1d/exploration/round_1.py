def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        # coin normal drift over all windows, 5-bar grid
        grid_rets = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                grid_rets.append(c[i + H] / c[i] - 1)
        drift = np.mean(grid_rets) if grid_rets else np.nan
        usual = np.std(grid_rets) if grid_rets else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            r5p = c / c.shift(5) - 1
            r20p = c / c.shift(20) - 1
            r60p = c / c.shift(60) - 1
            vol20 = r1.rolling(20).std()
            hi = df["high"].rolling(90, min_periods=30).max()
            near = c / hi
            fwd = c.shift(-H) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, win=w, f=df["forecast"].iloc[i],
                                 alloc=df["postRebalance_current_allocation"].iloc[i],
                                 r1=r1.iloc[i], r5p=r5p.iloc[i], r20p=r20p.iloc[i],
                                 r60p=r60p.iloc[i], vol20=vol20.iloc[i], near=near.iloc[i],
                                 fwd=fwd.iloc[i], ex=fwd.iloc[i] - drift,
                                 z=(fwd.iloc[i] - drift) / usual,
                                 wd=ts.iloc[i].dayofweek, yr=ts.iloc[i].year))
    g = pd.DataFrame(rows)
    out = {}
    def summ(by):
        t = g.groupby(by, observed=True)["ex"].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        return t.round(4)
    g["fbin"] = pd.cut(g["f"], [-0.01, 0.0001, 2, 5, 10, 21], labels=["0", "0-2", "2-5", "5-10", "10+"])
    out["excess5 by forecast bin"] = summ("fbin")
    # rank within coin to make graded quintiles
    for col in ["r1", "r5p", "r20p", "r60p", "vol20", "near"]:
        g[col + "_q"] = g.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False) if s.notna().sum() > 10 else np.nan)
        out["excess5 by " + col + " quintile (within coin)"] = summ(col + "_q")
    out["excess5 by weekday"] = summ("wd")
    out["excess5 by year"] = summ("yr")
    # Spearman per signal pooled on standardized z
    sp = {}
    for col in ["r1", "r5p", "r20p", "r60p", "vol20", "near", "f"]:
        s = g[[col, "z"]].dropna()
        rr, p = stats.spearmanr(s[col], s["z"])
        sp[col] = (round(rr, 4), len(s), round(p, 4))
    out["spearman signal vs z fwd5"] = pd.DataFrame(sp, index=["rho", "n", "p"]).T
    # forecast>0 interaction with r20p sign
    gp = g[g["f"] > 0].copy()
    gp["mom_up"] = gp["r20p_q"] >= 3
    out["f>0 cases by 20d momentum high/low"] = gp.groupby("mom_up")["ex"].agg(["count", "mean", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))]).round(4)
    # book: daily returns, largest gains/losses context
    d = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df[["book_return", "coin_return"]].copy(); x["coin"] = coin; x["win"] = w
            d.append(x)
    D = pd.concat(d)
    D = D.dropna()
    D["held"] = D["book_return"].abs() > 1e-9
    out["book daily: held share, corr book vs coin on held days"] = pd.Series({
        "held_share": D["held"].mean(),
        "corr_held": D.loc[D.held, ["book_return", "coin_return"]].corr().iloc[0, 1],
        "mean_book_held": D.loc[D.held, "book_return"].mean()})
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["dur_d"] = T["duration_minutes"] / 1440
    T["db"] = pd.qcut(T["dur_d"].rank(method="first"), 4, labels=False)
    out["trades by duration quartile"] = T.groupby("db").agg(n=("dur_d", "size"), dur=("dur_d", "mean"), pnl=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda s: (s > 0).mean())).round(3)
    T["eb"] = pd.qcut(T["entry_forecast"].rank(method="first"), 4, labels=False)
    out["trades by entry forecast quartile"] = T.groupby("eb").agg(n=("dur_d", "size"), ef=("entry_forecast", "mean"), pnl=("net_profit_loss_percent", "mean")).round(3)
    return out
