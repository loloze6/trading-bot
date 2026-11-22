import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    H = [6, 12, 18, 42, 84]
    rows = []
    for coin, wins in bars.items():
        # drift per horizon over all windows, non-overlapping grid
        drift = {}; usual = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c) - h, h)
                rs.extend(list(c[idx + h] / c[idx] - 1))
            drift[h] = np.mean(rs); usual[h] = np.std(rs)
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; f = df["forecast"].fillna(0).values
            v = df["volume"].values
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            n = len(df)
            ret30 = pd.Series(c).pct_change(180).values
            # streak length
            down = np.r_[False, c[1:] < c[:-1]]
            sl = np.zeros(n, int)
            for i in range(n):
                sl[i] = sl[i-1] + 1 if (down[i] and i > 0) else (1 if down[i] else 0)
            ref = 0.0; used_cell = set()
            for i in range(n):
                if f[i] <= 0:
                    ref = 0.0; continue
                ref = min(ref, f[i])
                if f[i] - ref >= 2:
                    cell = i // 42
                    ref = f[i]
                    if cell in used_cell: continue
                    used_cell.add(cell)
                    r = {"coin": coin, "win": w, "year": yr[i], "f": f[i], "sl": sl[i],
                         "ret30": ret30[i]}
                    for h in H:
                        if i + h < n:
                            r[f"u{h}"] = c[i+h]/c[i]-1-drift[h]
                            r[f"s{h}"] = r[f"u{h}"]/usual[h]
                    # streak depth
                    s = sl[i]
                    r["depth"] = c[i]/c[max(i-s,0)]-1 if s > 0 else np.nan
                    rows.append(r)
    d = pd.DataFrame(rows)
    def tt(x):
        x = x.dropna(); 
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: tt(d[f"u{h}"]) for h in H}).T
    out["by_horizon_strength"] = pd.DataFrame({h: tt(d[f"s{h}"]) for h in H}).T
    out["by_coin_42"] = d.groupby("coin")["u42"].apply(tt).unstack()
    out["by_year_42"] = d.groupby("year")["u42"].apply(tt).unstack()
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=False)
    out["by_forecast_q_42"] = d.groupby("fq").apply(lambda g: pd.concat([tt(g["u42"]), pd.Series({"fmean": g["f"].mean()})]))
    out["by_forecast_q_12"] = d.groupby("fq")["u12"].apply(tt).unstack()
    med = d["f"].median()
    out["supporting_check_42"] = d.loc[d.f > med, "u42"].mean() - d.loc[d.f <= med, "u42"].mean()
    out["f_median_share_at_median"] = (d.f == med).mean()
    d["slq"] = d["sl"].clip(upper=5)
    out["by_streaklen_42"] = d.groupby("slq")["u42"].apply(tt).unstack()
    d["rq"] = pd.qcut(d["ret30"], 4, labels=False)
    out["by_ret30_q_42"] = d.groupby("rq").apply(lambda g: pd.concat([tt(g["u42"]), pd.Series({"r30": g["ret30"].mean()})]))
    d["dq"] = pd.qcut(d["depth"], 4, labels=False)
    out["by_depth_q_42"] = d.groupby("dq").apply(lambda g: pd.concat([tt(g["u42"]), pd.Series({"depth": g["depth"].mean()})]))
    out["by_depth_q_12"] = d.groupby("dq")["u12"].apply(tt).unstack()
    return out
