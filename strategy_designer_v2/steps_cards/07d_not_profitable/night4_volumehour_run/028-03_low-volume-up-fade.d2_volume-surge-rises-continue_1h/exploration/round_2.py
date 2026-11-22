import numpy as np, pandas as pd

def explore(data):
    out = {}
    H = [2, 4, 6]
    rows = []
    bk = []
    for coin, wins in data["bars"].items():
        drift = {}; sd = {}
        for h in H:
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.append(c[idx + h] / c[idx] - 1)
            rs = np.concatenate(rs); drift[h] = rs.mean(); sd[h] = rs.std()
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r = c.pct_change()
            z = r / r.rolling(720, min_periods=120).std().shift(1)
            vr = b["volume"] / b["volume"].rolling(720, min_periods=120).mean().shift(1)
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            n = len(b)
            for h in H:
                idx = np.arange(0, n - h, h)
                fwd = c.values[idx + h] / c.values[idx] - 1
                rows.append(pd.DataFrame({"coin": coin, "w": w, "h": h, "yr": yr[idx], "z": z.values[idx],
                                          "vr": vr.values[idx], "fwd": fwd, "um": fwd - drift[h], "u": (fwd - drift[h]) / sd[h]}))
            a = b["postRebalance_current_allocation"].fillna(0)
            gross = a * (c.shift(-1) / c - 1)
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"]) / b["total_portfolio_value"]
            bk.append(pd.DataFrame({"fc": b["forecast"], "a": a, "gross": gross, "fee": fee}))
    D = pd.concat(rows).dropna(subset=["z", "vr", "u"])
    # down hours with volume surge: rebound graded by volume
    res = []
    for h in H:
        s = D[(D.h == h) & (D.z < -2)].copy()
        s["vb"] = pd.cut(s.vr, [0, 2, 3, 5, 8, np.inf])
        g = s.groupby("vb", observed=True).agg(n=("u", "size"), strength=("u", "mean"), um_pct=("um", lambda x: 100 * x.mean()),
                                                tot_pct=("fwd", lambda x: 100 * x.mean()), sdu=("u", "std"))
        g["t"] = g.strength / (g.sdu / np.sqrt(g.n)); g["h"] = h; g["side"] = "down z<-2"
        res.append(g.reset_index())
        s = D[(D.h == h) & (D.z > 2)].copy()
        s["vb"] = pd.cut(s.vr, [0, 2, 3, 5, 8, np.inf])
        g = s.groupby("vb", observed=True).agg(n=("u", "size"), strength=("u", "mean"), um_pct=("um", lambda x: 100 * x.mean()),
                                                tot_pct=("fwd", lambda x: 100 * x.mean()), sdu=("u", "std"))
        g["t"] = g.strength / (g.sdu / np.sqrt(g.n)); g["h"] = h; g["side"] = "up z>2"
        res.append(g.reset_index())
    out["forward move after big hours by volume (strength, %)"] = pd.concat(res)[["side", "h", "vb", "n", "strength", "um_pct", "tot_pct", "t"]].round(3)
    # graded signal: s = z*vr ; continuation in sign; deciles of |z*vr| among |z|>1
    s = D[(D.h == 4)].copy(); s["x"] = s.z * s.vr
    s = s[s.z.abs() > 1]
    s["q"] = pd.qcut(s.x, 10, labels=False)
    g = s.groupby("q").agg(n=("u", "size"), x_mean=("x", "mean"), strength=("u", "mean"), um_pct=("um", lambda x: 100 * x.mean()), sdu=("u", "std"))
    g["t"] = g.strength / (g.sdu / np.sqrt(g.n))
    out["h4: forward strength by decile of z*vr (|z|>1)"] = g.round(3)
    # rebound after down surge by year
    s = D[(D.h == 4) & (D.z < -2) & (D.vr > 3)]
    g = s.groupby("yr").agg(n=("u", "size"), strength=("u", "mean"), um_pct=("um", lambda x: 100 * x.mean()))
    out["h4 rebound after z<-2 vr>3 by year"] = g.round(3)
    g = s.groupby("coin").agg(n=("u", "size"), strength=("u", "mean"), um_pct=("um", lambda x: 100 * x.mean()))
    out["h4 rebound after z<-2 vr>3 by coin"] = g.round(3)
    B = pd.concat(bk)
    B["fb"] = pd.cut(B.fc, [-0.01, 0.001, 0.5, 2, 5, 10, 20.01])
    g = B.groupby("fb", observed=True).agg(bars=("gross", "size"), mean_alloc=("a", "mean"), gross_sum=("gross", "sum"), fee_sum=("fee", "sum"))
    out["book by forecast bin"] = g.round(4)
    return out
