def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        allret = []
        for w, b in wins.items():
            c = b["close"].astype(float).values
            allret.append(c[1:] / c[:-1] - 1)
        drift = np.nanmean(np.concatenate(allret))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float).values
            o = b["open"].astype(float).values
            h = b["high"].astype(float).values
            l = b["low"].astype(float).values
            n = len(c)
            r = np.full(n, np.nan); r[1:] = c[1:] / c[:-1] - 1
            f1 = np.full(n, np.nan); f1[:-1] = c[1:] / c[:-1] - 1
            f3 = np.full(n, np.nan); f3[:-3] = c[3:] / c[:-3] - 1
            rs = pd.Series(r)
            vol30 = rs.rolling(30, min_periods=20).std().values
            tr60 = np.full(n, np.nan); tr60[60:] = c[60:] / c[:-60] - 1
            ret5 = np.full(n, np.nan); ret5[5:] = c[5:] / c[:-5] - 1
            # down run length before today
            run = np.zeros(n, int); dep = np.full(n, np.nan)
            for t in range(2, n):
                k = 0; j = t - 1
                while j >= 1 and r[j] < 0:
                    k += 1; j -= 1
                run[t] = k
                if k > 0: dep[t] = c[t-1] / c[t-1-k] - 1
            # up run before today
            urun = np.zeros(n, int)
            for t in range(2, n):
                k = 0; j = t - 1
                while j >= 1 and r[j] > 0:
                    k += 1; j -= 1
                urun[t] = k
            rng = (h - l) / c
            clpos = np.where(h > l, (c - l) / (h - l), np.nan)
            ts = pd.to_datetime(b["timestamp"])
            for t in range(n):
                rows.append(dict(coin=coin, w=w, day=ts[t].floor("D"), wd=ts[t].dayofweek,
                    r=r[t], f1=f1[t], f3=f3[t], drift=drift, vol=vol30[t], tr60=tr60[t],
                    ret5=ret5[t], run=run[t], dep=dep[t], urun=urun[t], rng=rng[t], clpos=clpos[t],
                    alloc=b["postRebalance_current_allocation"].iloc[t]))
    d = pd.DataFrame(rows)
    d["u1"] = d["f1"] - d["drift"]
    d["z"] = d["r"] / d["vol"]
    def ct(sub, col, sign=-1):
        s = sub.dropna(subset=[col])
        x = sign * s[col]
        dev = (x - x.mean()).groupby(s["day"]).sum()
        G = len(dev)
        if G < 5: return pd.Series(dict(mean=np.nan, t=np.nan, n=len(s), days=G))
        se = np.sqrt((dev**2).sum() * G / (G - 1)) / len(s)
        return pd.Series(dict(mean=x.mean(), t=x.mean() / se, n=len(s), days=G))
    case = d[(d.r > 0) & (d.run >= 1)].copy()
    out = {}
    case["runb"] = case.run.clip(upper=5)
    out["short move by run length"] = case.groupby("runb").apply(lambda s: ct(s, "u1"))
    case["upq"] = pd.qcut(case.z, 4, labels=False, duplicates="drop")
    out["by up-day size (z quartile), run>=2"] = case[case.run >= 2].groupby("upq").apply(lambda s: ct(s, "u1"))
    out["by up-day size, run==1"] = case[case.run == 1].groupby("upq").apply(lambda s: ct(s, "u1"))
    case["depq"] = pd.qcut(case.dep / case.vol, 4, labels=False, duplicates="drop")
    out["by run depth/vol quartile"] = case.groupby("depq").apply(lambda s: ct(s, "u1"))
    case["trend"] = np.where(case.tr60 > 0.1, "rising", np.where(case.tr60 < -0.1, "falling", np.where(case.tr60.notna(), "choppy", "na")))
    case["agit"] = np.where(case.vol > d.groupby("coin").vol.transform("median").loc[case.index], "agit", "calm")
    out["run>=2 by trend x agit"] = case[case.run >= 2].groupby(["trend", "agit"]).apply(lambda s: ct(s, "u1"))
    out["by close position in range, run>=2"] = case[case.run >= 2].assign(q=pd.cut(case.clpos, [0, .33, .67, 1.01])).groupby("q").apply(lambda s: ct(s, "u1"))
    out["by weekday, run>=2"] = case[case.run >= 2].groupby("wd").apply(lambda s: ct(s, "u1"))
    case["u3"] = case.f3 - 3 * case.drift
    out["3-day after break by run"] = case.groupby("runb").apply(lambda s: ct(s, "u3"))
    # mirror: down day ending up run, next day long direction
    mir = d[(d.r < 0) & (d.urun >= 1)].copy(); mir["runb"] = mir.urun.clip(upper=5)
    out["mirror: down day after up-run, short move"] = mir.groupby("runb").apply(lambda s: ct(s, "u1"))
    # all bars: next-day by z quintile of today
    d["zq"] = pd.qcut(d.z, 5, labels=False)
    out["all bars next-day short move by today z quintile"] = d.groupby("zq").apply(lambda s: ct(s, "u1"))
    # continuation: down day after down run (run>=1, r<0) short move
    cont = d[(d.r < 0)].copy(); cont["runb"] = (cont.run + 1).clip(upper=5)
    out["down day continuing run (run incl today), short move"] = cont.groupby("runb").apply(lambda s: ct(s, "u1"))
    # book days
    dd = []
    for coin, wins in data["days"].items():
        for w, x in wins.items():
            dd.append(x.assign(coin=coin, w=w))
    dd = pd.concat(dd)
    bk = dd.groupby(["w", "day"])[["book_return", "coin_return"]].mean().dropna()
    q = bk.book_return.quantile([0.02, 0.98])
    out["book extreme days"] = pd.DataFrame({
        "worst2%": bk[bk.book_return <= q.iloc[0]].mean(), "best2%": bk[bk.book_return >= q.iloc[1]].mean(),
        "all": bk.mean()})
    out["book by window"] = bk.groupby(level=0).book_return.agg(["mean", "std", "count"])
    return out
