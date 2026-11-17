import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    cm = {}
    H = [1, 2, 3]
    for coin, wins in bars.items():
        grid = {h: [] for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            for h in H:
                for i in range(0, n - h, h):
                    grid[h].append(c[i + h] / c[i] - 1)
            reg = df["regime"].values
            vr = df["debug_info.components.volratio.last_history_value"].values
            rng = (df["high"] - df["low"]).values
            last = -10
            for i in range(n):
                if reg[i] == "mean_reversion" and i - last >= 3:
                    last = i
                    d = dict(coin=coin, win=w, year=pd.Timestamp(df["timestamp"][i]).year, vr=vr[i],
                             wick=(c[i] - df["low"][i]) / rng[i] if rng[i] > 0 else np.nan)
                    for h in H:
                        d[f"f{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                    # return day1->day3 (from close of next bar)
                    d["f1to3"] = c[i + 3] / c[i + 1] - 1 if i + 3 < n else np.nan
                    rows.append(d)
        cm[coin] = {h: np.mean(grid[h]) for h in H}
    K = pd.DataFrame(rows)
    for h in H:
        K[f"x{h}"] = K[f"f{h}"] - K["coin"].map(lambda c: cm[c][h])
    out = {}

    def slope(d, y="x1", x="vr"):
        d = d[[x, y]].dropna()
        if len(d) < 8:
            return (np.nan, np.nan, len(d), np.nan)
        r = stats.linregress(d[x], d[y])
        rho = stats.spearmanr(d[x], d[y]).correlation
        return (r.slope, r.slope / r.stderr, len(d), rho)

    idx = ["slope", "t", "n", "spearman"]
    out["h1 by coin"] = pd.DataFrame({c: slope(g) for c, g in K.groupby("coin")}, index=idx).T
    out["h1 by year"] = pd.DataFrame({y: slope(g) for y, g in K.groupby("year")}, index=idx).T
    out["pooled slopes"] = pd.DataFrame({y: slope(K, y) for y in ["x1", "x2", "x3", "f1to3"]}, index=idx).T
    Kc = K[K["vr"] <= K["vr"].quantile(0.95)]
    out["pooled slopes vr<=p95"] = pd.DataFrame({y: slope(Kc, y) for y in ["x1", "x2", "x3"]}, index=idx).T
    K["vq"] = pd.qcut(K["vr"], 5, labels=False)
    out["vr quintiles"] = K.groupby("vq")[["vr", "x1", "x2", "x3", "f1to3"]].mean().assign(n=K.groupby("vq").size())
    top = K[K["vq"] == 4]
    out["top quintile x1 t"] = stats.ttest_1samp(top["x1"].dropna(), 0).statistic
    K["half"] = np.where(K["year"] <= 2021, "2018-2021", "2022-2025")
    out["h1 by half"] = pd.DataFrame({y: slope(g) for y, g in K.groupby("half")}, index=idx).T
    return out
