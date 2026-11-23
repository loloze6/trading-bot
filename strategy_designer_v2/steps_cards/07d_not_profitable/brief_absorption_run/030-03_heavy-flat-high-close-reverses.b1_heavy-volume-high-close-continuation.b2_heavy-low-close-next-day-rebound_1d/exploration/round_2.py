def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days, bars = data["days"], data["bars"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    cs = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl, hi, lo, vol = b.close, b.high, b.low, b.volume
            r1 = cl.pct_change()
            fwd = cl.shift(-1) / cl - 1
            vr = vol / vol.shift(1).rolling(20, min_periods=20).mean()
            rng = (hi - lo)
            loc = (hi - cl) / rng.replace(0, np.nan)
            pos_gain = b.postRebalance_current_allocation * fwd
            df = pd.DataFrame({"coin": c, "win": w, "wn": int(w[1:]), "fc": b.forecast, "fwd": fwd, "r1": r1,
                               "r20": cl / cl.shift(20) - 1, "ma50": cl / cl.rolling(50, min_periods=30).mean() - 1,
                               "vr": vr, "loc": loc, "alloc": b.postRebalance_current_allocation, "pg": pos_gain})
            cs.append(df)
    A = pd.concat(cs).reset_index(drop=True)
    drift = A.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    A = A[A.fwd.notna()]
    def summ(g):
        n = len(g)
        return pd.Series({"n": n, "mean_fwd": g.fwd.mean(), "mean_ex": g.ex.mean(),
                          "t": g.ex.mean() / (g.ex.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "pos_gain_sum": g.pg.sum(), "mean_alloc": g.alloc.mean()})
    C = A[A.fc > 0].copy()
    C["locb"] = pd.cut(C["loc"], [-0.01, 0.25, 0.5, 0.75, 0.9, 1.01])
    out["cases by raw loc band"] = C.groupby("locb").apply(summ)
    C["down"] = C.r1 < 0
    out["cases loc>=0.75 x down day"] = C.groupby([C["loc"] >= 0.75, "down"]).apply(summ)
    # condition alone: heavy volume, loc<0.75 but down; and non-heavy loc>=0.75
    H = A[A.vr >= 2]
    out["heavy days by loc>=0.75"] = H.groupby(H["loc"] >= 0.75).apply(summ)
    N = A[(A.vr < 1.0)]
    out["ordinary-volume days by loc>=0.75"] = N.groupby(N["loc"] >= 0.75).apply(summ)
    # fall period w1-w3 vs rest
    C["fallwin"] = C.wn <= 3
    out["cases fall wins vs rest, by loc>=0.75"] = C.groupby(["fallwin", C["loc"] >= 0.75]).apply(summ)
    C["trend_dn"] = C.ma50 < 0
    out["cases by below ma50 x loc>=0.75"] = C.groupby(["trend_dn", C["loc"] >= 0.75]).apply(summ)
    # loss contribution of position by loc band over all
    out["pos gain share by band (all wins)"] = C.groupby("locb")["pg"].sum() / C["pg"].sum()
    # simulate a simple book: only cases loc>=0.75, alloc as recorded, daily mean over coins, then Calmar
    def calmar(mask):
        A2 = A.copy()
        A2["g"] = np.where(mask.reindex(A2.index, fill_value=False), A2.pg, 0.0)
        A2["g"] = A2["g"].fillna(0) - np.where(mask.reindex(A2.index, fill_value=False), 2 * 0.0019 / 2 * A2.alloc.abs().fillna(0), 0)
        A2["i"] = A2.groupby(["coin", "win"]).cumcount()
        D = A2.groupby(["wn", "i"])["g"].mean().sort_index()
        v = (1 + D).cumprod(); dd = (v / v.cummax() - 1).min()
        yr = v.iloc[-1] ** (365 / len(D)) - 1
        sh = D.mean() / D.std() * np.sqrt(365)
        return pd.Series({"yearly": yr, "maxdd": dd, "calmar": yr / -dd, "sharpe": sh})
    base = (A.fc > 0) & A.alloc.notna()
    out["approx book: all cases"] = calmar(base)
    out["approx book: loc>=0.75"] = calmar(base & (A["loc"] >= 0.75))
    out["approx book: loc>=0.5"] = calmar(base & (A["loc"] >= 0.5))
    out["approx book: down day"] = calmar(base & (A.r1 < 0))
    return out
