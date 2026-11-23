def explore(data):
    import numpy as np, pandas as pd
    out = {}
    coins = list(data["bars"].keys())
    wins = sorted(data["days"][coins[0]].keys(), key=lambda w: int(w[1:]))
    # book daily chain
    segs = []
    for w in wins:
        frames = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            frames.append(d.set_index("day")[["book_return", "coin_return"]].add_prefix(c + "_"))
        df = pd.concat(frames, axis=1)
        br = df[[k for k in df.columns if k.endswith("book_return")]].mean(axis=1)
        cr = df[[k for k in df.columns if k.endswith("coin_return")]].mean(axis=1)
        s = pd.DataFrame({"br": br.fillna(0), "cr": cr.fillna(0)})
        s["win"] = w
        segs.append(s.reset_index(drop=True))
    B = pd.concat(segs, ignore_index=True)
    v = (1 + B.br).cumprod()
    dd = v / v.cummax() - 1
    B["dd"] = dd
    out["maxdd"] = float(dd.min())
    # episodes: worst 5 drawdowns
    peak = v.cummax()
    eps = []
    i = 0; n = len(v)
    inep = False
    for k in range(n):
        if dd.iloc[k] < 0 and not inep:
            inep = True; st = k
        if inep and dd.iloc[k] == 0:
            seg = dd.iloc[st:k]
            eps.append((seg.min(), st, k, int(seg.idxmin())))
            inep = False
    if inep:
        seg = dd.iloc[st:]; eps.append((seg.min(), st, n, int(seg.idxmin())))
    eps = sorted(eps)[:6]
    rows = []
    for m, st, en, tr in eps:
        sub = B.iloc[st:tr + 1]
        rows.append({"depth": m, "days_to_trough": tr - st + 1, "wins": ",".join(sorted(set(sub.win), key=lambda x: int(x[1:]))),
                     "coin_avg_ret_over_fall": float((1 + sub.cr).prod() - 1), "book_ret": float((1 + sub.br).prod() - 1)})
    out["worst_falls"] = pd.DataFrame(rows)
    # bar-level panel
    P = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            r = b.close.pct_change()
            b["nxt"] = b.close.shift(-1) / b.close - 1
            b["r20"] = b.close / b.close.shift(20) - 1
            b["r5"] = b.close / b.close.shift(5) - 1
            vol = r.rolling(20).std()
            b["vr"] = vol / vol.rolling(60).mean()
            b["volr"] = b.volume / b.volume.shift(1).rolling(20).mean()
            rng = (b.high - b.low).replace(0, np.nan)
            b["cl"] = (b.high - b.close) / rng
            b["dayret"] = r
            b["alloc"] = b.postRebalance_current_allocation
            b["gain"] = b.alloc * b.nxt
            b["coin"] = c; b["win"] = w
            P.append(b[["coin", "win", "nxt", "r20", "r5", "vr", "volr", "cl", "dayret", "alloc", "gain", "forecast", "regime"]])
    P = pd.concat(P, ignore_index=True)
    out["forecast_desc"] = P.forecast.describe()
    out["alloc_desc"] = P.alloc.describe()
    P["inpos"] = P.alloc.abs() > 1e-6
    P["sig"] = P.forecast > 0
    out["inpos_vs_sig"] = pd.crosstab(P.inpos, P.sig)
    # holding: how long positions persist with forecast 0
    out["gain_by_sig_inpos"] = P.groupby(["sig", "inpos"]).agg(n=("gain", "size"), meangain=("gain", "mean"), meannxt=("nxt", "mean"))
    H = P[P.inpos].copy()
    H["r20q"] = pd.qcut(H.r20, 5, labels=False)
    out["held_by_r20q"] = H.groupby("r20q").agg(n=("gain", "size"), r20=("r20", "mean"), gain=("gain", "mean"), sd=("gain", "std"), nxt=("nxt", "mean"))
    H["vrq"] = pd.qcut(H.vr, 5, labels=False)
    out["held_by_vrq"] = H.groupby("vrq").agg(n=("gain", "size"), vr=("vr", "mean"), gain=("gain", "mean"), sd=("gain", "std"), nxt=("nxt", "mean"))
    H["dq"] = pd.qcut(H.dayret, 5, labels=False)
    out["held_by_dayret_q"] = H.groupby("dq").agg(n=("gain", "size"), d=("dayret", "mean"), gain=("gain", "mean"), sd=("gain", "std"))
    # all bars: next-day return by r20 quintile, signal vs not
    P["r20q"] = pd.qcut(P.r20, 5, labels=False)
    out["nxt_by_r20q_sig"] = P.groupby(["r20q", "sig"]).nxt.agg(["size", "mean"]).unstack()
    out["nxt_by_regime"] = P.groupby("regime").nxt.agg(["size", "mean"])
    return out
