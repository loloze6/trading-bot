import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    def drift(coin, h):
        r = []
        for w, df in bars[coin].items():
            c = df["close"].values
            for i in range(0, len(c) - h, h):
                r.append(c[i + h] / c[i] - 1)
        return np.mean(r), np.std(r)
    rows = []
    for h in [5, 10]:
        for coin in bars:
            d, sd = drift(coin, h)
            for w, df in bars[coin].items():
                c = df["close"].values; f = df["forecast"].values
                ts = pd.to_datetime(df["timestamp"]).values
                ret1 = df["close"].pct_change()
                v10 = ret1.rolling(10).std().values
                v30 = ret1.rolling(30).std().values
                v5 = ret1.rolling(5).std().values
                for i in range(0, len(c) - h, h):
                    if f[i] == 0 or np.isnan(f[i]): continue
                    r = c[i + h] / c[i] - 1
                    rows.append(dict(h=h, coin=coin, w=w, ts=ts[i], f=f[i],
                                     prod=f[i] / 10 * (r - d), sx=np.sign(f[i]) * (r - d),
                                     z=np.sign(f[i]) * (r - d) / sd,
                                     ag=v10[i] / v30[i] if v30[i] > 0 else np.nan,
                                     ag5=v5[i] / v30[i] if v30[i] > 0 else np.nan,
                                     year=pd.Timestamp(ts[i]).year))
    D = pd.DataFrame(rows)
    def summ(g):
        n = len(g); m = g["prod"].mean()
        dev = (g["prod"] - m).groupby(g["ts"]).sum(); J = len(dev)
        se = np.sqrt((dev**2).sum() * J / (J - 1)) / n if J > 1 else np.nan
        mz = g["z"].mean()
        devz = (g["z"] - mz).groupby(g["ts"]).sum()
        sez = np.sqrt((devz**2).sum() * J / (J - 1)) / n if J > 1 else np.nan
        return pd.Series(dict(n=n, days=J, mean_prod=m, t=m / se if se else np.nan,
                              mean_z=mz, t_z=mz / sez if sez else np.nan))
    out = {}
    D10 = D[D.h == 10].dropna(subset=["ag"]).copy()
    D10["agq"] = pd.qcut(D10.ag, 3, labels=["low", "mid", "high"])
    out["h10_ag_terciles"] = D10.groupby("agq").apply(summ)
    D10["agh"] = np.where(D10.ag > D10.ag.median(), "agit", "calm")
    D10["side"] = np.where(D10.f > 0, "long", "short")
    out["h10_ag_side"] = D10.groupby(["agh", "side"]).apply(summ)
    out["h10_ag_year"] = D10.groupby(["agh", "year"]).apply(summ)
    A = D10[D10.agh == "agit"].copy()
    A["fq"] = pd.qcut(A.f.abs(), 2, labels=["small", "large"])
    out["h10_agit_by_absf"] = A.groupby("fq").apply(summ)
    D5 = D[D.h == 5].dropna(subset=["ag"]).copy()
    D5["agh"] = np.where(D5.ag > D5.ag.median(), "agit", "calm")
    out["h5_ag"] = D5.groupby("agh").apply(summ)
    D10["ag5h"] = np.where(D10.ag5 > D10.ag5.median(), "agit5", "calm5")
    out["h10_ag5"] = D10.groupby("ag5h").apply(summ)
    out["corr_ag_vs_absf"] = float(np.corrcoef(D10.ag, D10.f.abs())[0, 1])
    # welch agit minus calm on sx
    a = D10[D10.agh == "agit"].sx; b = D10[D10.agh == "calm"].sx
    out["welch_agit_minus_calm_sx"] = float(stats.ttest_ind(a, b, equal_var=False).statistic)
    return out
