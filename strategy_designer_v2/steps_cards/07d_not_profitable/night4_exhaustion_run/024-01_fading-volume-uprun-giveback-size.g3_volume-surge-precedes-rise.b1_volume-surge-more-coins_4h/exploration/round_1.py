import pandas as pd, numpy as np

def explore(data):
    out = {}
    # ---- book daily returns, mean over coins per (window, day)
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy()
            dd["coin"] = c; dd["window"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["window"].str[1:].astype(int)
    B = D.groupby(["wn", "day"])[["book_return", "coin_return"]].mean().reset_index().sort_values(["wn", "day"])
    B = B.dropna()
    v = (1 + B["book_return"]).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd.values
    yr = v.iloc[-1] ** (365 / len(B)) - 1
    out["book summary"] = pd.Series({"yearly": yr, "maxdd": dd.min(), "calmar": yr / -dd.min(), "days": len(B)})
    # drawdown by window: worst within-window fall of book and coins
    wins = []
    for wn, g in B.groupby("wn"):
        vb = (1 + g["book_return"]).cumprod(); vc = (1 + g["coin_return"]).cumprod()
        wins.append({"wn": wn, "book_ret": vb.iloc[-1] - 1, "coin_ret": vc.iloc[-1] - 1,
                     "book_mdd": (vb / vb.cummax() - 1).min(), "coin_mdd": (vc / vc.cummax() - 1).min(),
                     "dd_end_of_window": g["dd"].iloc[-1]})
    out["by window"] = pd.DataFrame(wins).set_index("wn").round(3)
    # bottom decile days of book: coin return
    q = B["book_return"].quantile(0.05)
    worst = B[B["book_return"] <= q]
    out["worst 5% book days"] = pd.Series({"n": len(worst), "book_mean": worst["book_return"].mean(),
                                          "coin_mean": worst["coin_return"].mean(),
                                          "share coin down": (worst["coin_return"] < 0).mean()})
    # ---- case-level: forward 18-bar returns by situation
    H = 18
    cases = []
    allg = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            cl = b["close"].values; vol = b["volume"].values; op = b["open"].values
            n = len(cl)
            for i in range(0, n - H, H):
                allg.append((c, cl[i + H] / cl[i] - 1))
            f = b["forecast"].values
            r1 = pd.Series(cl).pct_change().values
            r6 = pd.Series(cl).pct_change(6).values
            r18 = pd.Series(cl).pct_change(18).values
            r42 = pd.Series(cl).pct_change(42).values
            alloc = b["postRebalance_current_allocation"].values
            for s in range(0, n - H, H):
                seg = f[s:s + H]
                idx = None
                for j in range(s, s + H):
                    prev = f[j - 1] if j > 0 else 0
                    if f[j] - prev >= 2 and f[j] > 0:
                        idx = j; break
                if idx is None or idx + H >= n: continue
                fw = cl[idx + H] / cl[idx] - 1
                mae = cl[idx:idx + H + 1].min() / cl[idx] - 1
                cases.append(dict(coin=c, wn=int(w[1:]), f=f[idx], fw=fw, r1=r1[idx], r6=r6[idx],
                                  r18=r18[idx], r42=r42[idx], bar=(cl[idx] / op[idx] - 1), mae=mae))
    A = pd.DataFrame(allg, columns=["coin", "r"])
    drift = A.groupby("coin")["r"].mean()
    C = pd.DataFrame(cases)
    C["ex"] = C["fw"] - C["coin"].map(drift)
    def tab(col, k=5):
        g = C.dropna(subset=[col]).copy()
        g["q"] = pd.qcut(g[col], k, labels=False, duplicates="drop")
        t = g.groupby("q").agg(n=("ex", "size"), lo=(col, "min"), hi=(col, "max"),
                               fw=("fw", "mean"), ex=("ex", "mean"), sd=("ex", "std"), mae=("mae", "mean"))
        t["t"] = t["ex"] / (t["sd"] / np.sqrt(t["n"]))
        return t.round(4)
    out["by surge bar own return"] = tab("bar")
    out["by prior 1-day return"] = tab("r6")
    out["by prior 3-day return"] = tab("r18")
    out["by prior 7-day return"] = tab("r42")
    out["by forecast"] = tab("f", 4)
    return out
