def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    dcol = "debug_info.components.depth_swings.last_history_value"
    H = [1, 3, 5, 10, 20]
    # drift per coin per h
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
            ret1 = pd.Series(cl).pct_change().values
            hh = b["high"].rolling(20, min_periods=20).max().values
            sd = pd.Series(ret1).rolling(20, min_periods=20).std().values
            depth = (cl - hh) / hh / sd
            tr60 = pd.Series(cl).pct_change(60).values * 100
            choppy = (tr60 >= -10) & (tr60 <= 10)
            vol30 = pd.Series(ret1).rolling(30).std()
            for t in range(n):
                if not choppy[t] or np.isnan(depth[t]) or np.isnan(ret1[t]):
                    continue
                for h in H:
                    if t + h >= n:
                        continue
                    rows.append(dict(coin=c, w=w, t=t, h=h, cell=t // h, up=ret1[t] > 0,
                                     depth=depth[t], day=str(b["timestamp"].iloc[t])[:10],
                                     yr=str(b["timestamp"].iloc[t])[:4],
                                     un=-(cl[t + h] / cl[t] - 1 - drift[(c, h)][0]),
                                     tot=-(cl[t + h] / cl[t] - 1),
                                     strg=-(cl[t + h] / cl[t] - 1 - drift[(c, h)][0]) / drift[(c, h)][1],
                                     regime=b["regime"].iloc[t]))
    df = pd.DataFrame(rows)
    df = df[df.depth < 0]
    # one per cell (first)
    g = df.sort_values("t").groupby(["coin", "w", "h", "cell", "up"]).head(1)

    def summ(x):
        d = x.groupby("day")["un"].apply(lambda s: (s - x["un"].mean()).sum())
        se = np.sqrt((d ** 2).sum()) / len(x) if len(x) > 1 else np.nan
        return pd.Series(dict(n=len(x), days=x.day.nunique(), mean_un=x.un.mean(),
                              t=x.un.mean() / se if se else np.nan, mean_tot=x.tot.mean(), strength=x.strg.mean()))
    out = {}
    out["by_h_up"] = g.groupby(["h", "up"]).apply(summ)
    gu = g.copy()
    gu["q"] = gu.groupby(["h", "up"])["depth"].transform(lambda s: pd.qcut(s, 4, labels=["deep", "q2", "q3", "shallow"]))
    out["by_h_up_quartile"] = gu[gu.h.isin([1, 5, 10])].groupby(["h", "up", "q"]).apply(summ)
    g10 = g[(g.h == 10) & g.up]
    out["h10_up_by_coin"] = g10.groupby("coin").apply(summ)
    out["h10_up_by_window"] = g10.groupby("w").apply(summ)
    out["h10_up_by_year"] = g10.groupby("yr").apply(summ)
    out["corr_depth_un_h10_up"] = float(stats.spearmanr(g10.depth, g10.un).correlation)
    return out
