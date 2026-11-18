def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    ev = []
    allr = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            cl = b["close"].values; f = b["forecast"].fillna(0).values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            n = len(b)
            ret = pd.Series(cl).pct_change()
            vs = ret.rolling(20).std()
            vol = (b["volume"]/b["volume"].rolling(30).mean()).values
            r20 = pd.Series(cl).pct_change(20).values
            for t in range(n):
                if t+1 < n: allr.append((c, cl[t+1]/cl[t]-1))
            for t in range(n-6):
                if f[t] >= 5:
                    d = {"coin":c,"w":w,"f":f[t],"vol":vol[t],"z":(ret.iloc[t]/vs.iloc[t]) if vs.iloc[t]>0 else np.nan,
                         "r20":r20[t],"pos0":pos[t]}
                    for k in range(1,6):
                        d[f"d{k}"] = cl[t+k]/cl[t+k-1]-1
                        d[f"pos{k}"] = pos[t+k]
                    d["r5"] = cl[t+5]/cl[t]-1
                    ev.append(d)
    E = pd.DataFrame(ev)
    R = pd.DataFrame(allr, columns=["coin","r"])
    cm = R.groupby("coin").r.mean()
    E["cm"] = E.coin.map(cm)
    rows = {}
    for k in range(1,6):
        x = E[f"d{k}"]-E.cm
        rows[f"day{k}"] = {"excess mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x),
                           "pos held into it": E[f"pos{k-1}"].mean()}
    out["daily excess after f>=5 events"] = pd.DataFrame(rows).T
    E["ex5"] = E.r5 - 5*E.cm
    E["ex24"] = E.d2+E.d3+E.d4+E.d5 - 4*E.cm
    E["volq"] = pd.qcut(E.vol, 3, labels=["low","mid","high"])
    E["zq"] = pd.qcut(E.z, 3, labels=["low","mid","high"])
    E["r20q"] = pd.qcut(E.r20, 3, labels=["low","mid","high"])
    for g in ["volq","zq","r20q"]:
        out[f"ex5 by {g}"] = E.groupby(g).agg(n=("ex5","size"), ex5=("ex5","mean"), ex_d2_5=("ex24","mean"), d1=("d1","mean"))
    out["ex5 by coin"] = E.groupby("coin").agg(n=("ex5","size"), ex5=("ex5","mean"), ex_d2_5=("ex24","mean"))
    out["spearman vol vs ex5 / z vs ex5"] = pd.Series({"vol": stats.spearmanr(E.vol, E.ex5, nan_policy="omit")[0],
                                                       "z": stats.spearmanr(E.z, E.ex5, nan_policy="omit")[0]})
    # trades gross vs fee by size
    tr = data["trades"]
    T = pd.concat([tr[c][w] for c in tr for w in tr[c]], ignore_index=True)
    T["eb"] = pd.cut(T.entry_forecast, [-1,0.5,2,5,20.1])
    out["trades by entry forecast"] = T.groupby("eb").agg(n=("net_profit_loss_percent","size"), pl=("profit_loss_percent","mean"),
                                                           net=("net_profit_loss_percent","mean"), dur=("duration_minutes", lambda s: s.mean()/1440))
    return out
