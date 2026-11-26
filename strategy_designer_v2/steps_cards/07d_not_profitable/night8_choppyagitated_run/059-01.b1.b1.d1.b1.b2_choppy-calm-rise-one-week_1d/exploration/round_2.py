def explore(data):
    import numpy as np, pandas as pd
    out = {}
    H = 7
    drift = {}
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            allr += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(allr)
    rows = []; prow = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; n = len(cl)
            fc = b["forecast"].fillna(0).values
            reg = b["regime"].astype(str).values
            al = b["postRebalance_current_allocation"].fillna(0).values
            hi7 = pd.Series(cl).rolling(7, min_periods=1).max().values
            offhi = cl / hi7 - 1
            r30 = pd.Series(cl).pct_change(30).values
            r7 = pd.Series(cl).pct_change(7).values
            for i in range(n - 1):
                prow.append(dict(coin=c, w=w, al=al[i], g=al[i] * (cl[i + 1] / cl[i] - 1),
                                 offhi=offhi[i], r30=r30[i], fc=fc[i]))
            for i in range(0, n - H, H):
                rows.append(dict(coin=c, w=w, fc=fc[i], reg=reg[i], ex=cl[i + H] / cl[i] - 1 - drift[c],
                                 fwd=cl[i + H] / cl[i] - 1, offhi=offhi[i], r30=r30[i], r7=r7[i],
                                 ex14=(cl[i + 14] / cl[i] - 1 - 2 * drift[c]) if i + 14 < n else np.nan))
    g = pd.DataFrame(rows)
    def summ(x):
        x = x.dropna(subset=["ex"])
        return pd.Series(dict(n=len(x), mean_ex=x.ex.mean(),
                              t=x.ex.mean() / (x.ex.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              ex14=x.ex14.mean()))
    g["athigh"] = g.offhi > -0.02
    g["r30pos"] = g.r30 > 0
    s = g[g.fc > 0]
    out["signal: at 7d high (within 2%) vs not"] = s.groupby("athigh").apply(summ)
    out["signal: 30d return >0 vs not"] = s.groupby("r30pos").apply(summ)
    out["signal: athigh x r30pos"] = s.groupby(["athigh", "r30pos"]).apply(summ)
    # condition alone, no signal
    ns = g[g.fc == 0]
    out["no signal, all regimes: athigh"] = ns.groupby("athigh").apply(summ)
    out["no signal, in profile: athigh"] = ns[ns.reg == "unknown"].groupby("athigh").apply(summ)
    out["no signal, rising week (r7>0) all regimes: athigh"] = ns[ns.r7 > 0].groupby("athigh").apply(summ)
    out["no signal, all regimes: r30pos"] = ns.groupby("r30pos").apply(summ)
    # forecast terciles among at-high signals
    sh = s[s.athigh].copy()
    if len(sh) > 9:
        sh["fq"] = pd.qcut(sh.fc.rank(method="first"), 3, labels=["lo", "mid", "hi"])
        out["at-high signals by forecast tercile"] = sh.groupby("fq").apply(summ)
    # book bar gains by state of the position's bar
    P = pd.DataFrame(prow)
    P = P[P.al != 0]
    P["athigh"] = P.offhi > -0.02
    out["held bar gains by at-high state"] = P.groupby("athigh").agg(n=("g", "size"), mean=("g", "mean"),
                                                                    total=("g", "sum"))
    P["r30pos"] = P.r30 > 0
    out["held bar gains by r30pos"] = P.groupby("r30pos").agg(n=("g", "size"), mean=("g", "mean"), total=("g", "sum"))
    out["held bar gains by coin"] = P.groupby("coin").agg(n=("g", "size"), mean=("g", "mean"), total=("g", "sum"))
    # deepest fall days: book
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd.append(pd.DataFrame(dict(w=w, day=d["day"].values, br=d["book_return"].values)))
    D = pd.concat(dd)
    B = D.groupby(["w", "day"]).br.mean().dropna().reset_index()
    B["wn"] = B.w.str[1:].astype(int); B = B.sort_values(["wn", "day"])
    v = (1 + B.br).cumprod().values; pk = np.maximum.accumulate(v)
    B["dd"] = v / pk - 1
    k = int(np.argmin(B.dd.values)); j = int(np.argmax(v[:k + 1]))
    out["deepest fall: window of peak, trough, days"] = f"{B.w.iloc[j]} -> {B.w.iloc[k]}, {k - j} days, {B.dd.iloc[k]:.3f}"
    worst = B.nsmallest(10, "br")
    out["10 worst book days by window"] = worst.groupby("w").br.agg(["size", "sum"])
    return out
