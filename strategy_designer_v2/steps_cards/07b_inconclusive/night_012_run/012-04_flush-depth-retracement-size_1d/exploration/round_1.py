def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    # coin mean h-bar return on non-overlapping grid, pooled windows
    coin_mean = {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            coin_mean[(c, h)] = np.mean(rs) if rs else np.nan
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            o, hi, lo, cl, v = [df[k].values.astype(float) for k in ["open", "high", "low", "close", "volume"]]
            r = pd.Series(cl).pct_change()
            sd = r.rolling(20).std().shift(1)
            z = (r / sd).values
            medv = pd.Series(v).shift(1).rolling(20).median().values
            vr = v / medv
            rng = hi - lo
            wick = np.where(rng > 0, (np.minimum(o, cl) - lo) / rng, np.nan)
            fc = df["forecast"].values.astype(float)
            reg = df["regime"].values
            ts = pd.to_datetime(df["timestamp"])
            n = len(df)
            for t in range(n):
                sharp = z[t] <= -2 if not np.isnan(z[t]) else False
                if not sharp and not (reg[t] == "mean_reversion" and fc[t] > 0):
                    continue
                rec = dict(coin=c, win=w, t=t, year=ts.iloc[t].year,
                           flush=(reg[t] == "mean_reversion" and fc[t] > 0),
                           fc=fc[t], drop=(o[t] - lo[t]) / o[t], ret1=cl[t] / cl[t-1] - 1 if t > 0 else np.nan,
                           z=z[t], vr=vr[t], wick=wick[t])
                for h in H:
                    rec[f"x{h}"] = cl[t+h] / cl[t] - 1 - coin_mean[(c, h)] if t + h < n else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def indep(g, h):
        keep = []
        for (c, w), gg in g.sort_values("t").groupby(["coin", "win"]):
            last = -999
            for i, row in gg.iterrows():
                if row["t"] - last > h and not np.isnan(row[f"x{h}"]):
                    keep.append(i); last = row["t"]
        return g.loc[keep]
    def summ(g, h, xcol="fc"):
        g = g.dropna(subset=[f"x{h}", xcol])
        if len(g) < 4: return dict(n=len(g))
        y = g[f"x{h}"]; x = g[xcol]
        lr = stats.linregress(x, y)
        return dict(n=len(g), mean=y.mean(), t_mean=y.mean() / (y.std() / np.sqrt(len(y))),
                    slope_t=lr.slope / lr.stderr if lr.stderr > 0 else np.nan, corr=np.corrcoef(x, y)[0, 1])
    fl = d[d.flush]
    res = {}
    for h in H:
        g = indep(fl, h)
        res[f"flush h{h} fc"] = summ(g, h)
        res[f"flush h{h} drop"] = summ(g, h, "drop")
        res[f"flush h{h} ret1"] = summ(g, h, "ret1")
    out["flush_by_h"] = pd.DataFrame(res).T
    g3 = indep(fl, 3)
    out["flush_by_coin_h3"] = pd.DataFrame({c: summ(gg, 3) for c, gg in g3.groupby("coin")}).T
    out["flush_by_year_h3"] = pd.DataFrame({y: summ(gg, 3) for y, gg in g3.groupby("year")}).T
    g3 = g3.copy(); g3["fq"] = pd.qcut(g3["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["flush_fc_tercile_h3"] = g3.groupby("fq")[["fc", "drop", "x1", "x3", "x5", "x10"]].agg(["mean", "count"]).iloc[:, ::1]
    nf = d[(~d.flush) & (d.z <= -2)]
    res = {}
    for h in H:
        a = indep(fl, h)[f"x{h}"].dropna(); b = indep(nf, h)[f"x{h}"].dropna()
        res[h] = dict(flush_mean=a.mean(), n_f=len(a), other_sharp_mean=b.mean(), n_o=len(b),
                      welch_t=stats.ttest_ind(a, b, equal_var=False).statistic)
    out["flush_vs_other_sharp"] = pd.DataFrame(res).T
    # among all sharp falls: slope on drop, wick
    sh = indep(d[d.z <= -2], 3)
    out["allsharp_h3_drop"] = summ(sh, 3, "drop"); out["allsharp_h3_wick"] = summ(sh, 3, "wick")
    out["allsharp_h3_vr"] = summ(sh, 3, "vr"); out["allsharp_h3_ret1"] = summ(sh, 3, "ret1")
    out["allsharp_h5_wick"] = summ(indep(d[d.z <= -2], 5), 5, "wick")
    out["allsharp_h10_wick"] = summ(indep(d[d.z <= -2], 10), 10, "wick")
    return {k: (pd.DataFrame([v]) if isinstance(v, dict) else v) for k, v in out.items()}
