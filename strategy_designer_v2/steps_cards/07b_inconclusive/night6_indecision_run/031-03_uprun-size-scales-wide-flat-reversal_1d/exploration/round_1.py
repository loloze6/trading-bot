def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}; usual = {}
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
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            fc = df["forecast"].values
            for t in range(len(c)):
                if not (width[t] >= 1.5) or np.isnan(r5[t]): continue
                flat = body[t] <= 0.1
                for h in H:
                    if t + h >= len(c): continue
                    rows.append(dict(coin=coin, win=w, t=t, h=h, cell=t // h, flat=flat,
                                     r5=r5[t], year=yr[t], day=day[t], fc=fc[t],
                                     fwd=c[t + h] / c[t] - 1,
                                     unus=c[t + h] / c[t] - 1 - drift[(coin, h)],
                                     usual=usual[(coin, h)], width=width[t], body=body[t]))
    d = pd.DataFrame(rows)
    d = d.sort_values("t").drop_duplicates(["coin", "win", "h", "cell", "flat"])
    d["side"] = np.where(d.r5 > 0, "up", "down")
    # signed in reversal direction
    d["rev"] = np.where(d.r5 > 0, -d.unus, d.unus)
    d["revstr"] = d.rev / d.usual

    def summ(g):
        s = g.groupby("day")["rev"].sum() - g["rev"].mean() * g.groupby("day").size()
        G = len(s); se = np.sqrt((s ** 2).sum() * G / max(G - 1, 1)) / len(g)
        return pd.Series(dict(n=len(g), days=G, mean_rev=g.rev.mean(), t=g.rev.mean() / se if se > 0 else np.nan,
                              strength=g.revstr.mean(), hit=(g.rev > 0).mean()))
    out = {}
    out["by flat/side/h"] = d.groupby(["flat", "side", "h"]).apply(summ)
    f5 = d[(d.h == 5) & d.flat]
    f5 = f5.assign(q=pd.qcut(f5.r5, 5, labels=False, duplicates="drop"))
    out["flat h5 by r5 quintile"] = f5.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series(dict(r5=g.r5.mean()))]))
    out["flat h5 by coin side"] = f5.groupby(["coin", "side"]).apply(summ)
    out["flat h5 by year side"] = f5.groupby(["year", "side"]).apply(summ)
    w5 = d[(d.h == 5) & ~d.flat]
    w5 = w5.assign(q=pd.qcut(w5.r5, 5, labels=False, duplicates="drop"))
    out["nonflat wide h5 by r5 quintile"] = w5.groupby("q").apply(lambda g: pd.concat([summ(g), pd.Series(dict(r5=g.r5.mean()))]))
    up5 = f5[f5.r5 > 0]
    out["flat up h5 corr r5 vs rev"] = float(np.corrcoef(up5.r5, up5.rev)[0, 1]) if len(up5) > 2 else np.nan
    return out
