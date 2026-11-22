import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float)
            n = len(c)
            # recompute situation from closes
            brk = np.zeros(n, bool); oldh = np.full(n, np.nan)
            for t in range(20, n):
                m = c[t-20:t].max()
                if c[t] > m:
                    brk[t] = True; oldh[t] = m
            vol = pd.Series(c).pct_change().rolling(20).std().values
            for t in range(0, n - 10, 5):
                b = None
                for k in (1, 2, 3):
                    if t - k >= 0 and brk[t - k]:
                        b = t - k; break
                if b is None or not (c[t] < oldh[b]):
                    continue
                r5 = c[t+5]/c[t]-1; r10 = c[t+10]/c[t]-1
                fromb = c[t]/c[b]-1
                depth = c[t]/oldh[b]-1
                ext = c[b]/oldh[b]-1
                rebreak = (c[t+1:t+11].max() > c[b])
                r60 = c[t]/c[t-60]-1 if t >= 60 else np.nan
                rows.append((coin, w, r5, r10, fromb, depth, ext, rebreak, vol[t], r60))
    d = pd.DataFrame(rows, columns=["coin","w","r5","r10","fromb","depth","ext","rebreak","vol","r60"])
    def summ(g, col="r5"):
        x = -g[col].dropna(); n = len(x)
        return pd.Series({"n": n, "short_tot": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n>2 else np.nan})
    out = {}
    out["all_h5"] = summ(d)
    out["share_rebreak_within10d"] = float(d["rebreak"].mean())
    for col in ["fromb", "ext", "vol", "r60"]:
        x = d.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col].rank(method="first"), 3, labels=["low","mid","high"])
        out[f"h5_by_{col}_tercile"] = x.groupby("q").apply(summ)
        rho, p = stats.spearmanr(x[col], -x["r5"])
        out[f"spearman_{col}_shortret5"] = f"rho={rho:.3f} p={p:.3f} n={len(x)}"
    return out
