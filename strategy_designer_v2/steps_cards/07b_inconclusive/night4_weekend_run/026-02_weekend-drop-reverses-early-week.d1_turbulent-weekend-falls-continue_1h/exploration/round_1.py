def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        for h in (24, 48, 72):
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[(coin, h)] = np.mean(rs); usual[(coin, h)] = np.std(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            ts = pd.to_datetime(df["timestamp"])
            c = df["close"].values
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            sel = np.where((ts.dt.dayofweek == 6) & (ts.dt.hour == 23))[0]
            for t in sel:
                if t < 216: continue
                wk = c[t] / c[t - 48] - 1
                v1 = np.nanstd(r1[t - 47:t + 1]); v0 = np.nanstd(r1[t - 215:t - 47])
                rec = dict(coin=coin, win=w, year=ts.iloc[t].year, wk=wk,
                           vr=v1 / v0 if v0 > 0 else np.nan, fc=df["forecast"].iloc[t],
                           raw=df.get("debug_info.components.wkend_fall_volratio.last_history_value", pd.Series(np.nan, index=df.index)).iloc[t])
                for h in (24, 48, 72):
                    rec[f"x{h}"] = (c[t + h] / c[t] - 1 - drift[(coin, h)]) if t + h < len(c) else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    out = {}
    def summ(g, col="x48", sign=-1):
        v = sign * g[col].dropna()
        return pd.Series(dict(n=len(v), mean_pct=100 * v.mean(), t=v.mean() / (v.std() / np.sqrt(len(v))) if len(v) > 2 else np.nan))
    cases = d[d.fc <= -2]
    falls = d[d.wk < 0]
    rises = d[d.wk > 0]
    out["cases_horizons"] = pd.DataFrame({h: summ(cases, f"x{h}") for h in (24, 48, 72)}).T
    out["all_falls_horizons_short"] = pd.DataFrame({h: summ(falls, f"x{h}") for h in (24, 48, 72)}).T
    out["all_rises_horizons_long"] = pd.DataFrame({h: summ(rises, f"x{h}", 1) for h in (24, 48, 72)}).T
    out["cases_by_coin"] = cases.groupby("coin").apply(summ)
    out["cases_by_year"] = cases.groupby("year").apply(summ)
    cases = cases.copy()
    cases["fq"] = pd.qcut(-cases.fc, 4, labels=False, duplicates="drop")
    out["cases_by_absfc_quartile"] = cases.groupby("fq").apply(summ)
    falls = falls.copy()
    falls["wkq"] = pd.qcut(-falls.wk, 4, labels=False)
    falls["vrq"] = pd.qcut(falls.vr, 4, labels=False)
    out["falls_by_fallsize_q"] = falls.groupby("wkq").apply(summ)
    out["falls_by_volratio_q"] = falls.groupby("vrq").apply(summ)
    out["falls_fallsize_x_vr_mean_pct"] = falls.groupby(["wkq", "vrq"])["x48"].apply(lambda s: -100 * s.mean()).unstack()
    out["falls_by_coin"] = falls.groupby("coin").apply(summ)
    # graded: correlation of weekend return with next 48h excess (all weekends)
    dd = d.dropna(subset=["x48", "wk"])
    out["corr_wk_x48_all"] = pd.Series(dict(spearman=stats.spearmanr(dd.wk, dd.x48)[0], n=len(dd)))
    return out
