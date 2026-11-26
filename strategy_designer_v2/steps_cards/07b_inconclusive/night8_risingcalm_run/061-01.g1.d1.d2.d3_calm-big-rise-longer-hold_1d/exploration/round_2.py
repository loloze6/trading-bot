import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    H = [5,10,20]
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
            for i in range(0, n, 10):
                if reg[i] != "trending": continue
                d = {"coin": c, "w": w, "yr": yr[i], "z": z[i],
                     "near": cl[i]/hi20[i], "day": str(df["timestamp"].iloc[i])[:10]}
                for h in H:
                    d[f"u{h}"] = (cl[i+h]/cl[i]-1 - drift[(c,h)]) if i+h < n else np.nan
                rows.append(d)
    R = pd.DataFrame(rows)
    def summ(g, col="u10"):
        g = g.dropna(subset=[col])
        if len(g) < 2: return pd.Series({"n": len(g), "days": np.nan, "mean": g[col].mean(), "t": np.nan})
        m = g[col].mean()
        dd = (g[col]-m).groupby(g["day"]).sum()
        nd = len(dd)
        se = np.sqrt((dd**2).sum()*nd/(nd-1))/len(g)
        return pd.Series({"n": len(g), "days": nd, "mean": m, "t": m/se})
    out = {}
    R["at_high"] = R["near"] >= R["near"].median()
    out["grid_trig_all_by_h"] = pd.DataFrame({h: summ(R, f"u{h}") for h in H}).T
    out["grid_trig_near_half_by_h"] = R.groupby("at_high").apply(lambda g: pd.DataFrame({h: summ(g, f"u{h}") for h in H}).T.stack()).T if False else pd.concat({k: pd.DataFrame({h: summ(g, f"u{h}") for h in H}).T for k, g in R.groupby("at_high")})
    out["grid_near_half_by_year_u10"] = pd.concat({k: g.groupby("yr").apply(summ) for k, g in R.groupby("at_high")})
    out["grid_near_half_by_coin_u10"] = pd.concat({k: g.groupby("coin").apply(summ) for k, g in R.groupby("at_high")})
    out["median_near"] = float(R["near"].median())
    R["zq"] = pd.qcut(R["z"], 2, labels=False)
    out["grid_near_x_zhalf_u10"] = R.groupby(["at_high","zq"]).apply(summ)
    out["corr_near_u10"] = float(R[["near","u10"]].dropna().corr().iloc[0,1])
    out["corr_near_u20"] = float(R[["near","u20"]].dropna().corr().iloc[0,1])
    return out
