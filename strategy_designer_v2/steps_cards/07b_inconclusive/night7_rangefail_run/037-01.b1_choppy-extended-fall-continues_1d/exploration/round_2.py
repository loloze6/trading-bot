import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    drift = {}
    for coin, wins in bars.items():
        g = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                g[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(g[h]) for h in H}
        drift[coin].update({f"sd{h}": np.std(g[h], ddof=1) for h in H})
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]; n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            z = (c / c.shift(5) - 1) / (sd20 * np.sqrt(5))
            vol30 = r.rolling(30).std()
            volrel = vol30 / vol30.expanding(30).median()
            r5 = c / c.shift(5) - 1
            fc = df["forecast"].values
            seen = set(); last_min = 0.0; prev = 0.0
            for t in range(n):
                f = fc[t]
                if f >= 0:
                    last_min = 0.0; prev = f; continue
                if prev >= 0:
                    last_min = 0.0
                newbet = f <= last_min - 2
                if newbet:
                    last_min = f
                else:
                    last_min = min(last_min, f) if False else last_min
                prev = f
                cell = t // 5
                if not newbet or cell in seen or t + 5 >= n:
                    continue
                seen.add(cell)
                d = {"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(),
                     "fc": f, "z": z[t], "volrel": volrel[t], "r5": r5[t]}
                for h in H:
                    if t + h < n:
                        d[f"u{h}"] = -((c[t + h] / c[t] - 1) - drift[coin][h])
                        d[f"tot{h}"] = -(c[t + h] / c[t] - 1)
                    else:
                        d[f"u{h}"] = np.nan; d[f"tot{h}"] = np.nan
                rows.append(d)
    X = pd.DataFrame(rows)

    def tclus(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return pd.Series({"n": len(s), "mean": np.nan, "median": np.nan, "t": np.nan, "days": np.nan})
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(s)
        return pd.Series({"n": len(s), "mean": m, "median": s[col].median(), "t": m / se, "days": D})

    out = {}
    out["step5cases_horizons_u"] = pd.DataFrame({h: tclus(X, f"u{h}") for h in H}).T
    out["step5cases_horizons_total"] = pd.DataFrame({h: tclus(X, f"tot{h}") for h in H}).T
    out["by_window_u5"] = X.groupby("win").apply(lambda s: tclus(s, "u5"))
    out["by_year_u5"] = X.groupby("year").apply(lambda s: tclus(s, "u5"))
    Xs = X[X["win"] != "w16"]
    out["excl_w16_u5"] = tclus(Xs, "u5")
    lo, hi = X["u5"].quantile([0.025, 0.975])
    Xw = X.copy(); Xw["u5w"] = Xw["u5"].clip(lo, hi)
    out["winsor_u5"] = tclus(Xw, "u5w")
    X["agit"] = np.where(X["volrel"] > 1, "agitated", np.where(X["volrel"].notna(), "calm", "na"))
    out["by_agit_u5"] = X.groupby("agit").apply(lambda s: tclus(s, "u5"))
    out["by_agit_u10"] = X.groupby("agit").apply(lambda s: tclus(s, "u10"))
    X["zq"] = pd.qcut(-X["z"], 3, labels=False, duplicates="drop")
    out["by_z_terc_u5"] = X.groupby("zq").apply(lambda s: tclus(s, "u5"))
    X["fq"] = pd.qcut(-X["fc"], 3, labels=False, duplicates="drop")
    out["by_fc_terc_u5"] = X.groupby("fq").apply(lambda s: tclus(s, "u5"))
    s = X.dropna(subset=["z", "u5"])
    out["slope_u5_on_negz"] = float(stats.linregress(-s["z"], s["u5"]).slope)
    out["slope_u5_on_absfc"] = float(stats.linregress(-s["fc"], s["u5"]).slope)
    return out
