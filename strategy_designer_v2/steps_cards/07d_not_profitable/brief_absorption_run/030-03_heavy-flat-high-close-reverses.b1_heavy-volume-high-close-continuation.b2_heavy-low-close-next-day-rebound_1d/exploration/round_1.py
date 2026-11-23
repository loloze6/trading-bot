def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    days, bars = data["days"], data["bars"]
    coins = list(bars.keys())
    wins = sorted({w for c in coins for w in bars[c].keys()}, key=lambda s: int(s[1:]))
    # book daily returns
    rows = []
    for w in wins:
        frames = []
        for c in coins:
            if w in days[c]:
                d = days[c][w][["day", "book_return", "coin_return"]].copy()
                d["coin"] = c
                frames.append(d)
        if not frames: continue
        f = pd.concat(frames)
        g = f.groupby("day").agg(book=("book_return", "mean"), hold=("coin_return", "mean")).reset_index()
        g["win"] = w
        rows.append(g)
    B = pd.concat(rows).reset_index(drop=True)
    B["book"] = B["book"].fillna(0)
    val = (1 + B["book"]).cumprod()
    peak = val.cummax()
    dd = val / peak - 1
    B["dd"] = dd
    i_tr = dd.idxmin()
    i_pk = val[:i_tr + 1].idxmax()
    out["deepest fall"] = pd.Series({"depth": dd.min(), "days": i_tr - i_pk, "start win": B.loc[i_pk, "win"], "end win": B.loc[i_tr, "win"]})
    # top drawdown episodes
    ep = []
    in_dd = False
    for i in range(len(B)):
        if dd[i] < 0 and not in_dd:
            in_dd = True; s = i - 1 if i > 0 else 0
        if in_dd and dd[i] == 0:
            seg = dd[s:i]; ep.append((seg.min(), s, seg.idxmin(), i)); in_dd = False
    if in_dd:
        seg = dd[s:]; ep.append((seg.min(), s, seg.idxmin(), len(B)))
    ep = sorted(ep)[:6]
    out["top falls"] = pd.DataFrame([{"depth": e[0], "len_to_trough": e[2] - e[1], "win_start": B.loc[e[1], "win"], "win_trough": B.loc[e[2], "win"], "hold_ret_in_fall": (1 + B.loc[e[1] + 1:e[2], "hold"].fillna(0)).prod() - 1} for e in ep])
    # cases
    cs = []
    for c in coins:
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl, hi, lo, op, vol = b.close, b.high, b.low, b.open, b.volume
            r1 = cl.pct_change()
            fwd = cl.shift(-1) / cl - 1
            vr = vol / vol.shift(1).rolling(20, min_periods=20).mean()
            rng = (hi - lo)
            loc = (hi - cl) / rng.replace(0, np.nan)
            df = pd.DataFrame({"coin": c, "win": w, "fc": b.forecast, "fwd": fwd, "r1": r1,
                               "r5": cl / cl.shift(5) - 1, "r20": cl / cl.shift(20) - 1,
                               "ma50": cl / cl.rolling(50, min_periods=30).mean() - 1,
                               "vr": vr, "loc": loc, "rngpct": rng / cl,
                               "vol20": r1.rolling(20, min_periods=15).std(),
                               "alloc": b.postRebalance_current_allocation})
            cs.append(df)
    A = pd.concat(cs).reset_index(drop=True)
    drift = A.groupby("coin")["fwd"].mean()
    A["ex"] = A["fwd"] - A["coin"].map(drift)
    A["case"] = A["fc"] > 0
    C = A[A.case & A.fwd.notna()].copy()
    out["n cases"] = len(C)
    def summ(g):
        return pd.Series({"n": len(g), "mean_fwd": g.fwd.mean(), "mean_ex": g.ex.mean(), "t": g.ex.mean() / (g.ex.std() / np.sqrt(len(g))) if len(g) > 2 else np.nan, "hit": (g.fwd > 0).mean()})
    for col in ["r1", "r5", "r20", "ma50", "vol20", "vr", "rngpct"]:
        C[col + "_q"] = pd.qcut(C[col], 4, labels=False, duplicates="drop")
        out["cases by " + col + " quartile"] = C.groupby(col + "_q").apply(summ)
    C["loc_q"] = pd.qcut(C["loc"], 4, labels=False, duplicates="drop")
    out["cases by loc quartile"] = C.groupby("loc_q").apply(summ)
    out["cases by coin"] = C.groupby("coin").apply(summ)
    C["yr"] = 0
    out["cases loss tail"] = pd.Series({"fwd p5": C.fwd.quantile(0.05), "fwd p1": C.fwd.quantile(0.01), "share fwd<-5%": (C.fwd < -0.05).mean(), "mean alloc": C.alloc.mean()})
    # cases in deepest fall
    fall_days = set(zip(B.loc[i_pk:i_tr, "win"], B.loc[i_pk:i_tr, "day"]))
    out["book days in fall"] = B.loc[i_pk:i_tr].shape[0]
    return out
