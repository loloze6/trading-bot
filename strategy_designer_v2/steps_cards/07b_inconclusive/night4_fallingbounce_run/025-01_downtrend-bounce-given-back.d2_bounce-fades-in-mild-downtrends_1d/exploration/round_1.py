import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 3, 5, 10, 20]
    # normal drift per coin per horizon (non-overlapping grids)
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs += list(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs)
    rows = []
    allb = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(df)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(20).std()
            z = (r1 / sd).values
            r90 = (pd.Series(cl) / pd.Series(cl).shift(90) - 1).values
            dep = df.get("debug_info.components.depth90.last_history_value")
            dep = dep.values if dep is not None else np.full(n, np.nan)
            # cases: first bar in each 5-grid cell with forecast <= -2 and falling (forecast < previous)
            for g in range(0, n, 5):
                for t in range(g, min(g + 5, n)):
                    prev = f[t - 1] if t > 0 else 0
                    if f[t] <= -2 and f[t] < prev - 1e-9:
                        rec = dict(coin=c, win=w, year=yr[t], f=f[t], z=z[t], dep=dep[t])
                        for h in H:
                            if t + h < n:
                                rec[f"u{h}"] = -(cl[t + h] / cl[t] - 1 - drift[(c, h)])
                        rows.append(rec)
                        break
            # all bounces (any regime) with z large, on 5-grid, for comparison
            for g in range(0, n - 5, 5):
                t = g
                if np.isfinite(z[t]) and np.isfinite(r90[t] if t < n else np.nan) and z[t] > 1.5:
                    rec = dict(coin=c, year=yr[t], z=z[t], r90=r90[t])
                    for h in H:
                        if t + h < n:
                            rec[f"u{h}"] = -(cl[t + h] / cl[t] - 1 - drift[(c, h)])
                    allb.append(rec)
    d = pd.DataFrame(rows); a = pd.DataFrame(allb)
    def summ(x, col="u5"):
        v = x[col].dropna()
        return pd.Series({"n": len(v), "mean": v.mean(), "t": v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["by_coin_u5"] = d.groupby("coin").apply(summ)
    out["by_year_u5"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=["weak", "q2", "q3", "strongest"][::-1])
    out["by_forecast_size_u5"] = d.groupby("fq").apply(summ)
    d["dq"] = pd.qcut(d["dep"], 4, labels=["deepest", "q2", "q3", "shallowest"])
    out["by_depth_u5"] = d.groupby("dq").apply(summ)
    out["by_depth_u10"] = d.groupby("dq").apply(lambda x: summ(x, "u10"))
    a["mkt"] = np.where(a["r90"] < 0, "falling", "rising")
    out["bounces_z>1.5_by_mkt_u5"] = a.groupby("mkt").apply(summ)
    out["bounces_z>1.5_by_mkt_u10"] = a.groupby("mkt").apply(lambda x: summ(x, "u10"))
    a["dbin"] = pd.cut(a["r90"], [-1, -0.4, -0.2, 0, 0.3, 100])
    out["bounces_by_r90bin_u5"] = a.groupby("dbin").apply(summ)
    out["usual5"] = pd.Series({c: usual[(c, 5)] for c in bars})
    return out
