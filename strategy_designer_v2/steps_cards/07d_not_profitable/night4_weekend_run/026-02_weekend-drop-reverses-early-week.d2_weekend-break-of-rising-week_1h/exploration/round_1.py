def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # trades
    tr = []
    for c, ws in data["trades"].items():
        for w, t in ws.items():
            if t is None or len(t) == 0: continue
            t = t.copy(); t["coin"] = c; t["win"] = w
            tr.append(t)
    T = pd.concat(tr, ignore_index=True)
    T["yr"] = pd.to_datetime(T["entry_time"]).dt.year
    g = T.groupby("coin").agg(n=("net_profit_loss_percent","size"),
                              gross=("profit_loss_percent","mean"),
                              net=("net_profit_loss_percent","mean"),
                              dur_h=("duration_minutes", lambda x: x.mean()/60))
    out["trades_by_coin"] = g
    out["trades_by_year"] = T.groupby("yr").agg(n=("net_profit_loss_percent","size"),
                              gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    out["trades_side"] = T.groupby("side").size()
    # cases from bars: forecast at sunday 23h
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            n = len(b)
            for i in np.where((ts.dt.weekday==6)&(ts.dt.hour==23))[0]:
                if i+48 >= n or i-168 < 0: continue
                wk = cl[i]/cl[i-48]-1
                pr = cl[i-48]/cl[i-168]-1
                f24 = cl[i+24]/cl[i]-1; f48 = cl[i+48]/cl[i]-1
                f96 = cl[i+96]/cl[i]-1 if i+96<n else np.nan
                rows.append(dict(coin=c, win=w, yr=ts[i].year, fc=b["forecast"].iloc[i],
                                 alloc=b["postRebalance_current_allocation"].iloc[i],
                                 wk=wk, pr=pr, f24=f24, f48=f48, f96=f96))
    S = pd.DataFrame(rows)
    S["active"] = S["fc"] < 0
    # drift 48 per coin approximate: mean over all sunday rows? use non overlapping grid
    dr = {}
    for c, ws in data["bars"].items():
        r = []
        for w, b in ws.items():
            cl = b["close"].values
            idx = np.arange(0, len(cl)-48, 48)
            r += list(cl[idx+48]/cl[idx]-1)
        dr[c] = np.mean(r)
    S["u48"] = -(S["f48"] - S["coin"].map(dr))
    S["tot48"] = -S["f48"]
    S["tot24"] = -S["f24"]; S["tot96"] = -S["f96"]
    A = S[S.active]
    def summ(x):
        return pd.Series({"n": len(x), "tot24": x.tot24.mean(), "tot48": x.tot48.mean(),
                          "tot96": x.tot96.mean(), "u48": x.u48.mean(),
                          "t48": x.tot48.mean()/(x.tot48.std()/np.sqrt(len(x))), "absalloc": x.alloc.abs().mean()})
    out["active_by_coin"] = A.groupby("coin").apply(summ)
    out["active_by_year"] = A.groupby("yr").apply(summ)
    # all sunday rows by weekend move quintile and prior rise sign
    S["wkq"] = pd.qcut(S["wk"], 5, labels=False)
    S["prpos"] = S["pr"] > 0
    out["all_sundays_wkq_prpos"] = S.groupby(["prpos","wkq"]).apply(summ)
    # within active, by prior rise tercile and weekend fall tercile
    A = S[S.active].copy()
    A["prq"] = pd.qcut(A["pr"], 3, labels=False)
    A["wkq3"] = pd.qcut(A["wk"], 3, labels=False)
    out["active_by_prq"] = A.groupby("prq").apply(summ)
    out["active_by_wkq3"] = A.groupby("wkq3").apply(summ)
    # book daily
    D = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["coin"]=c; d["win"]=w; D.append(d)
    D = pd.concat(D)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    out["book_by_weekday"] = D.groupby("wd")[["book_return","coin_return"]].mean()
    out["share_days_exposed"] = float((D["book_return"].abs()>1e-9).mean())
    return out
