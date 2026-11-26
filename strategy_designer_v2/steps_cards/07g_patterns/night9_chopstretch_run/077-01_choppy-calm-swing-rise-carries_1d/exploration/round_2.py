import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            vsr = (c / c.shift(14) - 1) / (sd30 * np.sqrt(14))
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({"coin": coin, "win": w, "pos": np.arange(len(b)), "vsr": vsr,
                              "regime": b["regime"].values, "year": ts.dt.year.values,
                              "day": ts.dt.floor("D").values,
                              "r60": (c / c.shift(60) - 1).values})
            for H in [3, 7, 14]:
                d[f"f{H}"] = (c.shift(-H) / c - 1).values
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    A["inprof"] = A.regime.isin(["trending", "unknown"])
    out = {}

    def cl_t(g, col):
        g = g.dropna(subset=[col])
        if len(g) < 3: return pd.Series({"n": len(g), "mean": np.nan, "t_day": np.nan, "days": 0})
        m = g[col].mean()
        s = (g[col] - m).groupby(g["day"]).sum()
        G = len(s)
        se = np.sqrt((s ** 2).sum() * G / (G - 1)) / len(g)
        return pd.Series({"n": len(g), "mean": m, "t_day": m / se, "days": G})

    res = []
    for H in [3, 7, 14]:
        drift = A[A.pos % H == 0].groupby("coin")[f"f{H}"].mean()
        A[f"u{H}"] = A[f"f{H}"] - A.coin.map(drift)
    # robustness over grid offsets, H=7, in profile, by vsr side
    for off in range(7):
        G = A[((A.pos - off) % 7 == 0) & A.inprof & A.vsr.notna()]
        rho, p = stats.spearmanr(G.vsr, G.u7, nan_policy="omit")
        neg = G[G.vsr < -0.5]; pos = G[G.vsr > 0.5]
        res.append({"off": off, "n": len(G), "rho": rho, "p": p,
                    "neg_mean": neg.u7.mean(), "neg_n": neg.u7.notna().sum(),
                    "pos_mean": pos.u7.mean(), "pos_n": pos.u7.notna().sum()})
    out["grid offsets H7 in profile"] = pd.DataFrame(res)
    # horizons, in profile, grid 0
    hr = []
    for H in [3, 7, 14]:
        G = A[(A.pos % H == 0) & A.inprof & A.vsr.notna()].copy()
        G["sv"] = -G.vsr  # short side signed
        neg = G[G.vsr < -0.5].copy(); neg["su"] = -neg[f"u{H}"]
        pos = G[G.vsr > 0.5].copy(); pos["su"] = pos[f"u{H}"]
        a = cl_t(neg, "su"); b = cl_t(pos, "su")
        rho, p = stats.spearmanr(G.vsr, G[f"u{H}"], nan_policy="omit")
        hr.append({"H": H, "rho": rho, "p": p, "short_n": a.n, "short_mean": a["mean"], "short_t": a.t_day,
                   "long_n": b.n, "long_mean": b["mean"], "long_t": b.t_day})
    out["horizons in profile (short = minus fwd)"] = pd.DataFrame(hr)
    # short side by coin and year, H7 grid 0
    G = A[(A.pos % 7 == 0) & A.inprof & (A.vsr < -0.5)].copy()
    G["su"] = -G.u7
    out["short side by coin"] = G.groupby("coin").apply(lambda g: cl_t(g, "su"))
    out["short side by year"] = G.groupby("year").apply(lambda g: cl_t(g, "su"))
    # graded within negative: corr of vsr vs u7 within vsr<0 in profile
    Gn = A[(A.pos % 7 == 0) & A.inprof & (A.vsr < 0)]
    out["within vsr<0 spearman"] = pd.Series(stats.spearmanr(Gn.vsr, Gn.u7, nan_policy="omit"), index=["rho", "p"])
    # choppy agitated vs choppy calm (recomputed trend) for vsr carry
    A["trend"] = np.where(A.r60 > 0.10, "rising", np.where(A.r60 < -0.10, "falling", "choppy"))
    G7 = A[(A.pos % 7 == 0) & A.vsr.notna() & A.u7.notna()]
    cc = []
    for (tr, ip), g in G7.groupby(["trend", "inprof"]):
        rho, p = stats.spearmanr(g.vsr, g.u7)
        cc.append({"trend": tr, "inprof_regime": ip, "n": len(g), "rho": rho, "p": p})
    out["spearman by recomputed trend x inprof"] = pd.DataFrame(cc)
    return out
