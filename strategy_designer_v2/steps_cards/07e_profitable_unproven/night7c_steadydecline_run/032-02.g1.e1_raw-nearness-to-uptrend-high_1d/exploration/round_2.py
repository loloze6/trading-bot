def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    def build(h):
        recs = []
        for c in bars:
            for w, b in bars[c].items():
                b = b.reset_index(drop=True)
                cl = b["close"]
                fr = cl.shift(-h) / cl - 1
                r28 = cl / cl.shift(28) - 1
                hi = cl.rolling(28, min_periods=28).max()
                D = 100 * (1 - cl / hi)
                prox = 1 / (1 + D)
                rng = (b["high"] - b["low"]) / cl
                vol20 = cl.pct_change().rolling(20).std()
                vol60 = cl.pct_change().rolling(60).std()
                vr = vol20 / vol60
                vv = b["volume"] / b["volume"].rolling(28).mean()
                idx = np.arange(0, len(cl), h)
                yr = pd.to_datetime(b["timestamp"]).dt.year
                recs.append(pd.DataFrame({"coin": c, "w": w, "day": pd.to_datetime(b["timestamp"]).dt.floor("D").iloc[idx].values,
                    "yr": yr.iloc[idx].values, "fr": fr.iloc[idx].values, "r28": r28.iloc[idx].values,
                    "D": D.iloc[idx].values, "prox": prox.iloc[idx].values, "vr": vr.iloc[idx].values,
                    "vv": vv.iloc[idx].values, "vol20": vol20.iloc[idx].values}))
        R = pd.concat(recs).dropna(subset=["fr"])
        R["ex"] = R.fr - R.groupby("coin").fr.transform("mean")
        return R.dropna(subset=["r28", "D"])
    def tslope(df, x):
        df = df.dropna(subset=[x, "ex"])
        if len(df) < 20: return np.nan
        s = stats.linregress(df[x], df.ex); return s.slope / s.stderr
    def day_t(df):
        g = df.groupby("day").ex.sum(); return g.mean() / (g.std() / np.sqrt(len(g)))
    for h in [5, 10]:
        R = build(h)
        up = R[R.r28 > 0]; dn = R[R.r28 <= 0]
        out[f"h{h}_slopes"] = pd.Series({"prox_all": tslope(R, "prox"), "prox_up": tslope(up, "prox"),
            "prox_dn": tslope(dn, "prox"), "D_all": tslope(R, "D"), "D_up": tslope(up, "D"),
            "n_all": len(R), "n_up": len(up)})
        # proximity buckets overall and in uptrend
        R["Db"] = pd.cut(R.D, [-0.01, 0.001, 2, 5, 10, 20, 100], labels=["at_high", "0-2", "2-5", "5-10", "10-20", ">20"])
        out[f"h{h}_Dbucket_all"] = R.groupby("Db").ex.agg(["mean", "count"]).assign(
            fr=R.groupby("Db").fr.mean())
        up = R[R.r28 > 0]
        out[f"h{h}_Dbucket_up"] = up.groupby("Db").ex.agg(["mean", "count"])
        if h == 5:
            out["h5_up_by_coin_tprox"] = up.groupby("coin").apply(lambda d: tslope(d, "prox"))
            out["h5_up_by_year_tprox"] = up.groupby("yr").apply(lambda d: tslope(d, "prox"))
            out["h5_all_by_year_tprox"] = R.groupby("yr").apply(lambda d: tslope(d, "prox"))
            ah = R[R.Db == "at_high"]
            out["h5_at_high_daycluster"] = pd.Series({"mean_ex": ah.ex.mean(), "t_day": day_t(ah),
                "days": ah.day.nunique(), "n": len(ah)})
            # calm vs not at high
            R["calm"] = R.vr < R.vr.median()
            out["h5_prox_by_calm"] = R.groupby("calm").apply(lambda d: pd.Series({"t_prox": tslope(d, "prox"), "n": len(d),
                "ex_at_high": d[d.Db == "at_high"].ex.mean()}))
            # 28-day return graded among at-high
            out["h5_athigh_r28_slope_t"] = tslope(ah, "r28")
            # prox controlling r28: residual
            X = np.column_stack([np.ones(len(R)), R.prox, R.r28])
            beta, res, rk, sv = np.linalg.lstsq(X, R.ex.values, rcond=None)
            e = R.ex.values - X @ beta
            cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(R) - 3)
            out["h5_multi_t"] = pd.Series({"t_prox": beta[1] / np.sqrt(cov[1, 1]), "t_r28": beta[2] / np.sqrt(cov[2, 2])})
    return out
