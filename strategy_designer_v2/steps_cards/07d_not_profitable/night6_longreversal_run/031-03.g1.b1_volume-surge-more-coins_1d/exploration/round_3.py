def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; al = b["postRebalance_current_allocation"]
            r1 = c.shift(-1)/c - 1
            r14 = c.pct_change(14)
            r28 = c.pct_change(28)
            day = pd.to_datetime(b["timestamp"]).dt.strftime("%Y-%m-%d")
            agree = np.sign(al) == np.sign(r14)
            agree28 = np.sign(al) == np.sign(r28)
            dfx = pd.DataFrame(dict(coin=coin, wn=int(w[1:]), day=day, g=al*r1,
                                    ga=np.where(agree, al, 0)*r1, ga28=np.where(agree28, al, 0)*r1,
                                    gl=np.where(al>0, al, 0)*r1, act=agree.astype(float), hold=r1,
                                    hs=np.sign(al)*r1))
            rows.append(dfx.dropna())
    d = pd.concat(rows)
    p = d.groupby(["wn","day"])[["g","ga","ga28","gl","act","hold"]].mean().reset_index().sort_values(["wn","day"])
    def stats(x):
        v = (1+x).cumprod(); dd = (v/v.cummax()-1).min()
        yrs = len(x)/365; yret = v.iloc[-1]**(1/yrs)-1
        return pd.Series(dict(sharpe=x.mean()/x.std()*np.sqrt(365), mean=x.mean(), sd=x.std(), maxdd=dd, yret=yret, calmar=yret/abs(dd)))
    out["books_nofee"] = pd.DataFrame({k: stats(p[k]) for k in ["g","ga","ga28","gl","hold"]})
    out["agree_share"] = float(p["act"].mean())
    p["v"] = (1+p["g"]).cumprod(); p["dd"] = p["v"]/p["v"].cummax()-1
    out["by_window_g_ga"] = p.groupby("wn").agg(g=("g","sum"), ga=("ga","sum"), hold=("hold","sum"), mindd=("dd","min"))
    # cost estimate: turnover
    tv = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            al = b["postRebalance_current_allocation"].values
            r14 = pd.Series(b["close"].values).pct_change(14).values
            a2 = np.where(np.sign(al)==np.sign(r14), al, 0)
            tv.append(dict(t1=np.nansum(np.abs(np.diff(al))), t2=np.nansum(np.abs(np.diff(a2))), n=len(al)))
    tv = pd.DataFrame(tv)
    out["turnover_per_day"] = pd.Series(dict(orig=tv.t1.sum()/tv.n.sum(), agree=tv.t2.sum()/tv.n.sum()))
    return out
