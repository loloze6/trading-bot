def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b["close"]; r1 = cl.pct_change()
            alloc = b["postRebalance_current_allocation"].fillna(0)
            r30 = cl / cl.shift(30) - 1; r10 = cl / cl.shift(10) - 1
            brk = b["debug_info.components.break.last_history_value"] if "debug_info.components.break.last_history_value" in b else pd.Series(np.nan, index=b.index)
            e30 = pd.Series(np.nan, index=b.index); e10 = e30.copy(); eb = e30.copy()
            cur = (np.nan, np.nan, np.nan)
            for i in range(len(b)):
                if alloc.iloc[i] > 0:
                    if i == 0 or alloc.iloc[i - 1] <= 0:
                        cur = (r30.iloc[i], r10.iloc[i], brk.iloc[i])
                    e30.iloc[i], e10.iloc[i], eb.iloc[i] = cur
            day = pd.to_datetime(b["timestamp"]).dt.floor("D")
            t = pd.DataFrame({"day": day, "p30": e30.shift(1), "p10": e10.shift(1), "pb": eb.shift(1), "pal": alloc.shift(1)})
            t = t.groupby("day").last().reset_index()
            d = data["days"][c][w][["day", "book_return", "coin_return"]].copy()
            d["day"] = pd.to_datetime(d["day"]).dt.floor("D")
            if getattr(d["day"].dt, "tz", None) is not None and getattr(t["day"].dt, "tz", None) is None:
                t["day"] = t["day"].dt.tz_localize(d["day"].dt.tz)
            if getattr(t["day"].dt, "tz", None) is not None and getattr(d["day"].dt, "tz", None) is None:
                d["day"] = d["day"].dt.tz_localize(t["day"].dt.tz)
            d = d.merge(t, on="day", how="left")
            d["coin"] = c; d["wn"] = int(w[1:])
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["book_return"])
    out["matched_share"] = pd.Series({"days": len(D), "held_days": (D["pal"] > 0).sum(), "tagged": D["p30"].notna().sum()})
    def stats_(br):
        B = D.assign(br=br).groupby(["wn", "day"])["br"].mean().reset_index().sort_values(["wn", "day"])
        eq = (1 + B["br"]).cumprod(); dd = (eq / eq.cummax() - 1).min()
        yrs = len(B) / 365; yr = eq.iloc[-1] ** (1 / yrs) - 1
        B["dd"] = eq / eq.cummax() - 1
        return {"mean": B["br"].mean(), "sharpe": B["br"].mean() / B["br"].std() * np.sqrt(365), "yearly": yr, "maxdd": dd, "calmar": yr / -dd,
                "dd_w1_6": B[B["wn"] <= 6]["dd"].min()}
    held = D["pal"] > 0
    res = {"base": stats_(D["book_return"])}
    for name, m in {"drop_r30_neg": held & (D["p30"] < 0), "drop_r10_neg": held & (D["p10"] < 0),
                    "drop_brk_low": held & (D["pb"] < 0.8),
                    "drop_r30neg_or_brklow": held & ((D["p30"] < 0) | (D["pb"] < 0.8))}.items():
        res[name] = stats_(D["book_return"].where(~m, 0.0))
        res[name]["share_days_dropped"] = m.sum() / held.sum()
    out["counterfactual"] = pd.DataFrame(res).T
    # held-day returns by entry r30 sign, per window group
    H = D[held & D["p30"].notna()].copy()
    H["g"] = np.where(H["p30"] < 0, "r30neg", "r30pos")
    H["era"] = np.where(H["wn"] <= 6, "w1-6", "w7-24")
    out["held_by_r30_era"] = H.groupby(["era", "g"]).agg(n=("book_return", "size"), br=("book_return", "mean"), cr=("coin_return", "mean"), p2=("book_return", lambda s: s.quantile(0.02)))
    return out
