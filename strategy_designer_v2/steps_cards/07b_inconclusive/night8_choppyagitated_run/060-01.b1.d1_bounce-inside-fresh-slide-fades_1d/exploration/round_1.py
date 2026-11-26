import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [1, 2, 3, 5]
    # normal drift per coin per horizon (non-overlapping, all windows)
    drift, usual = {}, {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs); usual[(c, h)] = np.std(rs, ddof=1)
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float)
            n = len(cl)
            r1 = pd.Series(cl).pct_change()
            sd30 = r1.rolling(30, min_periods=20).std()
            z = (r1 / sd30).values
            prior5 = (pd.Series(cl).shift(1) / pd.Series(cl).shift(6) - 1).values / sd30.values
            reg = df["regime"].astype(str).values
            fc = df["forecast"].values.astype(float)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            for g in range(0, n, 3):
                for i in range(g, min(g + 3, n)):
                    inprof = reg[i] in ("mean_reversion", "unknown")
                    kind = None
                    if reg[i] == "mean_reversion" and fc[i] <= -2:
                        kind = "case"
                    elif reg[i] == "unknown" and r1.values[i] > 0:
                        kind = "upday_no_priorfall"
                    if kind is None:
                        continue
                    rec = dict(coin=c, win=w, year=yr[i], kind=kind, fc=fc[i], z=z[i], prior=prior5[i],
                               day=str(df["timestamp"].iloc[i])[:10])
                    for h in H:
                        if i + h < n:
                            ret = cl[i + h] / cl[i] - 1
                            rec[f"u{h}"] = -(ret - drift[(c, h)])
                            rec[f"t{h}"] = -ret
                            rec[f"s{h}"] = rec[f"u{h}"] / usual[(c, h)]
                    rows.append(rec)
                    break
    d = pd.DataFrame(rows)
    def summ(x, col="u3"):
        x = x.dropna(subset=[col])
        if len(x) < 3: return pd.Series({"n": len(x)})
        dd = x.groupby("day")[col].sum()
        m = x[col].mean()
        dev = x.groupby("day")[col].apply(lambda v: (v - m).sum())
        G = len(dev); se = np.sqrt((dev**2).sum() * G / (G - 1)) / len(x)
        return pd.Series({"n": len(x), "days": G, "mean": m, "t_day": m / se if se > 0 else np.nan})
    out = {}
    cs = d[d.kind == "case"]
    out["case_by_horizon"] = pd.DataFrame({h: summ(cs, f"u{h}") for h in H}).T
    out["case_total_by_horizon"] = pd.DataFrame({h: summ(cs, f"t{h}") for h in H}).T
    out["upday_noprior_by_horizon"] = pd.DataFrame({h: summ(d[d.kind == "upday_no_priorfall"], f"u{h}") for h in H}).T
    out["case_by_coin"] = cs.groupby("coin").apply(summ).reset_index()
    out["case_by_window"] = cs.groupby("win").apply(summ).reset_index()
    out["case_by_year"] = cs.groupby("year").apply(summ).reset_index()
    cs = cs.copy()
    cs["zq"] = pd.qcut(cs["z"], 4, labels=False, duplicates="drop")
    cs["pq"] = pd.qcut(cs["prior"], 4, labels=False, duplicates="drop")
    cs["fq"] = pd.qcut(cs["fc"].abs(), 4, labels=False, duplicates="drop")
    out["case_by_rise_quartile"] = cs.groupby("zq").apply(lambda x: pd.concat([summ(x), summ(x, "u1").rename(lambda k: k + "_h1"), pd.Series({"z_mean": x.z.mean()})])).reset_index()
    out["case_by_prior_quartile"] = cs.groupby("pq").apply(lambda x: pd.concat([summ(x), summ(x, "u1").rename(lambda k: k + "_h1"), pd.Series({"p_mean": x.prior.mean()})])).reset_index()
    out["case_by_absfc_quartile"] = cs.groupby("fq").apply(summ).reset_index()
    up = d[d.kind == "upday_no_priorfall"].copy()
    up["zq"] = pd.qcut(up["z"], 4, labels=False, duplicates="drop")
    out["upday_noprior_by_rise_quartile"] = up.groupby("zq").apply(lambda x: pd.concat([summ(x), summ(x, "u1").rename(lambda k: k + "_h1"), pd.Series({"z_mean": x.z.mean()})])).reset_index()
    out["case_strength_mean_s3"] = float(cs["s3"].mean())
    return out
