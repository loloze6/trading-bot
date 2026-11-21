import numpy as np, pandas as pd

def explore(data):
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        dr_all = []
        for w, b in wins.items():
            dr_all.extend(list(b["close"].astype(float).pct_change().dropna().values))
        ddrift = np.mean(dr_all)
        for w, b in wins.items():
            c = b["close"].astype(float).values
            n = len(c)
            s = pd.Series(c)
            pos = b["postRebalance_current_allocation"].astype(float).fillna(0).values
            fc = b["forecast"].astype(float).fillna(0).values
            r1 = s.pct_change().shift(-1).values
            hi90 = s.shift(1).rolling(90, min_periods=30).max().values
            dist = c / hi90 - 1
            r5 = s.pct_change(5).values
            r10 = s.pct_change(10).values
            # days since entry
            held = np.zeros(n); h = 0
            for i in range(n):
                h = h + 1 if abs(pos[i]) > 1e-6 else 0
                held[i] = h
            for i in range(n):
                rows.append(dict(coin=coin, win=w, pos=pos[i], fc=fc[i],
                                 r1x=r1[i] - ddrift if not np.isnan(r1[i]) else np.nan,
                                 g=pos[i] * r1[i] if not np.isnan(r1[i]) else np.nan,
                                 dist=dist[i], r5=r5[i], r10=r10[i], held=held[i]))
    A = pd.DataFrame(rows)
    P = A[A.pos.abs() > 1e-6].dropna(subset=["r1x"]).copy()
    tt = lambda x: x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
    P["hb"] = pd.cut(P.held, [0, 3, 10, 20, 40, 500])
    out["r1x_inpos_by_days_held"] = P.groupby("hb")["r1x"].agg(["count", "mean", tt])
    out["gain_inpos_by_days_held"] = P.groupby("hb")["g"].agg(["sum", "mean"])
    P2 = P.dropna(subset=["dist"]).copy()
    P2["db"] = pd.cut(P2.dist, [-1, -0.2, -0.1, -0.05, 0, 0.05, 0.15, 5])
    out["r1x_inpos_by_dist_high"] = P2.groupby("db")["r1x"].agg(["count", "mean", tt])
    out["gain_inpos_by_dist_high"] = P2.groupby("db")["g"].agg(["sum", "mean"])
    P3 = P.dropna(subset=["r10"]).copy()
    P3["rb"] = pd.qcut(P3.r10, 5)
    out["r1x_inpos_by_past10"] = P3.groupby("rb")["r1x"].agg(["count", "mean", tt])
    # all bars (not only in position): r1x by distance from high, graded
    A2 = A.dropna(subset=["dist", "r1x"]).copy()
    A2["db"] = pd.cut(A2.dist, [-1, -0.4, -0.2, -0.1, -0.05, 0, 0.05, 0.15, 5])
    out["r1x_all_by_dist_high"] = A2.groupby("db")["r1x"].agg(["count", "mean", tt])
    return out
