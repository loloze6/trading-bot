def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            cloc = ((b["close"] - b["low"]) / rng).values
            ret5 = pd.Series(c).pct_change(5).values
            ret60 = pd.Series(c).pct_change(60).values
            inprof = (b["regime"] != "chop").values
            n = len(b)
            for h in (2, 5, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i, fwd=c[i + h] / c[i] - 1,
                                     cloc=cloc[i], ret5=ret5[i], ret60=ret60[i], prof=inprof[i],
                                     reg=b["regime"].iloc[i], yr=pd.Timestamp(b["timestamp"].iloc[i]).year))
    df = pd.DataFrame(rows)
    drift = df.groupby(["coin", "h"])["fwd"].mean().rename("drift")
    df = df.join(drift, on=["coin", "h"])
    df["um"] = -(df["fwd"] - df["drift"])  # short direction
    def st(s):
        s = s.dropna()
        if len(s) < 3: return pd.Series(dict(n=len(s), mean=np.nan, t=np.nan))
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s)))))
    conds = {
        "tested: prof&ret5<0&cloc>=.75": lambda d: d.prof & (d.ret5 < 0) & (d.cloc >= .75),
        "prof&cloc>=.75 any ret5": lambda d: d.prof & (d.cloc >= .75),
        "prof&ret5>0&cloc>=.75": lambda d: d.prof & (d.ret5 > 0) & (d.cloc >= .75),
        "prof&ret5<0&cloc>=.5": lambda d: d.prof & (d.ret5 < 0) & (d.cloc >= .5),
        "prof&ret5<0&cloc .5-.75": lambda d: d.prof & (d.ret5 < 0) & (d.cloc >= .5) & (d.cloc < .75),
        "prof&ret5<0 only": lambda d: d.prof & (d.ret5 < 0),
        "prof&ret5<0&cloc<.5": lambda d: d.prof & (d.ret5 < 0) & (d.cloc < .5),
        "prof all": lambda d: d.prof,
        "outprof&ret5<0&cloc>=.75": lambda d: (~d.prof) & (d.ret5 < 0) & (d.cloc >= .75),
        "outprof choppy60&ret5<0&cloc>=.75": lambda d: (~d.prof) & (d.ret60.abs() <= .1) & (d.ret5 < 0) & (d.cloc >= .75),
        "outprof rising60&ret5<0&cloc>=.75": lambda d: (~d.prof) & (d.ret60 > .1) & (d.ret5 < 0) & (d.cloc >= .75),
        "outprof falling60&ret5<0&cloc>=.75": lambda d: (~d.prof) & (d.ret60 < -.1) & (d.ret5 < 0) & (d.cloc >= .75),
        "all ret5<0&cloc>=.75": lambda d: (d.ret5 < 0) & (d.cloc >= .75),
    }
    res = []
    for h in (2, 5, 10):
        d = df[df.h == h]
        for k, f in conds.items():
            s = st(d.loc[f(d), "um"]); s["h"] = h; s["cond"] = k; res.append(s)
    out["conds"] = pd.DataFrame(res).set_index(["h", "cond"])
    d5 = df[(df.h == 5) & df.prof & (df.ret5 < 0)].copy()
    d5["clocb"] = pd.cut(d5.cloc, [0, .25, .5, .75, .9, 1.0001], include_lowest=True)
    out["prof ret5<0 by cloc h5"] = d5.groupby("clocb")["um"].apply(st).unstack()
    d5b = df[(df.h == 5) & df.prof & (df.cloc >= .5)].copy()
    d5b["r5b"] = pd.cut(d5b.ret5, [-1, -.1, -.05, -.02, 0, .02, .05, .1, 5])
    out["prof cloc>=.5 by ret5 h5"] = d5b.groupby("r5b")["um"].apply(st).unstack()
    out["share prof bars"] = float(df[df.h == 5].prof.mean())
    # trades
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if len(t): t = t.copy(); t["coin"] = coin; t["w"] = w; tr.append(t)
    T = pd.concat(tr)
    T["days"] = T.duration_minutes / 1440
    out["trades summary"] = pd.Series(dict(n=len(T), mean_net=T.net_profit_loss_percent.mean(),
                                           med_days=T.days.median(), win=(T.net_profit_loss_percent > 0).mean(),
                                           worst=T.net_profit_loss_percent.min(), sum_worst5=T.net_profit_loss_percent.nsmallest(5).sum(),
                                           sum_all=T.net_profit_loss_percent.sum()))
    out["trades by window"] = T.groupby("w").net_profit_loss_percent.agg(["count", "mean", "sum", "min"])
    out["trades by coin"] = T.groupby("coin").net_profit_loss_percent.agg(["count", "mean", "sum", "min"])
    # book daily fall
    dl = []
    for coin, wins in data["days"].items():
        for w, dd in wins.items():
            x = dd[["day", "book_return"]].copy(); x["w"] = w; dl.append(x)
    D = pd.concat(dl).groupby(["w", "day"])["book_return"].mean().dropna()
    wk = D.reset_index()
    order = sorted(wk.w.unique(), key=lambda s: int(s[1:]))
    wk["w"] = pd.Categorical(wk.w, order, ordered=True)
    wk = wk.sort_values(["w", "day"])
    v = (1 + wk.book_return).cumprod().values
    dd_ = v / np.maximum.accumulate(v) - 1
    j = int(np.argmin(dd_)); pk = int(np.argmax(v[:j + 1]))
    out["deepest fall"] = pd.Series(dict(depth=dd_[j], days_to_trough=j - pk, trough_window=str(wk.w.iloc[j]), peak_window=str(wk.w.iloc[pk])))
    out["worst days by window"] = wk.groupby("w", observed=True).book_return.agg(["sum", "min", "count"])
    return out
