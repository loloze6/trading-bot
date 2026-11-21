def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 72
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = pd.Series(b["close"].astype(float).values)
            n = len(c)
            if n < 3 * H:
                continue
            s = np.log(c).diff()
            sumabs = s.abs().rolling(H).sum()
            lr72 = np.log(c / c.shift(H))
            er = lr72.abs() / sumabs
            ret72 = c / c.shift(H) - 1
            rv = s.rolling(H).std(); rv720 = s.rolling(720).std()
            sumabs144 = s.abs().rolling(144).sum()
            er144 = np.log(c / c.shift(144)).abs() / sumabs144
            fwd = c.shift(-H) / c - 1
            fwd144 = c.shift(-144) / c - 1
            fwd24 = c.shift(-24) / c - 1
            fc = b["forecast"].astype(float)
            alloc = b["postRebalance_current_allocation"].astype(float)
            for i in range(0, n, H):
                rows.append(dict(coin=coin, w=w, wn=int(w[1:]), ret72=ret72.iloc[i], er=er.iloc[i],
                                 er144=er144.iloc[i], rvr=rv.iloc[i] / rv720.iloc[i] if rv720.iloc[i] > 0 else np.nan,
                                 fwd=fwd.iloc[i], fwd144=fwd144.iloc[i], fwd24=fwd24.iloc[i],
                                 fc=fc.iloc[i], alloc=alloc.iloc[i]))
    d = pd.DataFrame(rows).dropna(subset=["fwd", "ret72", "er"])
    for f in ["fwd", "fwd144", "fwd24"]:
        g = d.groupby("coin")[f]
        d[f + "_ex"] = d[f] - g.transform("mean")
        d[f + "_z"] = d[f + "_ex"] / g.transform("std")
    d["sgn"] = np.sign(d["ret72"])
    d["half"] = np.where(d.wn <= 12, "w1-12", "w13-24")
    out = {}
    def tq(df, key, val, q=5):
        df = df.dropna(subset=[key, val]).copy()
        df["q"] = df.groupby("coin")[key].transform(lambda x: pd.qcut(x.rank(method="first"), q, labels=False))
        r = df.groupby("q")[val].agg(["mean", "count", "std"])
        r["t"] = r["mean"] / (r["std"] / np.sqrt(r["count"]))
        r["key_mean"] = df.groupby("q")[key].mean()
        return r.drop(columns="std")
    up = d[d.ret72 > 0].copy()
    out["up: excess fwd72 (%) by raw ER quintile"] = tq(up, "er", "fwd_ex").assign(mean_pct=lambda r: r["mean"] * 100)
    out["up: excess fwd72 by forecast quintile"] = tq(up, "fc", "fwd_ex")
    out["up: corr er vs forecast"] = float(up[["er", "fc"]].corr().iloc[0, 1])
    for h in ["w1-12", "w13-24"]:
        out["up " + h + ": z by ER quintile"] = tq(up[up.half == h], "er", "fwd_z")
    out["up: z144 by ER quintile"] = tq(up, "er", "fwd144_z")
    out["up: z24 by ER quintile"] = tq(up, "er", "fwd24_z")
    out["up: z by ER144 quintile"] = tq(up, "er144", "fwd_z")
    # per-coin slope t of z on er, up moves, controlling for size
    res = {}
    for coin, x in up.groupby("coin"):
        x = x.dropna(subset=["er", "fwd_z"])
        X = np.column_stack([np.ones(len(x)), x.er, x.ret72 / x.ret72.std()])
        b_, *_ = np.linalg.lstsq(X, x.fwd_z.values, rcond=None)
        e = x.fwd_z.values - X @ b_
        cov = np.linalg.inv(X.T @ X) * e.var(ddof=3)
        res[coin] = dict(b_er=b_[1], t_er=b_[1] / np.sqrt(cov[1, 1]), n=len(x))
    out["up per coin: z ~ er + size"] = pd.DataFrame(res).T
    out["vol ratio z by quintile, halves"] = pd.concat({h: tq(d[d.half == h].dropna(subset=["rvr"]), "rvr", "fwd_z") for h in ["w1-12", "w13-24"]})
    out["vol ratio, up only"] = tq(up.dropna(subset=["rvr"]), "rvr", "fwd_z")
    out["vol ratio, down only"] = tq(d[d.ret72 < 0].dropna(subset=["rvr"]), "rvr", "fwd_z")
    # book: allocation level vs next return; days context
    dl = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            x = x.copy(); x["coin"] = coin; x["w"] = w; dl.append(x)
    D = pd.concat(dl)
    bk = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk.book_return.quantile([0.01, 0.99])
    out["book worst 1% days: mean book, mean coin"] = bk[bk.book_return <= q.iloc[0]].mean()
    out["book best 1% days: mean book, mean coin"] = bk[bk.book_return >= q.iloc[1]].mean()
    out["book beta to coin avg"] = float(np.polyfit(bk.coin_return, bk.book_return, 1)[0])
    return out
