import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        for h in (1, 3, 5, 10):
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                n = len(c)
                for i in range(0, n - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs))
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            for i in range(0, n - 5, 5):
                if reg[i] != "unknown":
                    continue
                r = {"coin": coin, "w": w, "year": ts.iloc[i].year, "day": ts.iloc[i].normalize(), "f": f[i]}
                for h in (1, 3, 5, 10):
                    if i + h < n:
                        m, s = drift[(coin, h)]
                        r["ex%d" % h] = c[i + h] / c[i] - 1 - m
                        r["st%d" % h] = r["ex%d" % h] / s
                # past 5-day return
                if i >= 5:
                    r["past5"] = c[i] / c[i - 5] - 1
                rows.append(r)
    d = pd.DataFrame(rows)
    out = {}
    neg = d[d.f < 0].copy()
    out["counts"] = pd.Series({"profile_grid": len(d), "neg": len(neg), "zero": (d.f == 0).sum()})

    def summ(g, col="ex5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean_ex": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    # short-direction unusual move by horizon
    hz = {}
    for h in (1, 3, 5, 10):
        x = -neg["ex%d" % h].dropna()
        hz[h] = {"n": len(x), "short_unusual": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))),
                 "slope_t": stats.linregress(neg.dropna(subset=["ex%d" % h])["f"], neg["ex%d" % h].dropna()).slope / stats.linregress(neg.dropna(subset=["ex%d" % h])["f"], neg["ex%d" % h].dropna()).stderr}
    out["by_horizon_neg"] = pd.DataFrame(hz).T
    # forecast quintiles across all profile bars (incl zero)
    neg["q"] = pd.qcut(neg["f"], 4, labels=["strongest", "q2", "q3", "weakest"])
    out["neg_by_quartile"] = neg.groupby("q").apply(lambda g: pd.Series({"n": len(g), "f": g.f.mean(), "ex5": g.ex5.mean(), "ex10": g.ex10.mean(), "t5": summ(g)["t"]}))
    out["zero_vs_neg"] = pd.DataFrame({"zero": summ(d[d.f == 0]), "neg": summ(neg)})
    out["neg_by_coin"] = neg.groupby("coin").apply(summ)
    out["neg_by_year"] = neg.groupby("year").apply(summ)
    out["neg_by_window"] = neg.groupby("w").apply(summ)
    # all profile bars: past5 scaled? use past5 quintiles
    dd = d.dropna(subset=["past5", "ex5"]).copy()
    dd["pq"] = pd.qcut(dd["past5"], 5, labels=False)
    out["profile_by_past5_quintile"] = dd.groupby("pq").apply(lambda g: pd.Series({"n": len(g), "past5": g.past5.mean(), "ex5": g.ex5.mean(), "ex10": g.ex10.mean(), "t5": summ(g)["t"]}))
    return out
