import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = 7
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - H, H):
                allr.append(c[i+H]/c[i]-1)
        drift[coin] = np.mean(allr) if allr else np.nan
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r30 = c / c.shift(30) - 1
            r7p = c / c.shift(7) - 1
            r1 = c.pct_change()
            vol20 = r1.rolling(20).std()
            fz = b.get("debug_info.components.month_rise.last_history_value")
            ts = pd.to_datetime(b["timestamp"])
            for i in range(0, len(c) - H, H):
                rows.append(dict(coin=coin, w=w, yr=ts[i].year, wd=ts[i].dayofweek,
                    chop=(b["regime"][i] == "unknown"), r30=r30[i], r7p=r7p[i], r1=r1[i],
                    vol=vol20[i], fz=(fz[i] if fz is not None else np.nan),
                    fc=b["forecast"][i], alloc=b["postRebalance_current_allocation"][i],
                    fwd=c[i+H]/c[i]-1, ex=c[i+H]/c[i]-1-drift[coin]))
    d = pd.DataFrame(rows)
    out = {}
    def tab(g):
        return g["ex"].agg(n="count", mean="mean", t=lambda x: x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan)
    dd = d.dropna(subset=["r30"]).copy()
    dd["q30"] = dd.groupby("chop")["r30"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["ex7 by chop x r30 quintile"] = dd.groupby(["chop","q30"]).apply(tab)
    for ch in [True, False]:
        s = dd[dd.chop==ch]
        sl = stats.linregress(s.r30, s.ex)
        out[f"slope ex on r30 chop={ch}"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(s)}"
        neg = s[s.r30<0]; sl2 = stats.linregress(neg.r30, neg.ex)
        out[f"slope neg r30 chop={ch}"] = f"slope {sl2.slope:.4f} t {sl2.slope/sl2.stderr:.2f} n {len(neg)}"
    d7 = d.dropna(subset=["r7p"]).copy()
    d7["q7"] = d7.groupby("chop")["r7p"].transform(lambda x: pd.qcut(x, 5, labels=False))
    out["ex7 by chop x past7d quintile"] = d7.groupby(["chop","q7"]).apply(tab)
    dv = d.dropna(subset=["vol"]).copy()
    dv["qv"] = dv.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    out["ex7 by chop x vol tercile"] = dv.groupby(["chop","qv"]).apply(tab)
    out["ex7 by year (chop only)"] = d[d.chop].groupby("yr").apply(tab)
    # daily-level: next 1d return after large 1d moves, by regime
    drows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True); c = b["close"]; r = c.pct_change()
            z = r / r.rolling(30).std().shift(1)
            nxt = c.shift(-3)/c - 1
            drows.append(pd.DataFrame(dict(z=z, n3=nxt, chop=(b["regime"]=="unknown"), wd=pd.to_datetime(b["timestamp"]).dt.dayofweek, n1=r.shift(-1))))
    D = pd.concat(drows).dropna()
    D = D.iloc[::3]
    D["zq"] = pd.cut(D.z, [-99,-2,-1,1,2,99])
    out["next3d ret by 1d z-move x chop (every 3rd bar)"] = D.groupby(["chop","zq"])["n3"].agg(n="count", mean="mean", t=lambda x: x.mean()/(x.std()/np.sqrt(len(x))))
    out["share chop cells"] = float(d.chop.mean())
    return out
