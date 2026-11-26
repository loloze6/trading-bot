import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    h = 10
    drift = {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            idx = np.arange(0, len(cl) - h, h)
            rs.extend(cl[idx + h] / cl[idx] - 1)
        drift[c] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values; hi = b["high"].values; lo = b["low"].values; op = b["open"].values
            rng = hi - lo
            loc = np.where(rng > 0, (cl - lo) / np.where(rng > 0, rng, 1), np.nan)
            ret1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            f = b["forecast"].fillna(0).values
            n = len(b)
            locs = pd.Series(loc)
            mloc10 = locs.rolling(10, min_periods=5).mean().shift(1).values
            mloc60 = locs.rolling(60, min_periods=20).mean().shift(1).values
            nhigh10 = (locs >= 0.8).astype(float).rolling(10, min_periods=5).sum().shift(1).values
            vol20 = pd.Series(ret1).rolling(20, min_periods=10).std().values
            for i in range(n):
                if i + h >= n: continue
                fp = f[i-1] if i > 0 else 0.0
                if not (f[i] <= -2 and fp - f[i] >= 2): continue
                r5 = cl[i] / cl[i-5] - 1 if i >= 5 else np.nan
                r20 = cl[i] / cl[i-20] - 1 if i >= 20 else np.nan
                rows.append({"coin": c, "win": w, "cell": i // 10, "loc": loc[i], "af": abs(f[i]),
                             "u": -(cl[i+h]/cl[i]-1 - drift[c]),
                             "day": pd.Timestamp(b["timestamp"].iloc[i]).normalize(),
                             "mloc10": mloc10[i], "mloc60": mloc60[i], "nhigh10": nhigh10[i],
                             "rngrel": (rng[i]/cl[i]) / vol20[i] if vol20[i] > 0 else np.nan,
                             "ret1rel": ret1[i] / vol20[i] if vol20[i] > 0 else np.nan,
                             "r5": r5, "r20": r20,
                             "body": (cl[i]-op[i])/rng[i] if rng[i] > 0 else np.nan})
    df = pd.DataFrame(rows)
    cases = df.groupby(["coin", "win", "cell"]).head(1).copy()

    def summ(g, col="u"):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "mean": np.nan, "t_day": np.nan, "days": 0})
        m = g[col].mean()
        dev = g.groupby("day")[col].apply(lambda x: (x - m).sum())
        se = np.sqrt((dev**2).sum()) / len(g)
        return pd.Series({"n": len(g), "mean": m, "t_day": m / se if se > 0 else np.nan, "days": g.day.nunique()})

    out = {}
    out["n_cases"] = len(cases)
    feats = ["loc", "af", "mloc10", "mloc60", "nhigh10", "rngrel", "ret1rel", "r5", "r20", "body"]
    cor = {}
    for ft in feats:
        g = cases[[ft, "u"]].dropna()
        rho, p = stats.spearmanr(g[ft], g["u"])
        cor[ft] = {"spearman": rho, "p": p, "n": len(g)}
    out["spearman_with_u"] = pd.DataFrame(cor).T
    for ft in ["loc", "af", "mloc60", "nhigh10", "rngrel", "ret1rel", "r5", "r20"]:
        g = cases.dropna(subset=[ft]).copy()
        med = g[ft].median()
        hiH = summ(g[g[ft] > med]); loH = summ(g[g[ft] <= med])
        out[f"halves_{ft}"] = pd.DataFrame({"above_median": hiH, "at_or_below": loH}).T
    out["spearman_af_vs_mloc60"] = float(stats.spearmanr(cases.dropna(subset=["mloc60"]).af, cases.dropna(subset=["mloc60"]).mloc60)[0])
    return out
