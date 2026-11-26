def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    cost = 0.0022
    # ---- per coin-window daily gains of the actual book and of variants
    rows = []; cases = []; grid = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values
            a = b["postRebalance_current_allocation"].fillna(0).values
            n = len(b)
            r1 = np.r_[np.diff(cl) / cl[:-1], np.nan]
            ph = np.full(n, np.nan); pl = np.full(n, np.nan)
            for t in range(60, n):
                ph[t] = hi[t - 60:t].max(); pl[t] = lo[t - 60:t].min()
            width = (ph - pl) / cl
            vol20 = pd.Series(r1).shift(1).rolling(20).std().values
            # episodes
            a_w = np.zeros(n); a_v = np.zeros(n); a_s = np.zeros(n); a_ws = np.zeros(n)
            t = 1
            while t < n:
                if a[t] > 0 and a[t - 1] <= 0:
                    e = t
                    while e + 1 < n and a[e + 1] > 0: e += 1
                    lvl = ph[t]; wd = width[t]; vv = vol20[t]
                    keep_w = (not np.isnan(wd)) and wd <= 0.42
                    keep_v = (not np.isnan(vv)) and vv <= 0.046
                    # stop: out after the first close back below the breakout level
                    stop_at = e
                    for k in range(t + 1, e + 1):
                        if not np.isnan(lvl) and cl[k] < lvl:
                            stop_at = k; break
                    seg = slice(t, e + 1)
                    g = np.nansum(a[seg] * r1[seg])
                    gs = np.nansum(a[t:stop_at] * r1[t:stop_at]) if stop_at > t else 0.0
                    a_s[t:stop_at] = a[t:stop_at]
                    if keep_w: a_w[seg] = a[seg]
                    if keep_v: a_v[seg] = a[seg]
                    if keep_w: a_ws[t:stop_at] = a[t:stop_at]
                    cases.append(dict(coin=c, w=w, width=wd, vol20=vv, gain=g, gain_stop=gs,
                                      stopped=stop_at < e, held=e - t + 1))
                    t = e + 1
                else:
                    t += 1
            def daily(al):
                ch = np.abs(np.diff(np.r_[0, al]))
                gg = np.r_[0, al[:-1] * r1[:-1]] - ch * cost / 2
                return gg
            for name, al in [("book", a), ("narrow", a_w), ("lowvol", a_v), ("stop", a_s), ("narrow_stop", a_ws)]:
                rows.append(pd.DataFrame({"t": b["timestamp"].values, "g": daily(al), "coin": c, "w": int(w[1:]), "v": name}))
            # condition-alone grid: every 10th bar
            for t in range(60, n - 10, 10):
                grid.append(dict(width=width[t], brk=cl[t] > ph[t], r10=cl[t + 10] / cl[t] - 1))
    R = pd.concat(rows)
    R["day"] = pd.to_datetime(R["t"]).dt.floor("D")
    res = {}
    for v, g in R.groupby("v"):
        B = g.groupby(["w", "day"])["g"].mean().reset_index().sort_values(["w", "day"])
        x = B["g"].values
        val = np.cumprod(1 + x); dd = val / np.maximum.accumulate(val) - 1
        yr = val[-1] ** (365 / len(x)) - 1
        wsum = B.groupby("w")["g"].sum()
        res[v] = dict(sharpe=x.mean() / x.std(ddof=1) * np.sqrt(365), yearly=yr, maxdd=dd.min(),
                      calmar=yr / -dd.min(), w12=wsum.get(12, 0), w16=wsum.get(16, 0), worst_w=wsum.min())
    out["variants_approx"] = pd.DataFrame(res).T
    C = pd.DataFrame(cases)
    out["cases_n"] = len(C)
    C["wq"] = pd.cut(C["width"], [0, 0.31, 0.42, 1.0])
    out["gain_by_width"] = C.groupby("wq").agg(n=("gain", "count"), gain=("gain", "mean"), gain_stop=("gain_stop", "mean"),
                                               share_loss=("gain", lambda s: (s < 0).mean()), stopped=("stopped", "mean"))
    out["gain_by_stopped"] = C.groupby("stopped").agg(n=("gain", "count"), gain=("gain", "mean"), gain_stop=("gain_stop", "mean"))
    out["gain_by_window"] = C.groupby("w").agg(n=("gain", "count"), gain=("gain", "sum"), gain_stop=("gain_stop", "sum"),
                                               mean_width=("width", "mean"))
    G = pd.DataFrame(grid).dropna()
    G["wq"] = pd.cut(G["width"], [0, 0.31, 0.42, 1.0, 100])
    out["condition_alone_width"] = G.groupby(["brk", "wq"]).agg(n=("r10", "count"), r10=("r10", "mean"))
    nb = G[~G["brk"]]
    out["narrow_nobreak_vs_wide_nobreak_t"] = float(stats.ttest_ind(nb[nb["width"] <= 0.42]["r10"], nb[nb["width"] > 0.42]["r10"], equal_var=False).statistic)
    return out
