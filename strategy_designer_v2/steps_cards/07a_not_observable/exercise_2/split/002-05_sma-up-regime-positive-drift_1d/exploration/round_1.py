def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            raw = b["debug_info.components.sma_cross_spread.last_history_value"].astype(float)
            post = b["debug_info.components.sma_cross_spread.post_pipeline_value"].astype(float)
            f = b["forecast"].astype(float)
            pos = (raw > 0).astype(int)
            runs = ((pos.diff().fillna(pos.iloc[0]) == 1)).sum()
            ret = b["close"].pct_change().shift(-1)
            ts = pd.to_datetime(b["timestamp"])
            rows.append({
                "coin": coin, "window": w, "bars": len(b),
                "span_days": (ts.iloc[-1] - ts.iloc[0]).days,
                "raw_pos_bars": int(pos.sum()), "raw_neg_bars": int((raw <= 0).sum()),
                "raw_pos_runs": int(runs),
                "fc_pos_bars": int((f > 0).sum()), "fc_zero_bars": int((f == 0).sum()),
                "post_pos_bars": int((post > 0).sum()),
                "raw_min": raw.min(), "raw_max": raw.max(), "raw_mean": raw.mean(),
                "raw_first": raw.iloc[0], "raw_last": raw.iloc[-1],
                "fc_mean_when_pos": f[f > 0].mean(), "fc_max": f.max(),
                "ret_std": ret.std(), "ret_mean": ret.mean(),
                "ret_in_mean": ret[f > 0].mean(), "ret_out_mean": ret[f == 0].mean(),
                "coin_total_ret": b["close"].iloc[-1] / b["close"].iloc[0] - 1,
                "year_first": ts.iloc[0].year, "year_last": ts.iloc[-1].year,
            })
            # sign changes of raw spread (crosses)
            out[f"{coin}_{w}_crosses_up_down"] = pd.Series({
                "up": int(((raw > 0) & (raw.shift() <= 0)).sum()),
                "down": int(((raw <= 0) & (raw.shift() > 0)).sum())})
            # raw spread by decile of bar position
            q = pd.Series(np.arange(len(b)) // 12)
            out[f"{coin}_{w}_raw_by_12bar_block"] = pd.DataFrame({
                "raw_mean": raw.groupby(q.values).mean(),
                "fc_pos_share": (f > 0).groupby(q.values).mean(),
                "close_ret_block": b["close"].groupby(q.values).agg(lambda s: s.iloc[-1]/s.iloc[0]-1)})
            # where forecast>0 vs raw>0 disagree
            out[f"{coin}_{w}_raw_vs_fc"] = pd.crosstab(raw > 0, f > 0).rename_axis(index="raw>0", columns="fc>0")
    out["summary"] = pd.DataFrame(rows).T
    return out
