import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1,3,5,10,20]
    # drift per coin per horizon
    drift = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                for i in range(0, len(cl)-h, h):
                    rs.append(cl[i+h]/cl[i]-1)
            drift[(c,h)] = np.mean(rs)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values
            r1 = pd.Series(cl).pct_change()
            sd = r1.rolling(30).std()
            z = (r1/sd).values
            hi20 = pd.Series(cl).rolling(20).max().values
            f = df["forecast"].fillna(0).values
            fprev = np.r_[0, f[:-1]]
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            for i in range(n):
                trig = reg[i] == "trending"
                case = (f[i]-fprev[i]) >= 2
                if not trig and not case: continue
                d = {"coin": c, "w": w, "i": i, "cell": i//10, "yr": yr[i], "z": z[i],
                     "near": cl[i]/hi20[i] if hi20[i]==hi20[i] else np.nan,
                     "f": f[i], "trig": trig, "case": case,
                     "day": str(df["timestamp"].iloc[i])[:10]}
                for h in H:
                    d[f"u{h}"] = (cl[i+h]/cl[i]-1 - drift[(c,h)]) if i+h < n else np.nan
                rows.append(d)
    R = pd.DataFrame(rows)
    out = {}
    def summ(g, col="u10"):
        g = g.dropna(subset=[col])
        dd = g.groupby("day")[col].sum()
        m = g[col].mean()
        nd = len(dd)
        se = np.sqrt(((dd - dd.mean()*0 - m*g.groupby("day").size())**2).sum()*nd/(nd-1))/len(g) if nd>1 else np.nan
        return pd.Series({"n": len(g), "days": nd, "mean": m, "t": m/se if se else np.nan})
    C = R[R.case].sort_values("i").groupby(["coin","w","cell"]).head(1)
    out["cases_by_horizon"] = pd.DataFrame({h: summ(C, f"u{h}") for h in H}).T
    T = R[R.trig]
    out["all_trigger_days_by_horizon"] = pd.DataFrame({h: summ(T, f"u{h}") for h in H}).T
    out["cases_by_coin"] = C.groupby("coin").apply(summ)
    out["cases_by_window"] = C.groupby("w").apply(summ)
    out["cases_by_year"] = C.groupby("yr").apply(summ)
    T2 = T.dropna(subset=["z"]).copy()
    T2["zq"] = pd.qcut(T2["z"], 4, labels=False, duplicates="drop")
    out["trig_by_z_quartile_u10"] = T2.groupby("zq").apply(lambda g: pd.concat([summ(g), pd.Series({"zmean": g.z.mean()})]))
    out["trig_by_z_quartile_u3"] = T2.groupby("zq").apply(lambda g: summ(g, "u3"))
    T2["nq"] = pd.qcut(T2["near"], 4, labels=False, duplicates="drop")
    out["trig_by_near_quartile_u10"] = T2.groupby("nq").apply(lambda g: pd.concat([summ(g), pd.Series({"nmean": g.near.mean()})]))
    C2 = C.copy(); C2["fq"] = pd.qcut(C2["f"], 4, labels=False, duplicates="drop")
    out["cases_by_forecast_quartile"] = C2.groupby("fq").apply(summ)
    out["corr_z_u10_trig"] = float(T2[["z","u10"]].dropna().corr().iloc[0,1])
    return out
