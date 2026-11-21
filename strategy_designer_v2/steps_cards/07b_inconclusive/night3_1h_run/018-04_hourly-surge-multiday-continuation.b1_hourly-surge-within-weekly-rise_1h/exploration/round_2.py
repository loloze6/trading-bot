import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 120
    rows = []
    for coin, ws in bars.items():
        rs = []
        for w, df in ws.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            rs.extend(c[idx + H] / c[idx] - 1)
        dm, ds = np.mean(rs), np.std(rs)
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            fprev = np.r_[0, f[:-1]]
            bet = (f - fprev) >= 2
            s = pd.Series(c)
            r24 = s.pct_change(24).values
            r168 = s.pct_change(168).values
            r720 = s.pct_change(720).values
            r1440 = s.pct_change(1440).values
            absm = pd.Series(np.abs(r24)).shift(1).rolling(720, min_periods=120).mean().values
            absw = pd.Series(np.abs(r168)).shift(1).rolling(1440, min_periods=240).mean().values
            z = r24 / absm
            cell = np.arange(n) // H
            seen = set()
            for t in np.where(bet)[0]:
                if cell[t] in seen:
                    continue
                seen.add(cell[t])
                if t + H >= n:
                    continue
                u = c[t + H] / c[t] - 1 - dm
                rows.append({"coin": coin, "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                             "z": z[t], "r168": r168[t], "wz": r168[t] / absw[t] if absw[t] > 0 else np.nan,
                             "r720": r720[t], "r1440": r1440[t], "u": u, "s": u / ds})
    X = pd.DataFrame(rows)
    def summ(g):
        u = g["u"].dropna()
        k = len(u)
        return pd.Series({"n": k, "mean_u": u.mean(), "t": u.mean() / (u.std() / np.sqrt(k)) if k > 2 else np.nan,
                          "strength": g["s"].mean()})
    out = {}
    X["zhi"] = X["z"] >= X["z"].quantile(0.8)
    X["whi"] = X["r168"] >= X["r168"].quantile(0.8)
    out["surge_x_week"] = X.groupby(["zhi", "whi"]).apply(summ)
    out["by_30d_sign"] = X.groupby(X["r720"] > 0).apply(summ)
    out["by_60d_sign"] = X.groupby(X["r1440"] > 0).apply(summ)
    X["m60q"] = pd.qcut(X["r1440"], 5, labels=False, duplicates="drop")
    out["by_60d_quintile"] = X.groupby("m60q").apply(lambda g: pd.concat([summ(g), pd.Series({"r1440_med": g["r1440"].median()})]))
    X["wzq"] = pd.qcut(X["wz"], 5, labels=False, duplicates="drop")
    out["by_weekz_quintile"] = X.groupby("wzq").apply(lambda g: pd.concat([summ(g), pd.Series({"wz_med": g["wz"].median()})]))
    top = X[X["zhi"]]
    out["top_surge_by_coin"] = top.groupby("coin").apply(summ)
    out["top_surge_by_year"] = top.groupby("year").apply(summ)
    out["top_surge_by_60d_sign"] = top.groupby(top["r1440"] > 0).apply(summ)
    out["corr_spearman"] = pd.DataFrame({k: [stats.spearmanr(X[k], X["u"], nan_policy="omit")[0]] for k in ["z", "r168", "wz", "r720", "r1440"]})
    out["year_60d_pos_share"] = X.groupby("year").apply(lambda g: pd.Series({"share_60d_pos": (g["r1440"] > 0).mean(), "mean_u": g["u"].mean()}))
    return out
