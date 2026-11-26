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
            ret1 = pd.Series(c).pct_change(1).values
            inprof = (b["regime"] != "chop").values
            n = len(b)
            for h in (3, 5, 7):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, fwd=c[i + h] / c[i] - 1, cloc=cloc[i],
                                     ret5=ret5[i], ret1=ret1[i], prof=inprof[i]))
    df = pd.DataFrame(rows)
    df = df.join(df.groupby(["coin", "h"])["fwd"].mean().rename("drift"), on=["coin", "h"])
    df["um"] = -(df["fwd"] - df["drift"])
    def st(s):
        s = s.dropna()
        if len(s) < 3: return pd.Series(dict(n=len(s), mean=np.nan, t=np.nan))
        return pd.Series(dict(n=len(s), mean=s.mean(), t=s.mean() / (s.std() / np.sqrt(len(s)))))
    conds = {
        "prof r5<-5% cloc>=.5": lambda d: d.prof & (d.ret5 < -.05) & (d.cloc >= .5),
        "prof r5<-5% cloc<.5": lambda d: d.prof & (d.ret5 < -.05) & (d.cloc < .5),
        "prof r5 -5..0 cloc>=.5": lambda d: d.prof & (d.ret5 >= -.05) & (d.ret5 < 0) & (d.cloc >= .5),
        "prof r5>=0 cloc>=.5": lambda d: d.prof & (d.ret5 >= 0) & (d.cloc >= .5),
        "prof r5<0 cloc>=.5 ret1>0": lambda d: d.prof & (d.ret5 < 0) & (d.cloc >= .5) & (d.ret1 > 0),
        "prof r5<0 cloc>=.5 ret1<=0": lambda d: d.prof & (d.ret5 < 0) & (d.cloc >= .5) & (d.ret1 <= 0),
        "prof r5<-5% any cloc": lambda d: d.prof & (d.ret5 < -.05),
    }
    res = []
    for h in (3, 5, 7):
        d = df[df.h == h]
        for k, f in conds.items():
            s = st(d.loc[f(d), "um"]); s["h"] = h; s["cond"] = k; res.append(s)
    out["conds"] = pd.DataFrame(res).set_index(["h", "cond"])
    # trades joined to entry bar
    tr = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            if not len(t): continue
            b = data["bars"][coin][w].reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"]; rng = (b["high"] - b["low"]).replace(0, np.nan)
            cl = (c - b["low"]) / rng; r5 = c.pct_change(5)
            for _, r in t.iterrows():
                et = pd.to_datetime(r["entry_time"])
                j = int(np.searchsorted(ts.values, np.datetime64(et.tz_localize(None) if et.tzinfo else et), side="right") - 1)
                j = max(j, 0)
                tr.append(dict(w=w, net=r["net_profit_loss_percent"], r5=r5.iloc[j], cl=cl.iloc[j],
                               days=r["duration_minutes"] / 1440, f=r["entry_forecast"]))
    T = pd.DataFrame(tr)
    T["r5b"] = pd.cut(T.r5, [-1, -.1, -.05, -.02, 0, 5])
    out["trades by entry ret5"] = T.groupby("r5b", observed=True).net.agg(["count", "mean", "sum"])
    T["clb"] = pd.cut(T.cl, [0, .5, .75, .9, 1.001], include_lowest=True)
    out["trades by entry cloc"] = T.groupby("clb", observed=True).net.agg(["count", "mean", "sum"])
    T["fb"] = pd.qcut(T.f.abs(), 3, duplicates="drop")
    out["trades by |forecast| tercile"] = T.groupby("fb", observed=True).net.agg(["count", "mean", "sum"])
    out["losers w12 w17 r5 mean"] = T[T.w.isin(["w12", "w17"])].groupby(T.net > 0).r5.agg(["count", "mean"])
    return out
