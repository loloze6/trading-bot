def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        hs = [6, 12, 24, 48, 72]
        allf = {h: [] for h in hs}
        prep = {}
        for w, b in ws.items():
            c = b["close"].astype(float).reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]).reset_index(drop=True)
            r24 = c / c.shift(24) - 1
            ratio = r24 / r24.abs().rolling(720, min_periods=120).mean()
            r168 = c / c.shift(168) - 1
            fw = {h: c.shift(-h) / c - 1 for h in hs}
            for h in hs:
                allf[h] += list(fw[h].iloc[np.arange(0, len(c), h)].dropna())
            prep[w] = (c, ts, ratio, r168, fw)
        drift = {h: np.mean(allf[h]) for h in hs}; sd = {h: np.std(allf[h]) for h in hs}
        for w, (c, ts, ratio, r168, fw) in prep.items():
            for h in hs:
                g = np.arange(0, len(c), h)
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "year": ts.iloc[g].dt.year.values,
                    "hour": ts.iloc[g].dt.hour.values, "ratio": ratio.iloc[g].values, "wk": r168.iloc[g].values,
                    "ex": (fw[h].iloc[g] - drift[h]).values, "tot": fw[h].iloc[g].values,
                    "st": ((fw[h].iloc[g] - drift[h]) / sd[h]).values}))
    A = pd.concat(rows).dropna()
    def summ(df, key):
        g = df.groupby(key, observed=True)
        r = g.agg(n=("ex", "size"), mean_ex=("ex", "mean"), mean_tot=("tot", "mean"), strength=("st", "mean"))
        r["t"] = g["ex"].apply(lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan)
        return r.round(4)
    A["rb"] = pd.cut(A["ratio"], [-np.inf, -3, -2, -1.3, -0.7, 0.7, 1.3, 2, 3, np.inf])
    out["by horizon x ratio bin"] = summ(A, ["h", "rb"])
    D = A[(A.h == 24) & (A.ratio <= -1.3)]
    out["down surge 24h by coin"] = summ(D, "coin")
    out["down surge 24h by year"] = summ(D, "year")
    D2 = D.copy(); D2["wkpos"] = D2["wk"] > 0
    out["down surge 24h by week sign"] = summ(D2, "wkpos")
    wn = D["w"].str[1:].astype(int)
    D3 = D.copy(); D3["wg"] = pd.cut(wn, [0, 6, 12, 18, 24])
    out["down surge 24h by window group"] = summ(D3, "wg")
    # grading within down surges: correlation of -ratio with ex
    from scipy import stats
    rr = stats.spearmanr(-D["ratio"], D["ex"])
    out["down surge 24h spearman(-ratio, ex)"] = f"rho {rr.correlation:.3f}, p {rr.pvalue:.4f}, n {len(D)}"
    # Saturday and hour 21-22 robustness
    H = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); dd = pd.to_datetime(d["day"])
            H.append(pd.DataFrame({"coin": coin, "wd": dd.dt.weekday, "year": dd.dt.year, "r": d["coin_return"]}))
    H = pd.concat(H).dropna()
    S = H[H.wd == 5]
    g = S.groupby("coin")["r"]
    out["saturday by coin"] = pd.DataFrame({"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size())), "n": g.size()}).round(4)
    g = S.groupby("year")["r"]
    out["saturday by year"] = pd.DataFrame({"mean": g.mean(), "t": g.mean() / (g.std() / np.sqrt(g.size())), "n": g.size()}).round(4)
    return out
