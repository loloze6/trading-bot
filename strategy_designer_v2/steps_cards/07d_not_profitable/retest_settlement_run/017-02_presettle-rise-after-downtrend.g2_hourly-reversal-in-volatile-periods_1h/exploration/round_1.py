def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd24 = r1.rolling(24).std()
            usual = sd24.rolling(720, min_periods=120).mean()
            ratio = sd24 / usual
            hr = pd.to_datetime(b["timestamp"]).dt.hour
            n = len(b)
            for P in [1, 4, 24]:
                past = c / c.shift(P) - 1
                zP = past / (usual * np.sqrt(P))
                for H in [1, 4, 12, 24]:
                    fwd = c.shift(-H) / c - 1
                    idx = np.arange(0, n, H)
                    d = pd.DataFrame({"z": zP.iloc[idx].values, "fwd": fwd.iloc[idx].values,
                                      "ratio": ratio.iloc[idx].values, "hour": hr.iloc[idx].values,
                                      "usual": (usual * np.sqrt(H)).iloc[idx].values})
                    d["coin"] = coin; d["P"] = P; d["H"] = H
                    rows.append(d)
    D = pd.concat(rows).dropna()
    # drift per coin per H
    drift = D.groupby(["coin", "P", "H"])["fwd"].transform("mean")
    D["fade"] = -np.sign(D["z"]) * (D["fwd"] - drift)
    D["fadetot"] = -np.sign(D["z"]) * D["fwd"]
    D["strength"] = D["fade"] / D["usual"]
    D["az"] = D["z"].abs()
    D["zbin"] = pd.cut(D["az"], [0, 0.5, 1, 1.5, 2, 3, 4, 100])
    out = {}
    g = D.groupby(["P", "H", "zbin"], observed=True)
    t = g["fade"].agg(["count", "mean", "std"])
    t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
    t["mean_pct"] = t["mean"] * 100
    t["tot_pct"] = g["fadetot"].mean() * 100
    t["strength"] = g["strength"].mean()
    tt = t[["count", "mean_pct", "tot_pct", "strength", "t"]].reset_index()
    out["fade_by_P_H_zbin_P1"] = tt[tt.P == 1].round(4)
    out["fade_by_P_H_zbin_P4"] = tt[tt.P == 4].round(4)
    out["fade_by_P_H_zbin_P24"] = tt[tt.P == 24].round(4)
    # vol ratio effect in strong cases, P=1
    S = D[(D.P == 1) & (D.az >= 2)].copy()
    S["vr"] = pd.cut(S["ratio"], [0, 0.8, 1.2, 1.6, 100])
    g2 = S.groupby(["H", "vr"], observed=True)["fade"].agg(["count", "mean", "std"])
    g2["t"] = g2["mean"] / (g2["std"] / np.sqrt(g2["count"]))
    g2["mean_pct"] = g2["mean"] * 100
    out["P1_strong_by_volratio"] = g2[["count", "mean_pct", "t"]].reset_index().round(4)
    # funding hours
    S2 = D[(D.P == 1) & (D.H == 1) & (D.az >= 2)].copy()
    S2["funding_hr"] = S2["hour"].isin([23, 7, 15, 0, 8, 16])
    g3 = S2.groupby("funding_hr")["fade"].agg(["count", "mean"])
    g3["mean_pct"] = g3["mean"] * 100
    out["P1H1_strong_funding_hours"] = g3.round(5)
    # by coin strong P1 H4
    S3 = D[(D.P == 1) & (D.H == 4) & (D.az >= 3)]
    g4 = S3.groupby("coin")["fade"].agg(["count", "mean"]); g4["mean_pct"] = g4["mean"] * 100
    out["P1H4_z3_by_coin"] = g4.round(5)
    # turnover
    tr = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            a = b["postRebalance_current_allocation"].astype(float)
            tr.append(a.diff().abs().mean())
    out["mean_abs_alloc_change_per_bar"] = float(np.nanmean(tr))
    return out
