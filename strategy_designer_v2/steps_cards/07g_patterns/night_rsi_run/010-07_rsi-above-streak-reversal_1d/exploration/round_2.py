def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    def rsi(c, n=14):
        d = c.diff()
        up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean()
        dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
        return 100 - 100/(1+up/dn)
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r = rsi(c)
            age = np.full(len(c), np.nan)
            for i in range(14, len(c)):
                prev = age[i-1] if not np.isnan(age[i-1]) else 0
                if r.iloc[i] > 50: age[i] = min(prev+1, 60) if prev > 0 else 1
                else: age[i] = max(prev-1, -60) if prev < 0 else -1
            ret1 = c.pct_change()
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "wn": int(w[1:]), "age": age, "rsi": r,
                               "vol20": ret1.rolling(20).std(), "vol60": ret1.rolling(60).std(),
                               "past3": c/c.shift(3)-1, "past7": c/c.shift(7)-1, "past30": c/c.shift(30)-1,
                               "year": ts.dt.year, "pos": b["postRebalance_current_allocation"].astype(float)})
            for h in [7, 14, 21, 28]:
                df[f"f{h}"] = c.shift(-h)/c - 1
            df["f3"] = c.shift(-3)/c - 1
            df["i"] = np.arange(len(c))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    def ols(s, x, y):
        s = s.dropna(subset=[x, y])
        if len(s) < 10: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(s)})
        res = stats.linregress(s[x].astype(float), s[y].astype(float))
        return pd.Series({"slope": res.slope, "t": res.slope/res.stderr, "n": len(s)})
    # below-50 run length vs forward excess, several horizons, own grid each
    tab = {}
    for h in [7, 14, 21, 28]:
        g = D[D.i % h == 0].copy()
        g["ex"] = g[f"f{h}"] - g.groupby("coin")[f"f{h}"].transform("mean")
        tab[f"h{h}:below"] = ols(g[g.age < 0], "age", "ex")
        tab[f"h{h}:above"] = ols(g[g.age > 0], "age", "ex")
        for coin in g.coin.unique():
            tab[f"h{h}:below:{coin}"] = ols(g[(g.age < 0) & (g.coin == coin)], "age", "ex")
        tab[f"h{h}:below:w1-12"] = ols(g[(g.age < 0) & (g.wn <= 12)], "age", "ex")
        tab[f"h{h}:below:w13-24"] = ols(g[(g.age < 0) & (g.wn > 12)], "age", "ex")
    out["below-run slope by horizon/coin/half"] = pd.DataFrame(tab).T
    # Spearman h14 below
    g = D[D.i % 14 == 0].copy()
    g["ex"] = g["f14"] - g.groupby("coin")["f14"].transform("mean")
    s = g[g.age < 0].dropna(subset=["ex"])
    rho, p = stats.spearmanr(s["age"], s["ex"])
    out["h14 below spearman"] = pd.Series({"rho": rho, "p": p, "n": len(s)})
    # does past30 explain it? below sub
    out["h14 below: past30 slope"] = ols(s, "past30", "ex")
    s2 = s.dropna(subset=["past30"])
    X = np.column_stack([np.ones(len(s2)), s2["age"], s2["past30"]]); y = s2["ex"].values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None); res = y - X@beta
    cov = (res@res/(len(y)-3))*np.linalg.inv(X.T@X)
    out["h14 below: age t with past30"] = pd.Series({"b_age": beta[1], "t_age": beta[1]/np.sqrt(cov[1,1]), "t_p30": beta[2]/np.sqrt(cov[2,2])})
    # low-vol momentum 3d robustness
    g3 = D[D.i % 3 == 0].dropna(subset=["past3", "f3", "vol20"]).copy()
    g3["vb"] = g3.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    t3 = {}
    for coin in g3.coin.unique():
        for v in [0, 1, 2]:
            t3[f"{coin}:v{v}"] = ols(g3[(g3.coin == coin) & (g3.vb == v)], "past3", "f3")
    for half, m in [("w1-12", g3.wn <= 12), ("w13-24", g3.wn > 12)]:
        t3[f"{half}:v0"] = ols(g3[m & (g3.vb == 0)], "past3", "f3")
    g3["z"] = g3["past3"]/(g3["vol20"]*np.sqrt(3))
    t3["all:z-past3 x lowvolrank"] = ols(g3.assign(zz=g3["z"]*(2-g3["vb"])), "zz", "f3")
    out["3d momentum by vol"] = pd.DataFrame(t3).T
    # 7d horizon low-vol momentum
    g7 = D[D.i % 7 == 0].dropna(subset=["past7", "f7", "vol20"]).copy()
    g7["vb"] = g7.groupby("coin")["vol20"].transform(lambda x: pd.qcut(x, 3, labels=False))
    out["7d momentum by vol"] = pd.DataFrame({v: ols(x, "past7", "f7") for v, x in g7.groupby("vb")}).T
    return out
