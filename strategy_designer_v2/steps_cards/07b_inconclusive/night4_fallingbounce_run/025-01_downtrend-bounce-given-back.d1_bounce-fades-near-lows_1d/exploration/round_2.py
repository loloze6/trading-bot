def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [1, 3, 5, 10]
    drift, usual = {}, {}
    for c in bars:
        for h in H:
            rs = []
            for w, df in bars[c].items():
                cl = df["close"].values.astype(float)
                idx = np.arange(0, len(cl) - h, h)
                if len(idx):
                    rs.extend(cl[idx + h] / cl[idx] - 1)
            rs = np.array(rs)
            drift[(c, h)] = rs.mean(); usual[(c, h)] = rs.std()
    recs = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values.astype(float)
            f = df["forecast"].fillna(0).values.astype(float)
            s = np.where(f < 0, -f, 0.0)
            col = "debug_info.components.bounce_near_low.last_history_value"
            raw = df[col].values.astype(float) if col in df.columns else np.full(len(df), np.nan)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            r1 = np.r_[np.nan, cl[1:] / cl[:-1] - 1]
            sd20 = pd.Series(r1).rolling(20, min_periods=15).std().shift(1).values
            low90 = pd.Series(cl).rolling(90, min_periods=60).min().values
            ret90 = np.r_[np.full(90, np.nan), cl[90:] / cl[:-90] - 1] if len(cl) > 90 else np.full(len(cl), np.nan)
            low = None; used = set()
            for t in range(len(df)):
                if s[t] <= 0:
                    low = None; continue
                if low is None:
                    low = 0.0
                if s[t] - low >= 2:
                    cell = t // 5
                    if cell not in used:
                        used.add(cell)
                        rec = dict(coin=c, win=w, year=int(yr[t]), fc=s[t], raw=raw[t],
                                   z=r1[t] / sd20[t] if sd20[t] and not np.isnan(sd20[t]) else np.nan,
                                   dist=cl[t] / low90[t] - 1, ret90=ret90[t])
                        for h in H:
                            if t + h < len(cl):
                                ret = cl[t + h] / cl[t] - 1
                                rec[f"u{h}"] = -(ret - drift[(c, h)])
                                rec[f"s{h}"] = rec[f"u{h}"] / usual[(c, h)]
                        recs.append(rec)
                    low = s[t]
                else:
                    low = min(low, s[t])
    d = pd.DataFrame(recs)
    def summ(g, col="u5"):
        x = g[col].dropna()
        n = len(x)
        return pd.Series({"n": n, "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(n)) if n > 2 else np.nan,
                          "strength": g[col.replace("u", "s")].mean()})
    out = {}
    out["all_by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    out["forecast_desc"] = d["fc"].describe()
    out["share_fc_20"] = float((d["fc"] >= 19.99).mean())
    d["fcq"] = pd.qcut(d["fc"].rank(method="first"), 3, labels=["lo", "mid", "hi"])
    out["by_fc_tercile"] = d.groupby("fcq").apply(summ)
    dd = d.dropna(subset=["z"]).copy()
    dd["zq"] = pd.qcut(dd["z"].rank(method="first"), 4, labels=["q1", "q2", "q3", "q4"])
    out["by_bounce_z_quartile"] = dd.groupby("zq").apply(summ)
    out["z_desc"] = dd["z"].describe()
    dd = d.dropna(subset=["dist"]).copy()
    dd["dq"] = pd.qcut(dd["dist"].rank(method="first"), 4, labels=["near", "q2", "q3", "far"])
    out["by_dist_low_quartile"] = dd.groupby("dq").apply(summ)
    dd = d.dropna(subset=["ret90"]).copy()
    dd["rq"] = pd.qcut(dd["ret90"].rank(method="first"), 3, labels=["deep", "mid", "mild"])
    out["by_ret90_tercile"] = dd.groupby("rq").apply(summ)
    out["by_ret90_tercile_h10"] = dd.groupby("rq").apply(lambda g: summ(g, "u10"))
    out["corr_z_u5"] = float(d[["z", "u5"]].corr().iloc[0, 1])
    out["corr_dist_u5"] = float(d[["dist", "u5"]].corr().iloc[0, 1])
    return out
