def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    rows = []
    for c, ws in bars.items():
        for w, b in ws.items():
            b = b.copy()
            b["day"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            cl = b["close"]
            r1 = cl.shift(-1) / cl - 1
            a = b["postRebalance_current_allocation"]
            x = pd.DataFrame({"day": b["day"], "gain": a * r1, "glong": (a.clip(lower=0)) * r1,
                              "gshort": (a.clip(upper=0)) * r1, "a": a, "r1": r1,
                              "ret30": cl / cl.shift(30) - 1, "ret60": cl / cl.shift(60) - 1,
                              "f": b["forecast"], "pv": b["total_portfolio_value"],
                              "wn": int(w[1:]), "coin": c})
            rows.append(x)
    B = pd.concat(rows).dropna(subset=["gain"])
    # daily book from days table
    recs = []
    for c, ws in days.items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["coin"] = c; dd["wn"] = int(w[1:])
            recs.append(dd)
    D = pd.concat(recs)
    D["day"] = pd.to_datetime(D["day"]).dt.floor("D")
    g = D.groupby(["wn", "day"]).agg(book=("book_return", "mean"), coin=("coin_return", "mean")).reset_index()
    h = B.groupby(["wn", "day"]).agg(gain=("gain", "mean"), glong=("glong", "mean"), gshort=("gshort", "mean"),
                                     a=("a", "mean")).reset_index()
    # gain is for bar t -> t+1; shift to the day it is realised
    h["day"] = h["day"] + pd.Timedelta(days=1)
    m = g.merge(h, on=["wn", "day"], how="left").dropna(subset=["book"]).fillna(0).sort_values(["wn", "day"]).reset_index(drop=True)
    out = {}
    out["book vs bar gains, corr and means"] = pd.Series({"corr": m["book"].corr(m["gain"]), "mean_book": m["book"].mean(),
                                                         "mean_gain": m["gain"].mean(), "mean_long": m["glong"].mean(),
                                                         "mean_short": m["gshort"].mean()})
    def stats(s):
        eq = (1 + s).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yr = eq.iloc[-1] ** (365 / len(s)) - 1
        return pd.Series({"mean": s.mean(), "sharpe": s.mean() / s.std() * np.sqrt(365), "maxdd": dd, "calmar": yr / -dd})
    out["book, long legs only, short legs only (before costs)"] = pd.DataFrame({
        "book": stats(m["book"]), "gain": stats(m["gain"]), "long only": stats(m["glong"]), "short only": stats(m["gshort"]),
        "long + half short": stats(m["glong"] + 0.5 * m["gshort"])})
    # deepest fall of book: windows composition
    eq = (1 + m["book"]).cumprod(); ddn = eq / eq.cummax() - 1
    tr = ddn.idxmin(); pk = eq[:tr + 1].idxmax(); sp = m.loc[pk:tr]
    out["deepest fall span"] = pd.Series({"book_sum": sp["book"].sum(), "gain_sum": sp["gain"].sum(), "long_sum": sp["glong"].sum(),
                                          "short_sum": sp["gshort"].sum(), "coin_sum": sp["coin"].sum(), "mean_alloc": sp["a"].mean(), "days": len(sp)})
    out["fall span by window"] = sp.groupby("wn")[["book", "glong", "gshort", "coin"]].sum()
    # short gains by coin's 60-day return state (known at close)
    S = B[B["a"] < 0].dropna(subset=["ret60"]).copy()
    S["q60"] = pd.qcut(S["ret60"], 4, labels=False)
    out["short bars by 60d return quartile"] = S.groupby("q60").agg(ret60=("ret60", "mean"), gain=("gain", "mean"), r1=("r1", "mean"), n=("gain", "count"))
    L = B[B["a"] > 0].dropna(subset=["ret60"]).copy()
    L["q60"] = pd.qcut(L["ret60"], 4, labels=False)
    out["long bars by 60d return quartile"] = L.groupby("q60").agg(ret60=("ret60", "mean"), gain=("gain", "mean"), r1=("r1", "mean"), n=("gain", "count"))
    # 10-bar grid: forward 10d return by 30d return decile (excess of coin mean)
    G = []
    for c, ws in bars.items():
        rr = []
        for w, b in ws.items():
            cl = b["close"].reset_index(drop=True)
            idx = np.arange(0, len(cl) - 10, 10)
            fr = cl.shift(-10) / cl - 1; r30 = cl / cl.shift(30) - 1
            rr.append(pd.DataFrame({"fr": fr.iloc[idx].values, "r30": r30.iloc[idx].values, "f": b["forecast"].reset_index(drop=True).iloc[idx].values}))
        rr = pd.concat(rr); rr["ex"] = rr["fr"] - rr["fr"].mean(); G.append(rr)
    G = pd.concat(G).dropna()
    G["fq"] = pd.qcut(G["f"], 6, labels=False)
    out["10d excess by forecast sextile (grid)"] = G.groupby("fq").agg(f=("f", "mean"), ex=("ex", "mean"), t=("ex", lambda s: s.mean() / s.std() * np.sqrt(len(s))), n=("ex", "count"))
    return out
