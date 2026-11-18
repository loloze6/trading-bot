def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [3, 5, 10, 20]
    # coin mean h-return on grid
    cmean = {}
    for c in bars:
        for h in H:
            r = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                r += list(cl[idx + h] / cl[idx] - 1)
            cmean[(c, h)] = np.mean(r)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"]
            prior_min = cl.shift(1).rolling(30, min_periods=30).min()
            newlow = (cl < prior_min) | (prior_min.isna() & (df["regime"] == "mean_reversion"))
            fc = df["forecast"].fillna(0)
            raw = df.get("debug_info.components.rsi_div.last_history_value")
            yr = pd.to_datetime(df["timestamp"]).dt.year
            # 30-day drop depth
            depth = cl / cl.shift(30) - 1
            for kind, mask in [("div", newlow & (fc > 0)), ("nodiv", newlow & (fc <= 0))]:
                last = -999
                for t in np.where(mask.values)[0]:
                    if t + 10 >= len(cl):
                        continue
                    if t - last <= 10:
                        continue
                    last = t
                    rec = dict(coin=c, win=w, year=yr.iloc[t], kind=kind, fc=fc.iloc[t],
                               raw=(raw.iloc[t] if raw is not None else np.nan), depth=depth.iloc[t])
                    for h in H:
                        if t + h < len(cl):
                            rec[f"r{h}"] = cl.iloc[t + h] / cl.iloc[t] - 1
                            rec[f"x{h}"] = (rec["fc"] / 10) * (rec[f"r{h}"] - cmean[(c, h)])
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        res = {"n": len(g)}
        for h in H:
            v = g[f"r{h}"].dropna()
            res[f"mean_r{h}"] = v.mean()
            res[f"t_r{h}"] = v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan
        x = g["x10"].dropna()
        res["mean_x10"] = x.mean()
        res["t_x10"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        return pd.Series(res)
    out["by_kind"] = d.groupby("kind").apply(summ)
    out["by_kind_coin"] = d.groupby(["kind", "coin"]).apply(summ)
    out["by_kind_year"] = d.groupby(["kind", "year"]).apply(summ)
    dv = d[d.kind == "div"].copy()
    dv["fcq"] = pd.qcut(dv["fc"], 3, labels=["lo", "mid", "hi"])
    out["div_by_fc_tercile"] = dv.groupby("fcq").apply(summ)
    out["corr_fc_r10"] = float(stats.spearmanr(dv["fc"], dv["r10"], nan_policy="omit").correlation)
    d["depthq"] = pd.qcut(d["depth"], 3, labels=["deep", "mid", "shallow"])
    out["by_kind_depth"] = d.groupby(["kind", "depthq"]).apply(summ)
    out["coin_means"] = pd.Series({f"{k[0]}_{k[1]}": v for k, v in cmean.items()})
    return out
