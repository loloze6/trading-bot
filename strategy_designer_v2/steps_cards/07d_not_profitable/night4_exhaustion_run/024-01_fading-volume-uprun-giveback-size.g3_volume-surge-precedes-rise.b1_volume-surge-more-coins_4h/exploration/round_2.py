import pandas as pd, numpy as np

def explore(data):
    out = {}
    H = 18
    cases = []; allg = []; barrows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; n = len(cl)
            for i in range(0, n - H, H):
                allg.append((c, cl[i + H] / cl[i] - 1))
            f = b["forecast"].values
            s = pd.Series(cl)
            r42 = s.pct_change(42).values; r180 = s.pct_change(180).values
            vol42 = s.pct_change().rolling(42).std().values
            alloc = b["postRebalance_current_allocation"].values
            nxt = np.append(cl[1:] / cl[:-1] - 1, np.nan)
            ts = pd.to_datetime(b["timestamp"])
            barrows.append(pd.DataFrame({"coin": c, "wn": int(w[1:]), "day": ts.dt.floor("D").values,
                                         "alloc": alloc, "g": alloc * nxt, "r42": r42, "r180": r180}))
            for st in range(0, n - H, H):
                idx = None
                for j in range(st, st + H):
                    prev = f[j - 1] if j > 0 else 0
                    if f[j] - prev >= 2 and f[j] > 0:
                        idx = j; break
                if idx is None or idx + H >= n: continue
                cases.append(dict(coin=c, wn=int(w[1:]), year=ts.iloc[idx].year, f=f[idx],
                                  fw=cl[idx + H] / cl[idx] - 1, r42=r42[idx], r180=r180[idx],
                                  z42=r42[idx] / (vol42[idx] * np.sqrt(42)) if vol42[idx] > 0 else np.nan))
    A = pd.DataFrame(allg, columns=["coin", "r"]); drift = A.groupby("coin")["r"].mean()
    C = pd.DataFrame(cases); C["ex"] = C["fw"] - C["coin"].map(drift)
    def tab(g, col, k=5):
        g = g.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], k, labels=False, duplicates="drop")
        t = g.groupby("q").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"), fw=("fw", "mean"),
                               ex=("ex", "mean"), sd=("ex", "std"))
        t["t"] = t["ex"] / (t["sd"] / np.sqrt(t["n"])); return t.round(4)
    out["by prior 30-day return"] = tab(C, "r180")
    out["by 7-day return in its own vol units"] = tab(C, "z42")
    C["up7"] = np.sign(C["r42"])
    y = C.dropna(subset=["r42"]).groupby(["year", "up7"])["ex"].agg(["size", "mean"]).unstack()
    out["ex by year, 7-day return sign"] = y.round(4)
    # book-level: bar gains by sign of 7-day return, and during the book's deepest fall
    Bb = pd.concat(barrows)
    Bb["s7"] = np.sign(Bb["r42"]); Bb["s30"] = np.sign(Bb["r180"])
    out["bar gain by 7d sign"] = Bb.groupby("s7").agg(bars=("g", "size"), mean_alloc=("alloc", "mean"),
                                                     sum_gain=("g", "sum"), mean_gain=("g", "mean")).round(5)
    out["bar gain by 30d sign"] = Bb.groupby("s30").agg(bars=("g", "size"), mean_alloc=("alloc", "mean"),
                                                       sum_gain=("g", "sum"), mean_gain=("g", "mean")).round(5)
    # approximate book daily return if only positions with r42>0 kept (gain per coin-day mean)
    Bb["g7"] = np.where(Bb["r42"] > 0, Bb["g"], 0.0)
    Bb["g30"] = np.where(Bb["r180"] > 0, Bb["g"], 0.0)
    cd = Bb.groupby(["wn", "day", "coin"])[["g", "g7", "g30"]].sum().groupby(["wn", "day"]).mean().sort_index()
    res = {}
    for col in ["g", "g7", "g30"]:
        v = (1 + cd[col]).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(cd)) - 1
        res[col] = {"yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                    "sharpe": cd[col].mean() / cd[col].std() * np.sqrt(365)}
    out["gross book (no fees) all / only 7d up / only 30d up"] = pd.DataFrame(res).round(3)
    return out
