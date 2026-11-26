def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c in data["bars"]:
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            dr = pd.Series(cl).pct_change()
            n = len(b)
            nxt = np.r_[cl[1:] / cl[:-1] - 1, np.nan]
            nxt2 = np.r_[cl[2:] / cl[:-2] - 1, np.nan, np.nan]
            sd30 = dr.rolling(30, min_periods=10).std().values
            t60 = pd.Series(cl).pct_change(60).values
            down = (dr < 0).values
            k = 0; lo = 0.0
            alloc = b["postRebalance_current_allocation"].values
            ts = pd.to_datetime(b["timestamp"]).dt.floor("D").values
            for i in range(n):
                if i > 0 and down[i]:
                    k += 1; lo = (1 + lo) * (1 + dr.iloc[i]) - 1
                    run = 0; loss = 0.0
                else:
                    run = k; loss = lo; k = 0; lo = 0.0
                if i == n - 1 or not np.isfinite(t60[i]) or not (sd30[i] > 0):
                    continue
                if run >= 2 and dr.iloc[i] > 0:
                    rows.append(dict(coin=c, w=w, day=ts[i], nxt=nxt[i], nxt2=nxt2[i], t60=t60[i], run=run,
                                     depth=-loss / sd30[i], inpos=alloc[i] < 0, sd30=sd30[i]))
    D = pd.DataFrame(rows)
    F = D[D.t60 < -0.10].copy()
    def dayt(df, col):
        x = (-df[col]).groupby(df["day"]).sum().dropna()
        m = (-df[col]).mean()
        return pd.Series({"n": df[col].notna().sum(), "days": len(x), "shortret": m,
                          "t_day": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})
    F["dq"] = pd.qcut(F.depth, 4, labels=["q1", "q2", "q3", "q4"])
    out["falling rb by depth, 1d, per-day t"] = F.groupby("dq", observed=True).apply(lambda d: dayt(d, "nxt"))
    out["falling rb by depth, 2d"] = F.groupby("dq", observed=True).apply(lambda d: dayt(d, "nxt2"))
    out["falling rb q4 by window"] = F[F.dq == "q4"].groupby("w").apply(lambda d: dayt(d, "nxt"))
    out["falling rb q4 by inpos(agitated)"] = F[F.dq == "q4"].groupby("inpos").apply(lambda d: dayt(d, "nxt"))
    # hypothetical books: short size proportional to depth (scaled) vs depth^2, vol-scaled to 0.02/sd30, per coin-day, then day mean over 6 coins
    def book(df, wfun):
        g = -df["nxt"] * wfun(df) * (0.02 / df["sd30"]).clip(upper=2) * 0.2
        s = g.groupby(df["day"]).sum() / 6.0
        return s
    res = {}
    for name, sub, wf in [("agitated lin", F[F.inpos], lambda d: d.depth),
                          ("falling lin", F, lambda d: d.depth),
                          ("falling sq", F, lambda d: d.depth ** 2 / 3),
                          ("falling excess(depth-1.5)+", F, lambda d: (d.depth - 1.5).clip(lower=0) * 1.5)]:
        s = book(sub, wf)
        res[name] = {"days": len(s), "sum": s.sum(), "worst": s.min(), "sum_neg": s[s < 0].sum(),
                     "ratio_sum_to_worst5": s.sum() / -s.nsmallest(5).sum()}
    out["hypothetical books"] = pd.DataFrame(res).T
    out["falling rb by run x depth half"] = F.groupby([F.run.clip(upper=4), F.depth > F.depth.median()]).apply(lambda d: dayt(d, "nxt"))
    return out
