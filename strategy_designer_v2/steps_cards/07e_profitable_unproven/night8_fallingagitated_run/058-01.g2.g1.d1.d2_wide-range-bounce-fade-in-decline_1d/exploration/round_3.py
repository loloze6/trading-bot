def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    mu = {}
    for c in bars:
        r = pd.concat([b["close"].pct_change() for b in bars[c].values()])
        mu[c] = r.mean()
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"]; r1 = cl.pct_change()
            d = pd.DataFrame({"coin": c, "win": w, "year": pd.to_datetime(b["timestamp"]).dt.year.values})
            d["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            d["r1"] = r1.values
            d["r3"] = (cl / cl.shift(3) - 1).values
            d["r60"] = (cl / cl.shift(60) - 1).values
            sd = r1.rolling(30, min_periods=20).std()
            sdy = sd.rolling(365, min_periods=120).median()
            d["agit"] = (sd > sdy).values
            d["agit_known"] = sdy.notna().values
            d["rr"] = (((b["high"] - b["low"]) / cl) / sd).values
            d["f1"] = (cl.shift(-1) / cl - 1).values
            d["f2"] = (cl.shift(-2) / cl - 1).values
            d["inprof"] = b["regime"].isin(["mean_reversion", "unknown"]).values
            d["mu"] = mu[c]
            rows.append(d)
    D = pd.concat(rows, ignore_index=True)
    D["trend"] = np.where(D.r60 > 0.10, "rising", np.where(D.r60 < -0.10, "falling", "choppy"))
    def summ(X, col="f1"):
        h = int(col[1:])
        X = X.dropna(subset=[col])
        u = -(X[col] - X["mu"] * h)
        g = u.groupby(X["day"]).sum()
        t = g.mean() / (g.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan
        return pd.Series({"n": len(u), "days": len(g), "mean_u": u.mean(), "t_day": t})
    S = D[(D.r1 > 0) & (D.r3 < 0)].dropna(subset=["rr"]).copy()
    S["rr_q"] = pd.qcut(S["rr"], 4, labels=False)
    F = S[(S.trend == "falling") & S.agit_known]
    out["falling_by_agit_rrq"] = F.groupby(["agit", "rr_q"]).apply(summ)
    out["falling_by_agit_rrq_f2"] = F.groupby(["agit", "rr_q"]).apply(lambda x: summ(x, "f2"))
    Fa = S[S.trend == "falling"]
    out["falling_top2q_excl_w14"] = summ(Fa[(Fa.rr_q >= 2) & (Fa.win != "w14")])
    out["falling_top2q_by_year"] = Fa[Fa.rr_q >= 2].groupby("year").apply(summ)
    out["falling_top2q_by_coin"] = Fa[Fa.rr_q >= 2].groupby("coin").apply(summ)
    P = S[S.inprof]
    out["prof_by_rrq_f2"] = P.groupby("rr_q").apply(lambda x: summ(x, "f2"))
    out["prof_by_rrq_f2_excl_w14"] = P[P.win != "w14"].groupby("rr_q").apply(lambda x: summ(x, "f2"))
    return out
