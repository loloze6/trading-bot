def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars, days = data["bars"], data["days"]
    recs = []
    for c in bars:
        gl = []
        for w in bars[c]:
            df = bars[c][w].reset_index(drop=True)
            cl = df["close"].values; v = df["volume"].values; n = len(df)
            s = pd.Series(cl)
            r1 = s.pct_change().values
            vr = (pd.Series(v) / pd.Series(v).shift(1).rolling(30).mean()).values
            ma = s.rolling(50).mean().values
            r60 = s.pct_change(60).values
            alloc = df["postRebalance_current_allocation"].values
            nxt = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            for h in (1, 2, 5, 10):
                pass
            for i in range(0, n-10, 10):
                gl.append({"coin": c, "w": w, "r1": r1[i], "vr": vr[i],
                           "f1": cl[i+1]/cl[i]-1, "f2": cl[i+2]/cl[i]-1, "f5": cl[i+5]/cl[i]-1, "f10": cl[i+10]/cl[i]-1,
                           "fc": df["forecast"].iloc[i],
                           "above": (cl[i] > ma[i]) if not np.isnan(ma[i]) else np.nan, "r60": r60[i]})
        g = pd.DataFrame(gl)
        for h in ("f1", "f2", "f5", "f10"):
            g["x"+h] = g[h] - g[h].mean()
        recs.append(g)
    G = pd.concat(recs)
    def summ(s):
        s = s.dropna()
        return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s) > 2 else np.nan})
    G["state"] = np.where(G["r1"] >= 0, "up", np.where(G["vr"] < 1, "down_thin", "down_heavy"))
    for h in ("xf1", "xf2", "xf5", "xf10"):
        out["by_state_"+h] = G.groupby("state")[h].apply(summ).unstack()
    D = G[G["r1"] < 0].copy()
    D["ma"] = D["above"]
    out["down_thin_vs_heavy_by_ma_xf5"] = D.groupby(["ma", D["vr"] < 1])["xf5"].apply(summ).unstack()
    D["r60q"] = pd.qcut(D["r60"], 3, labels=False)
    out["down_days_by_r60_tercile_xf5"] = D.groupby(["r60q", D["vr"] < 1])["xf5"].apply(summ).unstack()
    # book daily returns split by whether a position was held and coin trend
    rows = []
    for c in bars:
        for w in bars[c]:
            df = bars[c][w].reset_index(drop=True)
            cl = df["close"].values
            ma = pd.Series(cl).rolling(50).mean().values
            a = df["postRebalance_current_allocation"].values
            nxt = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            rows.append(pd.DataFrame({"g": a*nxt, "a": a, "above": cl > ma, "hasma": ~np.isnan(ma)}))
    R = pd.concat(rows).dropna()
    R = R[(R["a"].abs() > 1e-9) & R["hasma"]]
    out["position_gain_by_ma"] = R.groupby("above")["g"].apply(summ).unstack()
    out["total_position_gain_by_ma_sum"] = R.groupby("above")["g"].sum()
    return out
