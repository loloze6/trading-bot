def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]
    # coin mean daily return over all windows
    cm = {}
    for c in bars:
        r = []
        for w, b in bars[c].items():
            r.append(b["close"].pct_change().dropna())
        cm[c] = pd.concat(r).mean()
    # per-bar decomposition
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            nxt = b["close"].shift(-1) / b["close"] - 1
            a = b["postRebalance_current_allocation"].fillna(0)
            g = a * nxt
            rows.append(pd.DataFrame({"coin": c, "w": w, "year": pd.to_datetime(b["timestamp"]).dt.year,
                                      "gain": g, "mkt": a * cm[c], "alloc": a, "ret": nxt,
                                      "regime": b["regime"]}).dropna(subset=["gain"]))
    R = pd.concat(rows)
    R["timing"] = R["gain"] - R["mkt"]
    out["decomp_total"] = R[["gain", "mkt", "timing"]].mean().to_frame("mean_per_coin_bar")
    out["by_coin"] = R.groupby("coin")[["gain", "mkt", "timing", "alloc"]].mean()
    out["by_window"] = R.groupby("w")[["gain", "mkt", "timing"]].mean()
    out["by_year"] = R.groupby("year")[["gain", "mkt", "timing"]].mean()
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in trades for t in trades[c].values() if len(t)])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n": len(p), "sum": p.sum(), "top10_sum": p.head(10).sum(),
                               "top20_sum": p.head(20).sum(), "winrate": (p > 0).mean(), "mean": p.mean()})
    # horizon tests: grid samples per window, features recomputed
    res = []
    for h in [1, 3, 5, 10, 20]:
        cs = []
        for c in bars:
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                cl = b["close"]
                r28 = cl / cl.shift(28) - 1
                hi = cl.rolling(28, min_periods=28).max()
                D = (hi / cl - 1) * 100
                prox = 1 / (1 + D)
                fwd = cl.shift(-h) / cl - 1
                idx = np.arange(0, len(b), h)
                d = pd.DataFrame({"coin": c, "fwd": fwd.iloc[idx].values, "r28": r28.iloc[idx].values,
                                  "D": D.iloc[idx].values, "reg": (b["regime"].iloc[idx] == "trending").values})
                cs.append(d)
        S = pd.concat(cs).dropna()
        S["ex"] = S["fwd"] - S.groupby("coin")["fwd"].transform("mean")
        S["z"] = S["ex"] / S.groupby("coin")["fwd"].transform("std")
        inr = S[S.reg]; outr = S[~S.reg]
        tt = stats.ttest_ind(inr["ex"], outr["ex"], equal_var=False)
        lr_r28 = stats.linregress(S["r28"], S["z"])
        lr_r28in = stats.linregress(inr["r28"], inr["z"])
        lr_Din = stats.linregress(-np.log1p(inr["D"]), inr["z"])
        res.append({"h": h, "n_in": len(inr), "n_out": len(outr), "ex_in": inr["ex"].mean(), "ex_out": outr["ex"].mean(),
                    "t_in_minus_out": tt.statistic, "t_r28_all": lr_r28.slope / lr_r28.stderr,
                    "t_r28_inreg": lr_r28in.slope / lr_r28in.stderr, "t_nearhigh_inreg": lr_Din.slope / lr_Din.stderr})
    out["horizons"] = pd.DataFrame(res)
    # in-regime gain vs out
    out["gain_by_regime"] = R.groupby("regime")[["gain", "alloc", "ret"]].mean()
    return out
