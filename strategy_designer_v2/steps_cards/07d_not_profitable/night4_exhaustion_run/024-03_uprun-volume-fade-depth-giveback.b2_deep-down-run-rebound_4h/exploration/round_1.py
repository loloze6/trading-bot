def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c].keys()), key=lambda s: int(s[1:]))
    # book daily returns: mean over coins per day, per window
    rows = []
    for w in wins:
        br = []; cr = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            br.append(d.set_index("day")["book_return"].rename(c))
            cr.append(d.set_index("day")["coin_return"].rename(c))
        B = pd.concat(br, axis=1).mean(axis=1); C = pd.concat(cr, axis=1).mean(axis=1)
        df = pd.DataFrame({"b": B, "c": C}).dropna(); df["w"] = w
        rows.append(df.reset_index(drop=True))
    D = pd.concat(rows, ignore_index=True)
    eq = (1 + D.b).cumprod(); dd = eq / eq.cummax() - 1
    D["dd"] = dd.values
    out["overall"] = pd.Series({"mean_b": D.b.mean(), "sd_b": D.b.std(), "maxdd": dd.min(),
        "ann": eq.iloc[-1] ** (365 / len(D)) - 1, "ndays": len(D), "mean_c": D.c.mean()})
    # per-window stats
    g = D.groupby("w", sort=False)
    pw = pd.DataFrame({"book_sum": g.b.sum(), "coin_sum": g.c.sum(), "worst_dd_in_w": g.dd.min(),
                       "book_minday": g.b.min()})
    out["per_window"] = pw
    # worst 5% book days: coin return those days
    q = D.b.quantile(0.05)
    out["worst_days"] = pd.Series({"q05": q, "coin_on_worst": D.c[D.b <= q].mean(), "coin_all": D.c.mean(),
                                   "n": (D.b <= q).sum(), "share_loss_on_worst": D.b[D.b <= q].sum() / D.b[D.b < 0].sum()})
    # bar-level: allocation, gain decomposition, per coin
    pc = []
    allbars = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy()
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["a"] = b.postRebalance_current_allocation
            b["coin"] = c; b["w"] = w
            # prior 18-bar and 180-bar return
            b["ret3d_past"] = b.close / b.close.shift(18) - 1
            b["ret30d_past"] = b.close / b.close.shift(180) - 1
            b["fwd18"] = b.close.shift(-18) / b.close - 1
            allbars.append(b[["coin", "w", "a", "r1", "forecast", "ret3d_past", "ret30d_past", "fwd18", "volume", "close"]])
    A = pd.concat(allbars, ignore_index=True)
    A["gain"] = A.a * A.r1
    mr = A.groupby("coin").r1.mean()
    A["mkt"] = A.a * A.coin.map(mr)
    out["per_coin"] = A.groupby("coin").apply(lambda x: pd.Series({"share_in": (x.a > 0.01).mean(), "mean_alloc_in": x.a[x.a > 0.01].mean(),
        "gain_bar": x.gain.mean(), "mkt_part": x.mkt.mean()}))
    # gain by 30d trend regime when in position
    inn = A[A.a > 0.01].dropna(subset=["ret30d_past", "gain"])
    inn["trend_q"] = pd.qcut(inn.ret30d_past, 5, labels=False)
    out["in_pos_by_30d_trend_quintile"] = inn.groupby("trend_q").agg(n=("gain", "size"), mean_gain=("gain", "mean"),
        sum_gain=("gain", "sum"), mean_r1=("r1", "mean"), mean_alloc=("a", "mean"), ret30=("ret30d_past", "mean"))
    # non-overlapping 18-bar cases: forecast>=2 first in each cell, fwd by 30d trend
    cases = []
    for (c, w), x in A.groupby(["coin", "w"], sort=False):
        x = x.reset_index(drop=True); x["cell"] = x.index // 18
        s = x[x.forecast >= 2].groupby("cell").head(1)
        cases.append(s)
    S = pd.concat(cases).dropna(subset=["fwd18", "ret30d_past"])
    drift = {}
    for c in coins:
        v = []
        for w, b in data["bars"][c].items():
            cl = b.close.values[::18]; v += list(cl[1:] / cl[:-1] - 1)
        drift[c] = np.mean(v)
    S["unus"] = S.fwd18 - S.coin.map(drift)
    S["tq"] = pd.qcut(S.ret30d_past, 5, labels=False)
    def tt(x): return pd.Series({"n": len(x), "mean_fwd": x.fwd18.mean(), "mean_unus": x.unus.mean(),
                                "t": x.unus.mean() / (x.unus.std() / np.sqrt(len(x))), "ret30": x.ret30d_past.mean(),
                                "p10_fwd": x.fwd18.quantile(0.1)})
    out["cases_by_30d_trend"] = S.groupby("tq").apply(tt)
    S["dq"] = pd.qcut(S.ret3d_past, 5, labels=False)
    out["cases_by_3d_past"] = S.groupby("dq").apply(tt)
    return out
