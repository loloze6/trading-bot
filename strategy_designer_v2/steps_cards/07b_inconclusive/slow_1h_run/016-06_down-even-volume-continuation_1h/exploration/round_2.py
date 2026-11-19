def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].astype(float)
            conc = np.log(v.rolling(72).mean() / v.rolling(72).median().replace(0, np.nan))
            lr = np.log(b["close"]).diff()
            past = b["close"]/b["close"].shift(72)-1
            # path efficiency: |net log move| / sum |hourly log moves| (1 = grind, small = choppy/jumpy)
            eff = lr.rolling(72).sum().abs() / lr.abs().rolling(72).sum()
            # jump share: largest 3 |hourly moves| over sum |moves|
            top3 = lr.abs().rolling(72).apply(lambda a: np.sort(a)[-3:].sum(), raw=True) / lr.abs().rolling(72).sum()
            n = len(b)
            for i in range(0, n, 72):
                r = {"coin": coin, "year": pd.Timestamp(b["timestamp"].iloc[i]).year,
                     "regime": b["regime"].iloc[i], "fc": b["forecast"].iloc[i],
                     "conc": conc.iloc[i], "past": past.iloc[i], "eff": eff.iloc[i], "top3": top3.iloc[i]}
                for h in (24, 72, 168):
                    r[f"f{h}"] = c[i+h]/c[i]-1 if i+h < n else np.nan
                rows.append(r)
    df = pd.DataFrame(rows)
    for h in (24, 72, 168):
        df[f"x{h}"] = df[f"f{h}"] - df.groupby("coin")[f"f{h}"].transform("mean")
    def mreg(d, xs, y):
        d = d[xs+[y]].dropna()
        X = np.column_stack([np.ones(len(d))]+[d[x].values for x in xs]); Y = d[y].values
        beta, *_ = np.linalg.lstsq(X, Y, rcond=None); e = Y - X@beta
        s2 = e@e/(len(d)-X.shape[1]); se = np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
        return {f"{x}_t": beta[k+1]/se[k+1] for k, x in enumerate(xs)} | {"n": len(d)}
    out = {}
    res = {}
    for side, d in (("down", df[df.past < 0]), ("up", df[df.past > 0])):
        for h in (24, 72, 168):
            res[f"{side}_conc+past_x{h}"] = mreg(d, ["conc", "past"], f"x{h}")
            res[f"{side}_eff+past_x{h}"] = mreg(d, ["eff", "past"], f"x{h}")
            res[f"{side}_top3+past_x{h}"] = mreg(d, ["top3", "past"], f"x{h}")
            res[f"{side}_fc+past_x{h}"] = mreg(d, ["fc", "past"], f"x{h}") if side == "down" else {}
    out["multi t"] = pd.DataFrame(res).T
    up = df[df.past > 0].copy()
    up["cq"] = pd.qcut(up["conc"], 5, labels=False)
    out["up conc quintile"] = up.groupby("cq").agg(conc=("conc","mean"), past=("past","mean"), x72=("x72","mean"), x168=("x168","mean"), n=("x168","count"))
    dn = df[df.past < 0].copy()
    dn["pq"] = pd.qcut(dn["past"], 5, labels=False)
    out["down past quintile"] = dn.groupby("pq").agg(past=("past","mean"), x24=("x24","mean"), x72=("x72","mean"), x168=("x168","mean"), n=("x72","count"))
    out["up conc x168 by coin"] = pd.DataFrame({k: mreg(g, ["conc","past"], "x168") for k, g in up.groupby("coin")}).T
    return out
