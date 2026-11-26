import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    H = 7
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            vsr = (c / c.shift(14) - 1) / (sd30 * np.sqrt(14))
            r1d_z = r1 / sd30
            fwd = c.shift(-H) / c - 1
            fwd1 = c.shift(-1) / c - 1
            ret60 = c / c.shift(60) - 1
            ts = pd.to_datetime(b["timestamp"])
            d = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(len(b)),
                "vsr": vsr, "z1": r1d_z, "fwd": fwd, "fwd1": fwd1, "r60": ret60,
                "regime": b["regime"].values, "dow": ts.dt.dayofweek.values,
                "year": ts.dt.year.values,
                "alloc": b["postRebalance_current_allocation"].astype(float).values,
            })
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    drift = A.groupby("coin").apply(lambda g: g[g.pos % H == 0]["fwd"].mean())
    A["ufwd"] = A["fwd"] - A["coin"].map(drift)
    A["inprof"] = A["regime"].isin(["trending", "unknown"])
    G = A[(A.pos % H == 0) & A.ufwd.notna() & A.vsr.notna()].copy()

    def summ(g):
        x = g["ufwd"]
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan})

    G["vbin"] = pd.cut(G.vsr, [-np.inf, -1.5, -1, -0.5, 0, 0.5, 1, 1.5, np.inf])
    out = {}
    out["regime counts all bars"] = A.regime.value_counts()
    out["vsr bin, in profile"] = G[G.inprof].groupby("vbin").apply(summ)
    out["vsr bin, out of profile"] = G[~G.inprof].groupby("vbin").apply(summ)
    # trend-split out of profile
    G["trend"] = np.where(G.r60 > 0.10, "rising", np.where(G.r60 < -0.10, "falling", "choppy"))
    out["vsr sign x trend (60d in-window), |vsr|>1"] = G[G.vsr.abs() > 1].assign(sgn=np.sign(G.vsr)).groupby(["trend", "sgn"]).apply(summ)
    # corr vsr with fwd in profile
    gp = G[G.inprof]
    out["in-profile spearman vsr vs ufwd"] = pd.Series(stats.spearmanr(gp.vsr, gp.ufwd), index=["rho", "p"])
    go = G[~G.inprof]
    out["out-profile spearman vsr vs ufwd"] = pd.Series(stats.spearmanr(go.vsr, go.ufwd), index=["rho", "p"])
    # 1-day large moves, next-day return, all bars grid 1 (every bar)
    A["z1bin"] = pd.cut(A.z1, [-np.inf, -2, -1, 1, 2, np.inf])
    def s1(g):
        x = g["fwd1"].dropna(); n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n))})
    out["next day by 1d z, in profile"] = A[A.inprof].groupby("z1bin").apply(s1)
    out["next day by 1d z, out profile"] = A[~A.inprof].groupby("z1bin").apply(s1)
    out["next day by weekday"] = A.groupby("dow").apply(s1)
    # 7d fwd after big 1d moves on grid
    G["z1bin"] = pd.cut(G.z1, [-np.inf, -2, -1, 1, 2, np.inf])
    out["7d after 1d z bin, all"] = G.groupby("z1bin").apply(summ)
    # book day returns by year & window
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d.assign(coin=coin, win=w))
    D = pd.concat(dd)
    out["book ret by window (sum over coins mean)"] = D.groupby("win")["book_return"].agg(["mean", "count"])
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items()])
    out["trades by coin"] = T.groupby("coin")["net_profit_loss_percent"].agg(["count", "mean", "median"])
    out["trades entry_forecast tercile"] = T.groupby(pd.qcut(T.entry_forecast, 3, duplicates="drop"))["net_profit_loss_percent"].agg(["count", "mean"])
    return out
