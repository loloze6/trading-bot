def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    recs = {2: [], 8: [], 24: []}
    for c in bars:
        for w, b in bars[c].items():
            cl = b["close"].astype(float).values
            s = pd.Series(cl)
            ch = s.pct_change(72)
            z = (ch - ch.rolling(72, min_periods=20).mean()) / ch.rolling(72, min_periods=20).std()
            hr = pd.to_datetime(b["timestamp"]).dt.hour.values
            gate = b["regime"].values == "mean_reversion"
            for h in recs:
                idx = np.arange(0, len(b) - h, h)
                r = cl[idx + h] / cl[idx] - 1
                recs[h].append(pd.DataFrame({"coin": c, "z": z.values[idx], "r": r,
                                             "gate": gate[idx], "hour": hr[idx]}))
    for h in recs:
        df = pd.concat(recs[h]).dropna()
        df["ex"] = df.r - df.groupby("coin").r.transform("mean")
        df["zb"] = pd.cut(-df.z, [-np.inf, 0, 0.5, 1, 1.5, 2, np.inf])
        g = df.groupby(["zb", "gate"], observed=True).ex.agg(["size", "mean"]).unstack()
        out[f"h{h}_ex_by_fall_gate"] = g
        deep = df[-df.z > 1.5]
        out[f"h{h}_deep_t"] = pd.Series({
            "n": len(deep), "mean_ex": deep.ex.mean(),
            "t": deep.ex.mean() / (deep.ex.std() / np.sqrt(len(deep))),
            "share_falls_z_gt_1": (-df.z > 1).mean()})
    # fee per unit turnover
    fees = []; turns = []
    for c in bars:
        for w, b in bars[c].items():
            fees.append(((b.total_portfolio_value - b.postRebalance_total_value) / b.total_portfolio_value).sum())
            turns.append((b.postRebalance_current_allocation.fillna(0) - b.previous_allocation.fillna(0)).abs().sum())
    out["fee_per_unit_turnover"] = float(np.sum(fees) / np.sum(turns))
    return out
