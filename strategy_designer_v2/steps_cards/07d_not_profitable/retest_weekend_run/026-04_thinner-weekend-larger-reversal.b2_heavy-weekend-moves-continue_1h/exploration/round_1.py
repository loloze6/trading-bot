def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    wins = [f"w{i}" for i in range(1, 25)]
    coins = list(data["bars"].keys())
    # book daily chain
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            frames.append(d.set_index("day")["book_return"].rename(c))
        if not frames: continue
        df = pd.concat(frames, axis=1)
        m = df.mean(axis=1).dropna()
        for i, v in enumerate(m.values):
            rows.append((w, i, v))
    bk = pd.DataFrame(rows, columns=["w", "i", "r"])
    val = (1 + bk.r).cumprod()
    dd = val / val.cummax() - 1
    bk["dd"] = dd.values
    trough = bk.dd.idxmin()
    peak = val[:trough + 1].idxmax()
    out["deepest_fall"] = pd.Series({"dd": bk.dd.min(), "peak_win": bk.w[peak], "trough_win": bk.w[trough],
                                     "days_long": trough - peak})
    # per-window book return and max dd within window
    wb = bk.groupby("w").apply(lambda g: pd.Series({"ret": (1 + g.r).prod() - 1,
                                                    "mindd": (((1 + g.r).cumprod()) / ((1 + g.r).cumprod().cummax()) - 1).min(),
                                                    "days": len(g)}))
    out["by_window"] = wb.reindex(wins)
    # cases
    cs = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b.close.values
            n = len(b)
            ts = pd.to_datetime(b.timestamp)
            idx = np.where((b.forecast.fillna(0) != 0) & (b.regime == "trending"))[0]
            lr = np.log(cl)
            for t in idx:
                if t + 48 >= n: continue
                s = np.sign(b.forecast[t])
                r48 = cl[t + 48] / cl[t] - 1
                r12 = cl[t + 12] / cl[t] - 1
                r24 = cl[t + 24] / cl[t] - 1
                path = cl[t:t + 49] / cl[t] - 1
                mae = np.min(s * path)
                wk = cl[t] / cl[t - 48] - 1 if t >= 48 else np.nan
                p30 = cl[t - 48] / cl[t - 720] - 1 if t >= 720 else np.nan
                vol = np.std(np.diff(lr[max(0, t - 720):t + 1])) * np.sqrt(48)
                cs.append(dict(coin=c, w=w, year=ts[t].year, s=s, f=abs(b.forecast[t]),
                               alloc=b.postRebalance_current_allocation[t],
                               d48=s * r48, d12=s * r12, d24=s * r24, rest=s * (cl[t + 48] / cl[t + 12] - 1),
                               mae=mae, wk=wk / vol if vol > 0 else np.nan,
                               trend=s * np.sign(p30) if not np.isnan(p30) else np.nan,
                               p30z=s * p30 / (vol * np.sqrt(15)) if (not np.isnan(p30) and vol > 0) else np.nan,
                               vol=vol, pnl=b.postRebalance_current_allocation[t] * r48))
    cs = pd.DataFrame(cs)
    def g(df, key):
        return df.groupby(key).agg(n=("d48", "size"), d48=("d48", "mean"), t=("d48", lambda x: x.mean() / x.std() * np.sqrt(len(x))),
                                   pnl=("pnl", "mean"), pnlsum=("pnl", "sum"), mae=("mae", "mean"))
    out["by_side"] = g(cs, "s")
    out["by_coin"] = g(cs, "coin")
    out["by_year"] = g(cs, "year")
    cs["fq"] = pd.qcut(cs.f, 4, labels=False)
    out["by_fq"] = g(cs, "fq")
    cs["volq"] = cs.groupby("coin").vol.transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["by_volq"] = g(cs, "volq")
    out["by_trend_align"] = g(cs.dropna(subset=["trend"]), "trend")
    cs["p30q"] = pd.qcut(cs.p30z, 4, labels=False)
    out["by_p30z_q"] = g(cs.dropna(subset=["p30z"]), "p30q")
    cs["wkq"] = pd.qcut(cs.wk.abs(), 4, labels=False)
    out["by_wk_absz_q"] = g(cs.dropna(subset=["wk"]), "wkq")
    # stop: first 12h against
    cs["early"] = pd.cut(cs.d12, [-1, -0.03, -0.01, 0.01, 0.03, 1])
    out["rest_after_first12h"] = cs.groupby("early").agg(n=("rest", "size"), rest=("rest", "mean"),
                                                        t=("rest", lambda x: x.mean() / x.std() * np.sqrt(len(x))))
    out["pnl_quantiles"] = cs.pnl.quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
    srt = cs.pnl.sort_values()
    out["tail"] = pd.Series({"sum_all": cs.pnl.sum(), "sum_worst10": srt.iloc[:10].sum(), "sum_best10": srt.iloc[-10:].sum(),
                             "mean_abs_alloc": cs.alloc.abs().mean()})
    # cases in deepest fall windows
    fw = bk.w[peak:trough + 1].unique().tolist()
    sub = cs[cs.w.isin(fw)]
    out["fall_cases_by_side"] = g(sub, "s")
    out["fall_cases_by_trend"] = g(sub.dropna(subset=["trend"]), "trend")
    out["fall_cases_by_volq"] = g(sub, "volq")
    return out
