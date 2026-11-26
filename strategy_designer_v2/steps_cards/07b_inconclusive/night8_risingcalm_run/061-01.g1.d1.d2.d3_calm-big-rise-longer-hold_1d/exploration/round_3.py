import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [5,10]
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
            z = (r1/r1.rolling(30).std()).values
            hi20 = pd.Series(cl).rolling(20).max().values
            reg = df["regime"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(cl)
            for i in range(n):
                if reg[i] != "trending": continue
                d = {"coin": c, "w": w, "cell": i//10, "i": i, "yr": yr[i], "z": z[i],
                     "near": cl[i]/hi20[i], "day": str(df["timestamp"].iloc[i])[:10]}
                for h in H:
                    d[f"u{h}"] = (cl[i+h]/cl[i]-1 - drift[(c,h)]) if i+h < n else np.nan
                rows.append(d)
    R = pd.DataFrame(rows).dropna(subset=["z","near"])
    def summ(g, col="u10"):
        g = g.dropna(subset=[col])
        if len(g) < 2: return pd.Series({"n": len(g), "days": np.nan, "mean": g[col].mean(), "t": np.nan})
        m = g[col].mean()
        dd = (g[col]-m).groupby(g["day"]).sum()
        nd = len(dd)
        se = np.sqrt((dd**2).sum()*nd/(nd-1))/len(g)
        return pd.Series({"n": len(g), "days": nd, "mean": m, "t": m/se})
    out = {}
    # one case per 10-bar cell (first trigger day), non-overlapping
    C = R.sort_values("i").groupby(["coin","w","cell"]).head(1).copy()
    C["nq"] = pd.qcut(C["near"], 4, labels=False, duplicates="drop")
    out["cell_cases_by_near_q_u10"] = C.groupby("nq").apply(lambda g: pd.concat([summ(g), pd.Series({"nmean": g.near.mean()})]))
    out["cell_cases_by_near_q_u5"] = C.groupby("nq").apply(lambda g: summ(g, "u5"))
    C["top"] = C["nq"] >= 2
    out["cell_cases_nearhalf_by_year"] = pd.concat({k: g.groupby("yr").apply(summ) for k, g in C.groupby("top")})
    out["cell_cases_nearhalf_by_coin"] = pd.concat({k: g.groupby("coin").apply(summ) for k, g in C.groupby("top")})
    zm = C["z"].median()
    out["cell_cases_bigz_by_near_half"] = C[C.z >= zm].groupby("top").apply(summ)
    out["corr_near_u10_cells"] = float(C[["near","u10"]].dropna().corr().iloc[0,1])
    out["corr_z_u10_cells"] = float(C[["z","u10"]].dropna().corr().iloc[0,1])
    out["corr_near_u10_cells_bigz"] = float(C[C.z >= zm][["near","u10"]].dropna().corr().iloc[0,1])
    return out
