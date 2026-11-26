import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10]
    rows = []
    drift = {}
    for coin, wins in bars.items():
        # normal drift and usual move per horizon: non-overlapping grid, all windows
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs += list(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = (np.mean(rs), np.std(rs, ddof=1))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            lo, hi, cl, op = b["low"].values, b["high"].values, b["close"].values, b["open"].values
            L = pd.Series(lo).rolling(30).min().shift(1).values
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for t in range(30, n):
                ev = (lo[t] < L[t]) and (cl[t] >= L[t])
                inprof = b["regime"].iloc[t] != "chop"
                r = {"coin": coin, "w": w, "t": t, "ev": ev, "prof": inprof,
                     "depth": (L[t] - lo[t]) / L[t] * 100 if ev else 0.0,
                     "clpos": (cl[t] - lo[t]) / (hi[t] - lo[t]) if hi[t] > lo[t] else np.nan,
                     "up": cl[t] > op[t],
                     "year": ts.iloc[t].year, "day": ts.iloc[t].normalize()}
                for h in H:
                    if t + h < n:
                        m, s = drift[(coin, h)]
                        r[f"u{h}"] = cl[t + h] / cl[t] - 1 - m
                    else:
                        r[f"u{h}"] = np.nan
                rows.append(r)
    df = pd.DataFrame(rows)

    def summ(g, h):
        x = g.dropna(subset=[f"u{h}"])
        # one per coin-window grid cell of h
        x = x.assign(cell=x["t"] // h).drop_duplicates(["coin", "w", "cell"])
        d = x.groupby("day")[f"u{h}"].sum()
        G = len(d)
        if len(x) < 3 or G < 2:
            return pd.Series({"n": len(x), "days": G, "mean_long": np.nan, "t": np.nan})
        mean = x[f"u{h}"].mean()
        se = np.sqrt((d - d.mean() * 0).pow(2).sum() * 0 + ((x.groupby("day")[f"u{h}"].sum() - x.groupby("day")[f"u{h}"].count() * mean) ** 2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean_long": mean, "t": mean / se})

    out = {}
    evp = df[df.ev & df.prof]
    evall = df[df.ev]
    base = df[df.prof & ~df.ev]
    out["events_in_profile_by_h"] = pd.DataFrame({h: summ(evp, h) for h in H}).T
    out["events_all_profiles_by_h"] = pd.DataFrame({h: summ(evall, h) for h in H}).T
    out["ordinary_profile_days_by_h"] = pd.DataFrame({h: summ(base, h) for h in H}).T
    out["events_outside_profile_by_h"] = pd.DataFrame({h: summ(df[df.ev & ~df.prof], h) for h in H}).T
    evp = evp.copy()
    evp["dq"] = pd.qcut(evp["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["profile_by_depth_h5"] = evp.groupby("dq").apply(lambda g: summ(g, 5))
    out["profile_by_depth_h3"] = evp.groupby("dq").apply(lambda g: summ(g, 3))
    out["profile_by_coin_h5"] = evp.groupby("coin").apply(lambda g: summ(g, 5))
    out["profile_by_year_h5"] = evp.groupby("year").apply(lambda g: summ(g, 5))
    out["profile_by_window_h5"] = evp.groupby("w").apply(lambda g: summ(g, 5))
    evp["cq"] = pd.cut(evp["clpos"], [-0.01, 0.33, 0.66, 1.01], labels=["lowclose", "midclose", "highclose"])
    out["profile_by_closepos_h5"] = evp.groupby("cq").apply(lambda g: summ(g, 5))
    out["profile_by_updown_h5"] = evp.groupby("up").apply(lambda g: summ(g, 5))
    evall = evall.copy()
    evall["dq"] = pd.qcut(evall["depth"].rank(method="first"), 3, labels=["shallow", "mid", "deep"])
    out["all_by_depth_h5"] = evall.groupby("dq").apply(lambda g: summ(g, 5))
    out["corr_depth_u5_profile"] = float(evp[["depth", "u5"]].dropna().corr(method="spearman").iloc[0, 1])
    out["usual_move_5"] = pd.Series({c: drift[(c, 5)][1] for c in bars})
    return out
