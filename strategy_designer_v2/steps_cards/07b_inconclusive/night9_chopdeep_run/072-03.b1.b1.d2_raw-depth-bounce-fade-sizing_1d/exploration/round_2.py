def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [5, 10]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            r = []
            for w, b in ws.items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = (np.mean(r), np.std(r)) if r else (np.nan, np.nan)
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            r1 = pd.Series(cl).pct_change()
            ret1 = r1.values
            hh = b["high"].rolling(20, min_periods=20).max().values
            sd = r1.rolling(20, min_periods=20).std().values
            depth = (cl - hh) / hh / sd
            tr60 = pd.Series(cl).pct_change(60).values * 100
            choppy = (tr60 >= -10) & (tr60 <= 10)
            v30 = r1.rolling(30).std()
            vmed = v30.rolling(365, min_periods=60).median().values
            v30 = v30.values
            for t in range(n):
                if not choppy[t] or np.isnan(depth[t]) or not (ret1[t] > 0) or depth[t] >= 0:
                    continue
                for h in H:
                    if t + h >= n:
                        continue
                    rows.append(dict(coin=c, w=w, t=t, h=h, cell=t // h, depth=depth[t],
                                     agit=("na" if np.isnan(vmed[t]) else ("agit" if v30[t] > vmed[t] else "calm")),
                                     tr=("neg" if tr60[t] < 0 else "pos"),
                                     day=str(b["timestamp"].iloc[t])[:10], yr=str(b["timestamp"].iloc[t])[:4],
                                     un=-(cl[t + h] / cl[t] - 1 - drift[(c, h)][0]),
                                     strg=-(cl[t + h] / cl[t] - 1 - drift[(c, h)][0]) / drift[(c, h)][1]))
    df = pd.DataFrame(rows)
    g = df.sort_values("t").groupby(["coin", "w", "h", "cell"]).head(1).copy()

    def summ(x):
        m = x.un.mean()
        d = x.groupby("day")["un"].apply(lambda s: (s - m).sum())
        se = np.sqrt((d ** 2).sum()) / len(x) if len(x) > 1 else np.nan
        return pd.Series(dict(n=len(x), days=x.day.nunique(), mean_un=m, med_un=x.un.median(),
                              t=m / se if se else np.nan, strength=x.strg.mean(),
                              share_pos=(x.un > 0).mean()))
    g["q"] = g.groupby("h")["depth"].transform(lambda s: pd.qcut(s, 4, labels=["deep", "q2", "q3", "shallow"]))
    out = {}
    out["q_depth_bounds"] = g[g.h == 10].groupby("q")["depth"].agg(["min", "max", "median"])
    g10 = g[g.h == 10]
    out["h10_q_noDOGE"] = g10[g10.coin != "DOGEUSD"].groupby("q").apply(summ)
    out["h10_q_agit"] = g10.groupby(["agit", "q"]).apply(summ)
    out["h10_q_trend"] = g10.groupby(["tr", "q"]).apply(summ)
    out["h10_deep_by_year"] = g10[g10.q == "deep"].groupby("yr").apply(summ)
    out["h10_shallow_by_year"] = g10[g10.q == "shallow"].groupby("yr").apply(summ)
    out["h10_deep_by_coin"] = g10[g10.q == "deep"].groupby("coin").apply(summ)
    out["h5_deep_by_year"] = g[(g.h == 5) & (g.q == "deep")].groupby("yr").apply(summ)
    g10 = g10.copy()
    g10["dec"] = pd.qcut(g10.depth, 8, labels=False)
    out["h10_octiles"] = g10.groupby("dec").apply(summ)
    out["spearman_noDOGE"] = float(stats.spearmanr(g10[g10.coin != "DOGEUSD"].depth, g10[g10.coin != "DOGEUSD"].un).correlation)
    return out
