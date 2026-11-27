def explore(data):
    import numpy as np, pandas as pd
    out = {}
    cs = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True).copy()
            r = b["close"].pct_change()
            b["r"] = r
            b["nxt"] = b["close"].shift(-1) / b["close"] - 1
            b["vol30"] = r.rolling(30).std()
            b["vol10"] = r.rolling(10).std()
            b["vol60"] = r.rolling(60).std()
            b["vratio"] = b["vol10"] / b["vol60"]
            b["v30_60"] = b["vol30"] / b["vol60"]
            b["tr20"] = b["close"] / b["close"].shift(20) - 1
            b["tr60"] = b["close"] / b["close"].shift(60) - 1
            b["r_z"] = r / b["vol30"]
            down = (r < 0).astype(int)
            run = []; k = 0
            for x in down:
                k = k + 1 if x else 0
                run.append(k)
            b["runprev"] = pd.Series(run).shift(1)
            b["alloc"] = b["postRebalance_current_allocation"]
            b["coin"] = c; b["wn"] = int(w[1:])
            cs.append(b)
    A = pd.concat(cs)
    mu = A["r"].mean()
    A["gain"] = -(A["nxt"] - mu)
    A["pnl"] = A["alloc"] * A["nxt"]
    C = A[A["forecast"] < 0].dropna(subset=["nxt"]).copy()
    def tt(s):
        return s.mean() / s.std() * np.sqrt(len(s)) if len(s) > 2 else np.nan
    def g(X, col, q=4):
        x = X.dropna(subset=[col]).copy()
        x["bin"] = pd.qcut(x[col], q, duplicates="drop")
        return x.groupby("bin").agg(n=("gain", "size"), gain=("gain", "mean"), t=("gain", tt), pnl=("pnl", "sum"), pnl_min=("pnl", "min"), alloc=("alloc", "mean"))
    out["cases by vratio (10d/60d swing)"] = g(C, "vratio")
    out["cases by v30_60"] = g(C, "v30_60")
    out["cases by r_z (bounce in 30d swings)"] = g(C, "r_z")
    out["cases by alloc"] = g(C, "alloc")
    # worst 40 case pnl: their features vs all cases
    W = C.nsmallest(40, "pnl")
    feats = ["r", "r_z", "runprev", "forecast", "vratio", "tr20", "tr60", "alloc", "nxt"]
    out["worst 40 cases vs all (medians)"] = pd.DataFrame({"worst40": W[feats].median(), "all": C[feats].median()})
    # condition alone: falling-market non-case days by vratio
    F = A[(A["tr60"] < -0.10) & ~(A["forecast"] < 0)].dropna(subset=["nxt", "vratio"]).copy()
    out["noncase falling days by vratio"] = g(F, "vratio")
    # condition alone tr20
    out["noncase falling days by tr20"] = g(F.dropna(subset=["tr20"]), "tr20")
    # subset books: daily pnl per (wn,day) mean over coins, compare chained calmar-like
    def chain(mask):
        X = A.copy()
        X["p"] = np.where(mask(X), X["pnl"].fillna(0), 0.0)
        S = X.groupby(["wn", "timestamp"])["p"].mean().sort_index()
        v = (1 + S).cumprod()
        dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(S)) - 1
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": S.mean() / S.std() * np.sqrt(365)})
    isc = lambda X: X["forecast"] < 0
    out["book variants (gross, no fees)"] = pd.DataFrame({
        "all": chain(isc),
        "vratio>q25": chain(lambda X: isc(X) & (X["vratio"] > C["vratio"].quantile(0.25))),
        "runprev>=2": chain(lambda X: isc(X) & (X["runprev"] >= 2)),
        "forecast<-6.4": chain(lambda X: isc(X) & (X["forecast"] < -6.38)),
        "tr20<-0.125": chain(lambda X: isc(X) & (X["tr20"] < -0.125)),
    })
    return out
