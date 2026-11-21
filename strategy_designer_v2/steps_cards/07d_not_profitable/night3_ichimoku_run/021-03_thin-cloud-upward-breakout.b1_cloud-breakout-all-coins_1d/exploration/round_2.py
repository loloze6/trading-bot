def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; trades = data["trades"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            al = b["postRebalance_current_allocation"].fillna(0).values.astype(float)
            lr = np.r_[np.nan, np.diff(np.log(cl))]
            vol30 = pd.Series(lr).rolling(30, min_periods=30).std().values * np.sqrt(365)
            r26 = np.full(len(cl), np.nan); r26[26:] = cl[26:] / cl[:-26] - 1
            ts = pd.to_datetime(b["timestamp"])
            t = trades[c].get(w) if hasattr(trades[c], "get") else None
            tag_v = np.full(len(cl), np.nan); tag_r = np.full(len(cl), np.nan); tid = np.full(len(cl), -1)
            if t is not None and len(t) > 0:
                for k, (_, r) in enumerate(t.iterrows()):
                    i0 = ts.searchsorted(pd.to_datetime(r["entry_time"]), side="right") - 1
                    i1 = ts.searchsorted(pd.to_datetime(r["exit_time"]), side="right") - 1
                    if i0 < 0: continue
                    tag_v[i0:i1] = vol30[i0]; tag_r[i0:i1] = r26[i0]; tid[i0:i1] = k
            g = np.r_[al[:-1] * (cl[1:] / cl[:-1] - 1), np.nan]
            df = pd.DataFrame({"coin": c, "wn": int(w[1:]), "pos": np.arange(len(cl)), "al": al, "g": g,
                               "ev": tag_v, "er": tag_r, "vol_now": vol30, "r26_now": r26, "ret": np.r_[cl[1:] / cl[:-1] - 1, np.nan]})
            rows.append(df)
    B = pd.concat(rows).dropna(subset=["g"])
    held = B[B["al"] > 0].copy()
    # per-bar gain on held bars by entry-vol tercile (pooled thresholds)
    h = held.dropna(subset=["ev"])
    h["evq"] = pd.qcut(h["ev"], 3, labels=["low", "mid", "high"])
    def summ(x):
        return pd.Series({"mean_g_bps": x["g"].mean() * 1e4, "std_g": x["g"].std(), "sharpe_bar": x["g"].mean() / x["g"].std() * np.sqrt(365),
                          "share_bars": len(x), "worst5pct_bps": x["g"].quantile(0.05) * 1e4, "mean_al": x["al"].mean()})
    out["held_by_entry_vol"] = h.groupby("evq").apply(summ)
    h2 = held.dropna(subset=["er"]).copy()
    h2["erq"] = pd.qcut(h2["er"], 3, labels=["low", "mid", "high"])
    out["held_by_entry_r26"] = h2.groupby("erq").apply(summ)
    # the deepest fall stretch: w1 pos>=87, w2, w3 pos<=68
    fall = B[((B.wn == 1) & (B.pos >= 87)) | (B.wn == 2) | ((B.wn == 3) & (B.pos <= 68))]
    out["fall_by_coin"] = fall.groupby("coin").agg(sum_g=("g", "sum"), held_share=("al", lambda x: (x > 0).mean()), coin_ret_sum=("ret", "sum"), mean_al=("al", "mean")).sort_values("sum_g").head(12)
    fh = fall[fall.al > 0]
    out["fall_held_entry_vol_median"] = float(fh["ev"].median())
    out["all_held_entry_vol_median"] = float(held["ev"].median())
    # coin's 30-day vol at entry vs 26-day forward return (unusual), non-overlapping per trade start
    # held-bar gain by current vol state quartile
    hv = held.dropna(subset=["vol_now"]).copy()
    hv["vq"] = pd.qcut(hv["vol_now"], 4, labels=False)
    out["held_by_current_vol"] = hv.groupby("vq").apply(summ)
    # correlation of daily held-bar losses: share of coins long on the worst portfolio days
    return out
