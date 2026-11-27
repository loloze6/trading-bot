import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r1 = c.pct_change()
            sd = r1.rolling(30, min_periods=20).std()
            z = (c / c.shift(14) - 1) / (sd * np.sqrt(14))
            fc = df["forecast"].astype(float)
            inprof = (df["regime"] == "unknown").values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            n = len(df); h = 7
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, day=day[i], ret=c.iloc[i+h]/c.iloc[i]-1,
                                 z=z.iloc[i], fc=fc.iloc[i], prof=inprof[i]))
    d = pd.DataFrame(rows)
    d["ex"] = d["ret"] - d.groupby("coin")["ret"].transform("mean")
    d = d.dropna(subset=["z", "fc"])

    def cl_slope(g, xcol):
        x = g[xcol].values; y = g["ex"].values
        if len(g) < 10 or np.std(x) == 0:
            return pd.Series({"n": len(g), "slope": np.nan, "t_cl": np.nan, "days": np.nan})
        X = np.column_stack([np.ones(len(x)), x])
        XtX_inv = np.linalg.inv(X.T @ X)
        b = XtX_inv @ X.T @ y
        e = y - X @ b
        sc = pd.DataFrame(X * e[:, None]).groupby(g["day"].values).sum().values
        G = sc.shape[0]
        V = XtX_inv @ (sc.T @ sc) @ XtX_inv * G / (G - 1)
        return pd.Series({"n": len(g), "slope": b[1], "t_cl": b[1] / np.sqrt(V[1, 1]), "days": G})

    p = d[d.prof].copy()
    pn = p[p.fc != 0].copy()
    p["zc"] = p["z"].clip(-4, 4)
    p["z3"] = np.sign(p["z"]) * p["z"] ** 2
    out = {}
    res = {}
    res["prof_all_on_z"] = cl_slope(p, "z")
    res["prof_all_on_zclip4"] = cl_slope(p, "zc")
    res["prof_all_on_signed_z2"] = cl_slope(p, "z3")
    res["prof_all_on_fc"] = cl_slope(p, "fc")
    res["prof_fcnonzero_on_fc"] = cl_slope(pn, "fc")
    res["prof_fcnonzero_on_z"] = cl_slope(pn, "z")
    res["outside_on_z"] = cl_slope(d[~d.prof], "z")
    res["all_on_z"] = cl_slope(d, "z")
    out["clustered_slopes_h7"] = pd.DataFrame(res).T
    out["corr_fc_z_prof"] = float(p[["fc", "z"]].corr().iloc[0, 1])
    out["share_fc_sign_matches_z"] = float((np.sign(p.fc) == np.sign(p.z))[p.fc != 0].mean())
    out["share_prof_fc_zero"] = float((p.fc == 0).mean())
    p["zq"] = pd.qcut(p["z"], 5, labels=False)
    out["prof_by_z_quintile"] = p.groupby("zq").agg(n=("ex", "size"), z=("z", "mean"),
                                                   fc=("fc", "mean"), mean_ex=("ex", "mean"))
    return out
