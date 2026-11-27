def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values.astype(float)
            o = b["open"].values.astype(float)
            h = b["high"].values.astype(float); l = b["low"].values.astype(float)
            n = len(c)
            r1 = np.full(n, np.nan); r1[1:] = c[1:]/c[:-1]-1
            # run of down closes before an up close
            run = np.zeros(n); dn = 0
            for i in range(1, n):
                if r1[i] < 0:
                    dn += 1
                elif r1[i] > 0:
                    run[i] = dn; dn = 0
                else:
                    dn = 0
            # prior up-run before a down close (mirror)
            urun = np.zeros(n); up = 0
            for i in range(1, n):
                if r1[i] > 0: up += 1
                elif r1[i] < 0: urun[i] = up; up = 0
                else: up = 0
            sd20 = pd.Series(r1).rolling(20, min_periods=10).std().shift(1).values
            r5 = np.full(n, np.nan); r5[5:] = c[5:]/c[:-5]-1
            r20 = np.full(n, np.nan); r20[20:] = c[20:]/c[:-20]-1
            f1 = np.full(n, np.nan); f1[:-1] = c[1:]/c[:-1]-1
            f3 = np.full(n, np.nan); f3[:-3] = c[3:]/c[:-3]-1
            f23 = np.full(n, np.nan); f23[:-3] = c[3:]/c[1:-2]-1
            rng = (h-l)/c
            clpos = np.where(h > l, (c-l)/(h-l), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            alloc = b["postRebalance_current_allocation"].values
            df = pd.DataFrame(dict(coin=coin, w=w, pos=np.arange(n), r1=r1, run=run, urun=urun,
                                   z=r1/sd20, r5=r5, r20=r20, f1=f1, f3=f3, f23=f23, rng=rng,
                                   clpos=clpos, wd=ts.dt.weekday.values, alloc=alloc,
                                   day=ts.dt.floor("D").values, yr=ts.dt.year.values, sd20=sd20))
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    drift3 = D[D.pos % 3 == 0].groupby("coin")["f3"].mean()
    D["ex3"] = D["f3"] - D["coin"].map(drift3)
    D["exz"] = D["ex3"] / D["sd20"]
    G = D[(D.pos % 3 == 0) & D.ex3.notna()].copy()

    def summ(g, col="ex3"):
        x = g[col].dropna()
        dd = g.loc[x.index].groupby("day")[col].sum() - 0  # cluster by day
        m = x.mean()
        se = np.sqrt(((g.loc[x.index].assign(d=x - m).groupby("day")["d"].sum())**2).sum())/len(x)
        return pd.Series(dict(n=len(x), days=g.loc[x.index, "day"].nunique(), mean=m, t=m/se if se > 0 else np.nan))

    out = {}
    G["runc"] = G["run"].clip(upper=5)
    out["fwd3 ex by down-run broken (0=not a break)"] = G.groupby("runc").apply(summ).round(4)
    G["urunc"] = G["urun"].clip(upper=5)
    out["fwd3 ex by up-run broken by down day"] = G.groupby("urunc").apply(summ).round(4)
    G["zq"] = pd.qcut(G["z"], 10, labels=False, duplicates="drop")
    out["fwd3 ex by z of today's move decile"] = G.groupby("zq").apply(summ).round(4)
    G["r5q"] = pd.qcut(G["r5"], 5, labels=False, duplicates="drop")
    out["fwd3 ex by 5d return quintile"] = G.groupby("r5q").apply(summ).round(4)
    G["r20q"] = pd.qcut(G["r20"], 5, labels=False, duplicates="drop")
    out["fwd3 ex by 20d return quintile"] = G.groupby("r20q").apply(summ).round(4)
    G["vq"] = pd.qcut(G["sd20"], 5, labels=False, duplicates="drop")
    out["fwd3 ex by vol20 quintile"] = G.groupby("vq").apply(summ).round(4)
    G["cq"] = pd.qcut(G["clpos"], 5, labels=False, duplicates="drop")
    out["fwd3 ex by close position in range quintile"] = G.groupby("cq").apply(summ).round(4)
    D1 = D[D.f1.notna()].copy()
    D1["ex1"] = D1["f1"] - D1["coin"].map(D1.groupby("coin")["f1"].mean())
    out["next-day ex by weekday of signal bar"] = D1.groupby("wd").apply(lambda g: summ(g, "ex1")).round(4)
    br = G[G.run >= 1]
    out["breaks: fwd3 ex by year"] = br.groupby("yr").apply(summ).round(4)
    out["breaks: fwd3 ex by window"] = br.groupby("w").apply(summ).round(4)
    out["breaks: fwd3 ex by coin"] = br.groupby("coin").apply(summ).round(4)
    br2 = br.copy(); br2["r20s"] = np.sign(br2["r20"])
    out["breaks: by 20d trend sign x runc"] = br2.groupby(["r20s", "runc"]).apply(summ).round(4)
    # book daily returns
    dl = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dl.append(d.assign(coin=coin, w=w))
    DD = pd.concat(dl)
    bk = DD.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book daily mean/sd/sharpe"] = pd.Series(dict(mean=bk.book_return.mean(), sd=bk.book_return.std(),
        sharpe=bk.book_return.mean()/bk.book_return.std()*np.sqrt(365), corr_coin=bk.book_return.corr(bk.coin_return)))
    return out
