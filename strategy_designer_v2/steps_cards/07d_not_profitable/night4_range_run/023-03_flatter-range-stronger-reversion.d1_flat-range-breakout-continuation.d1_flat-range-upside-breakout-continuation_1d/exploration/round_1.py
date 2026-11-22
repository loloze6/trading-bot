def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # ---- book daily returns, per window, mean over coins
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy()
            t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B = B.dropna().sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + B["book"]).cumprod()
    peak = eq.cummax(); dd = eq / peak - 1
    B["dd"] = dd
    yrs = len(B) / 365
    out["book summary"] = pd.Series({"days": len(B), "yearly": eq.iloc[-1] ** (1 / yrs) - 1, "maxdd": dd.min(),
                                     "mean": B.book.mean(), "sharpe": B.book.mean() / B.book.std() * np.sqrt(365)})
    # drawdown episodes
    ep = []; inDD = False
    for i in range(len(B)):
        if dd[i] < 0 and not inDD:
            inDD = True; s = i - 1 if i > 0 else 0
        if inDD and dd[i] == 0:
            seg = dd[s:i]; ep.append((s, seg.idxmin(), i, seg.min())); inDD = False
    if inDD:
        seg = dd[s:]; ep.append((s, seg.idxmin(), len(B) - 1, seg.min()))
    ep = sorted(ep, key=lambda x: x[3])[:6]
    er = []
    for s, m, e, v in ep:
        seg = B.iloc[s + 1:m + 1]
        er.append({"depth": v, "days_to_trough": m - s, "windows": f"w{B.wn[s+1]}-w{B.wn[m]}",
                   "book_ret": (1 + seg.book).prod() - 1, "hold_ret": (1 + seg.hold).prod() - 1})
    out["deepest falls"] = pd.DataFrame(er)
    # ---- per-bar features
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]
            r1 = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            hi = cl.rolling(30).max(); lo = cl.rolling(30).min()
            net = cl / cl.shift(29) - 1
            netr = (cl - cl.shift(29)).abs() / (hi - lo)
            pos = (cl - lo) / (hi - lo)
            vol = np.log(cl).diff().rolling(20).std()
            r5p = cl / cl.shift(5) - 1
            r90 = cl / cl.shift(90) - 1
            t = pd.DataFrame({"coin": c, "w": w, "g": a * r1, "a": a, "r1": r1, "net30": net, "netr": netr,
                              "pos": pos, "vol": vol, "r5p": r5p, "r90": r90, "f": b["forecast"]})
            br.append(t)
    X = pd.concat(br)
    act = X[X.a.abs() > 1e-6].dropna(subset=["g"])
    out["active bars"] = pd.Series({"n": len(act), "mean_gain": act.g.mean(), "share_active": len(act) / X.g.notna().sum()})
    def grp(col, q=5):
        z = act.dropna(subset=[col]).copy()
        z["q"] = pd.qcut(z[col], q, labels=False, duplicates="drop")
        g = z.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("g", "size"), gain=("g", "mean"),
                               sd=("g", "std"), alloc=("a", "mean"), r1=("r1", "mean"),
                               worst=("g", lambda s: s.quantile(0.02)))
        g["t"] = g.gain / (g.sd / np.sqrt(g.n))
        g["sum_gain"] = g.gain * g.n
        return g
    for col in ["net30", "netr", "vol", "r5p", "r90", "f", "pos"]:
        out["by " + col] = grp(col)
    return out
