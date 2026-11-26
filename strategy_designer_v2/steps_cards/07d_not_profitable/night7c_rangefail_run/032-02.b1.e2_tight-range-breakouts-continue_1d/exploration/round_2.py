def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    bars = data["bars"]; days = data["days"]
    coins = list(bars.keys())
    # grid samples: 10-bar forward return, range width, ER60, breakout flag
    S = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(b)
            for i in range(0, n - 10, 10):
                if i < 60: continue
                ph = hi[i-60:i]; pl = lo[i-60:i]
                rng = ph.max() / pl.min() - 1
                er = abs(cl[i] - cl[i-60]) / np.sum(np.abs(np.diff(cl[i-60:i+1])))
                brk = cl[i] > ph.max()
                fwd = cl[i+10] / cl[i] - 1
                S.append(dict(coin=c, w=w, rng=rng, er=er, brk=brk, fwd=fwd, choppy=er <= 0.3))
    S = pd.DataFrame(S)
    drift = S["fwd"].mean()
    S["unus"] = S["fwd"] - drift
    out["n_grid_drift"] = pd.Series({"n": len(S), "drift": drift, "sd": S["fwd"].std()})
    S["rngq"] = pd.qcut(S["rng"], 3, labels=["tight", "mid", "wide"])
    out["grid_by_rng_brk"] = S.groupby(["rngq", "brk"]).agg(n=("unus", "size"), mean=("unus", "mean"), sd=("unus", "std"))
    out["grid_by_rng_brk_choppy"] = S[S.choppy].groupby(["rngq", "brk"]).agg(n=("unus", "size"), mean=("unus", "mean"))
    # every-bar breakout events (choppy) by range width, forward 10 and 20 days, non-overlapping per coin-window
    E = []
    for c in coins:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            n = len(b); last = -99
            for i in range(60, n - 20):
                ph = hi[i-60:i]; pl = lo[i-60:i]
                if cl[i] <= ph.max(): continue
                er = abs(cl[i] - cl[i-60]) / np.sum(np.abs(np.diff(cl[i-60:i+1])))
                if er > 0.3 or i - last < 10: continue
                last = i
                path = cl[i:i+21] / cl[i] - 1
                E.append(dict(coin=c, w=w, rng=ph.max()/pl.min()-1, f5=cl[i+5]/cl[i]-1, f10=cl[i+10]/cl[i]-1,
                              f20=cl[i+20]/cl[i]-1, mae10=path[:11].min(), back_in=(cl[i+1:i+11] < ph.max()).mean()))
    E = pd.DataFrame(E)
    E["rngq"] = pd.qcut(E["rng"], 3, labels=["tight", "mid", "wide"])
    g = E.groupby("rngq").agg(n=("f10", "size"), rng=("rng", "mean"), f5=("f5", "mean"), f10=("f10", "mean"),
                              med10=("f10", "median"), f20=("f20", "mean"), mae10=("mae10", "mean"), back_in=("back_in", "mean"))
    out["events_by_rng"] = g
    out["events_t_f10"] = E.groupby("rngq")["f10"].apply(lambda s: s.mean() / (s.std() / np.sqrt(len(s))))
    out["events_spearman_rng_f10"] = stats.spearmanr(E["rng"], E["f10"])[0]
    out["events_spearman_rng_f20"] = stats.spearmanr(E["rng"], E["f20"])[0]
    # size actually given vs tightness on active bars
    A = []
    for c in coins:
        for w, b in bars[c].items():
            a = b[b["postRebalance_current_allocation"].fillna(0) > 0]
            if len(a): A.append(a[["forecast", "postRebalance_current_allocation", "debug_info.components.tight.last_history_value"]].assign(coin=c))
    A = pd.concat(A)
    out["spearman_alloc_vs_tightness"] = stats.spearmanr(A["debug_info.components.tight.last_history_value"], A["postRebalance_current_allocation"], nan_policy="omit")[0]
    out["spearman_forecast_vs_tightness"] = stats.spearmanr(A["debug_info.components.tight.last_history_value"], A["forecast"], nan_policy="omit")[0]
    out["alloc_by_coin"] = A.groupby("coin")["postRebalance_current_allocation"].mean()
    # book falls: which coins' days drive the worst book days
    rows = []
    for c in coins:
        for w, d in days[c].items():
            rows.append(d[["day", "book_return"]].assign(coin=c, w=w))
    D = pd.concat(rows).dropna()
    bk = D.groupby(["w", "day"])["book_return"].mean()
    worst = bk.nsmallest(20).index
    Dw = D.set_index(["w", "day"]).loc[worst]
    out["worst20_days_contrib_by_coin"] = Dw.groupby("coin")["book_return"].sum() / 6
    return out
