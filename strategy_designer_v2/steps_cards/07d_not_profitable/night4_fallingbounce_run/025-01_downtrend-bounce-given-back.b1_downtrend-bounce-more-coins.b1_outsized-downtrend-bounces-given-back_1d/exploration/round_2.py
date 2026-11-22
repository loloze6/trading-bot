def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]; trades = data["trades"]
    drift = {h: {} for h in (3, 5, 10)}
    for c in bars:
        for h in (3, 5, 10):
            r = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            drift[h][c] = np.mean(r)
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"]
            r1 = cl.pct_change()
            vol = r1.rolling(20).std()
            z = r1 / vol
            n = len(cl)
            d = {"z": z.values, "r30": (cl / cl.shift(30) - 1).values, "r90": (cl / cl.shift(90) - 1).values,
                 "fc": b["forecast"].values, "reg": b["regime"].values,
                 "pos": b["postRebalance_current_allocation"].fillna(0).values, "coin": c}
            for h in (3, 5, 10):
                g = np.zeros(n, bool); g[np.arange(0, n, h)] = True
                d["g%d" % h] = g
                d["f%d" % h] = (cl.shift(-h) / cl - 1).values
            rows.append(pd.DataFrame(d))
    A = pd.concat(rows)
    for h in (3, 5, 10):
        A["u%d" % h] = -(A["f%d" % h] - A["coin"].map(drift[h]))
    F = A[(A.reg == "mean_reversion")].dropna(subset=["z", "r30", "f10"])
    def tt(x):
        x = x.dropna(); return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    # forecast vs z relation
    act = F[F.fc < -2]
    out["fc_vs_z_corr_active"] = float(np.corrcoef(act.fc, act.z)[0, 1])
    out["z_when_fc_le_-15"] = act[act.fc <= -15].z.describe().to_frame()
    out["share_active_with_z_below_1"] = float((act.z < 1).mean())
    # z>1 cases, grid 5, by r30 tercile and z
    G = F[F.g5 & (F.z > 1)].copy()
    G["r30b"] = pd.qcut(G.r30, 3); G["zb"] = pd.cut(G.z, [1, 1.75, 2.5, np.inf])
    out["z>1_r30xz_u5"] = G.groupby(["r30b", "zb"])["u5"].apply(tt).unstack()
    G["r90b"] = pd.qcut(G.r90, 3)
    out["z>1_by_r90_u5"] = G.groupby("r90b")["u5"].apply(tt).unstack()
    # graded by z*(-r30): bounce in a coin with deep 30-day fall
    G["score"] = G.z * (-G.r30).clip(lower=0)
    G["sb"] = pd.qcut(G.score.rank(method="first"), 4)
    out["z>1_by_z_x_depth30_u5"] = G.groupby("sb")["u5"].apply(tt).unstack()
    # horizons for deep-fall bounces (r30 bottom tercile)
    q = F.r30.quantile(1/3)
    for h in (3, 5, 10):
        Gh = F[F["g%d" % h] & (F.z > 1)]
        out["horizon_%d" % h] = pd.DataFrame({"deep30": tt(Gh[Gh.r30 < q]["u%d" % h]), "other": tt(Gh[Gh.r30 >= q]["u%d" % h])})
    # book bars held short, by r30 at bar
    S = A[A.pos < 0].dropna(subset=["r30", "f3"])
    S = S.assign(g1=S.pos * 0)  # placeholder
    rows2 = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].values
            pos = b["postRebalance_current_allocation"].fillna(0).values
            r30 = pd.Series(cl) / pd.Series(cl).shift(30) - 1
            rows2.append(pd.DataFrame({"g": pos[:-1] * (cl[1:] / cl[:-1] - 1), "pos": pos[:-1], "r30": r30.values[:-1]}))
    B = pd.concat(rows2); B = B[B.pos < 0].dropna()
    B["r30b"] = pd.qcut(B.r30, 4)
    out["short_bars_gain_by_r30"] = B.groupby("r30b")["g"].agg(["count", "mean", "sum"])
    return out
