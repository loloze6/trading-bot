def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd20 = r1.rolling(20, min_periods=15).std()
            z = r1 / sd20
            ret90 = c / c.shift(90) - 1
            fall = np.where(ret90.notna(), ret90 < 0, b["regime"].eq("mean_reversion"))
            ret20 = c / c.shift(20) - 1
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            ts = pd.to_datetime(b["timestamp"])
            df = pd.DataFrame({"coin": coin, "w": w, "z": z, "sd20": sd20, "fall": fall,
                               "ret90": ret90, "ret20": ret20, "f5": f5, "f1": f1,
                               "fc": b["forecast"], "pos": b["postRebalance_current_allocation"],
                               "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "grid": (np.arange(len(b)) % 5 == 0)})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    G = A[A.grid & A.f5.notna()].copy()
    drift = G.groupby("coin").f5.mean()
    G["u5"] = G.f5 - G.coin.map(drift)
    usual = G.groupby("coin").f5.std()
    G["s5"] = G.u5 / G.coin.map(usual)

    def summ(g, col="u5"):
        x = g[col].dropna()
        n = len(x)
        m = x.mean()
        t = m / (x.std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series({"n": n, "mean": m, "t": t})

    G["zb"] = pd.cut(G.z, [-np.inf, -2, -1, -0.3, 0.3, 1, 2, np.inf])
    out = {}
    out["u5 by fall x z bucket"] = G.groupby(["fall", "zb"]).apply(summ).round(4)
    G["r90b"] = pd.cut(G.ret90, [-np.inf, -0.5, -0.3, -0.1, 0, 0.1, 0.3, 0.6, np.inf])
    out["u5 by 90d return bucket"] = G.groupby("r90b").apply(summ).round(4)
    G["r20b"] = pd.cut(G.ret20, [-np.inf, -0.3, -0.15, -0.05, 0.05, 0.15, 0.3, np.inf])
    out["u5 by 20d return bucket"] = G.groupby("r20b").apply(summ).round(4)
    G["vq"] = G.groupby("coin").sd20.transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["u5 by vol quintile (within coin)"] = G.groupby("vq").apply(summ).round(4)
    out["u5 by year"] = G.groupby("yr").apply(summ).round(4)
    # next-day returns by weekday, all bars
    A1 = A[A.f1.notna()].copy()
    d1 = A1.groupby("coin").f1.mean()
    A1["u1"] = A1.f1 - A1.coin.map(d1)
    out["u1 by weekday"] = A1.groupby("wd").apply(lambda g: summ(g, "u1")).round(5)
    # book: position sign
    A1["pnl"] = A1.pos * A1.f1
    A1["ps"] = np.sign(A1.pos.fillna(0))
    out["bar pnl by position sign"] = A1.groupby("ps").apply(lambda g: summ(g, "pnl")).round(5)
    A1["drift_part"] = A1.pos * A1.coin.map(d1)
    out["book split"] = pd.Series({"mean pnl/bar": A1.pnl.mean(), "drift part": A1.drift_part.mean(),
                                   "timing": (A1.pnl - A1.drift_part).mean(), "share short bars": (A1.ps < 0).mean()})
    # by coin, short cases
    S = G[G.fc <= -2]
    out["short-forecast cases by coin"] = S.groupby("coin").apply(summ).round(4)
    out["corr z with u5 by fall"] = G.groupby("fall").apply(lambda g: pd.Series({"corr": g[["z","u5"]].corr().iloc[0,1], "n": len(g)})).round(4)
    return out
