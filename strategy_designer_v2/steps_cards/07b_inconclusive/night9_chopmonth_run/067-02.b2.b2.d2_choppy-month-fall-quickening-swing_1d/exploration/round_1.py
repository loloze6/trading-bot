import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        # coin mean returns per horizon over all visible windows, non-overlapping grid
        means = {}
        for h in (3, 5, 10, 20):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                for i in range(0, len(c) - h, h):
                    rs.append(c[i + h] / c[i] - 1)
            means[h] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].values
            ts = pd.to_datetime(df["timestamp"])
            r = pd.Series(c).pct_change()
            sd30 = r.rolling(30).std().values
            sd10 = r.rolling(10).std().values
            ret30 = pd.Series(c).pct_change(30).values
            for i in range(0, len(c) - 10, 10):
                if not (f[i] < 0):
                    continue
                d = {"coin": coin, "win": w, "year": ts[i].year, "day": ts[i].normalize(),
                     "f": f[i], "ret30": ret30[i], "vr": sd10[i] / sd30[i] if sd30[i] else np.nan}
                for h in (3, 5, 10, 20):
                    if i + h < len(c):
                        d[f"ex{h}"] = -(c[i + h] / c[i] - 1 - means[h])
                        d[f"tot{h}"] = -(c[i + h] / c[i] - 1)
                rows.append(d)
    X = pd.DataFrame(rows)
    out = {}
    def tday(s, days):
        g = s.groupby(days).sum()
        return pd.Series({"mean": s.mean(), "n": len(s), "days": len(g),
                          "t_day": g.mean() / (g.std(ddof=1) / np.sqrt(len(g))) if len(g) > 2 else np.nan})
    out["by_horizon"] = pd.DataFrame({h: tday(X[f"ex{h}"].dropna(), X.loc[X[f"ex{h}"].notna(), "day"]) for h in (3, 5, 10, 20)}).T
    out["by_horizon_total"] = pd.DataFrame({h: tday(X[f"tot{h}"].dropna(), X.loc[X[f"tot{h}"].notna(), "day"]) for h in (3, 5, 10, 20)}).T
    out["by_coin_ex10"] = X.groupby("coin")["ex10"].agg(["mean", "count", "median"])
    out["by_year_ex10"] = X.groupby("year")["ex10"].agg(["mean", "count", "median"])
    X["fq"] = pd.qcut(-X["f"], 3, labels=["weak", "mid", "strong"])
    out["by_forecast_tercile"] = X.groupby("fq")[["ex5", "ex10", "ex20", "f"]].mean()
    X["vrq"] = pd.qcut(X["vr"], 3, labels=["low", "mid", "high"])
    out["by_vr_tercile"] = X.groupby("vrq")[["ex5", "ex10", "ex20", "vr"]].mean()
    out["share_positive_ex10"] = float((X["ex10"] > 0).mean())
    out["ex10_quantiles"] = X["ex10"].quantile([.05, .25, .5, .75, .95])
    out["corr_f_ex10"] = float(np.corrcoef(-X["f"], X["ex10"])[0, 1])
    return out
