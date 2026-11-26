import pandas as pd, numpy as np
from scipy import stats

def ctt(g, col):
    g = g.dropna(subset=[col])
    if len(g) < 5: return pd.Series({"n": len(g), "days": g["day"].nunique() if len(g) else 0, "mean": np.nan, "t_day": np.nan})
    m = g[col].mean()
    s = (g[col] - m).groupby(g["day"]).sum()
    se = np.sqrt((s**2).sum()) / len(g)
    return pd.Series({"n": len(g), "days": g["day"].nunique(), "mean": m, "t_day": m / se if se > 0 else np.nan})

def explore(data):
    bars = data["bars"]; rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            ts = pd.to_datetime(b["timestamp"])
            rows.append(pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)), "day": ts.dt.floor("D"),
                "yr": ts.dt.year, "wd": ts.dt.weekday,
                "r1s": r1 / sd30.shift(1), "sd30": sd30,
                "r60": c / c.shift(60) - 1, "r30": c / c.shift(30) - 1,
                "f1": c.shift(-1) / c - 1, "f2": c.shift(-2) / c - 1, "f7": c.shift(-7) / c - 1}))
    A = pd.concat(rows, ignore_index=True)
    for h, col in [(1, "f1"), (2, "f2"), (7, "f7")]:
        cm = A[A.pos % h == 0].groupby("coin")[col].mean()
        A["x" + col[1:]] = A[col] - A["coin"].map(cm)
    A["trend"] = pd.cut(A["r60"], [-9, -0.1, 0.1, 99], labels=["falling", "choppy", "rising"])
    A["volhalf"] = A.groupby("coin")["sd30"].transform(lambda s: (s > s.median()).astype(float).where(s.notna()))
    A["agit"] = A["volhalf"].map({0.0: "calmish", 1.0: "agitish"})
    out = {}
    D = A.dropna(subset=["r1s"]).copy()
    D["dn"] = (-D["r1s"]).clip(lower=0)
    D["r1b"] = pd.cut(D["r1s"], [-99, -1.5, -0.5, 0.5, 99], labels=["<-1.5", "-1.5..-0.5", "mid", ">0.5"])
    out["next-day x1 by fall bucket x trend"] = D.groupby(["trend", "r1b"]).apply(lambda g: ctt(g, "x1")).unstack()[["n", "mean", "t_day"]]
    out["next-day x1 by fall bucket x agitation"] = D.groupby(["agit", "r1b"]).apply(lambda g: ctt(g, "x1"))
    E = D[D.r1s < -0.5]
    out["fall<-0.5: next-day x1 by year"] = E.groupby("yr").apply(lambda g: ctt(g, "x1"))
    out["fall<-0.5: next-day x1 by trend x agit"] = E.groupby(["trend", "agit"]).apply(lambda g: ctt(g, "x1"))
    E2 = D[(D.r1s < -0.5) & (D.pos % 2 == 0)]
    out["fall<-0.5: 2-day x2 (grid2) by trend x agit"] = E2.groupby(["trend", "agit"]).apply(lambda g: ctt(g, "x2"))
    # grade: correlation of fall size with next-day return, calm only
    for a in ["calmish", "agitish"]:
        S = D[(D.agit == a) & (D.r1s < 0)].dropna(subset=["x1"])
        out[f"spearman fall size vs x1, {a}"] = pd.Series({"n": len(S), "rho": stats.spearmanr(S["dn"], S["x1"])[0], "p": stats.spearmanr(S["dn"], S["x1"])[1]})
    # 30d fall continuation (short side), grid7
    G = A[A.pos % 7 == 0].dropna(subset=["f7", "r30"]).copy()
    G["r30b"] = pd.cut(G["r30"], [-9, -0.2, -0.05, 0.05, 0.2, 9])
    out["x7 by r30 bucket x trend (grid7)"] = G.groupby(["trend", "r30b"]).apply(lambda g: ctt(g, "x7"))[["n", "mean", "t_day"]]
    out["x7 r30<-0.2 by year"] = G[G.r30 < -0.2].groupby("yr").apply(lambda g: ctt(g, "x7"))
    out["x7 r30<-0.2 by agit"] = G[G.r30 < -0.2].groupby("agit").apply(lambda g: ctt(g, "x7"))
    out["weekday x1 by year (t_day)"] = D.groupby(["yr", "wd"]).apply(lambda g: ctt(g, "x1"))["t_day"].unstack()
    return out
