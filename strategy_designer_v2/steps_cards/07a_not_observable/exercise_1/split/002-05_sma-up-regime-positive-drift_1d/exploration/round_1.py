def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.copy()
            raw = b["debug_info.components.sma_cross_spread.last_history_value"]
            post = b["debug_info.components.sma_cross_spread.post_pipeline_value"]
            f = b["forecast"]
            r = b["close"].pct_change().shift(-1)
            pos = raw > 0
            runs = (pos != pos.shift()).cumsum()
            up_runs = pos.groupby(runs).agg(["first", "size"])
            up_runs = up_runs[up_runs["first"]]
            down_runs = (~pos).groupby(runs).agg(["first", "size"])
            down_runs = down_runs[down_runs["first"]]
            ts = pd.to_datetime(b["timestamp"])
            rows.append({
                "coin": coin, "window": w, "bars": len(b),
                "span_days": (ts.iloc[-1] - ts.iloc[0]).days,
                "year_first": ts.iloc[0].year, "year_last": ts.iloc[-1].year,
                "raw_pos_bars": int(pos.sum()), "raw_neg_bars": int((~pos).sum()),
                "fc_pos_bars": int((f > 0).sum()), "fc_zero_bars": int((f == 0).sum()),
                "up_runs": len(up_runs), "up_run_max_len": int(up_runs["size"].max()) if len(up_runs) else 0,
                "down_runs": len(down_runs), "down_run_max_len": int(down_runs["size"].max()) if len(down_runs) else 0,
                "sign_changes": int((pos != pos.shift()).sum() - 1),
                "raw_min": raw.min(), "raw_med": raw.median(), "raw_max": raw.max(),
                "post_min": post.min(), "post_max": post.max(),
                "fc_mean_when_pos": f[f > 0].mean(), "fc_max": f.max(),
                "ret_std": r.std(), "ret_mean": r.mean(),
                "ret_mean_in": r[f > 0].mean(), "ret_mean_out": r[f == 0].mean(),
                "ret_std_in": r[f > 0].std(), "ret_std_out": r[f == 0].std(),
            })
            # raw spread by position in window (thirds)
            third = pd.Series(np.arange(len(b)) * 3 // len(b), index=b.index)
            out[f"{coin}_{w}_raw_by_third"] = pd.DataFrame({"raw_mean": raw.groupby(third).mean(),
                "raw_pos_share": pos.groupby(third).mean(), "fc_pos_share": (f > 0).groupby(third).mean()})
            out[f"{coin}_{w}_up_runs"] = up_runs.reset_index(drop=True)
            # where the in-stretch bars sit: raw>0 but fc==0 count
            out[f"{coin}_{w}_raw_pos_fc_zero"] = int((pos & (f == 0)).sum())
            out[f"{coin}_{w}_raw_neg_fc_pos"] = int((~pos & (f > 0)).sum())
            # needed bars to detect: with std, what mean diff detectable at t=2 with 100/100
            s = r.std()
            out[f"{coin}_{w}_detectable_diff_100_100"] = 2 * s * np.sqrt(1/100 + 1/100)
            out[f"{coin}_{w}_detectable_diff_actual"] = 2 * np.sqrt(r[f>0].var()/max((f>0).sum(),1) + r[f==0].var()/max((f==0).sum(),1))
    out["summary"] = pd.DataFrame(rows).T
    return out
