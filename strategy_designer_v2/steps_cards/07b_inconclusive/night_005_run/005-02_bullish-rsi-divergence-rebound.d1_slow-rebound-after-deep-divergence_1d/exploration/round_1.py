import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    mean_ret = {}
    Hs = [1,5,10,20,40]
    for coin in bars:
        for H in Hs:
            r = []
            for w, df in bars[coin].items():
                c = df["close"].values
                for i in range(0, len(c)-H, H):
                    r.append(c[i+H]/c[i]-1)
            mean_ret[(coin,H)] = np.mean(r)
        for w, df in bars[coin].items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            last = -999
            for i in range(n):
                if f[i] > 0 and i > last + 20 and i + 20 < n:
                    last = i
                    d = {"coin": coin, "window": w, "year": ts.iloc[i].year, "fc": f[i]}
                    for H in Hs:
                        d[f"x{H}"] = (c[i+H]/c[i]-1 - mean_ret[(coin,H)]) if i+H < n else np.nan
                    # trend context: 90-bar return within window
                    d["r90"] = c[i]/c[i-90]-1 if i >= 90 else np.nan
                    d["rg"] = df["debug_info.components.rsi_gap.last_history_value"].iloc[i]
                    d["fall"] = df["debug_info.components.fall30.last_history_value"].iloc[i]
                    rows.append(d)
    ev = pd.DataFrame(rows)
    def summ(g):
        out = {}
        for H in Hs:
            x = g[f"x{H}"].dropna()
            out[f"m{H}"] = x.mean()
            out[f"t{H}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan
        out["n"] = len(g)
        return pd.Series(out)
    res = {}
    res["all"] = summ(ev)
    res["by coin"] = ev.groupby("coin").apply(summ)
    res["by year"] = ev.groupby("year").apply(summ)
    ev["fcq"] = pd.qcut(ev["fc"], 3, labels=["lo","mid","hi"])
    res["by forecast tercile"] = ev.groupby("fcq").apply(summ)
    ev["trend"] = np.where(ev["r90"].isna(), "na", np.where(ev["r90"] > 0, "up90", "down90"))
    res["by 90d trend"] = ev.groupby("trend").apply(summ)
    ev["fallq"] = pd.qcut(ev["fall"].rank(method="first"), 3, labels=["lo","mid","hi"])
    res["by fall raw tercile (raw pct change)"] = ev.groupby("fallq").apply(summ)
    ev["rgq"] = pd.qcut(ev["rg"].rank(method="first"), 3, labels=["lo","mid","hi"])
    res["by rsi gap tercile"] = ev.groupby("rgq").apply(summ)
    res["spearman fall raw vs x20"] = stats.spearmanr(ev["fall"], ev["x20"], nan_policy="omit")[0]
    res["spearman rg vs x20"] = stats.spearmanr(ev["rg"], ev["x20"], nan_policy="omit")[0]
    res["spearman r90 vs x20"] = stats.spearmanr(ev["r90"], ev["x20"], nan_policy="omit")[0]
    res["fall raw describe"] = ev["fall"].describe()
    return res
