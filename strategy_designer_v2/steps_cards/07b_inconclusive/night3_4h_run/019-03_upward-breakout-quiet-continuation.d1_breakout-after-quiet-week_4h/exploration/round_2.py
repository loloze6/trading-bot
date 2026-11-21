def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}; usual = {}
    for coin, ws in bars.items():
        rr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 18, 18)
            rr += list(c[idx + 18] / c[idx] - 1)
        drift[coin] = np.mean(rr); usual[coin] = np.std(rr)
    allbrk = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; h = b["high"].values; l = b["low"].values
            f = b["forecast"].fillna(0).values
            rng_s = pd.Series((h - l) / c)
            q = (rng_s.rolling(42).mean() / rng_s.rolling(360, min_periods=90).mean()).values
            hi12 = pd.Series(h).shift(1).rolling(12).max().values
            lo12 = pd.Series(l).shift(1).rolling(12).min().values
            narrow = ((hi12 - lo12) / c) / (rng_s.rolling(180, min_periods=60).mean().values * 12)
            brk = (c - hi12) / c
            n = len(c)
            # every breakout bar (close > prior 12-bar high), first per 18-bar cell
            taken = set()
            for t in range(13, n - 18):
                if c[t] > hi12[t] and np.isfinite(q[t]):
                    cell = t // 18
                    if cell in taken: continue
                    taken.add(cell)
                    allbrk.append(dict(coin=coin, year=pd.Timestamp(b["timestamp"].iloc[t]).year,
                                       q=q[t], narrow=narrow[t], brk=brk[t],
                                       r18=c[t+18]/c[t]-1-drift[coin], s=(c[t+18]/c[t]-1-drift[coin])/usual[coin]))
    d = pd.DataFrame(allbrk)
    def summ(g):
        x = g["r18"].dropna()
        return pd.Series(dict(n=len(x), mean=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan, strength=g["s"].mean()))
    out = {}
    out["all_breakouts"] = summ(d)
    d["qq"] = pd.qcut(d["q"], 4, labels=False)
    out["by_q"] = d.groupby("qq").apply(summ)
    out["q_bounds"] = pd.Series(np.quantile(d["q"], [0.25, 0.5, 0.75]))
    out["q_coin_lowq"] = d[d.qq == 0].groupby("coin").apply(summ)
    out["q_coin_highq"] = d[d.qq == 3].groupby("coin").apply(summ)
    d["half"] = np.where(d.year <= 2021, "early", "late")
    out["q_by_half"] = d.groupby(["half", "qq"]).apply(summ)
    sp = {}
    for v in ("q", "narrow", "brk"):
        x = d[[v, "s"]].dropna()
        rho, p = stats.spearmanr(x[v], x["s"])
        sp[v] = pd.Series(dict(rho=rho, p=p, n=len(x)))
    out["spearman_vs_strength"] = pd.DataFrame(sp)
    # quiet ratio rank within coin, slope
    d["qr"] = d.groupby("coin")["q"].rank(pct=True)
    x = d[["qr", "r18"]].dropna()
    lr = stats.linregress(x["qr"], x["r18"])
    out["slope_r18_on_qrank"] = pd.Series(dict(slope=lr.slope, t=lr.slope/lr.stderr, n=len(x)))
    return out
