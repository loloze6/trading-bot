def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    cm = {}
    for coin, wins in data["bars"].items():
        x = pd.concat([(b["close"].shift(-1)/b["close"]-1) for b in wins.values()])
        cm[coin] = x.mean()
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].values; n = len(c)
            tr = (b["regime"] == "trending").values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            vr = (pd.Series(v).rolling(10).mean() / pd.Series(v).rolling(90, min_periods=30).mean()).values
            vr5 = (pd.Series(v).rolling(5).mean() / pd.Series(v).rolling(90, min_periods=30).mean()).values
            last = -999; vrb = np.nan
            for t in range(n - 1):
                if tr[t] and (t == 0 or not tr[t-1]):
                    last = t; vrb = vr[t]
                k = t - last
                if 0 <= k <= 29:
                    rows.append(dict(coin=coin, w=w, k=k, vrb=vrb, vr5=vr5[t],
                                     ex1=c[t+1]/c[t]-1-cm[coin], r1=c[t+1]/c[t]-1, inpos=abs(alloc[t]) > 1e-9))
    R = pd.DataFrame(rows).dropna(subset=["vrb"])
    R["vq"] = pd.qcut(R["vrb"], 3, labels=["light", "mid", "heavy"])
    g = R.groupby("vq", observed=True)["ex1"]
    out["30d post-break daily excess by break volume ratio"] = pd.DataFrame({"mean vr": R.groupby("vq", observed=True)["vrb"].mean(),
        "mean ex1": g.mean(), "n": g.size(), "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    R["kb"] = pd.cut(R["k"], [-1, 2, 10, 29])
    h = R.groupby(["vq", "kb"], observed=True)["ex1"]
    out["by volume tercile and days since break"] = pd.DataFrame({"mean ex1": h.mean(), "n": h.size(),
        "t": h.mean()/(h.std()/np.sqrt(h.size()))})
    # held vs out bars among post-break, held share by tercile
    out["held share by tercile"] = R.groupby("vq", observed=True)["inpos"].mean()
    # simple 30-day hold book stats on post-break bars, unit position
    r = R["r1"]
    out["unit 30d-hold on post-break bars"] = pd.Series({"mean r1": r.mean(), "std": r.std(),
        "sharpe ann (on held days)": r.mean()/r.std()*np.sqrt(365), "n": len(r),
        "share of all bars": len(r) / sum(len(b) for ws in data["bars"].values() for b in ws.values())})
    return out
