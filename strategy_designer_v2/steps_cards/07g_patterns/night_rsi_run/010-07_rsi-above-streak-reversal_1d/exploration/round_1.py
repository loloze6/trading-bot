def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 14
    def rsi(c, n=14):
        d = c.diff()
        up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
        dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
        return 100 - 100/(1+up/dn)
    grid = []; daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = rsi(c)
            side = np.sign(r - 50)
            age = np.zeros(len(c)); 
            for i in range(len(c)):
                if np.isnan(r.iloc[i]) or i < 14: age[i] = np.nan; continue
                s = side.iloc[i]
                prev = age[i-1] if i > 0 and not np.isnan(age[i-1]) else 0
                if s > 0: age[i] = min(prev+1, 60) if prev > 0 else 1
                else: age[i] = max(prev-1, -60) if prev < 0 else -1
            ret1 = c.pct_change()
            vol20 = ret1.rolling(20).std()
            past14 = c / c.shift(14) - 1
            past3 = c / c.shift(3) - 1
            fwd = c.shift(-H) / c - 1
            fwd3 = c.shift(-3) / c - 1
            pos = b["postRebalance_current_allocation"].astype(float)
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "rsi": r, "age": age, "past14": past14, "vol20": vol20,
                               "fwd": fwd, "pos": pos, "year": ts.dt.year})
            idx = np.arange(0, len(c), H)
            grid.append(df.iloc[idx])
            daily.append(pd.DataFrame({"coin": coin, "w": w, "ret1": ret1, "next1": ret1.shift(-1), "past3": past3,
                                       "fwd3": fwd3, "vol20": vol20, "wd": ts.dt.weekday, "pos": pos,
                                       "rsi": r, "age": age}))
    g = pd.concat(grid).dropna(subset=["fwd", "age", "past14"])
    g["ex"] = g["fwd"] - g.groupby("coin")["fwd"].transform("mean")
    def ols(x, y):
        m = ~(np.isnan(x) | np.isnan(y))
        res = stats.linregress(x[m], y[m]); return pd.Series({"slope": res.slope, "t": res.slope/res.stderr, "n": m.sum()})
    tab = {}
    for name, sub in [("all", g), ("above", g[g.age > 0]), ("below", g[g.age < 0])]:
        for col in ["age", "rsi", "past14", "vol20"]:
            tab[f"{name}:{col}"] = ols(sub[col].values.astype(float), sub["ex"].values.astype(float))
    for coin in g.coin.unique():
        sub = g[g.coin == coin]
        for col in ["age", "rsi", "past14"]:
            tab[f"{coin}:{col}"] = ols(sub[col].values.astype(float), sub["ex"].values.astype(float))
    out["grid14 slopes ex-return"] = pd.DataFrame(tab).T
    g["agebin"] = pd.cut(g["age"], [-61, -20, -7, 0, 7, 20, 61])
    out["fwd14 by age bin"] = g.groupby("agebin", observed=True)["ex"].agg(["mean", "count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    g["rsibin"] = pd.cut(g["rsi"], [0, 35, 45, 50, 55, 65, 100])
    out["fwd14 by rsi bin"] = g.groupby("rsibin", observed=True)["ex"].agg(["mean", "count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    d = pd.concat(daily)
    # 3-day non-overlap grid
    d3 = d.groupby(["coin", "w"], group_keys=False).apply(lambda x: x.iloc[::3]).dropna(subset=["past3", "fwd3"])
    out["fwd3 on past3 (3d grid)"] = ols(d3["past3"].values, d3["fwd3"].values)
    d3["vb"] = d3.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["fwd3 slope on past3 by vol tercile"] = pd.DataFrame({v: ols(s["past3"].values, s["fwd3"].values) for v, s in d3.groupby("vb")}).T
    dd = d.dropna(subset=["next1", "ret1"])
    dd["z"] = dd["ret1"]/dd["vol20"]
    dd["zb"] = pd.cut(dd["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["next1 by today z-move"] = dd.groupby("zb", observed=True)["next1"].agg(["mean", "count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    out["ret1 by weekday"] = d.dropna(subset=["ret1"]).groupby("wd")["ret1"].agg(["mean", "count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # book
    bk = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            bk.append(x.assign(coin=coin, w=w))
    bk = pd.concat(bk)
    out["book daily by coin"] = bk.groupby("coin")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    out["share bars short"] = float((d["pos"] < 0).mean())
    out["book by window-year?"] = g.groupby("year")["ex"].agg(["mean", "count"])
    return out
