def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    # coin mean daily return over all windows
    cmean = {}
    for c in bars:
        r = []
        for w, d in days[c].items():
            r.append(d["coin_return"].dropna())
        cmean[c] = pd.concat(r).mean()
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(b)
            dist = b["debug_info.components.below_ma.last_history_value"].values if "debug_info.components.below_ma.last_history_value" in b else np.full(n, np.nan)
            alloc = b["postRebalance_current_allocation"].values
            fc = b["forecast"].values
            # sma200 slope proxy: dist change? compute from close: sma = close/(1+dist)
            sma = cl / (1 + dist) if np.nanmax(np.abs(dist)) < 5 else cl / (1 + dist / 100)
            for i in range(0, n - 10, 10):
                f = cl[i + 10] / cl[i] - 1
                ex = f - 10 * cmean[c]
                mom20 = cl[i] / cl[i - 20] - 1 if i >= 20 else np.nan
                slope = sma[i] / sma[i - 20] - 1 if i >= 20 else np.nan
                vol = np.std(np.diff(np.log(cl[max(0, i - 20):i + 1]))) if i >= 5 else np.nan
                rows.append(dict(coin=c, win=w, alloc=alloc[i], fc=fc[i], dist=dist[i],
                                 ex=ex, gain=alloc[i] * ex, mom20=mom20, slope=slope, vol=vol,
                                 year=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    act = df[df.alloc < 0].copy()
    out = {}
    out["dist scale"] = df["dist"].describe()
    def grp(g):
        return pd.Series(dict(n=len(g), mean_ex=g.ex.mean(), mean_gain=g.gain.mean(),
                              t_gain=g.gain.mean() / (g.gain.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                              mean_alloc=g.alloc.mean()))
    act["fcq"] = pd.qcut(act.fc, 4, labels=False, duplicates="drop")
    out["by forecast quartile (0=deepest)"] = act.groupby("fcq").apply(grp)
    act["distq"] = pd.qcut(act.dist, 4, labels=False, duplicates="drop")
    out["by dist quartile (0=deepest)"] = act.groupby("distq").apply(grp)
    act["mom_q"] = pd.qcut(act.mom20, 4, labels=False, duplicates="drop")
    out["by 20bar momentum quartile"] = act.groupby("mom_q").apply(grp)
    act["slope_sign"] = np.sign(act.slope)
    out["by sma slope sign"] = act.groupby("slope_sign").apply(grp)
    act["volq"] = pd.qcut(act.vol, 4, labels=False, duplicates="drop")
    out["by vol quartile"] = act.groupby("volq").apply(grp)
    out["by coin"] = act.groupby("coin").apply(grp)
    out["by year"] = act.groupby("year").apply(grp)
    flat = df[df.alloc == 0]
    out["flat blocks mean ex"] = pd.Series(dict(n=len(flat), mean_ex=flat.ex.mean()))
    # book: daily drawdown windows
    bk = []
    for c in days:
        for w, d in days[c].items():
            s = d["book_return"].dropna()
            bk.append(pd.DataFrame(dict(win=w, br=s.values, cr=d.loc[s.index, "coin_return"].values)))
    bk = pd.concat(bk)
    out["book by window"] = bk.groupby("win").agg(mean_br=("br", "mean"), mean_cr=("cr", "mean")).T
    return out
