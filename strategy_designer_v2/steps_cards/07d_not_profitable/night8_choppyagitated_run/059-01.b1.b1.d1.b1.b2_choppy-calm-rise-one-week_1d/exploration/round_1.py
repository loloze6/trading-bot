def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = 7
    rows = []
    drift = {}
    # normal drift per coin over all windows (grid)
    for c, ws in data["bars"].items():
        allr = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - H, H)
            allr += list(cl[idx + H] / cl[idx] - 1)
        drift[c] = np.mean(allr) if allr else np.nan
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            n = len(cl)
            fc = b["forecast"].fillna(0).values
            reg = b["regime"].astype(str).values
            for i in range(0, n - H, H):
                r7p = cl[i] / cl[i - 7] - 1 if i >= 7 else np.nan
                r30p = cl[i] / cl[i - 30] - 1 if i >= 30 else np.nan
                hi7 = cl[max(0, i - 6):i + 1].max()
                lr = np.diff(np.log(cl[max(0, i - 20):i + 1]))
                rows.append(dict(coin=c, w=w, ts=b["timestamp"].iloc[i], fc=fc[i], reg=reg[i],
                                 fwd=cl[i + H] / cl[i] - 1, ex=cl[i + H] / cl[i] - 1 - drift[c],
                                 r7p=r7p, r30p=r30p, offhi=cl[i] / hi7 - 1,
                                 vol20=np.std(lr) if len(lr) > 5 else np.nan,
                                 ret1=cl[i] / cl[i - 1] - 1 if i >= 1 else np.nan))
    g = pd.DataFrame(rows)
    g["year"] = pd.to_datetime(g["ts"]).dt.year
    s = g[g.fc > 0].copy()
    def summ(x):
        return pd.Series(dict(n=len(x), mean_fwd=x.fwd.mean(), mean_ex=x.ex.mean(),
                              t_ex=x.ex.mean() / (x.ex.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                              hit=(x.fwd > 0).mean()))
    out["signal cases overall"] = summ(s)
    out["in-profile no signal (fc==0, regime unknown)"] = summ(g[(g.fc == 0) & (g.reg == "unknown")])
    out["out of profile"] = summ(g[g.reg != "unknown"])
    s["fq"] = pd.qcut(s.fc, 3, labels=["lo", "mid", "hi"])
    out["by forecast tercile"] = s.groupby("fq").apply(summ)
    s["r30q"] = pd.qcut(s.r30p, 3, labels=["lo", "mid", "hi"])
    out["by prior 30d return tercile"] = s.groupby("r30q").apply(summ)
    s["offq"] = pd.qcut(s.offhi.rank(method="first"), 3, labels=["far", "mid", "athigh"])
    out["by distance from 7d high"] = s.groupby("offq").apply(summ)
    s["ret1q"] = pd.qcut(s.ret1, 3, labels=["lo", "mid", "hi"])
    out["by last day return"] = s.groupby("ret1q").apply(summ)
    out["by year"] = s.groupby("year").apply(summ)
    out["by window"] = s.groupby("w").apply(summ)
    # book daily
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            b = data["bars"][c][w]
            al = b["postRebalance_current_allocation"].values
            dd.append(pd.DataFrame(dict(w=w, day=d["day"].values, coin=c, br=d["book_return"].values,
                                        cr=d["coin_return"].values,
                                        held=np.r_[np.nan, al[:-1]][:len(d)] if len(al) == len(d) else np.nan)))
    D = pd.concat(dd)
    B = D.groupby(["w", "day"]).agg(br=("br", "mean"), cr=("cr", "mean")).dropna().reset_index()
    B["wn"] = B.w.str[1:].astype(int)
    B = B.sort_values(["wn", "day"])
    val = (1 + B.br).cumprod().values
    peak = np.maximum.accumulate(val)
    dda = val / peak - 1
    out["book deepest fall"] = float(dda.min())
    B["dd"] = dda
    B["year"] = pd.to_datetime(B.day).dt.year
    out["book vs hold by window"] = B.groupby("wn").agg(book=("br", "sum"), hold=("cr", "sum"),
                                                        mindd=("dd", "min"), days=("br", "size"))
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["fq"] = pd.qcut(T.entry_forecast.rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["trades by entry forecast"] = T.groupby("fq").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"), gross=("profit_loss_percent", "mean"),
        dur_days=("duration_minutes", lambda x: x.mean() / 1440))
    out["trades overall"] = pd.Series(dict(n=len(T), net=T.net_profit_loss_percent.mean(),
        gross=T.profit_loss_percent.mean(), worst=T.net_profit_loss_percent.min(),
        hit=(T.net_profit_loss_percent > 0).mean(), dur=T.duration_minutes.mean() / 1440))
    out["trades by coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"),
        net=("net_profit_loss_percent", "mean"))
    return out
