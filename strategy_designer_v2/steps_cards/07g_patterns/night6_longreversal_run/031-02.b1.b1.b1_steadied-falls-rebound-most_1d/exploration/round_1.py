def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}

    def ols_t(x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        m = np.isfinite(x) & np.isfinite(y); x, y = x[m], y[m]
        if len(x) < 5: return np.nan, np.nan, len(x)
        r = stats.linregress(x, y); return r.slope, r.slope / r.stderr if r.stderr > 0 else np.nan, len(x)

    # per-coin drift and usual move for horizon h
    def coin_stats(coin, h):
        rs = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for p in range(0, len(c) - h, h):
                rs.append(c[p + h] / c[p] - 1)
        rs = np.array(rs)
        return (rs.mean(), rs.std(ddof=1)) if len(rs) > 2 else (np.nan, np.nan)

    combos = [(1, 1), (3, 3), (7, 7), (7, 30), (14, 14), (30, 30), (30, 60)]
    summ = []; qtabs = {}
    for h, L in combos:
        rows = []
        for coin in bars:
            dh, sh = coin_stats(coin, h); dL, sL = coin_stats(coin, L)
            for w, df in bars[coin].items():
                c = df["close"].values; reg = df["regime"].values
                for p in range(0, len(c) - h, h):
                    if p - L < 0: continue
                    past = c[p] / c[p - L] - 1; fwd = c[p + h] / c[p] - 1
                    rows.append(dict(z=(past - dL) / sL, ex=(fwd - dh) / sh, exr=fwd - dh, reg=reg[p]))
        d = pd.DataFrame(rows)
        if len(d) < 10: continue
        s, t, n = ols_t(d.z, d.ex)
        d["q"] = pd.qcut(d.z, 5, labels=False, duplicates="drop")
        q = d.groupby("q").agg(n=("ex", "size"), z=("z", "mean"), strength=("ex", "mean"), exret=("exr", "mean"))
        summ.append(dict(h=h, L=L, n=n, slope=s, t=t, q1_minus_q5=q.strength.iloc[0] - q.strength.iloc[-1]))
        if (h, L) in [(7, 7), (30, 30), (1, 1)]: qtabs[f"quint h{h} L{L}"] = q.round(4)
    out["past-vs-forward slope (units of usual move)"] = pd.DataFrame(summ).round(4)
    out.update(qtabs)

    # volatility level vs forward 7d
    rows = []
    for coin in bars:
        d7, s7 = coin_stats(coin, 7)
        alld = np.concatenate([np.diff(np.log(df["close"].values)) for df in bars[coin].values()])
        sd = alld.std()
        for w, df in bars[coin].items():
            c = df["close"].values; lr = np.diff(np.log(c))
            for p in range(0, len(c) - 7, 7):
                if p < 14: continue
                rv = lr[p - 14:p].std() / sd
                fwd = c[p + 7] / c[p] - 1
                past7 = c[p] / c[p - 7] - 1
                rows.append(dict(rv=rv, ex=(fwd - d7) / s7, absf=abs(fwd - d7) / s7, sgnpast=np.sign(past7)))
    v = pd.DataFrame(rows); v["q"] = pd.qcut(v.rv, 5, labels=False)
    out["vol quintile -> fwd 7d strength"] = v.groupby("q").agg(n=("ex", "size"), rv=("rv", "mean"), strength=("ex", "mean"), absmove=("absf", "mean")).round(4)
    out["vol slope t on fwd 7d"] = round(ols_t(v.rv, v.ex)[1], 3)

    # weekday / daily
    wd = []
    for coin in bars:
        for w, df in bars[coin].items():
            ts = pd.to_datetime(df["timestamp"]); c = df["close"].values
            r = c[1:] / c[:-1] - 1
            wd.append(pd.DataFrame(dict(wd=ts.dt.dayofweek.values[1:], r=r)))
    wd = pd.concat(wd)
    g = wd.groupby("wd").r.agg(["size", "mean", "std"]); g["t"] = g["mean"] / (g["std"] / np.sqrt(g["size"]))
    out["weekday daily returns"] = g.round(5)

    # regime at grid bar -> fwd 30 excess
    rows = []
    for coin in bars:
        d30, s30 = coin_stats(coin, 30)
        for w, df in bars[coin].items():
            c = df["close"].values; reg = df["regime"].values
            for p in range(0, len(c) - 30, 30):
                rows.append(dict(reg=reg[p], ex=(c[p + 30] / c[p] - 1 - d30)))
    rr = pd.DataFrame(rows)
    out["regime -> fwd30 excess"] = rr.groupby("reg").ex.agg(["size", "mean", "std"]).assign(t=lambda x: x["mean"] / (x["std"] / np.sqrt(x["size"]))).round(4)

    # positions gain by side, trades by side
    pg = []
    for coin in bars:
        for w, df in bars[coin].items():
            c = df["close"].values; a = df["postRebalance_current_allocation"].fillna(0).values
            r = np.append(c[1:] / c[:-1] - 1, np.nan)
            pg.append(pd.DataFrame(dict(a=a, g=a * r, r=r, fc=df["forecast"].values)))
    pg = pd.concat(pg).dropna(); pg = pg[pg.a != 0]
    pg["side"] = np.sign(pg.a)
    out["position bar gain by side"] = pg.groupby("side").agg(n=("g", "size"), gain=("g", "mean"), coin_r=("r", "mean")).round(5)
    tr = pd.concat([t for coin in data["trades"] for t in data["trades"][coin].values() if len(t)])
    out["trades by side"] = tr.groupby("side").agg(n=("net_profit_loss_percent", "size"), mean_net=("net_profit_loss_percent", "mean"), median=("net_profit_loss_percent", "median"), win=("net_profit_loss_percent", lambda x: (x > 0).mean())).round(3)
    return out
