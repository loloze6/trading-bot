import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        g = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                g[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: (np.mean(g[h]) if len(g[h]) else np.nan) for h in H}
        drift[coin].update({f"sd{h}": (np.std(g[h], ddof=1) if len(g[h]) > 1 else np.nan) for h in H})
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            n = len(df)
            ts = pd.to_datetime(df["timestamp"])
            r = c.pct_change()
            sd20 = r.rolling(20).std()
            z = (c / c.shift(5) - 1) / (sd20 * np.sqrt(5))
            r20 = c / c.shift(20) - 1
            r60 = c / c.shift(60) - 1
            vol30 = r.rolling(30).std()
            fc = df["forecast"].values
            seen = set()
            for t in range(n):
                if fc[t] >= 0:
                    continue
                cell = t // 5
                if cell in seen or t + 5 >= n:
                    continue
                seen.add(cell)
                d = {"coin": coin, "win": w, "year": ts[t].year, "day": ts[t].normalize(),
                     "fc": fc[t], "z": z[t], "r20": r20[t], "r60": r60[t], "vol30": vol30[t],
                     "sd20": sd20[t]}
                for h in H:
                    if t + h < n:
                        d[f"u{h}"] = -((c[t + h] / c[t] - 1) - drift[coin][h])
                        d[f"s{h}"] = d[f"u{h}"] / drift[coin][f"sd{h}"]
                    else:
                        d[f"u{h}"] = np.nan; d[f"s{h}"] = np.nan
                rows.append(d)
    X = pd.DataFrame(rows)

    def tclus(sub, col):
        s = sub.dropna(subset=[col])
        if len(s) < 5:
            return pd.Series({"n": len(s), "mean": np.nan, "t": np.nan, "days": np.nan})
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        D = len(dev)
        se = np.sqrt((dev ** 2).sum() * D / (D - 1)) / len(s) if D > 1 else np.nan
        return pd.Series({"n": len(s), "mean": m, "t": m / se, "days": D})

    out = {}
    out["horizons"] = pd.DataFrame({h: tclus(X, f"u{h}") for h in H}).T
    out["by_year_u5"] = X.groupby("year").apply(lambda s: tclus(s, "u5"))
    out["by_coin_u5"] = X.groupby("coin").apply(lambda s: tclus(s, "u5"))
    out["by_window_u5"] = X.groupby("win").apply(lambda s: tclus(s, "u5"))
    X["fcq"] = pd.qcut(-X["fc"], 4, labels=False, duplicates="drop")
    out["by_fc_quart_u5"] = X.groupby("fcq").apply(lambda s: tclus(s, "u5"))
    X["zq"] = pd.qcut(-X["z"], 4, labels=False, duplicates="drop")
    out["by_rawz_quart_u5"] = X.groupby("zq").apply(lambda s: tclus(s, "u5"))
    out["by_rawz_quart_u10"] = X.groupby("zq").apply(lambda s: tclus(s, "u10"))
    X["r20q"] = pd.qcut(-X["r20"], 4, labels=False, duplicates="drop")
    out["by_r20_quart_u5"] = X.groupby("r20q").apply(lambda s: tclus(s, "u5"))
    X["r60s"] = np.sign(X["r60"])
    out["by_r60sign_u5"] = X.groupby("r60s").apply(lambda s: tclus(s, "u5"))
    X["volq"] = pd.qcut(X["vol30"], 3, labels=False, duplicates="drop")
    out["by_vol30_terc_u5"] = X.groupby("volq").apply(lambda s: tclus(s, "u5"))
    out["slope_u5_on_rawz"] = float(stats.linregress(-X.dropna(subset=["z","u5"])["z"], X.dropna(subset=["z","u5"])["u5"]).slope)
    out["n_total"] = len(X)
    return out
