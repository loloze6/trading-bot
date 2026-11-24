import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    # drift per coin per horizon (all windows, grid)
    def drift(c, H):
        a = []
        for w, df in bars[c].items():
            cl = df["close"].values.astype(float)
            for i in range(0, len(cl) - H, H):
                a.append(cl[i + H] / cl[i] - 1)
        return np.mean(a)
    # bounce after large vol-scaled down day: forward H days, non-overlapping grid
    rows = []; byc = []; byy = []; byw = []
    for H in [1, 2, 3, 5, 10]:
        recs = []
        for c, ws in bars.items():
            d = drift(c, H)
            for w, df in ws.items():
                cl = df["close"].values.astype(float); n = len(cl)
                r = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
                vol = pd.Series(r).rolling(30).std().values
                ts = pd.to_datetime(df["timestamp"]).values
                for i in range(0, n - H, H):
                    if i < 30 or np.isnan(vol[i]) or vol[i] == 0: continue
                    recs.append((c, w, pd.Timestamp(ts[i]).year, pd.Timestamp(ts[i]).normalize(), r[i] / vol[i], cl[i + H] / cl[i] - 1 - d))
        D = pd.DataFrame(recs, columns=["c", "w", "yr", "day", "z", "fx"])
        D["zq"] = pd.qcut(D["z"].rank(method="first"), 10, labels=False)
        for q in [0, 1, 2, 5, 9]:
            s = D[D.zq == q]
            g = s.groupby("day")["fx"].sum()
            tcl = g.mean() / (g.std(ddof=1) / np.sqrt(len(g))) * 1  # per-day sums
            rows.append({"H": H, "decile": q, "n": len(s), "days": len(g), "z": s.z.mean(), "fx": s.fx.mean(), "t": tstat(s.fx), "t_daycl": s.fx.sum() / len(s) / (np.sqrt(((g - g.mean()*0) ** 2).sum()) / len(s))})
        r_, p_ = stats.spearmanr(D["z"], D["fx"])
        rows.append({"H": H, "decile": "rho", "n": len(D), "days": np.nan, "z": r_, "fx": p_, "t": np.nan, "t_daycl": np.nan})
        if H in (1, 3):
            neg = D[D.z < 0].copy()
            neg["zb"] = pd.qcut(neg["z"].rank(method="first"), 4, labels=False)
            out[f"grade_neg_H{H}"] = neg.groupby("zb").agg(n=("fx", "size"), z=("z", "mean"), fx=("fx", "mean"), t=("fx", tstat))
            low = D[D.zq == 0]
            out[f"low_by_coin_H{H}"] = low.groupby("c").agg(n=("fx", "size"), fx=("fx", "mean"), t=("fx", tstat))
            out[f"low_by_year_H{H}"] = low.groupby("yr").agg(n=("fx", "size"), fx=("fx", "mean"), t=("fx", tstat))
    out["bounce_after_drop"] = pd.DataFrame(rows)
    # Saturday by coin and by year
    recs = []
    for c, ws in bars.items():
        for w, df in ws.items():
            cl = df["close"].astype(float); ts = pd.to_datetime(df["timestamp"])
            recs.append(pd.DataFrame({"c": c, "wd": ts.dt.weekday, "yr": ts.dt.year, "r": cl.pct_change()}))
    S = pd.concat(recs).dropna()
    sat = S[S.wd == 5]
    out["sat_by_coin"] = sat.groupby("c")["r"].agg(["count", "mean", tstat])
    out["sat_by_year"] = sat.groupby("yr")["r"].agg(["count", "mean", tstat])
    # recorded overreach z vs forward 30 (graded continuation?)
    recs = []
    col = "debug_info.components.overreach.last_history_value"
    for c, ws in bars.items():
        d = drift(c, 30)
        for w, df in ws.items():
            if col not in df.columns: continue
            cl = df["close"].values.astype(float); z = pd.to_numeric(df[col], errors="coerce").values
            for i in range(0, len(cl) - 30, 30):
                if not np.isnan(z[i]):
                    recs.append((z[i], cl[i + 30] / cl[i] - 1 - d))
    Z = pd.DataFrame(recs, columns=["z", "fx"])
    if len(Z) > 20:
        Z["b"] = pd.qcut(Z["z"].rank(method="first"), 3, labels=False)
        out["z90_tercile_fwd30"] = Z.groupby("b").agg(n=("fx", "size"), z=("z", "mean"), fx=("fx", "mean"), t=("fx", tstat))
        out["z90_spearman"] = str(stats.spearmanr(Z["z"], Z["fx"]))
    return out
