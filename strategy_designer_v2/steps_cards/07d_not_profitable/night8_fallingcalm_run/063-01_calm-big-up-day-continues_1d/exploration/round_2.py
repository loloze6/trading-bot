import pandas as pd, numpy as np

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sd = r.rolling(30, min_periods=20).std()
            df = pd.DataFrame({"coin": coin, "w": w, "z": r / sd, "fwd": c.shift(-5) / c - 1,
                "r20p": c / c.shift(20) - 1, "r10p": c / c.shift(10) - 1, "r60p": c / c.shift(60) - 1,
                "calm": (b["regime"] == "unknown"), "pos": b["postRebalance_current_allocation"].astype(float),
                "g": (b["postRebalance_total_value"].astype(float).shift(-1) / b["postRebalance_total_value"].astype(float) - 1),
                "cr1": c.shift(-1) / c - 1, "i": np.arange(len(b))})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[(A.i % 5 == 0) & A.fwd.notna()].copy()
    drift = G.groupby("coin").fwd.mean()
    G["ex"] = G.fwd - G.coin.map(drift)
    def summ(g):
        n = len(g)
        return pd.Series({"n": n, "fwd": g.fwd.mean(), "ex": g.ex.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(n)) if n > 2 else np.nan})
    C = G[G.calm & G.z.notna()].copy()
    C["sig"] = pd.cut(C.z, [-99, 0, 1, 2, 99])
    C["tr"] = pd.cut(C.r20p, [-9, -0.1, 0, 0.1, 9])
    out["calm_sig_x_r20"] = C.groupby(["tr", "sig"]).apply(summ)
    C["tr10"] = pd.cut(C.r10p, [-9, -0.05, 0, 0.05, 9])
    out["calm_z>0_by_r10"] = C[C.z > 0].groupby("tr10").apply(summ)
    C["t60"] = pd.cut(C.r60p, [-9, -0.1, 0.1, 9])
    out["calm_by_r60_sig"] = C[C.r60p.notna()].groupby(["t60", C.z > 1]).apply(summ)
    out["r60_coverage"] = float(C.r60p.notna().mean())
    # book bars in a position: gain by prior 20d trend
    P = A[A.pos.abs() > 0.01].dropna(subset=["g"]).copy()
    P["tr"] = pd.cut(P.r20p, [-9, -0.1, 0, 0.1, 9])
    out["held_bars_by_r20"] = P.groupby("tr").agg(n=("g", "size"), g=("g", "mean"), cr=("cr1", "mean"), pos=("pos", "mean"))
    # simulated filter: only r20>0 bars of the position
    A["gf"] = np.where(A.r20p > 0, A.g, 0.0)
    A["gs"] = A.g
    def book(col):
        X = A.dropna(subset=["g"]).groupby(["w", "i"])[col].mean().reset_index().sort_values(["w", "i"])
        v = (1 + X[col]).cumprod(); dd = (v / v.cummax() - 1).min()
        yrs = len(X) / 365
        yr = v.iloc[-1] ** (1 / yrs) - 1
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                          "sharpe": X[col].mean() / X[col].std() * np.sqrt(365)})
    out["book_full_vs_r20pos"] = pd.DataFrame({"full": book("gs"), "r20>0 only": book("gf")})
    # in worst windows w14,w15,w13: held bars by r20
    W = P[P.w.isin(["w13", "w14", "w15"])]
    out["worst_windows_held_by_r20"] = W.groupby("tr").agg(n=("g", "size"), g=("g", "mean"))
    out["worst_windows_by_coin"] = W.groupby("coin").agg(n=("g", "size"), g=("g", "sum"))
    return out
