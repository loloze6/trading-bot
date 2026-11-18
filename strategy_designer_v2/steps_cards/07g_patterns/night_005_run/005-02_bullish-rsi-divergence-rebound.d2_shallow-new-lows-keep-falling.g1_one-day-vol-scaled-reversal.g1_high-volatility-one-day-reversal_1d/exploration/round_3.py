import pandas as pd, numpy as np
from scipy import stats

def ols(y, X):
    X = np.column_stack([np.ones(len(y))] + list(X))
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    s2 = e @ e / (len(y) - X.shape[1])
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    return b[1:], (b / se)[1:]

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            vol = r.rolling(20).std()
            z = r / vol
            rng = np.log(b["high"] / b["low"])
            rz = rng / vol
            vrel = vol / vol.rolling(60, min_periods=40).mean()
            nxt = c.shift(-1) / c - 1
            n2 = c.shift(-2) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)), "z": z, "rz": rz,
                                      "rng": rng, "vrel": vrel, "nxt": nxt, "n2": n2, "yr": ts.dt.year}))
    D = pd.concat(rows)
    D["ex"] = D["nxt"] - D.groupby("coin")["nxt"].transform("mean")
    E = D.dropna(subset=["z", "rz", "ex"]).copy()
    res = []
    groups = [("all", E)] + [(f"coin {k}", g) for k, g in E.groupby("coin")] + [(f"yr {k}", g) for k, g in E.groupby("yr")] \
        + [("z<0", E[E.z < 0]), ("z>0", E[E.z > 0])]
    for name, g in groups:
        b, t = ols(g["ex"].values, [g["rz"].values, g["z"].values])
        res.append({"grp": name, "b_rz_bps": b[0] * 1e4, "t_rz": t[0], "b_z_bps": b[1] * 1e4, "t_z": t[1], "n": len(g)})
    out["ex_on_rangez_and_z"] = pd.DataFrame(res).round(2)
    E["rq"] = E.groupby("coin")["rz"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["ex_bps_by_rangez_quintile"] = E.groupby("rq")["ex"].agg(["mean", "count"]).assign(mean=lambda x: x["mean"] * 1e4).round(1)
    # causal vol relative level: z slope by vrel tercile
    F = E.dropna(subset=["vrel"]).copy()
    F["vt"] = pd.qcut(F["vrel"], 3, labels=False)
    rr = []
    for k, g in F.groupby("vt"):
        b, t = ols(g["ex"].values, [g["z"].values])
        b2, t2 = ols(g["ex"].values, [g["z"].values * g["vrel"].values])
        rr.append({"vt": k, "slope_z_bps": b[0] * 1e4, "t": t[0], "n": len(g)})
    out["z_slope_by_causal_vol_tercile"] = pd.DataFrame(rr).round(2)
    b, t = ols(F["ex"].values, [F["z"].values, (F["z"] * F["vrel"]).values])
    out["interaction_z_x_vrel"] = pd.DataFrame({"b_bps": b * 1e4, "t": t}, index=["z", "z*vrel"]).round(2)
    # 2-day non-overlapping range
    G = D[D.pos % 2 == 0].dropna(subset=["n2", "rz", "z"])
    G = G.assign(ex2=G["n2"] - G.groupby("coin")["n2"].transform("mean"))
    b, t = ols(G["ex2"].values, [G["rz"].values, G["z"].values])
    out["h2_nonoverlap"] = pd.DataFrame({"b_bps": b * 1e4, "t": t, "n": len(G)}, index=["rz", "z"]).round(2)
    return out
