import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [10, 20, 30]
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(list(cl[idx + h] / cl[idx] - 1))
            drift[(c, h)] = np.mean(rs)
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
                    cell = t // 10
                    if cell in seen: continue
                    seen.add(cell)
                    r = {"coin": c, "window": w, "year": ts.iloc[t].year, "fc": f[t], "t_in_win": t}
                    for h in H:
                        if t + h < len(cl):
                            r[f"ex{h}"] = cl[t + h] / cl[t] - 1 - drift[(c, h)]
                    r["past60"] = cl[t] / cl[t - 60] - 1 if t >= 60 else np.nan
                    r["past10"] = cl[t] / cl[t - 10] - 1 if t >= 10 else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g, col):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    out = {}
    out["ex30_by_year"] = d.groupby("year").apply(lambda g: summ(g, "ex30"))
    out["ex30_by_coin"] = d.groupby("coin").apply(lambda g: summ(g, "ex30"))
    d["fq"] = pd.qcut(d["fc"].rank(method="first"), 4, labels=False)
    out["ex30_by_fc_quart"] = d.groupby("fq").apply(lambda g: summ(g, "ex30"))
    out["spearman_fc_ex30"] = float(stats.spearmanr(d["fc"], d["ex30"], nan_policy="omit")[0])
    d["p60"] = np.where(d["past60"].isna(), np.nan, np.sign(d["past60"]))
    out["ex10_by_past60_sign"] = d.groupby("p60").apply(lambda g: summ(g, "ex10"))
    out["ex30_by_past60_sign"] = d.groupby("p60").apply(lambda g: summ(g, "ex30"))
    d["p10q"] = pd.qcut(d["past10"], 3, labels=False)
    out["ex10_by_past10_terc"] = d.groupby("p10q").apply(lambda g: summ(g, "ex10"))
    out["past10_ranges"] = d.groupby("p10q")["past10"].agg(["min", "max"])
    # median-split check at 30
    x = d.dropna(subset=["ex30"]).sort_values("fc")
    n = len(x) // 2
    out["ex30_top_minus_bottom"] = float(x["ex30"].iloc[-n:].mean() - x["ex30"].iloc[:n].mean())
    out["share_pos_ex10"] = float((d["ex10"].dropna() > 0).mean())
    out["ex10_std"] = float(d["ex10"].std())
    return out
