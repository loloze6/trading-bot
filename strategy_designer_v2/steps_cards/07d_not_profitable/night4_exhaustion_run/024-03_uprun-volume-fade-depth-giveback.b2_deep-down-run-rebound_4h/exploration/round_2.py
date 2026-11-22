def explore(data):
    import pandas as pd, numpy as np
    out = {}
    coins = list(data["days"].keys())
    wins = sorted(set(w for c in coins for w in data["days"][c].keys()), key=lambda s: int(s[1:]))
    # holding's drawdown on same construction
    rows = []
    for w in wins:
        br = []; cr = []
        for c in coins:
            d = data["days"][c].get(w)
            if d is None: continue
            br.append(d.set_index("day")["book_return"].rename(c)); cr.append(d.set_index("day")["coin_return"].rename(c))
        df = pd.DataFrame({"b": pd.concat(br, axis=1).mean(axis=1), "c": pd.concat(cr, axis=1).mean(axis=1)}).dropna()
        df["w"] = w; rows.append(df.reset_index(drop=True))
    D = pd.concat(rows, ignore_index=True)
    eqc = (1 + D.c).cumprod(); eqb = (1 + D.b).cumprod()
    out["hold_vs_book"] = pd.Series({"hold_maxdd": (eqc / eqc.cummax() - 1).min(), "hold_ann": eqc.iloc[-1] ** (365 / len(D)) - 1,
        "book_maxdd": (eqb / eqb.cummax() - 1).min(), "corr_b_c": D.b.corr(D.c),
        "beta": np.polyfit(D.c, D.b, 1)[0], "hold_sd": D.c.std(), "book_sd": D.b.std()})
    # forecast vs allocation
    A = []
    for c in coins:
        for w, b in data["bars"][c].items():
            b = b.copy(); b["coin"] = c; b["w"] = w
            b["raw"] = b["debug_info.components.down_streak.last_history_value"]
            b["r1"] = b.close.shift(-1) / b.close - 1
            b["fwd18"] = b.close.shift(-18) / b.close - 1
            b["a"] = b.postRebalance_current_allocation
            # recompute streak length
            dn = (b.close < b.close.shift(1)).astype(int)
            grp = (dn == 0).cumsum(); b["slen"] = dn.groupby(grp).cumsum()
            b["vol_ratio"] = b.volume / b.volume.rolling(30).mean()
            b["ret30"] = b.close / b.close.shift(180) - 1
            A.append(b[["coin", "w", "forecast", "a", "raw", "r1", "fwd18", "slen", "vol_ratio", "ret30", "sizing_realised_vol"]])
    A = pd.concat(A, ignore_index=True)
    out["forecast_dist"] = pd.Series({"share_fc_pos": (A.forecast > 0).mean(), "share_fc_ge2": (A.forecast >= 2).mean(),
        "share_fc_zero": (A.forecast == 0).mean(), "median_fc_pos": A.forecast[A.forecast > 0].median(),
        "mean_alloc_fc0": A.a[A.forecast == 0].mean(), "share_in_when_fc0": (A.a[A.forecast == 0] > 0.01).mean(),
        "fc_p90": A.forecast.quantile(0.9), "fc_p99": A.forecast.quantile(0.99)})
    # graded: non-overlap cases on streak-ending bars by raw depth
    drift = {}
    for c in coins:
        v = []
        for w, b in data["bars"][c].items():
            cl = b.close.values[::18]; v += list(cl[1:] / cl[:-1] - 1)
        drift[c] = np.mean(v)
    cs = []
    for (c, w), x in A.groupby(["coin", "w"], sort=False):
        x = x.reset_index(drop=True); x["cell"] = x.index // 18
        s = x[x.raw > 0].sort_values("raw").groupby("cell").tail(1)  # deepest streak bar in cell
        cs.append(s)
    S = pd.concat(cs).dropna(subset=["fwd18", "raw"])
    S["unus"] = S.fwd18 - S.coin.map(drift)
    def tt(x): return pd.Series({"n": len(x), "raw": x.raw.mean(), "mean_fwd": x.fwd18.mean(), "mean_unus": x.unus.mean(),
        "t": x.unus.mean() / (x.unus.std() / np.sqrt(len(x)))})
    S["rq"] = pd.qcut(S.raw, 5, labels=False, duplicates="drop")
    out["deepest_streak_by_depth"] = S.groupby("rq").apply(tt)
    S2 = S.dropna(subset=["vol_ratio"]).copy()
    S2["vq"] = pd.qcut(S2.vol_ratio, 3, labels=False)
    S2["deep"] = (S2.rq >= 3).astype(int)
    out["by_depth_and_volfade"] = S2.groupby(["deep", "vq"]).apply(tt)
    S3 = S.dropna(subset=["ret30"]).copy(); S3["tq"] = pd.qcut(S3.ret30, 3, labels=False)
    out["by_depth_and_30dtrend"] = S3.groupby(["deep" if False else "rq", "tq"]).apply(tt) if False else S3.assign(deep=(S3.rq >= 3).astype(int)).groupby(["deep", "tq"]).apply(tt)
    # allocation vs realised vol quintile, gain
    A["gain"] = A.a * A.r1
    Z = A.dropna(subset=["sizing_realised_vol", "gain"]).copy()
    Z["vq"] = pd.qcut(Z.sizing_realised_vol, 5, labels=False)
    out["gain_by_realised_vol"] = Z.groupby("vq").agg(alloc=("a", "mean"), gain=("gain", "mean"), r1=("r1", "mean"), sd_gain=("gain", "std"))
    return out
