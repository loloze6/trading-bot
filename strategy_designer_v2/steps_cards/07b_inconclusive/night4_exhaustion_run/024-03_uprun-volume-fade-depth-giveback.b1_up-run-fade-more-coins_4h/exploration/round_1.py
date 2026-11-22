def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    for coin, wins in data["bars"].items():
        # drift per horizon from non-overlapping grids
        drifts = {}
        for h in (6, 12, 18, 36):
            rs = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drifts[h] = (np.mean(rs), np.std(rs))
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values
            f = b["forecast"].values
            rg = b.get("debug_info.components.run_gain.last_history_value")
            vf = b.get("debug_info.components.vol_fade.last_history_value")
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            c180 = pd.Series(c).pct_change(180).values
            n = len(c)
            for start in range(0, n, H):
                cell = np.arange(start, min(start + H, n))
                hit = cell[f[cell] <= -2]
                if len(hit) == 0:
                    continue
                t = hit[0]
                r = {"coin": coin, "win": w, "year": yr[t], "fc": f[t],
                     "rg": rg.values[t] if rg is not None else np.nan,
                     "vf": vf.values[t] if vf is not None else np.nan,
                     "past30": c180[t]}
                for h in (6, 12, 18, 36):
                    if t + h < n:
                        r[f"u{h}"] = -(c[t + h] / c[t] - 1 - drifts[h][0])
                        r[f"s{h}"] = r[f"u{h}"] / drifts[h][1]
                    else:
                        r[f"u{h}"] = np.nan
                        r[f"s{h}"] = np.nan
                rows.append(r)
    d = pd.DataFrame(rows)

    def summ(g, col="u18"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan})

    out = {}
    out["overall_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in (6, 12, 18, 36)}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fcq"] = pd.qcut(d["fc"].rank(method="first"), 5, labels=False)
    out["by_forecast_quintile(0=most_short)"] = d.groupby("fcq").apply(summ)
    d["rgq"] = pd.qcut(d["rg"].rank(method="first"), 5, labels=False)
    out["by_rungain_quintile"] = d.groupby("rgq").apply(summ)
    d["vfq"] = pd.qcut(d["vf"].rank(method="first"), 5, labels=False)
    out["by_volfade_quintile"] = d.groupby("vfq").apply(summ)
    d["p30q"] = pd.qcut(d["past30"].rank(method="first"), 5, labels=False)
    out["by_past30d_return_quintile"] = d.groupby("p30q").apply(summ)
    out["rg_x_vf_mean_u18"] = d.pivot_table(index="rgq", columns="vfq", values="u18", aggfunc="mean")
    return out
