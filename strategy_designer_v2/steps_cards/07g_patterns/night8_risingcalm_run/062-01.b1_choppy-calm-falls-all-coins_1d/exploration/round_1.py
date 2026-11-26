import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows = []
    daily = []
    for coin, wins in data["bars"].items():
        # coin drift on 5-bar grid over all windows
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            s5 = (c / c.shift(5) - 1) / (sd30 * np.sqrt(5))
            s10 = (c / c.shift(10) - 1) / (sd30 * np.sqrt(10))
            s1 = r1 / sd30
            f5 = c.shift(-5) / c - 1
            f1 = c.shift(-1) / c - 1
            f2 = c.shift(-2) / c - 1
            rng = (b["high"] - b["low"]) / c / sd30
            clo = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            vol_rank = sd30.rolling(60, min_periods=30).rank(pct=True)
            ret20 = c / c.shift(20) - 1
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(len(b)),
                               "s1": s1, "s5": s5, "s10": s10, "f1": f1, "f2": f2, "f5": f5,
                               "rng": rng, "clo": clo, "wd": ts.dt.weekday, "yr": ts.dt.year,
                               "prof": (b["regime"] == "unknown"), "fc": b["forecast"],
                               "alloc": b["postRebalance_current_allocation"],
                               "vr": vol_rank, "r20": ret20 / (sd30 * np.sqrt(20)), "day": ts.dt.floor("D")})
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    # drift per coin (5-bar grid) and 1-bar mean
    g5 = A[A.pos % 5 == 0].dropna(subset=["f5"])
    d5 = g5.groupby("coin")["f5"].mean()
    d1 = A.groupby("coin")["f1"].mean()
    A["x5"] = A["f5"] - A["coin"].map(d5)
    A["x1"] = A["f1"] - A["coin"].map(d1)
    G = A[A.pos % 5 == 0].dropna(subset=["x5", "s5"])
    out = {}
    def tab(df, key, val, q=5):
        d = df.dropna(subset=[key, val]).copy()
        d["b"] = pd.qcut(d[key], q, labels=False, duplicates="drop")
        t = d.groupby("b")[val].agg(["count", "mean", "std"])
        t["t"] = t["mean"] / (t["std"] / np.sqrt(t["count"]))
        t["keymean"] = d.groupby("b")[key].mean()
        return t.round(4)
    out["s5 quint -> x5, in profile"] = tab(G[G.prof], "s5", "x5")
    out["s5 quint -> x5, out of profile"] = tab(G[~G.prof], "s5", "x5")
    out["s5 quint -> x5, all"] = tab(G, "s5", "x5")
    out["s10 quint -> x5, all"] = tab(G, "s10", "x5")
    out["r20 quint -> x5, all"] = tab(G, "r20", "x5")
    A1 = A.dropna(subset=["x1", "s1"])
    out["s1 quint -> next day x1, all"] = tab(A1, "s1", "x1")
    out["range (swing units) quint -> x1"] = tab(A1, "rng", "x1")
    out["close-in-range quint -> x1"] = tab(A1.dropna(subset=["clo"]), "clo", "x1")
    out["vol rank quint -> x5"] = tab(G.dropna(subset=["vr"]), "vr", "x5")
    wd = A1.groupby("wd")["x1"].agg(["count", "mean", "std"]); wd["t"] = wd["mean"] / (wd["std"] / np.sqrt(wd["count"]))
    out["weekday -> x1"] = wd.round(5)
    # interaction: big range & low close, out of profile vs in
    for name, m in [("in", A1.prof), ("out", ~A1.prof)]:
        d = A1[m].dropna(subset=["rng", "clo"])
        k = (d.rng > d.rng.quantile(0.8)) & (d.clo < 0.25)
        out[f"wide low-close next-day x1 {name}"] = pd.Series({"n": k.sum(), "mean": d.x1[k].mean(), "t": stats.ttest_1samp(d.x1[k], 0).statistic})
    # book daily returns by weekday and per window
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            bd.append(d.assign(coin=coin, w=w))
    D = pd.concat(bd)
    D["day"] = pd.to_datetime(D["day"])
    bk = D.groupby("day")["book_return"].mean()
    out["book by window"] = D.groupby("w")["book_return"].agg(["count", "mean"]).round(5)
    # trades
    T = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for w, t in ws.items() if len(t)])
    T["ef"] = T["entry_forecast"]
    T["b"] = pd.qcut(T["ef"], 4, labels=False, duplicates="drop")
    out["trades by entry forecast quartile"] = T.groupby("b")[["profit_loss_percent", "net_profit_loss_percent", "ef"]].agg(["count", "mean"]).round(3)
    return out
