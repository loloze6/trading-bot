import numpy as np, pandas as pd

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); h = b["high"].astype(float); l = b["low"].astype(float)
            d = pd.DataFrame({
                "coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]),
                "r1": c / c.shift(1) - 1, "s4": c.shift(1) / c.shift(5) - 1,
                "s5": c / c.shift(5) - 1, "r2": c / c.shift(2) - 1,
                "nxt": c.shift(-1) / c - 1, "nxt2": c.shift(-2) / c - 1,
                "inprof": (b["regime"] == "unknown").astype(int),
                "clpos": (c - l) / (h - l).replace(0, np.nan),
            })
            d["g2"] = (np.arange(len(d)) % 2 == 0)
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["day"] = A["ts"].dt.floor("D")
    sd = A.groupby("coin")["nxt"].std()
    A["ex"] = A["nxt"] - A["coin"].map(A.groupby("coin")["nxt"].mean())
    A["ex2"] = A["nxt2"] - A["coin"].map(A.groupby("coin")["nxt2"].mean())
    for k, s in [("z1", "r1"), ("zs4", "s4"), ("zs5", "s5"), ("zr2", "r2")]:
        A[k] = A[s] / A["coin"].map(sd)

    def dt(g, col="ex"):
        g = g.dropna(subset=[col]); n = len(g)
        if n < 5: return pd.Series({"n": n, "days": 0, "mean%": np.nan, "t": np.nan})
        mean = g[col].mean()
        se = np.sqrt(((g.groupby("day")[col].sum() - g.groupby("day").size() * mean) ** 2).sum()) / n
        return pd.Series({"n": n, "days": g["day"].nunique(), "mean%": 100 * mean, "t": mean / se})

    def reg(g, ys, xs):
        g = g.dropna(subset=[ys] + xs)
        X = np.column_stack([np.ones(len(g))] + [g[x].values for x in xs]); y = g[ys].values
        XtXi = np.linalg.inv(X.T @ X); b = XtXi @ X.T @ y; e = y - X @ b
        S = pd.DataFrame(X * e[:, None]).groupby(g["day"].values).sum().values
        V = XtXi @ (S.T @ S) @ XtXi
        return pd.Series({**{f"b_{n}": v for n, v in zip(["c"] + xs, b)},
                          **{f"t_{n}": v for n, v in zip(["c"] + xs, b / np.sqrt(np.diag(V)))}, "n": len(g)})

    P = A[A.inprof == 1].copy(); Q = A[A.inprof == 0].copy()
    out = {}
    out["reg_in_z1_zs4"] = pd.DataFrame({"in": reg(P, "ex", ["z1", "zs4"]), "out": reg(Q, "ex", ["z1", "zs4"])})
    out["reg_in_z1_clpos"] = pd.DataFrame({"in": reg(P, "ex", ["z1", "clpos"]), "out": reg(Q, "ex", ["z1", "clpos"])})
    out["reg_in_zs5"] = pd.DataFrame({"in": reg(P, "ex", ["zs5"]), "out": reg(Q, "ex", ["zs5"])})
    P["r1d"] = pd.qcut(P["z1"], 8, labels=False)
    out["in_lastday_octile"] = P.groupby("r1d").apply(dt)
    P["s5q"] = pd.qcut(P["zs5"], 5, labels=False)
    out["in_5d_incl_quintile"] = P.groupby("s5q").apply(dt)
    G = P[P.g2]
    out["in_lastday_quintile_2d"] = G.assign(q=pd.qcut(G["z1"], 5, labels=False)).groupby("q").apply(lambda g: dt(g, "ex2"))
    # up days in profile: graded short?
    U = P[P.r1 > 0]
    out["in_updays_tercile"] = U.assign(q=pd.qcut(U["z1"], 3, labels=False)).groupby("q").apply(dt)
    out["in_updays_reg"] = reg(U, "ex", ["z1"])
    # half split by window parity for stability
    P["half"] = P["win"].str[1:].astype(int) % 2
    out["in_lastday_bottom_quintile_by_half"] = P.assign(q=pd.qcut(P["z1"], 5, labels=False)).query("q==0").groupby("half").apply(dt)
    out["in_mid_quintiles_by_half"] = P.assign(q=pd.qcut(P["z1"], 5, labels=False)).query("q in [2,3]").groupby("half").apply(dt)
    return out
