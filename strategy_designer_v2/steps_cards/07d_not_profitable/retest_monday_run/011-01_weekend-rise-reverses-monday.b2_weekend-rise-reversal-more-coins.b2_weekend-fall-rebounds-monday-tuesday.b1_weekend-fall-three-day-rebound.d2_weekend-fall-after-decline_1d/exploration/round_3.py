def explore(data):
    import numpy as np, pandas as pd
    out = {}
    drift = {}; cases = []
    for c, ws in data["bars"].items():
        rr = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            if len(cl) > 3: rr += list(cl[3::3] / cl[0:-3:3] - 1)
            ts = pd.to_datetime(b["timestamp"])
            s = pd.Series(cl); r1 = s.pct_change()
            v20 = r1.rolling(20).std().values; v60 = r1.rolling(60).std().values
            r20 = s.pct_change(20).values; r100 = s.pct_change(100).values
            ma50 = s.rolling(50).mean().values
            for i in range(len(b) - 3):
                if ts[i].dayofweek != 6: continue
                cases.append(dict(coin=c, wn=int(w[1:]), date=ts[i].normalize(), fc=b["forecast"].iloc[i],
                                  alloc=b["postRebalance_current_allocation"].iloc[i], r1=r1.iloc[i],
                                  z1=r1.iloc[i] / v60[i] if v60[i] else np.nan, r20=r20[i], r100=r100[i],
                                  vrat=v20[i] / v60[i] if v60[i] else np.nan,
                                  below50=float(cl[i] < ma50[i]) if not np.isnan(ma50[i]) else np.nan,
                                  fwd=cl[i + 3] / cl[i] - 1))
        drift[c] = np.mean(rr)
    C = pd.DataFrame(cases)
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    C["pnl"] = C["alloc"] * C["fwd"]
    A = C[C["fc"] > 0].copy(); N = C[~(C["fc"] > 0)].copy()
    med = A["vrat"].median()
    def book(g):
        # per-date mean pnl over coins (19 coin book approx), chained
        d = g.groupby("date")["pnl"].sum() / 19.0
        d = d.sort_index()
        v = (1 + d).cumprod(); dd = (v / v.cummax() - 1).min()
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))),
                              total=v.iloc[-1] - 1, maxdd=dd, ratio=(v.iloc[-1] - 1) / -dd if dd < 0 else np.nan))
    filt = {"all": A, "vrat>med": A[A["vrat"] > med], "below50": A[A["below50"] == 1],
            "vrat>med & below50": A[(A["vrat"] > med) & (A["below50"] == 1)],
            "z1<-1": A[A["z1"] < -1], "r100<-0.4": A[A["r100"] < -0.4], "r100>=-0.4": A[A["r100"] >= -0.4]}
    out["filtered case-books"] = pd.DataFrame({k: book(v) for k, v in filt.items()}).T
    def summ(g):
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(),
                              t=g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan))
    A["r100q"] = pd.qcut(A["r100"], 4, labels=False)
    out["active by 100d ret q"] = A.groupby("r100q").apply(summ)
    out["active w2,w17 means"] = A[A["wn"].isin([2, 17])][["r1", "z1", "r20", "r100", "vrat", "below50", "alloc"]].mean()
    out["active other means"] = A[~A["wn"].isin([2, 17])][["r1", "z1", "r20", "r100", "vrat", "below50", "alloc"]].mean()
    A["zq"] = pd.qcut(A["z1"], 4, labels=False)
    out["active by z1 q"] = A.groupby("zq").apply(summ)
    out["nonactive z1<-1 (cond alone)"] = summ(N[N["z1"] < -1])
    return out
