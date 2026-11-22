def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 2, 3, 5, 10]
    rows = []
    for coin, wins in bars.items():
        cm = {h: [] for h in H}
        for w, df in wins.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                cm[h].extend(list(c[idx + h] / c[idx] - 1))
        cmean = {h: np.mean(cm[h]) for h in H}
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            bounce = r1 / sd
            r30 = c / c.shift(30) - 1
            r10 = c.shift(1) / c.shift(11) - 1
            fd = df.get("debug_info.components.fall_depth.last_history_value")
            year = pd.to_datetime(df["timestamp"]).dt.year
            for i in range(len(df)):
                if not (df["regime"].iat[i] == "mean_reversion" and df["forecast"].iat[i] < 0):
                    continue
                rec = dict(coin=coin, window=w, i=i, cell=i // 5, year=year.iat[i],
                           depth=fd.iat[i] if fd is not None else np.nan,
                           bounce=bounce.iat[i], r30=r30.iat[i], r10=r10.iat[i],
                           r1=r1.iat[i])
                for h in H:
                    rec[f"x{h}"] = (c.iat[i + h] / c.iat[i] - 1 - cmean[h]) if i + h < len(df) else np.nan
                    rec[f"t{h}"] = (c.iat[i + h] / c.iat[i] - 1) if i + h < len(df) else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows).sort_values(["coin", "window", "i"]).groupby(["coin", "window", "cell"]).head(1)
    out = {}
    def summ(g):
        res = {"n": len(g)}
        for h in H:
            x = g[f"x{h}"].dropna()
            res[f"mx{h}"] = x.mean()
            res[f"tx{h}"] = x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan
        res["mtot1"] = g["t1"].mean()
        return pd.Series(res)
    out["all"] = summ(d).to_frame().T
    # graded on bounce size, short horizons
    sl = {}
    for var in ["bounce", "depth", "r30", "r10", "r1"]:
        for h in [1, 2, 3, 5]:
            g = d[[var, f"x{h}"]].dropna()
            r = stats.linregress(g[var], g[f"x{h}"])
            sl[f"{var}_h{h}"] = dict(n=len(g), slope=r.slope, t=r.slope / r.stderr)
    out["slopes"] = pd.DataFrame(sl).T
    d["r30_side"] = np.where(d["r30"] < 0, "r30_neg", np.where(d["r30"] >= 0, "r30_pos", "na"))
    out["by_r30_sign"] = d.groupby("r30_side").apply(summ)
    d["r10_side"] = np.where(d["r10"] < 0, "r10_neg", np.where(d["r10"] >= 0, "r10_pos", "na"))
    out["by_r10_sign"] = d.groupby("r10_side").apply(summ)
    g = d[d.r30 < 0]
    sl2 = {}
    for var in ["depth", "r30", "bounce"]:
        for h in [1, 3, 5, 10]:
            gg = g[[var, f"x{h}"]].dropna()
            r = stats.linregress(gg[var], gg[f"x{h}"])
            sl2[f"{var}_h{h}"] = dict(n=len(gg), slope=r.slope, t=r.slope / r.stderr)
    out["slopes_in_r30_neg"] = pd.DataFrame(sl2).T
    out["x1_by_year"] = d.groupby("year").apply(summ)[["n", "mx1", "tx1", "mx3", "tx3"]]
    d["bq"] = pd.qcut(d["bounce"], 4, labels=["b1", "b2", "b3", "b4"])
    out["by_bounce_q"] = d.groupby("bq").apply(summ)
    return out
