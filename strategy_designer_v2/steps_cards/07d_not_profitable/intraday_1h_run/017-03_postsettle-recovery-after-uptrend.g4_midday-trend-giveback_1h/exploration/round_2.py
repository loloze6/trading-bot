def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            r72 = b["close"] / b["close"].shift(72) - 1
            vol = b["close"].pct_change().rolling(240, min_periods=100).std()
            idx = np.where(ts.dt.hour.values == 10)[0]
            for i in idx:
                rec = {"coin": c, "win": w, "f": b["forecast"].iat[i], "r72": r72.iat[i], "vol": vol.iat[i]}
                for h in [3, 6, 12, 24, 48]:
                    rec[f"f{h}"] = cl[i + h] / cl[i] - 1 if i + h < len(cl) else np.nan
                rows.append(rec)
    D = pd.DataFrame(rows)
    D["sgn"] = -np.sign(D["r72"])
    for h in [3, 6, 12, 24, 48]:
        D[f"g{h}"] = D["sgn"] * D[f"f{h}"]
    D["fq"] = pd.qcut(D["f"].abs(), 5, labels=False, duplicates="drop")
    out["signed_move_by_force_quintile_pct"] = (D.groupby("fq")[[f"g{h}" for h in [3, 6, 12, 24, 48]]].mean() * 100)
    tt = {}
    for h in [3, 6, 12, 24, 48]:
        x = D[f"g{h}"].dropna()
        tt[h] = {"mean_pct": x.mean() * 100, "t": stats.ttest_1samp(x, 0).statistic, "n": len(x)}
    out["signed_move_by_horizon"] = pd.DataFrame(tt).T
    D["vq"] = D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["g3_by_vol_tercile_pct"] = D.groupby("vq").agg(g3=("g3", "mean"), absf3=("f3", lambda s: s.abs().mean()), n=("g3", "size")) * pd.Series({"g3": 100, "absf3": 100, "n": 1})
    D["side"] = np.where(D["sgn"] > 0, "long_after_fall", "short_after_rise")
    out["g3_by_side_pct"] = D.groupby("side")[["g3", "g12", "g24"]].mean() * 100
    return out
