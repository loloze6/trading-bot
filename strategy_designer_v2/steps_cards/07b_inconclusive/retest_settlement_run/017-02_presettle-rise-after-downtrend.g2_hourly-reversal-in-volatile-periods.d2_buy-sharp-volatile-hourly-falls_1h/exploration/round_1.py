import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.sort_values("timestamp").reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd24 = r1.rolling(24).std()
            volm = sd24.rolling(720, min_periods=120).mean()
            s = r1 / volm
            vr = sd24 / volm
            z = r1 / sd24
            ret24p = c / c.shift(24) - 1
            ret168p = c / c.shift(168) - 1
            hour = pd.to_datetime(df["timestamp"]).dt.hour
            year = pd.to_datetime(df["timestamp"]).dt.year
            fc = df["forecast"].astype(float)
            n = len(df)
            for h in [1, 4, 8, 24, 72]:
                idx = np.arange(0, n - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({
                    "coin": coin, "win": w, "h": h, "fwd": fwd,
                    "s": s.values[idx], "z": z.values[idx], "vr": vr.values[idx],
                    "r1": r1.values[idx], "p24": ret24p.values[idx], "p168": ret168p.values[idx],
                    "hour": hour.values[idx], "year": year.values[idx], "fc": fc.values[idx]}))
    A = pd.concat(rows, ignore_index=True)
    A["drift"] = A.groupby(["coin", "h"])["fwd"].transform("mean")
    A["ex"] = A["fwd"] - A["drift"]
    A = A.dropna(subset=["s", "ex"])
    def summ(g):
        m = g["ex"].mean(); sd = g["ex"].std(); n = len(g)
        return pd.Series({"n": n, "mean_ex_%": 100*m, "t": m/(sd/np.sqrt(n)) if n > 2 and sd > 0 else np.nan})
    out = {}
    fall = A[A["r1"] < 0].copy()
    # bins of scaled fall by horizon
    fall["sbin"] = pd.qcut(fall["s"], 5, labels=["q1_largest_fall","q2","q3","q4","q5_smallest"])
    out["fall_by_h_bin"] = fall.groupby(["h","sbin"], observed=True).apply(summ).unstack("sbin")["t"]
    out["fall_by_h_bin_mean"] = fall.groupby(["h","sbin"], observed=True).apply(summ).unstack("sbin")["mean_ex_%"]
    # rises for comparison
    rise = A[A["r1"] > 0].copy()
    rise["sbin"] = pd.qcut(rise["s"], 5, labels=["q1_small","q2","q3","q4","q5_largest_rise"])
    out["rise_by_h_bin_mean"] = rise.groupby(["h","sbin"], observed=True).apply(summ).unstack("sbin")["mean_ex_%"]
    out["rise_by_h_bin_t"] = rise.groupby(["h","sbin"], observed=True).apply(summ).unstack("sbin")["t"]
    # extreme falls (top decile) at h=24, by coin, year, vr tercile, prior trend, hour group
    f24 = fall[(fall["h"] == 24)].copy()
    thr = f24["s"].quantile(0.1)
    e = f24[f24["s"] <= thr].copy()
    out["ext24_by_coin"] = e.groupby("coin").apply(summ)
    out["ext24_by_year"] = e.groupby("year").apply(summ)
    e["vrbin"] = pd.qcut(e["vr"], 3, labels=["lowvr","midvr","highvr"])
    out["ext24_by_vr"] = e.groupby("vrbin", observed=True).apply(summ)
    e["trend7"] = np.where(e["p168"] > 0, "up7d", "down7d")
    out["ext24_by_trend7"] = e.groupby("trend7").apply(summ)
    # h=1 and h=4 extreme falls by settlement hour (grid hours differ by h; use h=1)
    f1 = fall[fall["h"] == 1].copy()
    t1 = f1["s"].quantile(0.1)
    e1 = f1[f1["s"] <= t1].copy()
    e1["settle"] = np.where(e1["hour"].isin([23, 7, 15]), "pre_settle_hour", "other")
    out["ext1_by_settle"] = e1.groupby("settle").apply(summ)
    # correlation of -s with ex on falls, per h
    cor = {}
    for h, g in fall.groupby("h"):
        rr, p = stats.spearmanr(-g["s"], g["ex"])
        cor[h] = pd.Series({"n": len(g), "spearman": rr, "p": p})
    out["fall_rank_corr"] = pd.DataFrame(cor).T
    return out
