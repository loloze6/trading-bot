def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day", "book_return", "coin_return"]].copy(); t["coin"] = c; t["w"] = w
            rows.append(t)
    D = pd.concat(rows); D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
    B = B.dropna().sort_values(["wn", "day"]).reset_index(drop=True)
    eq = (1 + B.book).cumprod(); dd = eq / eq.cummax() - 1
    # mark fall days: days from a peak to its trough, in the 4 deepest episodes
    ep = []; inDD = False
    for i in range(len(B)):
        if dd[i] < 0 and not inDD: inDD = True; s = i
        if inDD and dd[i] == 0:
            seg = dd[s:i]; ep.append((s, seg.idxmin(), seg.min())); inDD = False
    if inDD: seg = dd[s:]; ep.append((s, seg.idxmin(), seg.min()))
    ep = sorted(ep, key=lambda x: x[2])[:6]
    B["fall"] = 0
    for k, (s, m, v) in enumerate(ep): B.loc[s:m, "fall"] = 1
    fallkey = set(zip(B.wn[B.fall == 1], B.day[B.fall == 1]))
    br = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True); cl = b["close"]
            r1 = cl.shift(-1) / cl - 1; a = b["postRebalance_current_allocation"]
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            wn = int(w[1:])
            t = pd.DataFrame({"g": a * r1, "a": a, "r1": r1,
                              "r30": cl / cl.shift(30) - 1, "r90": cl / cl.shift(90) - 1,
                              "dd90": cl / cl.rolling(90, min_periods=30).max() - 1,
                              "ma50": cl / cl.rolling(50).mean() - 1,
                              "r5p": cl / cl.shift(5) - 1})
            t["fall"] = [ (wn, d) in fallkey for d in day ]
            t["wn"] = wn
            br.append(t)
    X = pd.concat(br).dropna(subset=["g"])
    act = X[X.a.abs() > 1e-6]
    out["fall vs rest (active)"] = act.groupby("fall").agg(n=("g", "size"), gain=("g", "mean"), alloc=("a", "mean"),
        r1=("r1", "mean"), r30=("r30", "median"), r90=("r90", "median"), dd90=("dd90", "median"), ma50=("ma50", "median"))
    out["fall vs rest (all bars)"] = X.groupby("fall").agg(n=("g", "size"), share_active=("a", lambda s: (s.abs() > 1e-6).mean()),
        r1=("r1", "mean"), dd90=("dd90", "median"), ma50=("ma50", "median"))
    def grp(col, q=5):
        z = act.dropna(subset=[col]).copy()
        z["q"] = pd.qcut(z[col], q, labels=False, duplicates="drop")
        g = z.groupby("q").agg(lo=(col, "min"), hi=(col, "max"), n=("g", "size"), gain=("g", "mean"), sd=("g", "std"),
                               alloc=("a", "mean"), fall_share=("fall", "mean"),
                               worst=("g", lambda s: s.quantile(0.02)))
        g["t"] = g.gain / (g.sd / np.sqrt(g.n)); g["sum_gain"] = g.gain * g.n
        return g
    for col in ["dd90", "ma50", "r30"]:
        out["by " + col] = grp(col)
    # gain in falls by sign of ma50
    f = act[act.fall]
    out["in falls by ma50 sign"] = f.groupby(f.ma50 > 0).agg(n=("g", "size"), gain=("g", "mean"), sum_gain=("g", "sum"))
    out["rest by ma50 sign"] = act[~act.fall].groupby(act[~act.fall].ma50 > 0).agg(n=("g", "size"), gain=("g", "mean"), sum_gain=("g", "sum"))
    # 5-day grid unusual move by forecast bucket and ma50 sign
    return out
