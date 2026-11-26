import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    out = {}
    ev = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            prox = b["debug_info.components.low_prox.last_history_value"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(c)
            D = 1/prox - 1  # in percent
            last = -999
            for i in range(1, n):
                if prox[i] >= 0.9999 and not np.isnan(D[i-1]) and i - last >= 20:
                    Lprev = c[i-1]/(1 + D[i-1]/100.0)
                    depth = c[i]/Lprev - 1
                    r = {}
                    for h in [5, 10, 20]:
                        r[f"f{h}"] = c[i+h]/c[i]-1 if i + h < n else np.nan
                    ev.append(dict(coin=coin, day=ts.iloc[i].normalize(), depth=depth, **r))
                    last = i
    e = pd.DataFrame(ev)
    # drift per horizon from non-overlapping grid
    drift = {}
    for h in [5, 10, 20]:
        v = []
        for coin, wins in data["bars"].items():
            for w, b in wins.items():
                c = b["close"].values
                v += [c[i+h]/c[i]-1 for i in range(0, len(c)-h, h)]
        drift[h] = np.mean(v)
    res = []
    for h in [5, 10, 20]:
        d = e.dropna(subset=[f"f{h}"]).copy()
        d["ex"] = d[f"f{h}"] - drift[h]
        s = stats.linregress(d["depth"], d["ex"]) if len(d) > 3 else None
        sd = d.groupby("day")["ex"].sum()
        res.append(dict(h=h, n=len(d), days=len(sd), mean_ex=d.ex.mean(),
                        t_day=sd.mean()/(sd.std()/np.sqrt(len(sd))),
                        slope_depth=s.slope if s else np.nan, t_slope=(s.slope/s.stderr) if s else np.nan))
    out["first new 365d-low close (20d apart): excess fwd"] = pd.DataFrame(res)
    out["depth quantiles"] = e["depth"].describe()
    # Saturday graded by prior 5-day return
    dd = pd.concat([x.assign(coin=c) for c, ws in data["days"].items() for x in ws.values()])
    dd["day"] = pd.to_datetime(dd["day"])
    rows = []
    for (coin), g in dd.groupby("coin"):
        pass
    parts = []
    for coin, ws in data["days"].items():
        for w, x in ws.items():
            x = x.copy(); x["day"] = pd.to_datetime(x["day"])
            x["p5"] = x["close"]/x["close"].shift(5) - 1
            x["nxt"] = x["coin_return"].shift(-1)
            x["vol20"] = x["coin_return"].rolling(20).std()
            x["coin"] = coin
            parts.append(x)
    a = pd.concat(parts).dropna(subset=["p5", "nxt", "vol20"])
    a["wdn"] = (a["day"] + pd.Timedelta(days=1)).dt.dayofweek
    sat = a[a.wdn == 5].copy()
    s = stats.linregress(sat["p5"], sat["nxt"])
    out["Saturday return on prior 5d return: slope,t,n"] = f"{s.slope:.4f}, {s.slope/s.stderr:.2f}, {len(sat)}"
    sat["vq"] = pd.qcut(sat["vol20"], 3, labels=False)
    g = sat.groupby("vq")["nxt"].agg(["size", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["Saturday return by vol tercile"] = g
    sat["pq"] = pd.qcut(sat["p5"], 3, labels=False)
    g = sat.groupby("pq")["nxt"].agg(["size", "mean", "std"]); g["t"] = g["mean"]/(g["std"]/np.sqrt(g["size"]))
    out["Saturday return by prior-5d tercile"] = g
    # book: Saturday share of book mean
    m = dd.groupby("day").agg(book=("book_return", "mean"), coin=("coin_return", "mean")).dropna()
    m["wd"] = m.index.dayofweek
    out["book by weekday sum share"] = (m.groupby("wd")["book"].sum()/m["book"].sum())
    return out
