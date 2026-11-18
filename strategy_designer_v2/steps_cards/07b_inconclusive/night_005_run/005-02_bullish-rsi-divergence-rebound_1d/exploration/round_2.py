def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    H = [5, 10, 20]
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
            tr60 = cl / cl.shift(60) - 1
            ma = cl.rolling(60, min_periods=40).mean()
            above = cl / ma - 1
            vol = np.log(cl).diff().rolling(20, min_periods=15).std()
            for kind, mask in [("div", newlow & (fc > 0)), ("nodiv", newlow & (fc <= 0))]:
                last = -999
                for t in np.where(mask.values)[0]:
                    if t + 10 >= len(cl) or t - last <= 10:
                        continue
                    last = t
                    rec = dict(coin=c, kind=kind, fc=fc.iloc[t], tr60=tr60.iloc[t], vol=vol.iloc[t])
                    for h in H:
                        if t + h < len(cl):
                            rec[f"r{h}"] = cl.iloc[t + h] / cl.iloc[t] - 1 - cmean[(c, h)]
                    rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        res = {"n": len(g)}
        for h in H:
            v = g[f"r{h}"].dropna()
            res[f"ex_r{h}"] = v.mean()
            res[f"t{h}"] = v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan
        return pd.Series(res)
    d2 = d.dropna(subset=["tr60"]).copy()
    d2["trend"] = np.where(d2["tr60"] > 0, "up60", "down60")
    out["by_kind_trend60"] = d2.groupby(["kind", "trend"]).apply(summ)
    d3 = d.dropna(subset=["vol"]).copy()
    d3["volq"] = pd.qcut(d3["vol"], 2, labels=["lowvol", "highvol"])
    out["by_kind_vol"] = d3.groupby(["kind", "volq"]).apply(summ)
    dv = d2[d2.kind == "div"]
    for tr in ["up60", "down60"]:
        s = dv[dv.trend == tr]
        if len(s) > 5:
            out[f"spearman_fc_r10_{tr}"] = float(stats.spearmanr(s["fc"], s["r10"], nan_policy="omit").correlation)
    nd = d2[d2.kind == "nodiv"]
    for tr in ["up60", "down60"]:
        a = dv[dv.trend == tr]["r10"].dropna(); b = nd[nd.trend == tr]["r10"].dropna()
        out[f"welch_div_minus_nodiv_r10_{tr}"] = f"diff={a.mean()-b.mean():.4f} t={stats.ttest_ind(a,b,equal_var=False).statistic:.2f} n={len(a)}/{len(b)}"
    return out
