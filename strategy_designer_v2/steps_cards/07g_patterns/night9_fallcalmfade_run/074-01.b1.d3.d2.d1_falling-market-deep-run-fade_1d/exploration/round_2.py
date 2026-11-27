import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float); r = c.pct_change()
            d = pd.DataFrame({"coin": coin, "win": w, "ts": pd.to_datetime(b["timestamp"]), "r": r,
                              "nxt": c.shift(-1)/c-1, "nxt3": c.shift(-3)/c-1})
            d["trend"] = (c/c.shift(60)-1)*100
            usual = r.abs().rolling(30).mean().shift(1)
            v30 = r.rolling(30).std()
            d["agit"] = np.where(v30 > v30.rolling(365, min_periods=120).median(), "agit", "calm")
            run = np.zeros(len(d)); loss = np.zeros(len(d))
            for i in range(1, len(d)):
                if r.iloc[i] < 0:
                    run[i] = run[i-1]+1; loss[i] = loss[i-1]+abs(r.iloc[i])
            d["prevrun"] = pd.Series(run).shift(1).values
            d["prevloss"] = pd.Series(loss).shift(1).values/usual.values
            d["rz"] = r/usual
            d["ret5z"] = (c/c.shift(5)-1)/usual
            d["upbreak"] = (r > 0) & (d["prevrun"] > 0)
            d["alloc"] = b["postRebalance_current_allocation"].astype(float)
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["mu"] = D["coin"].map(D.groupby("coin")["r"].mean())
    D["prof"] = np.where(D["trend"] < -10, "falling", np.where(D["trend"] > 10, "rising", np.where(D["trend"].notna(), "choppy", "na")))
    D["day"] = D["ts"].dt.floor("D")
    D["x"] = -(D["nxt"]-D["mu"])  # short gain
    D["x3"] = -(D["nxt3"]-3*D["mu"])

    def stat(g, col="x"):
        g2 = g[[col, "day"]].dropna()
        if len(g2) < 10: return pd.Series({"n": len(g2), "mean%": np.nan, "t": np.nan})
        m = g2[col].mean(); dev = (g2[col]-m).groupby(g2["day"]).sum()
        se = np.sqrt((dev**2).sum())/len(g2)
        return pd.Series({"n": len(g2), "days": g2["day"].nunique(), "mean%": 100*m, "t": m/se})
    out = {}
    # 1. up days in falling markets (all, not only breaks): graded by up size, break vs not
    U = D[(D["r"] > 0) & (D["prof"] != "na")].copy()
    U["kind"] = np.where(U["upbreak"], "break", "cont")
    U["rzq"] = U.groupby("prof")["rz"].transform(lambda s: pd.qcut(s, 3, labels=False))
    out["up days short next1 by prof x kind x upsize tercile"] = U.groupby(["prof", "kind", "rzq"]).apply(stat)
    # 2. falling: up days, graded by 5-day return before (bounce after deep slide)
    F = U[U["prof"] == "falling"].copy()
    F["r5q"] = pd.qcut(F["ret5z"], 4, labels=False)
    out["falling up days short next1 by prior 5d tercile x agit"] = F.groupby(["agit", "r5q"]).apply(stat)
    out["falling up days short next3 by prior 5d quartile"] = F.groupby("r5q").apply(lambda g: stat(g, "x3"))
    # 3. rank correlations inside falling upbreaks
    B = F[F["upbreak"]].dropna(subset=["x", "prevloss", "rz"])
    res = {}
    for nm, v in {"prevloss": B["prevloss"], "rz": B["rz"], "loss*rz": B["prevloss"]*B["rz"], "loss+rz": B["prevloss"]+B["rz"]}.items():
        rho, p = stats.spearmanr(v, B["x"]); res[nm] = (rho, p, len(B))
    out["falling upbreak spearman vs short gain"] = pd.DataFrame(res, index=["rho", "p", "n"]).T
    # 4. choppy agitated: big up / down days next day
    C = D[(D["prof"] == "choppy")].copy()
    C["rzq"] = pd.qcut(C["rz"], 5, labels=False)
    out["choppy short next1 by agit x rz quintile"] = C.groupby(["agit", "rzq"]).apply(stat)
    # 5. falling all days by agit x rz quintile (long-sign flipped shown as short gain)
    A = D[D["prof"] == "falling"].copy()
    A["rzq"] = pd.qcut(A["rz"], 5, labels=False)
    out["falling short next1 by agit x rz quintile"] = A.groupby(["agit", "rzq"]).apply(stat)
    # 6. book: in falling upbreaks held vs not held
    out["falling upbreak held vs not"] = B.assign(held=B["alloc"].abs() > 0).groupby("held").apply(stat)
    return out
