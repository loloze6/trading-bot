def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    fc_rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            f = b["forecast"]
            c = b["close"]
            n = len(b)
            fwd = c.shift(-5) / c - 1
            grid = b.index[b.index % 5 == 0]
            gfwd = fwd.loc[grid]
            ext = (f <= -10)
            gext = ext.loc[grid] & gfwd.notna()
            base = fwd.mean()
            ex = (gfwd[gext] - base)
            # recompute RSI 14 (Wilder) from closes
            d = c.diff()
            up = d.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
            dn = (-d.clip(upper=0)).ewm(alpha=1/14, adjust=False).mean()
            rsi = 100 - 100 / (1 + up / dn)
            rows.append({
                "coin": coin, "window": w, "bars": n,
                "grid_with_fwd": int(gfwd.notna().sum()),
                "bars_fc_lt0": int((f < 0).sum()),
                "bars_fc_le_-5": int((f <= -5).sum()),
                "bars_fc_le_-10": int(ext.sum()),
                "bars_fc_eq_-20": int((f <= -19.99).sum()),
                "grid_ext_cases": int(gext.sum()),
                "ext_excess_mean": float(ex.mean()) if len(ex) else np.nan,
                "ext_excess_std": float(ex.std()) if len(ex) > 1 else np.nan,
                "all_grid_fwd_std": float(gfwd.std()),
                "base_fwd5_mean": float(base),
                "rsi_mean": float(rsi.mean()),
                "rsi_share_gt50": float((rsi > 50).mean()),
                "rsi_share_gt70": float((rsi > 70).mean()),
                "year": int(pd.to_datetime(b["timestamp"]).dt.year.iloc[0]),
            })
            fc_rows.append(f.describe())
            # runs of extreme
            runs = (ext != ext.shift()).cumsum()[ext]
            out[f"{coin}_{w}_ext_run_lengths"] = runs.value_counts().describe()
            # forecast quantiles
            out[f"{coin}_{w}_fc_quantiles"] = f.quantile([0, .05, .1, .25, .5, .75, .9, 1])
            # rsi when ext vs not
            out[f"{coin}_{w}_rsi_by_fc_bucket"] = pd.DataFrame({"rsi": rsi, "b": pd.cut(f, [-21, -10, -5, -1e-9, 0.1])}).groupby("b", observed=False)["rsi"].agg(["count", "mean"])
    out["summary"] = pd.DataFrame(rows)
    out["fc_describe"] = pd.DataFrame(fc_rows)
    return out
