import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    H = [1, 2, 3, 5, 8, 10]
    rows = []
    drift = {}
    for coin, wins in data["bars"].items():
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1)) if rs else (np.nan, np.nan)
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=30).std()
            r3 = c / c.shift(3) - 1
            sc = r3 / sd
            inprof = (b["regime"] == "unknown").values
            for h in H:
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    if not inprof[i] or not np.isfinite(sc.iloc[i]) or not np.isfinite(fwd.iloc[i]):
                        continue
                    if sc.iloc[i] <= 0:
                        side = "fall"
                    else:
                        side = "rise"
                    mu, s = drift[(coin, h)]
                    ex = fwd.iloc[i] - mu
                    rows.append(dict(coin=coin, w=w, h=h, sc=sc.iloc[i], side=side,
                                     ex=ex, tot=fwd.iloc[i], strength=-ex / s,
                                     day=str(b["timestamp"].iloc[i])[:10],
                                     year=str(b["timestamp"].iloc[i])[:4], fc=b["forecast"].iloc[i]))
    df = pd.DataFrame(rows)
    out = {}
    def summ(g):
        n = len(g)
        m = g["ex"].mean()
        t = m / (g["ex"].std(ddof=1) / np.sqrt(n)) if n > 2 else np.nan
        rho = stats.spearmanr(g["sc"], g["ex"])[0] if n > 5 else np.nan
        return pd.Series(dict(n=n, days=g["day"].nunique(), short_excess=-m, t_short=-t,
                              short_total=-g["tot"].mean(), strength=g["strength"].mean(), spearman_sc_ex=rho))
    out["by_h_side"] = df.groupby(["h", "side"]).apply(summ)
    r = df[df.side == "rise"].copy()
    r["q"] = r.groupby("h")["sc"].transform(lambda x: pd.qcut(x, 4, labels=False, duplicates="drop"))
    out["rise_by_h_quartile"] = r.groupby(["h", "q"]).apply(summ)
    r5 = r[r.h == 5]
    out["rise5_by_coin"] = r5.groupby("coin").apply(summ)
    out["rise5_by_window"] = r5.groupby("w").apply(summ)
    out["rise5_by_year"] = r5.groupby("year").apply(summ)
    out["rise5_fc_neg_vs_zero"] = r5.groupby(r5["fc"] < 0).apply(summ)
    return out
