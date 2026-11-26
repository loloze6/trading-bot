import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = [1, 3, 7, 14, 21]
    rows = []
    gridstats = {h: [] for h in H}
    for coin, wins in data["bars"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(c)
            for h in H:
                for i in range(0, n - h, h):
                    gridstats[h].append((coin, c[i + h] / c[i] - 1))
            hi7 = df["high"].rolling(7).max(); lo7 = df["low"].rolling(7).min()
            pos = (df["close"] - lo7) / (hi7 - lo7)
            r7b = df["close"] / df["close"].shift(7) - 1
            for i in range(0, n, 7):
                f = df["forecast"].iloc[i]
                if not (f > 0):
                    continue
                rec = {"coin": coin, "win": w, "year": pd.Timestamp(df["timestamp"].iloc[i]).year,
                       "f": f, "pos": pos.iloc[i], "r7back": r7b.iloc[i]}
                for h in H:
                    rec[f"r{h}"] = c[i + h] / c[i] - 1 if i + h < n else np.nan
                rows.append(rec)
    cs = pd.DataFrame(rows)
    means = {h: pd.DataFrame(gridstats[h], columns=["coin", "r"]).groupby("coin")["r"].mean() for h in H}
    for h in H:
        cs[f"x{h}"] = cs[f"r{h}"] - cs["coin"].map(means[h])
    out = {}
    hz = []
    for h in H:
        d = cs.dropna(subset=[f"x{h}"])
        x = d[f"x{h}"]
        sl = stats.linregress(d["f"], x)
        hz.append({"h": h, "n": len(d), "mean_x": x.mean(), "t_mean": x.mean() / (x.std() / np.sqrt(len(x))),
                   "slope_t": sl.slope / sl.stderr, "share_pos": (d[f"r{h}"] > 0).mean()})
    out["by_horizon"] = pd.DataFrame(hz)
    d = cs.dropna(subset=["x7"])
    def agg(g):
        return pd.Series({"n": len(g), "mean_x7": g["x7"].mean(),
                          "t": g["x7"].mean() / (g["x7"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan,
                          "mean_r7": g["r7"].mean()})
    out["by_coin"] = d.groupby("coin").apply(agg)
    out["by_window"] = d.groupby("win").apply(agg)
    out["by_year"] = d.groupby("year").apply(agg)
    d = d.copy()
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_forecast_quartile"] = d.groupby("fq").apply(agg)
    out["forecast_stats"] = d["f"].describe()
    d["r7bq"] = pd.qcut(d["r7back"].rank(method="first"), 3, labels=["low", "mid", "high"])
    out["by_past_week_rise_tercile"] = d.groupby("r7bq").apply(agg)
    return out
