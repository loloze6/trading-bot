import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        allr = {h: [] for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            n = len(c)
            for h in H:
                idx = np.arange(0, n - h, h)
                allr[h] += list(c[idx + h] / c[idx] - 1)
            lr = pd.Series(np.log(c)).diff()
            sd = lr.rolling(30).std().values
            r3 = np.full(n, np.nan); r3[3:] = c[3:] / c[:-3] - 1
            inprof = (df["regime"].astype(str) == "unknown").values
            fc = df["forecast"].astype(float).values
            for i in range(0, n, 5):
                if not inprof[i] or not np.isfinite(sd[i]) or not (r3[i] > 0):
                    continue
                rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "z": r3[i] / (sd[i] * np.sqrt(3)), "r3": r3[i], "fc": fc[i],
                       "day": i}
                for h in H:
                    rec[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
        drift[coin] = {h: np.mean(allr[h]) for h in H}
    d = pd.DataFrame(rows)
    for h in H:
        d[f"u{h}"] = -(d[f"f{h}"] - d["coin"].map(lambda k: drift[k][h]))
    out = {}
    def summ(g):
        res = {"n": len(g)}
        for h in H:
            x = g[f"u{h}"].dropna()
            res[f"u{h}_mean%"] = 100 * x.mean()
            res[f"u{h}_t"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(res)
    out["all"] = summ(d)
    d["zq"] = pd.qcut(d["z"], 4, labels=["q1", "q2", "q3", "q4"])
    out["by_z_quartile"] = d.groupby("zq").apply(summ)
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_window"] = d.groupby("win").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["corr_z_u5"] = stats.spearmanr(d["z"], d["u5"], nan_policy="omit")[0]
    out["corr_z_u1"] = stats.spearmanr(d["z"], d["u1"], nan_policy="omit")[0]
    out["forecast_nonzero_share"] = float((d["fc"] < 0).mean())
    out["z_quartile_bounds"] = d["z"].quantile([.25, .5, .75])
    return out
