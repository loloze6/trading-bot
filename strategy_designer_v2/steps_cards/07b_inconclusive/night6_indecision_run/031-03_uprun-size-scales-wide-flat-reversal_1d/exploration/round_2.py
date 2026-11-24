def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [3, 5, 10]
    drift = {}; usual = {}
    rows = []
    for coin, wins in bars.items():
        for h in H:
            rr = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rr += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rr); usual[(coin, h)] = np.std(rr, ddof=1)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            o, hi, lo, c = [df[k].values for k in ["open", "high", "low", "close"]]
            rng = hi - lo
            mr = pd.Series(rng).rolling(20, min_periods=20).mean().values
            width = rng / mr
            body = np.abs(c - o) / np.where(rng > 0, rng, np.nan)
            r5 = np.full(len(c), np.nan); r5[5:] = c[5:] / c[:-5] - 1
            sd = pd.Series(r5).rolling(60, min_periods=20).std().values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            for h in H:
                for t in range(0, len(c) - h, h):
                    if np.isnan(r5[t]) or np.isnan(width[t]) or np.isnan(sd[t]) or r5[t] <= 0: continue
                    kind = "wideflat" if (width[t] >= 1.5 and body[t] <= 0.1) else ("wide" if width[t] >= 1.5 else "other")
                    rows.append(dict(coin=coin, h=h, kind=kind, r5=r5[t], z=r5[t] / sd[t], year=yr[t], day=day[t],
                                     cont=c[t + h] / c[t] - 1 - drift[(coin, h)], usual=usual[(coin, h)]))
    d = pd.DataFrame(rows)
    def summ(g):
        s = g.groupby("day")["cont"].sum() - g["cont"].mean() * g.groupby("day").size()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean_cont=g.cont.mean(), t=g.cont.mean() / se if se > 0 else np.nan,
                              strength=(g.cont / g.usual).mean(), hit=(g.cont > 0).mean()))
    d["zq"] = d.groupby("h")["z"].transform(lambda s: pd.qcut(s, 4, labels=False, duplicates="drop"))
    out = {}
    out["upruns: kind x z-quartile, h5"] = d[d.h == 5].groupby(["kind", "zq"]).apply(summ)
    out["upruns: kind, by h"] = d.groupby(["kind", "h"]).apply(summ)
    big = d[(d.zq == 3) & (d.h == 5)]
    out["top z quartile h5 by year x kind(wide incl flat)"] = big.assign(k=np.where(big.kind == "other", "other", "wide")).groupby(["year", "k"]).apply(summ)
    out["wideflat h5 excl 2021"] = summ(d[(d.h == 5) & (d.kind == "wideflat") & (d.year != 2021)])
    out["wide(any) h5 top z excl 2021"] = summ(d[(d.h == 5) & (d.kind != "other") & (d.zq == 3) & (d.year != 2021)])
    out["other h5 top z excl 2021"] = summ(d[(d.h == 5) & (d.kind == "other") & (d.zq == 3) & (d.year != 2021)])
    return out
