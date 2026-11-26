def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy().reset_index(drop=True)
            if len(b) < 40: continue
            c = b["close"]; h = b["high"]; l = b["low"]
            d = pd.DataFrame({"ts": pd.to_datetime(b["timestamp"])})
            d["coin"] = coin; d["win"] = w
            d["ret"] = c / c.shift(1) - 1
            d["f1"] = c.shift(-1) / c - 1
            d["f2"] = c.shift(-2) / c.shift(-1) - 1
            d["rm"] = (h - l) / (h - l).rolling(30, min_periods=10).mean()
            sd = d["ret"].rolling(30, min_periods=10).std()
            d["z"] = d["ret"] / sd
            d["cl"] = (c - l) / (h - l).replace(0, np.nan)
            d["ag"] = (b["regime"] != "chop").astype(int)
            dn = (d["ret"] < 0).astype(int)
            up = (d["ret"] > 0).astype(int)
            # run length of consecutive down / up closes ending at t
            g = (dn != dn.shift()).cumsum()
            d["dnrun"] = dn.groupby(g).cumsum() * dn
            g2 = (up != up.shift()).cumsum()
            d["uprun"] = up.groupby(g2).cumsum() * up
            d["alloc"] = b["postRebalance_current_allocation"]
            d["prevalloc"] = b["previous_allocation"]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    drift = D.groupby("coin")["f1"].mean()
    D["x1"] = D["f1"] - D["coin"].map(drift)
    D["x2"] = D["f2"] - D["coin"].map(drift)
    def tcl(s, ts):
        m = s.mean(); dev = (s - m).groupby(ts).sum()
        se = np.sqrt((dev**2).sum()) / len(s)
        return m / se if se > 0 else np.nan
    def summ(g, col="x1"):
        g = g.dropna(subset=[col])
        return pd.Series({"n": len(g), "days": g["ts"].nunique(), "mean%": g[col].mean()*100, "t": tcl(g[col], g["ts"])})
    def creg(g, xs, y="x1"):
        g = g.dropna(subset=xs + [y])
        X = np.column_stack([np.ones(len(g))] + [g[x].values for x in xs])
        Y = g[y].values
        XtX = np.linalg.inv(X.T @ X); b = XtX @ X.T @ Y
        e = Y - X @ b
        S = pd.DataFrame(X * e[:, None]).groupby(g["ts"].values).sum().values
        V = XtX @ (S.T @ S) @ XtX
        return pd.DataFrame({"coef": b, "t": b / np.sqrt(np.diag(V))}, index=["const"] + xs).round(4).assign(n=len(g))
    out = {}
    A = D[D["ag"] == 1].copy(); C = D[D["ag"] == 0].copy()
    # down-run length
    out["ag: next day by down-run length"] = A[A["dnrun"] > 0].groupby(A["dnrun"].clip(upper=4)).apply(summ).round(3)
    out["calm: next day by down-run length"] = C[C["dnrun"] > 0].groupby(C["dnrun"].clip(upper=4)).apply(summ).round(3)
    out["ag: next day by up-run length"] = A[A["uprun"] > 0].groupby(A["uprun"].clip(upper=4)).apply(summ).round(3)
    # pooled agitated up days
    out["ag up days pooled"] = summ(A[A["ret"] > 0]).round(3).to_frame().T
    out["calm up days pooled"] = summ(C[C["ret"] > 0]).round(3).to_frame().T
    # graded regressions, agitated down days
    Ad = A[A["ret"] < 0].copy(); Ad["negz"] = -Ad["z"]; Ad["lrm"] = np.log(Ad["rm"])
    Ad["inter"] = Ad["negz"] * Ad["lrm"]
    out["ag down: x1 ~ negz + lrm + inter"] = creg(Ad, ["negz", "lrm", "inter"])
    out["ag down: x1 ~ lrm + closeloc"] = creg(Ad, ["lrm", "cl"])
    Cd = C[C["ret"] < 0].copy(); Cd["negz"] = -Cd["z"]; Cd["lrm"] = np.log(Cd["rm"]); Cd["inter"] = Cd["negz"]*Cd["lrm"]
    out["calm down: x1 ~ negz + lrm + inter"] = creg(Cd, ["negz", "lrm", "inter"])
    # agitated all days: close location graded
    A["lrm"] = np.log(A["rm"]); A["clc"] = A["cl"] - 0.5; A["clxr"] = A["clc"] * A["lrm"]
    out["ag all: x1 ~ clc + lrm + clc*lrm"] = creg(A, ["clc", "lrm", "clxr"])
    Au = A[A["ret"] > 0].copy()
    out["ag up: x1 ~ z + lrm"] = creg(Au, ["z", "lrm"])
    # calm day-2 continuation after wide rise
    Cu = C[C["ret"] > 0].copy(); Cu["lrm"] = np.log(Cu["rm"])
    out["calm up: x2 ~ z + lrm"] = creg(Cu, ["z", "lrm"], y="x2")
    out["calm all: x2 ~ ret-z"] = creg(C.assign(zz=C["z"]), ["zz"], y="x2")
    # by window, agitated down wide (third by coin)
    Ad["rq"] = Ad.groupby("coin")["rm"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["ag down wide third by window"] = Ad[Ad["rq"] == 2].groupby("win").apply(summ).round(3)
    # second-day of held position: entered yesterday, still held after another down day
    out["ag: down day after down day, by today's range third"] = Ad[Ad["dnrun"] >= 2].groupby("rq").apply(summ).round(3)
    out["ag: first down day, by range third"] = Ad[Ad["dnrun"] == 1].groupby("rq").apply(summ).round(3)
    return out
