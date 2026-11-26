import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin mean 7d return over all windows (grid)
        g7 = []
        for w, b in wins.items():
            c = b["close"].values
            for i in range(0, len(c) - 7, 7):
                g7.append(c[i+7]/c[i]-1)
        m7 = np.mean(g7)
        d1 = []
        for w, b in wins.items():
            c = b["close"].reset_index(drop=True)
            r1 = c.pct_change()
            d1.extend(r1.dropna().tolist())
        m1 = np.mean(d1)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            r7 = c / c.shift(7) - 1
            z = r7 / (sd30 * np.sqrt(7))
            f7 = c.shift(-7) / c - 1
            f1 = c.shift(-1) / c - 1
            f3 = c.shift(-3) / c - 1
            inprof = (b["regime"] == "unknown")
            ts = pd.to_datetime(b["timestamp"])
            rng = (b["high"] - b["low"]) / c
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            for i in range(0, len(b) - 7, 7):
                rows.append(dict(coin=coin, win=w, z=z[i], f7x=f7[i]-m7, inprof=inprof[i],
                                 sd=sd30[i]))
            for i in range(1, len(b)-1):
                daily.append(dict(coin=coin, win=w, r1z=r1[i]/sd30[i] if sd30[i] > 0 else np.nan,
                                  f1x=f1[i]-m1, f3x=f3[i]-3*m1 if not np.isnan(f3[i]) else np.nan,
                                  inprof=inprof[i], wd=ts[i].weekday(), r1=r1[i], clo=clo[i],
                                  rng=rng[i]/sd30[i] if sd30[i] > 0 else np.nan))
    G = pd.DataFrame(rows).dropna()
    D = pd.DataFrame(daily)
    out = {}
    def summ(df, col):
        return pd.Series({"n": len(df), "mean": df[col].mean(),
                          "t": df[col].mean()/(df[col].std()/np.sqrt(len(df))) if len(df) > 2 else np.nan})
    G["zq"] = pd.qcut(G["z"], 5, labels=False)
    out["grid7_by_zq_inprof"] = G.groupby(["inprof", "zq"]).apply(lambda d: summ(d, "f7x")).unstack()
    out["grid7_spearman"] = pd.DataFrame({k: [stats.spearmanr(d["z"], d["f7x"])[0], len(d)]
                                          for k, d in G.groupby("inprof")}, index=["rho", "n"])
    out["grid7_spearman_all"] = stats.spearmanr(G["z"], G["f7x"])[0]
    Dd = D.dropna(subset=["r1z", "f1x"])
    Dd["q"] = pd.qcut(Dd["r1z"], 5, labels=False)
    out["d1_next_by_r1q_inprof"] = Dd.groupby(["inprof", "q"]).apply(lambda d: summ(d, "f1x")).unstack()
    out["weekday_r1"] = D.dropna(subset=["r1"]).groupby("wd").apply(lambda d: summ(d.assign(x=d["r1"]-d["r1"].mean()*0+0), "r1"))
    Dc = D.dropna(subset=["clo", "f3x", "rng"])
    Dc["cq"] = pd.qcut(Dc["clo"], 5, labels=False, duplicates="drop")
    out["closeloc_f3"] = Dc.groupby(["inprof", "cq"]).apply(lambda d: summ(d, "f3x")).unstack()
    Dc["rq"] = pd.qcut(Dc["rng"], 5, labels=False, duplicates="drop")
    out["range_f3"] = Dc.groupby("rq").apply(lambda d: summ(d, "f3x"))
    out["share_inprof_days"] = D["inprof"].mean()
    return out
