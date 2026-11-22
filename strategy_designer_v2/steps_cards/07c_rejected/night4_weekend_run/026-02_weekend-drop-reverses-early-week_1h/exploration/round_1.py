def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    H = [24, 48, 72, 120]
    for coin, wins in bars.items():
        grid = {h: [] for h in H}
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"], utc=True)
            c = df["close"].values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                grid[h].extend(list(c[idx + h] / c[idx] - 1))
            pos = {t: i for i, t in enumerate(ts)}
            for i in range(n):
                t = ts.iloc[i]
                # signal bar: Sunday 23:00 (close Mon 00:00); also mid-week control: Wednesday 23:00 (close Thu 00:00)
                if t.hour != 23 or t.dayofweek not in (6, 2):
                    continue
                t0 = t - pd.Timedelta(hours=48)
                j = pos.get(t0)
                if j is None:
                    continue
                past = c[i] / c[j] - 1
                r = {"coin": coin, "win": w, "year": (t + pd.Timedelta(hours=1)).year,
                     "kind": "weekend" if t.dayofweek == 6 else "midweek", "past": past}
                for h in H:
                    k = pos.get(t + pd.Timedelta(hours=h))
                    r["f%d" % h] = c[k] / c[i] - 1 if k is not None else np.nan
                rows.append(r)
        for h in H:
            g = np.array(grid[h])
            drift[(coin, h)] = np.nanmean(g)
            usual[(coin, h)] = np.nanstd(g)
    d = pd.DataFrame(rows)
    for h in H:
        d["u%d" % h] = d["f%d" % h] - d["coin"].map(lambda x: drift[(x, h)])
    out = {}
    def summ(g):
        res = {}
        for h in H:
            x = g["u%d" % h].dropna()
            res["mean_u%d" % h] = x.mean()
            res["t_u%d" % h] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        res["n"] = len(g)
        return pd.Series(res)
    d["side"] = np.where(d["past"] < 0, "fall", "rise")
    out["by_kind_side"] = d.groupby(["kind", "side"]).apply(summ)
    w = d[d.kind == "weekend"].copy()
    w["q"] = w.groupby("coin")["past"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["weekend_by_quintile"] = w.groupby("q").apply(summ)
    out["weekend_fall_by_coin"] = w[w.side == "fall"].groupby("coin").apply(summ)
    out["weekend_all_by_coin"] = w.groupby("coin").apply(summ)
    out["weekend_fall_by_year"] = w[w.side == "fall"].groupby("year").apply(summ)
    cr = {}
    for kind in ["weekend", "midweek"]:
        g = d[d.kind == kind]
        for h in H:
            x = g[["past", "u%d" % h]].dropna()
            sl = stats.linregress(x["past"], x["u%d" % h])
            cr["%s_h%d" % (kind, h)] = pd.Series({"slope": sl.slope, "t": sl.slope / sl.stderr, "corr": sl.rvalue, "n": len(x)})
    out["slope_future_on_past"] = pd.DataFrame(cr).T
    out["usual48"] = pd.Series({k[0]: v for k, v in usual.items() if k[1] == 48})
    return out
