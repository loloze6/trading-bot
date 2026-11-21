import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [5, 10]
    drift = {}; sd = {}
    for coin, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(c[idx + h] / c[idx] - 1)
            drift[(coin, h)] = np.mean(rs); sd[(coin, h)] = np.std(rs)
    rows = []; base = []
    for coin, ws in bars.items():
        for wi, (w, df) in enumerate(ws.items()):
            c = df["close"].values; f = df["forecast"].values; n = len(c)
            ma50 = pd.Series(c).rolling(50, min_periods=20).mean().values
            ma20 = pd.Series(c).rolling(20, min_periods=10).mean().values
            r20 = pd.Series(c).pct_change(20).values
            # baseline grid
            for t in range(0, n - 5, 5):
                if np.isfinite(ma50[t]):
                    base.append({"coin": coin, "trend": np.sign(c[t]/ma50[t]-1),
                                 "u5": -(c[t+5]/c[t]-1-drift[(coin,5)])})
            ref = None; last_cell = -1
            for t in range(n):
                ft = f[t]
                if not np.isfinite(ft) or ft >= 0:
                    ref = None; continue
                if ref is None: ref = 0.0
                ref = max(ref, ft)
                if ref - ft >= 2:
                    cell = t // 5
                    if cell != last_cell:
                        last_cell = cell
                        rec = {"coin": coin, "f": abs(ft),
                               "gap50": c[t]/ma50[t]-1 if np.isfinite(ma50[t]) else np.nan,
                               "gap20": c[t]/ma20[t]-1 if np.isfinite(ma20[t]) else np.nan,
                               "r20": r20[t], "year": pd.Timestamp(df["timestamp"].iloc[t]).year}
                        for h in H:
                            if t + h < n:
                                rec[f"u{h}"] = -(c[t+h]/c[t]-1-drift[(coin,h)])
                        rows.append(rec)
                    ref = ft
    d = pd.DataFrame(rows); b = pd.DataFrame(base)
    def summ(g):
        out = {}
        for h in H:
            x = g[f"u{h}"].dropna()
            out[f"m{h}"] = x.mean(); out[f"t{h}"] = x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan
        out["n"] = len(g); return pd.Series(out)
    d["tr"] = np.sign(d["gap50"])
    down = d[d["tr"] < 0].copy()
    down["fq"] = pd.qcut(down["f"], 3, labels=False, duplicates="drop")
    down["gq"] = pd.qcut(down["gap50"], 3, labels=False, duplicates="drop")
    d["g50q"] = pd.qcut(d["gap50"], 5, labels=False, duplicates="drop")
    corr_down = stats.spearmanr(down["f"], down["u5"], nan_policy="omit")
    corr_gap = stats.spearmanr(-d["gap50"], d["u5"], nan_policy="omit")
    bs = b.groupby("trend")["u5"].agg(["mean","count",lambda x: x.mean()/(x.std()/np.sqrt(len(x)))])
    # signal minus baseline below ma50, Welch
    bd = b[b["trend"]<0]["u5"].dropna(); sdn = down["u5"].dropna()
    w = stats.ttest_ind(sdn, bd, equal_var=False)
    return {
        "by_g50q": d.groupby("g50q").apply(summ),
        "down_by_fq": down.groupby("fq").apply(summ),
        "down_by_coin": down.groupby("coin").apply(summ),
        "down_by_year": down.groupby("year").apply(summ),
        "up_by_year": d[d["tr"]>0].groupby("year").apply(summ),
        "spearman_f_u5_down": pd.Series({"rho": corr_down.correlation, "p": corr_down.pvalue}),
        "spearman_neg_gap50_u5": pd.Series({"rho": corr_gap.correlation, "p": corr_gap.pvalue}),
        "baseline_grid_by_trend": bs,
        "down_signal_minus_base": pd.Series({"diff": sdn.mean()-bd.mean(), "t": w.statistic, "n_sig": len(sdn), "n_base": len(bd)}),
    }
