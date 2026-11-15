def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            f = b["forecast"]
            raw = b.get("debug_info.components.sma_cross_spread.last_history_value")
            r = b["close"].shift(-1) / b["close"] - 1
            pos = f > 0
            rawpos = raw > 0 if raw is not None else pd.Series(False, index=b.index)
            runs = int(((rawpos) & (~rawpos.shift(1, fill_value=False))).sum())
            frun = int(((pos) & (~pos.shift(1, fill_value=False))).sum())
            rows.append(dict(coin=coin, window=w, bars=len(b),
                             forecast_pos=int(pos.sum()), forecast_zero=int((f == 0).sum()),
                             forecast_neg=int((f < 0).sum()),
                             raw_pos=int(rawpos.sum()), raw_runs=runs, fc_runs=frun,
                             raw_min=float(raw.min()), raw_max=float(raw.max()),
                             fc_max=float(f.max()), fc_mean_pos=float(f[pos].mean()) if pos.any() else np.nan,
                             r_std=float(r.std()), r_mean=float(r.mean()),
                             r_std_in=float(r[pos].std()), r_std_out=float(r[f == 0].std()),
                             first_raw=float(raw.dropna().iloc[0]), last_raw=float(raw.dropna().iloc[-1]),
                             pos_first_idx=int(np.argmax(pos.values)) if pos.any() else -1,
                             raw_pos_first_idx=int(np.argmax(rawpos.values)) if rawpos.any() else -1,
                             year=int(pd.to_datetime(b["timestamp"]).dt.year.mode()[0])))
    out["summary"] = pd.DataFrame(rows).T
    # raw spread vs forecast agreement
    b = list(list(data["bars"].values())[0].values())[0]
    raw = b["debug_info.components.sma_cross_spread.last_history_value"]
    f = b["forecast"]
    out["raw_pos_but_fc_zero"] = int(((raw > 0) & (f == 0)).sum())
    out["raw_neg_but_fc_pos"] = int(((raw <= 0) & (f > 0)).sum())
    # spread by bar thirds
    thirds = pd.cut(np.arange(len(b)), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_quarter"] = pd.DataFrame({"raw_mean": raw.groupby(thirds).mean(), "fc_pos": (f > 0).groupby(thirds).sum()})
    # required n for t=2 given std, with an effect of, say, 0.2%/day
    s = (b["close"].shift(-1) / b["close"] - 1).std()
    out["daily_std"] = float(s)
    out["n_per_group_for_t2_at_0.2pct"] = float(2 * (2 * s / 0.002) ** 2)
    return out
