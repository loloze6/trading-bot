def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]; days = data["days"]
    out = {}
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values
            r30 = b["close"] / b["close"].shift(30) - 1
            r1 = b["close"].pct_change()
            for h in (3, 6, 10):
                for i in range(0, len(b) - h, h):
                    recs.append(dict(coin=c, w=w, h=h, f=b["forecast"].iloc[i], r30=r30.iloc[i], r1=r1.iloc[i],
                                     fwd=cl[i + h] / cl[i] - 1))
    g = pd.DataFrame(recs)
    g["ex"] = g["fwd"] - g.groupby(["coin", "h"])["fwd"].transform("mean")
    g = g.dropna(subset=["r30"])
    g["trend"] = np.where(g.r30 > 0, "up", "down")
    g["fb"] = pd.cut(g["f"], [-100, -1.5, 0, 1.5, 3, 100])
    tt = lambda x: x.mean() / x.std() * np.sqrt(len(x))
    out["h3_graded_by_trend"] = g[g.h == 3].groupby(["trend", "fb"]).agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                                          t=("ex", tt))
    out["wide_up_by_h"] = g[(g.f > 1.5)].groupby(["h", "trend"]).agg(n=("ex", "size"), mean_ex=("ex", "mean"),
                                                                    mean_fwd=("fwd", "mean"), t=("ex", tt))
    # slope within up trend and down trend, h3
    for tr in ("up", "down"):
        s = g[(g.h == 3) & (g.trend == tr)]
        sl = np.polyfit(s.f, s.ex, 1)[0]
        res = s.ex - np.polyval(np.polyfit(s.f, s.ex, 1), s.f)
        se = res.std() / (s.f.std() * np.sqrt(len(s)))
        out[f"slope_{tr}"] = f"n={len(s)} slope={sl:.5f} t={sl/se:.2f}"
    # book daily gain by side, fee by side
    pos = []
    for c in bars:
        for w, b in bars[c].items():
            r30 = b["close"] / b["close"].shift(30) - 1
            a = b["postRebalance_current_allocation"].values[:-1]
            r = (b["close"].shift(-1) / b["close"] - 1).values[:-1]
            fee = (b["postRebalance_total_value"] / b["total_portfolio_value"] - 1).values[:-1]
            pos.append(pd.DataFrame(dict(w=w, a=a, g=a * r, fee=fee, tr=np.where(r30.values[:-1] > 0, "up", "down"))))
    p = pd.concat(pos)
    p["side"] = np.where(p.a > 0, "long", np.where(p.a < 0, "short", "flat"))
    out["gain_by_side_trend"] = p.groupby(["side", "tr"]).agg(n=("g", "size"), gain=("g", "sum"), fee=("fee", "sum"))
    out["gain_by_side_worst_windows"] = p[p.w.isin(["w9", "w8", "w2", "w10"])].groupby(["w", "side"]).agg(
        gain=("g", "sum"), fee=("fee", "sum"))
    out["coin_ret_worst_windows"] = pd.Series({w: np.mean([days[c][w]["coin_return"].add(1).prod() - 1 for c in days
                                                           if w in days[c]]) for w in ["w9", "w8", "w2", "w10"]})
    return out
