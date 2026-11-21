import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = 120
    rows = []
    drift = {}
    for coin, ws in bars.items():
        # drift per horizon on non-overlapping grid
        d = {}
        for h in (24, 48, 120, 240):
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            d[h] = (np.mean(rs), np.std(rs))
        drift[coin] = d
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
            absm = pd.Series(np.abs(r24)).shift(1).rolling(720, min_periods=120).mean().values
            z = r24 / absm
            cell = np.arange(n) // H
            seen = set()
            for t in np.where(bet)[0]:
                if cell[t] in seen:
                    continue
                seen.add(cell[t])
                rec = {"coin": coin, "w": int(w[1:]), "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                       "f": f[t], "z": z[t], "r168": r168[t], "r24": r24[t],
                       "hour": pd.Timestamp(df["timestamp"].iloc[t]).hour}
                for h in (24, 48, 120, 240):
                    if t + h < n:
                        rec[f"u{h}"] = c[t + h] / c[t] - 1 - d[h][0]
                        rec[f"s{h}"] = rec[f"u{h}"] / d[h][1]
                rows.append(rec)
    X = pd.DataFrame(rows)
    def summ(g):
        u = g["u120"].dropna()
        return pd.Series({"n": len(u), "mean_u120": u.mean(), "t": u.mean() / (u.std() / np.sqrt(len(u))) if len(u) > 2 else np.nan,
                          "strength": g["s120"].mean()})
    out = {}
    out["all"] = summ(X).to_frame().T
    out["by_coin"] = X.groupby("coin").apply(summ)
    out["by_year"] = X.groupby("year").apply(summ)
    X["zq"] = pd.qcut(X["z"], 5, labels=False, duplicates="drop")
    out["by_surge_quintile"] = X.groupby("zq").apply(lambda g: pd.concat([summ(g), pd.Series({"z_med": g["z"].median()})]))
    X["wq"] = pd.qcut(X["r168"], 5, labels=False, duplicates="drop")
    out["by_week_quintile"] = X.groupby("wq").apply(lambda g: pd.concat([summ(g), pd.Series({"r168_med": g["r168"].median()})]))
    hz = {}
    for h in (24, 48, 120, 240):
        u = X[f"u{h}"].dropna()
        hz[h] = {"n": len(u), "mean_u": u.mean(), "t": u.mean() / (u.std() / np.sqrt(len(u))), "strength": X[f"s{h}"].mean()}
    out["by_horizon"] = pd.DataFrame(hz).T
    out["forecast_level"] = X.groupby(pd.cut(X["f"], [0, 5, 10, 15, 20.01])).apply(summ)
    return out
