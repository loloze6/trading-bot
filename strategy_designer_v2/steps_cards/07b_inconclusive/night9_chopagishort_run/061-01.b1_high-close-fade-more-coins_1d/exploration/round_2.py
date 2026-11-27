import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            rng = (b.high - b.low)
            cl = ((b.close - b.low) / rng.replace(0, np.nan))
            inprof = b.regime != "chop"
            ret1 = b.close.pct_change()
            for h in (2, 4, 5, 7):
                fwd = b.close.shift(-h) / b.close - 1
                df = pd.DataFrame({"coin": coin, "win": w, "h": h, "pos": np.arange(len(b)),
                                   "cell": np.arange(len(b)) // h, "cl": cl, "inprof": inprof,
                                   "fwd": fwd, "ret1": ret1, "rngpct": rng / b.close,
                                   "year": pd.to_datetime(b.timestamp).dt.year,
                                   "day": pd.to_datetime(b.timestamp).dt.floor("D")})
                rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    grid = A[A.pos % A.h == 0].dropna(subset=["fwd"])
    drift = grid.groupby(["coin", "h"]).fwd.mean().rename("drift")
    sd = grid.groupby(["coin", "h"]).fwd.std().rename("sd")
    A = A.join(drift, on=["coin", "h"]).join(sd, on=["coin", "h"])
    A = A.dropna(subset=["fwd", "cl"])
    A["fall"] = -(A.fwd - A.drift)

    def cases(sub):
        return sub.sort_values("pos").groupby(["coin", "win", "h", "cell"]).head(1)

    def stat(c):
        n = len(c)
        if n < 3: return pd.Series({"n": n})
        m = c.fall.mean()
        dev = c.groupby("day").fall.apply(lambda x: (x - m).sum())
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean_fall": m, "t": m / se, "strength": (c.fall / c.sd).mean()})

    out = {}
    hi = A[(A.cl >= 0.8) & A.inprof]
    out["by_h_inprof"] = pd.DataFrame({h: stat(cases(hi[hi.h == h])) for h in (2, 4, 5, 7)}).T
    for h in (2, 5):
        C = cases(hi[hi.h == h]).copy()
        med = C.cl.median()
        C["half"] = np.where(C.cl > med, "upper", "lower")
        out[f"h{h}_by_cl_half"] = C.groupby("half").apply(stat)
        C["r1q"] = pd.qcut(C.ret1, 3, labels=["low", "mid", "high"])
        out[f"h{h}_by_dayret_tercile"] = C.groupby("r1q", observed=True).apply(stat)
        if h == 5:
            out["h5_by_year"] = C.groupby("year").apply(stat)
            C["coingrp"] = np.where(C.coin.isin(["BTCUSD", "ETHUSD", "LTCUSD", "XMRUSD", "XRPUSD", "ZECUSD"]), "core", "other")
            out["h5_by_coingroup"] = C.groupby("coingrp").apply(stat)
            out["h5_by_coin_mean"] = C.groupby("coin").fall.agg(["count", "mean"])
            out["h5_corr_cl_fall"] = float(C[["cl", "fall"]].corr().iloc[0, 1])
            out["h5_corr_ret1_fall"] = float(C[["ret1", "fall"]].corr().iloc[0, 1])
    return out
