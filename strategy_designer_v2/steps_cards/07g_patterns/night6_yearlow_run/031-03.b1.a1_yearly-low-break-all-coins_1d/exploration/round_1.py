def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    H = 10
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            n = len(c)
            reg = b["regime"].astype(str).values
            fc = b["forecast"].astype(float).values
            r1 = pd.Series(c).pct_change().values
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            ret10p = pd.Series(c).pct_change(10).values
            ret30p = pd.Series(c).pct_change(30).values
            lo30 = pd.Series(c).rolling(30, min_periods=30).min().shift(1).values
            dist30 = c / lo30 - 1
            hi30 = pd.Series(c).rolling(30, min_periods=30).max().values
            dd30 = c / hi30 - 1
            ts = pd.to_datetime(b["timestamp"])
            for t in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, wd=ts.iloc[t].weekday(), yr=ts.iloc[t].year,
                                 fwd=c[t+H]/c[t]-1, mr=int(reg[t]=="mean_reversion"),
                                 fc=fc[t], vol=vol20[t], p10=ret10p[t], p30=ret30p[t],
                                 d30=dist30[t], dd30=dd30[t], day=ts.iloc[t].normalize()))
    df = pd.DataFrame(rows)
    drift = df.groupby("coin")["fwd"].mean()
    sd = df.groupby("coin")["fwd"].std()
    df["ex"] = df["fwd"] - df["coin"].map(drift)
    df["z"] = df["ex"] / df["coin"].map(sd)
    out = {}
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), mean_z=g["z"].mean(),
                              t=g["ex"].mean()/(g["ex"].std()/np.sqrt(len(g))) if len(g)>2 else np.nan))
    out["by_regime"] = df.groupby("mr").apply(summ)
    for col in ["p10", "p30", "vol", "dd30", "d30"]:
        d = df.dropna(subset=[col]).copy()
        d["q"] = d.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
        out["by_" + col + "_quintile"] = d.groupby("q").apply(summ)
        rho, p = stats.spearmanr(d[col], d["z"])
        out["spearman_" + col] = f"rho={rho:.4f} p={p:.4f} n={len(d)}"
    out["by_weekday"] = df.groupby("wd").apply(summ)
    out["by_year"] = df.groupby("yr").apply(summ)
    # daily: book on largest days; next-day after large moves
    dr = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            c = b["close"].astype(float).values
            r = pd.Series(c).pct_change()
            sdv = r.rolling(60, min_periods=30).std().shift(1)
            zz = r / sdv
            nxt = r.shift(-1)
            n3 = pd.Series(c).shift(-3) / pd.Series(c) - 1
            dr.append(pd.DataFrame(dict(coin=coin, z=zz, nxt=nxt, n3=n3, mr=(b["regime"].astype(str)=="mean_reversion").astype(int).values)))
    dd = pd.concat(dr).dropna()
    dd["zb"] = pd.cut(dd["z"], [-np.inf, -3, -2, -1, 1, 2, 3, np.inf])
    out["next_day_after_zmove"] = dd.groupby("zb").agg(n=("nxt", "size"), next1=("nxt", "mean"), next3=("n3", "mean"))
    out["next_day_by_regime_daily"] = dd.groupby("mr").agg(n=("nxt", "size"), next1=("nxt", "mean"), next3=("n3", "mean"))
    out["share_mr_bars"] = float(dd["mr"].mean())
    return out
