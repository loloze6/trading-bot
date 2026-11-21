import numpy as np
import pandas as pd
from scipy import stats

def explore(data):
    out = {}
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            vol20 = r1.rolling(20, min_periods=10).std()
            f = pd.DataFrame({
                "coin": coin, "win": w, "wnum": int(w[1:]),
                "pos": np.arange(len(b)),
                "fwd5": c.shift(-H) / c - 1,
                "r1z": r1 / vol20,
                "r1": r1,
                "hi20": c / c.rolling(20, min_periods=10).max() - 1,
                "rng": (b["high"] - b["low"]) / c,
                "ret90": c / c.shift(90) - 1,
                "regime": b["regime"].values,
                "year": pd.to_datetime(b["timestamp"]).dt.year,
            })
            f["rngz"] = f["rng"] / f["rng"].rolling(60, min_periods=20).mean()
            rows.append(f)
    A = pd.concat(rows, ignore_index=True)
    G0 = A[A["pos"] % H == 0]
    dr = G0.groupby("coin")["fwd5"].mean(); sd = G0.groupby("coin")["fwd5"].std()
    G = G0.copy()
    G["ex"] = G["fwd5"] - G["coin"].map(dr)
    G["exu"] = G["ex"] / G["coin"].map(sd)
    U = G[G["regime"] == "unknown"].dropna(subset=["r1z", "ex"]).copy()
    M = G[G["regime"] == "mean_reversion"].dropna(subset=["rng", "ex"]).copy()

    def slope(g, x, y="exu"):
        s = stats.linregress(g[x], g[y]); return s.slope, s.slope / s.stderr, len(g)

    # r1z in uptrend: per coin, by window half, by year, quintile in pct
    pc = []
    for coin, g in U.groupby("coin"):
        s, t, n = slope(g, "r1z"); pc.append({"coin": coin, "slope": s, "t": t, "n": n})
    out["r1z_up_per_coin"] = pd.DataFrame(pc)
    U["half"] = np.where(U["wnum"] <= 12, "w1-w12", "w13-w24")
    out["r1z_up_by_half"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(g, "r1z")), half=h) for h, g in U.groupby("half")])
    out["r1z_up_by_year"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(g, "r1z")), year=y) for y, g in U.groupby("year")])
    U["q"] = U.groupby("coin")["r1z"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["r1z_up_quint"] = U.groupby("q").agg(n=("ex", "size"), r1z_mean=("r1z", "mean"), ex_pct=("ex", lambda s: s.mean() * 100),
                                             total_pct=("fwd5", lambda s: s.mean() * 100), exu=("exu", "mean"),
                                             t=("ex", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    # rank-based slope (robust to outliers) and excluding top quintile
    s = stats.spearmanr(U["r1z"], U["ex"]); out["r1z_up_spearman"] = f"rho {s.correlation:.4f} p {s.pvalue:.5f} n {len(U)}"
    s2 = slope(U[U["q"] < 4], "r1z"); out["r1z_up_without_topq"] = f"slope {s2[0]:.4f} t {s2[1]:.2f} n {s2[2]}"
    # positive side only (r1z>0)
    s3 = slope(U[U["r1z"] > 0], "r1z"); out["r1z_up_positive_days_only"] = f"slope {s3[0]:.4f} t {s3[1]:.2f} n {s3[2]}"
    # partial: r1z and hi20 together in uptrend
    UU = U.dropna(subset=["hi20"])
    X = np.column_stack([np.ones(len(UU)), (UU["r1z"] - UU["r1z"].mean()) / UU["r1z"].std(), (UU["hi20"] - UU["hi20"].mean()) / UU["hi20"].std()])
    beta, res, *_ = np.linalg.lstsq(X, UU["exu"].values, rcond=None)
    e = UU["exu"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(e) - 3)
    out["up_joint_r1z_hi20"] = pd.DataFrame({"beta": beta, "t": beta / np.sqrt(np.diag(cov))}, index=["const", "r1z", "hi20"])
    out["corr_r1z_hi20_up"] = float(UU[["r1z", "hi20"]].corr().iloc[0, 1])

    # range in downtrend
    pc = []
    for coin, g in M.groupby("coin"):
        s, t, n = slope(g, "rng"); pc.append({"coin": coin, "slope": s, "t": t, "n": n})
    out["rng_down_per_coin"] = pd.DataFrame(pc)
    M["half"] = np.where(M["wnum"] <= 12, "w1-w12", "w13-w24")
    out["rng_down_by_half"] = pd.DataFrame([dict(zip(["slope", "t", "n"], slope(g, "rng")), half=h) for h, g in M.groupby("half")])
    M["q"] = M.groupby("coin")["rng"].transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    out["rng_down_quint"] = M.groupby("q").agg(n=("ex", "size"), ex_pct=("ex", lambda s: s.mean() * 100),
                                               total_pct=("fwd5", lambda s: s.mean() * 100),
                                               t=("ex", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
    s = stats.spearmanr(M["rng"], M["ex"]); out["rng_down_spearman"] = f"rho {s.correlation:.4f} p {s.pvalue:.5f} n {len(M)}"
    # depth forecast within downtrend: quintiles of the recorded forecast
    Bp = G[G["regime"] == "mean_reversion"].dropna(subset=["ex"]).copy()
    out["usual_move_5d_pct_mean"] = float(sd.mean() * 100)
    return out
