def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [5, 10, 15, 20]
    L = [3, 7, 14, 30]
    coinmean = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].astype(float).values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                allr[h].extend(list(c[idx + h] / c[idx] - 1))
        coinmean[coin] = {h: np.mean(allr[h]) for h in H}
    def ct(s, days):
        s = pd.Series(s.values); days = pd.Series(days.values)
        dev = (s - s.mean()).groupby(days).sum()
        se = np.sqrt((dev ** 2).sum()) / len(s)
        return s.mean() / se if se > 0 else np.nan
    res = []
    rows_all = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            dr = c.pct_change()
            sd = dr.rolling(30, min_periods=20).std()
            inp = (df["regime"] == "unknown")
            for h in H:
                for i in range(0, len(df) - h, h):
                    if not inp.iloc[i]: continue
                    rec = dict(coin=coin, win=w, h=h, day=str(df["timestamp"].iloc[i])[:10],
                               x=c.iloc[i + h] / c.iloc[i] - 1 - coinmean[coin][h])
                    for l in L:
                        rec[f"s{l}"] = (c.iloc[i] / c.iloc[i - l] - 1) / (sd.iloc[i] * np.sqrt(l)) if i >= l else np.nan
                    rows_all.append(rec)
    d = pd.DataFrame(rows_all)
    for h in H:
        for l in L:
            g = d[(d.h == h)].dropna(subset=[f"s{l}"])
            pos = g[g[f"s{l}"] > 0]
            top = pos[pos[f"s{l}"] > pos[f"s{l}"].median()] if len(pos) > 4 else pos
            res.append(dict(h=h, lookback=l, n_all=len(g),
                            rho_all=stats.spearmanr(g[f"s{l}"], g.x)[0],
                            n_pos=len(pos), x_pos=pos.x.mean(), t_pos=ct(pos.x, pos.day),
                            rho_pos=stats.spearmanr(pos[f"s{l}"], pos.x)[0] if len(pos) > 4 else np.nan,
                            x_top_half_pos=top.x.mean(), t_top=ct(top.x, top.day),
                            neg_n=(g[f"s{l}"] < 0).sum(), x_neg=g[g[f"s{l}"] < 0].x.mean(),
                            t_neg=ct(g[g[f"s{l}"] < 0].x, g[g[f"s{l}"] < 0].day)))
    out["profile grid: lookback x horizon"] = pd.DataFrame(res).round(4)
    g = d[d.h == 10].dropna(subset=["s7"])
    pos = g[g.s7 > 0]
    out["h10 s7>0 by coin"] = pos.groupby("coin").x.agg(["count", "mean"]).round(4)
    out["h10 s7>0 by window"] = pos.groupby("win").x.agg(["count", "mean"]).round(4)
    return out
