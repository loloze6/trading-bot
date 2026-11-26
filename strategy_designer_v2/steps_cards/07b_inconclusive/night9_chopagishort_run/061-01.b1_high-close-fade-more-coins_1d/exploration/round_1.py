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
            for h in (1, 2, 3, 5):
                fwd = b.close.shift(-h) / b.close - 1
                df = pd.DataFrame({"coin": coin, "win": w, "h": h, "pos": np.arange(len(b)),
                                   "cell": np.arange(len(b)) // h, "cl": cl, "inprof": inprof,
                                   "fwd": fwd, "ret1": ret1, "rngpct": rng / b.close,
                                   "year": pd.to_datetime(b.timestamp).dt.year,
                                   "day": pd.to_datetime(b.timestamp).dt.floor("D")})
                rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin and h from grid
    grid = A[A.pos % A.h == 0].dropna(subset=["fwd"])
    drift = grid.groupby(["coin", "h"]).fwd.mean().rename("drift")
    sd = grid.groupby(["coin", "h"]).fwd.std().rename("sd")
    A = A.join(drift, on=["coin", "h"]).join(sd, on=["coin", "h"])
    A = A.dropna(subset=["fwd", "cl"])
    A["fall"] = -(A.fwd - A.drift)

    def cases(sub):
        # first case per grid cell
        return sub.sort_values("pos").groupby(["coin", "win", "h", "cell"]).head(1)

    def stat(c):
        if len(c) < 3: return pd.Series({"n": len(c)})
        g = c.groupby("day").fall.sum()
        G = len(g); m = c.fall.mean(); n = len(c)
        se = np.sqrt((g - g.mean() * 0 - (g.index.map(lambda d: 0)) * 0).pow(2).sum() * 0 + ((c.groupby("day").fall.apply(lambda x: (x - m).sum())) ** 2).sum() * G / (G - 1)) / n
        return pd.Series({"n": n, "days": G, "mean_fall": m, "t": m / se, "strength": (c.fall / c.sd).mean()})

    out = {}
    hi = A[A.cl >= 0.8]
    out["by_h_inprofile_cl>=0.8"] = pd.DataFrame({h: stat(cases(hi[(hi.h == h) & hi.inprof])) for h in (1, 2, 3, 5)}).T
    out["by_h_outprofile_cl>=0.8"] = pd.DataFrame({h: stat(cases(hi[(hi.h == h) & ~hi.inprof])) for h in (1, 2, 3, 5)}).T
    P = A[(A.h == 2) & A.inprof].copy()
    P["clbin"] = pd.cut(P.cl, [-0.01, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 1.0])
    out["h2_inprof_by_clbin"] = P.groupby("clbin", observed=True).apply(lambda s: stat(cases(s)))
    H2 = cases(hi[(hi.h == 2) & hi.inprof]).copy()
    out["h2_cases_by_coin"] = H2.groupby("coin").apply(stat)
    out["h2_cases_by_year"] = H2.groupby("year").apply(stat)
    H2["upday"] = np.where(H2.ret1 > 0, "up", "down")
    out["h2_cases_by_dayret_sign"] = H2.groupby("upday").apply(stat)
    H2["rngq"] = pd.qcut(H2.rngpct / H2.sd, 3, labels=["narrow", "mid", "wide"])
    out["h2_cases_by_range_tercile"] = H2.groupby("rngq", observed=True).apply(stat)
    H2["r1q"] = pd.qcut(H2.ret1, 3, labels=["low", "mid", "high"])
    out["h2_cases_by_dayret_tercile"] = H2.groupby("r1q", observed=True).apply(stat)
    out["share_inprof_bars"] = float(A[A.h == 1].inprof.mean())
    return out
