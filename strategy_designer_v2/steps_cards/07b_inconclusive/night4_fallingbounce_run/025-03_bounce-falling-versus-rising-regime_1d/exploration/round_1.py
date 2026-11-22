import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    base = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(allr[h]) for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            # unconditional baseline on 5-grid
            for s in range(0, n - 5, 5):
                base.append(dict(coin=coin, reg=reg[s], r5=c[s+5]/c[s]-1 - drift[coin][5]))
            for s in range(0, n, 5):
                cell = range(s, min(s + 5, n))
                hit = [i for i in cell if abs(f[i]) >= 2]
                if not hit:
                    continue
                i = hit[0]
                rec = dict(coin=coin, win=w, year=ts[i].year, f=f[i], side=np.sign(f[i]))
                for h in H:
                    if i + h < n:
                        rec[f"x{h}"] = c[i+h]/c[i]-1 - drift[coin][h]
                    else:
                        rec[f"x{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    b = pd.DataFrame(base)
    def gap(g, col="x5"):
        L = g.loc[g.side > 0, col].dropna(); S = g.loc[g.side < 0, col].dropna()
        if len(L) < 5 or len(S) < 5:
            return pd.Series(dict(nL=len(L), nS=len(S)))
        t = stats.ttest_ind(L, S, equal_var=False).statistic
        return pd.Series(dict(nL=len(L), nS=len(S), meanL=L.mean(), tL=L.mean()/L.std()*np.sqrt(len(L)),
                              meanS=S.mean(), tS=S.mean()/S.std()*np.sqrt(len(S)), gap=L.mean()-S.mean(), t=t))
    out = {}
    out["by_horizon"] = pd.DataFrame({h: gap(d, f"x{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(gap)
    out["by_year"] = d.groupby("year").apply(gap)
    d["fq"] = d.groupby("side")["f"].transform(lambda s: pd.qcut(s.abs().rank(method="first"), 3, labels=["lo","mid","hi"]))
    out["by_forecast_tercile"] = d.groupby("fq").apply(gap)
    out["by_forecast_tercile_h10"] = d.groupby("fq").apply(lambda g: gap(g, "x10"))
    bb = b.groupby("reg")["r5"].agg(["count", "mean", "std"])
    bb["t"] = bb["mean"] / bb["std"] * np.sqrt(bb["count"])
    out["baseline_all_bars_by_regime"] = bb
    out["forecast_abs_quantiles"] = d["f"].abs().describe()
    return out
