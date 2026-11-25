def explore(data):
    import pandas as pd, numpy as np
    out = {}
    bars = data["bars"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    variants = ["orig", "age5", "age5_fresh", "orig_fresh", "age10"]
    recs = {v: [] for v in variants}
    loss_attr = []
    for w in wins:
        per = {v: [] for v in variants}
        for c in coins:
            if w not in bars[c]: continue
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; n = len(cl)
            al = b["postRebalance_current_allocation"].fillna(0).values
            nxt = np.r_[cl[1:] / cl[:-1] - 1, 0.0]
            isb = np.zeros(n)
            for t in range(20, n):
                isb[t] = 1.0 if cl[t] > hi[t-20:t].max() else 0.0
            nb = np.array([isb[max(0, t-19):t+1].sum() for t in range(n)])
            age = np.zeros(n); a = 0; enb = np.zeros(n); e = 0
            for t in range(n):
                if al[t] != 0:
                    if a == 0: e = nb[t]
                    a += 1
                else:
                    a = 0
                age[t] = a; enb[t] = e
            fresh = enb <= 2
            A = {"orig": al, "age5": np.where(age <= 5, al, 0), "age10": np.where(age <= 10, al, 0),
                 "age5_fresh": np.where((age <= 5) & fresh, al, 0), "orig_fresh": np.where(fresh, al, 0)}
            for v, x in A.items():
                prev = np.r_[0, x[:-1]]
                g = x * nxt - 0.00095 * np.abs(x - prev)
                per[v].append(pd.Series(g))
            loss_attr.append(pd.DataFrame({"win": w, "aged": age > 5, "inpos": al != 0, "g": al * nxt}))
        for v in variants:
            m = pd.concat(per[v], axis=1).mean(axis=1)
            recs[v].append(m)
    res = {}
    for v in variants:
        r = pd.concat(recs[v]).values
        eq = np.cumprod(1 + r); dd = (eq / np.maximum.accumulate(eq) - 1).min()
        yr = eq[-1] ** (365 / len(r)) - 1
        res[v] = {"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": r.mean() / r.std(ddof=1) * np.sqrt(365),
                  "mean": r.mean()}
    out["variants"] = pd.DataFrame(res).T
    L = pd.concat(loss_attr); L = L[L.inpos]
    out["gain_by_win_aged"] = L.groupby(["win", "aged"]).g.sum().unstack()
    return out
