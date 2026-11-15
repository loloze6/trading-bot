def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.copy()
            ret = b["close"].shift(-1) / b["close"] - 1
            spread = b["debug_info.components.sma_cross_spread.last_history_value"]
            f = b["forecast"]
            s_pos = (spread > 0).astype(int)
            runs = int(((s_pos.diff() == 1).sum()) + (1 if s_pos.iloc[0] == 1 else 0))
            dn = int((s_pos.diff() == -1).sum())
            rows.append({
                "coin": coin, "window": w, "bars": len(b),
                "year_first": int(pd.to_datetime(b["timestamp"]).dt.year.min()),
                "year_last": int(pd.to_datetime(b["timestamp"]).dt.year.max()),
                "spread>0 bars": int((spread > 0).sum()),
                "spread missing": int(spread.isna().sum()),
                "forecast>0 bars": int((f > 0).sum()),
                "forecast==0 bars": int((f == 0).sum()),
                "up runs": runs, "down crosses": dn,
                "spread min": float(spread.min()), "spread max": float(spread.max()),
                "spread mean": float(spread.mean()),
                "ret std": float(ret.std()), "ret mean": float(ret.mean()),
                "ret mean in(f>0)": float(ret[f > 0].mean()),
                "ret mean out(f=0)": float(ret[f == 0].mean()),
                "ret std in": float(ret[f > 0].std()),
                "forecast mean when >0": float(f[f > 0].mean()),
                "alloc mean when f>0": float(b["postRebalance_current_allocation"][f > 0].mean()),
            })
    out["per window"] = pd.DataFrame(rows).T
    # spread sign by spread-positive but forecast zero
    b = list(list(data["bars"].values())[0].values())[0]
    spread = b["debug_info.components.sma_cross_spread.last_history_value"]
    f = b["forecast"]
    out["spread>0 & f==0"] = int(((spread > 0) & (f == 0)).sum())
    out["spread<=0 & f>0"] = int(((spread <= 0) & (f > 0)).sum())
    # spread by tercile of bar position
    pos = np.arange(len(b)) // 20
    out["spread by 20-bar block"] = pd.DataFrame({"spread mean": spread.groupby(pos).mean(), "f>0 share": (f > 0).groupby(pos).mean()})
    # required bars for t=2 given observed std, for an effect of 0.1% /day
    sd = (b["close"].shift(-1) / b["close"] - 1).std()
    out["bars per group for t=2 at 0.1%/day diff"] = float(2 * (2 * sd / 0.001) ** 2)
    out["bars per group for t=2 at 0.2%/day diff"] = float(2 * (2 * sd / 0.002) ** 2)
    return out
