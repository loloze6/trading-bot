def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H_list = [6, 18, 42, 84]
    drift = {}
    rows = []
    for coin, wins in bars.items():
        rets = {h: [] for h in H_list}
        for w, df in wins.items():
            c = df["close"].values; n = len(c)
            for h in H_list:
                idx = np.arange(0, n - h, h)
                rets[h].extend(list(c[idx + h] / c[idx] - 1))
        drift[coin] = {h: (np.mean(rets[h]), np.std(rets[h], ddof=1)) for h in H_list}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(c)
            fc = df["forecast"].fillna(0).values
            prev = np.r_[0, fc[:-1]]
            reg = df["regime"].astype(str).values
            cs_ = pd.Series(c)
            ch6 = cs_.pct_change(6).values * 100
            dd180 = (cs_ / cs_.rolling(180, min_periods=1).max() - 1).values * 100
            rng = (df["high"] - df["low"]) / df["close"]
            ratio = (rng.rolling(6).mean() / rng.rolling(180).mean()).values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            sig = (reg == "mean_reversion") & ((fc - prev) >= 2)
            for h in H_list:
                seen = set()
                for t in np.where(sig)[0]:
                    cell = t // h
                    if cell in seen or t + h >= n:
                        continue
                    seen.add(cell)
                    d, s = drift[coin][h]
                    rows.append({"h": h, "coin": coin, "year": year[t], "fall": -ch6[t], "dd": -dd180[t],
                                 "ratio": ratio[t], "ex": (c[t+h]/c[t]-1-d)/s, "unus": c[t+h]/c[t]-1-d,
                                 "tot": c[t+h]/c[t]-1})
    cs = pd.DataFrame(rows)
    out = {}
    def tt(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std(ddof=1)/np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out["own_grid_by_h"] = cs.groupby("h").apply(lambda g: pd.Series({"n": len(g), "ex": g.ex.mean(), "t": tt(g.ex)["t"], "unus%": 100*g.unus.mean(), "tot%": 100*g.tot.mean()}))
    g18 = cs[cs.h == 18]; g42 = cs[cs.h == 42]
    out["h18_by_coin"] = g18.groupby("coin")["ex"].apply(tt).unstack()
    out["h18_by_year"] = g18.groupby("year")["ex"].apply(tt).unstack()
    out["h42_by_year"] = g42.groupby("year")["ex"].apply(tt).unstack()
    sl = {}
    for h in H_list:
        g = cs[cs.h == h].dropna()
        for v in ["fall", "dd", "ratio"]:
            r = stats.linregress(g[v], g["ex"])
            sl[f"{h}_{v}"] = {"n": len(g), "slope": r.slope, "t": r.slope/r.stderr, "rank": stats.spearmanr(g[v], g["ex"])[0]}
    out["slopes"] = pd.DataFrame(sl).T
    g = g18.dropna().copy()
    g["ddq"] = pd.qcut(g["dd"], 3, labels=False)
    out["h18_by_dd_tercile"] = g.groupby("ddq").agg(n=("ex","size"), dd=("dd","mean"), ex=("ex","mean"))
    g["fq"] = pd.qcut(g["fall"], 3, labels=False)
    out["h18_by_fall_tercile"] = g.groupby("fq").agg(n=("ex","size"), fall=("fall","mean"), ex=("ex","mean"))
    out["h18_excl_2018"] = tt(g18[g18.year != 2018]["ex"])
    return out
