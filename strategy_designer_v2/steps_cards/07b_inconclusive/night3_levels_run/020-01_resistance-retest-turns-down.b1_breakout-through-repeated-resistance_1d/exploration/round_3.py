import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    drift = {}
    for c in bars:
        for h in [10, 30]:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(list(cl[idx + h] / cl[idx] - 1))
            drift[(c, h)] = np.mean(rs)
    def cases(cellsize):
        rows = []
        for c in bars:
            for w, df in bars[c].items():
                df = df.reset_index(drop=True)
                f = df["forecast"].fillna(0).values
                cl = df["close"].values
                ts = pd.to_datetime(df["timestamp"])
                seen = set()
                for t in range(1, len(df)):
                    if f[t] >= 2 and f[t - 1] < 2:
                        cell = t // cellsize
                        if cell in seen: continue
                        seen.add(cell)
                        r = {"coin": c, "year": ts.iloc[t].year, "fc": f[t]}
                        for h in [10, 30]:
                            if t + h < len(cl):
                                r[f"ex{h}"] = cl[t + h] / cl[t] - 1 - drift[(c, h)]
                        r["past60"] = cl[t] / cl[t - 60] - 1 if t >= 60 else np.nan
                        r["past30"] = cl[t] / cl[t - 30] - 1 if t >= 30 else np.nan
                        rows.append(r)
        return pd.DataFrame(rows)
    def summ(x):
        x = x.dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    d30 = cases(30)
    out["ex30_nonoverlap_all"] = summ(d30["ex30"])
    d30["p60"] = np.sign(d30["past60"])
    out["ex30_nonoverlap_by_p60"] = d30.groupby("p60")["ex30"].apply(summ).unstack()
    out["ex30_nonoverlap_by_year"] = d30.groupby("year")["ex30"].apply(summ).unstack()
    up = d30[d30["p60"] > 0].dropna(subset=["ex30"])
    out["up_spearman_fc_ex30"] = float(stats.spearmanr(up["fc"], up["ex30"])[0]) if len(up) > 5 else np.nan
    up = up.copy(); up["q"] = pd.qcut(up["past60"], 3, labels=False)
    out["up_ex30_by_past60_terc"] = up.groupby("q")["ex30"].apply(summ).unstack()
    out["up_past60_ranges"] = up.groupby("q")["past60"].agg(["min", "max"])
    d10 = cases(10)
    d10["p60"] = np.sign(d10["past60"])
    u10 = d10[d10["p60"] > 0].dropna(subset=["ex10"])
    out["up_spearman_fc_ex10"] = float(stats.spearmanr(u10["fc"], u10["ex10"])[0])
    out["spearman_past60_ex10_all"] = float(stats.spearmanr(d10["past60"], d10["ex10"], nan_policy="omit")[0])
    out["spearman_past60_ex30_nonoverlap"] = float(stats.spearmanr(d30["past60"], d30["ex30"], nan_policy="omit")[0])
    return out
