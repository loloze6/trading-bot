def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # pooled bars with fwd 20 returns on non-overlapping grid
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            f = b["forecast"].values
            raw = b["debug_info.components.above_ma.last_history_value"].values if "debug_info.components.above_ma.last_history_value" in b else np.full(len(b), np.nan)
            n = len(b)
            # 20-bar past return, 60-bar past return
            for i in range(0, n - 20, 20):
                r = cl[i+20]/cl[i]-1
                p20 = cl[i]/cl[i-20]-1 if i >= 20 else np.nan
                rows.append(dict(coin=c, win=w, f=f[i], raw=raw[i], r=r, p20=p20,
                                 dd=cl[i]/np.max(cl[max(0,i-60):i+1])-1))
    d = pd.DataFrame(rows)
    mu = {}
    for c, ws in data["days"].items():
        allr = pd.concat([x["coin_return"] for x in ws.values()]).dropna()
        mu[c] = allr.mean()
    d["ex"] = d["r"] - 20*d["coin"].map(mu)
    d["fb"] = pd.cut(d["f"], [-0.1, 0.0001, 5, 10, 15, 20.1], labels=["0","0-5","5-10","10-15","15-20"])
    out["fwd20 by forecast bucket"] = d.groupby("fb")["ex"].agg(["count","mean","median",lambda x: (x>0).mean()])
    act = d[d.f > 0].copy()
    act["rawq"] = pd.qcut(act["raw"], 4, labels=False, duplicates="drop")
    out["active: fwd20 excess by raw distance quartile"] = act.groupby("rawq").agg(n=("ex","size"), raw=("raw","mean"), ex=("ex","mean"), sd=("ex","std"))
    act["p20q"] = pd.qcut(act["p20"], 4, labels=False, duplicates="drop")
    out["active: fwd20 excess by past20 return quartile"] = act.groupby("p20q").agg(n=("ex","size"), p20=("p20","mean"), ex=("ex","mean"))
    act["ddq"] = pd.qcut(act["dd"], 4, labels=False, duplicates="drop")
    out["active: fwd20 excess by drawdown from 60-bar high quartile"] = act.groupby("ddq").agg(n=("ex","size"), dd=("dd","mean"), ex=("ex","mean"))
    out["flat bars fwd20 excess by past20 quartile"] = d[d.f==0].assign(q=lambda x: pd.qcut(x.p20,4,labels=False,duplicates="drop")).groupby("q").agg(n=("ex","size"),p20=("p20","mean"),ex=("ex","mean"))
    # book daily
    dl = []
    for c, ws in data["days"].items():
        for w, x in ws.items():
            dl.append(x.assign(coin=c, win=w))
    D = pd.concat(dl)
    B = D.groupby(["win","day"]).agg(b=("book_return","mean"), h=("coin_return","mean")).dropna().reset_index()
    B["wn"] = B["win"].str[1:].astype(int)
    B = B.sort_values(["wn","day"])
    out["by window book vs hold sum"] = B.groupby("wn").agg(n=("b","size"), book=("b","sum"), hold=("h","sum"))
    eq = (1+B["b"]).cumprod().values
    dd = eq/np.maximum.accumulate(eq)-1
    out["max dd book"] = float(dd.min())
    i = int(dd.argmin()); pk = int(np.argmax(eq[:i+1]))
    seg = B.iloc[pk:i+1]
    out["deepest fall: windows, days, book sum, hold sum"] = f"{seg.wn.min()}-{seg.wn.max()} days={len(seg)} book={seg.b.sum():.3f} hold={seg.h.sum():.3f}"
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    out["trades"] = f"n={len(T)} mean_net={T.net_profit_loss_percent.mean():.3f} mean_gross={T.profit_loss_percent.mean():.3f} comm_sum={T.total_commission.sum():.2f}"
    return out
