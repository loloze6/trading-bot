def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    drift = {}
    usual = {}
    for coin, wins in bars.items():
        r5 = []
        for w, df in wins.items():
            c = df["close"].values
            for i in range(0, len(c) - 5, 5):
                r5.append(c[i+5]/c[i]-1)
        drift[coin] = np.mean(r5); usual[coin] = np.std(r5)
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; lo = df["low"].values
            n = len(df)
            prior_low = pd.Series(lo).shift(1).rolling(30, min_periods=30).min().values
            ret30 = pd.Series(c).pct_change(30).values
            reg = (df["regime"] == "mean_reversion").values
            fc = df["forecast"].fillna(0).values
            seen_cells = set()
            for t in range(n):
                brk = (not np.isnan(prior_low[t])) and c[t] < prior_low[t]
                if not (reg[t] or brk):
                    continue
                cell = t // 5
                rec = {"coin": coin, "w": w, "t": t, "reg": reg[t], "brk": brk,
                       "ret30neg": (ret30[t] < 0) if not np.isnan(ret30[t]) else np.nan,
                       "fc": fc[t], "depth": (c[t]/prior_low[t]-1) if not np.isnan(prior_low[t]) else np.nan,
                       "year": pd.Timestamp(df["timestamp"].iloc[t]).year,
                       "first_in_cell": cell not in seen_cells}
                seen_cells.add(cell)
                for h in (1, 3, 5, 10, 20):
                    rec[f"r{h}"] = c[t+h]/c[t]-1 if t+h < n else np.nan
                rec["u5"] = rec["r5"] - drift[coin] if not np.isnan(rec["r5"]) else np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["u5"].dropna()
        return pd.Series({"n": len(x), "mean_u5": x.mean(), "median_u5": x.median(),
                          "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "share_pos": (x > 0).mean(),
                          "mean_r1": g["r1"].mean(), "mean_r3": g["r3"].mean(),
                          "mean_r10": g["r10"].mean(), "mean_r20": g["r20"].mean()})
    R = d[d.reg & d.first_in_cell]
    out["regime cases all"] = summ(R)
    out["regime cases by coin"] = R.groupby("coin").apply(summ)
    out["regime cases by window"] = R.groupby("w").apply(summ)
    R2 = R.copy(); R2["fcq"] = pd.qcut(R2["fc"].rank(method="first"), 3, labels=["lo","mid","hi"])
    out["regime cases by forecast tercile"] = R2.groupby("fc_q" if False else "fcq").apply(summ)
    B = d[d.brk & d.first_in_cell]
    out["all breaks (no vol/ret filter)"] = summ(B)
    B2 = B.copy(); B2["dq"] = pd.qcut(B2["depth"].rank(method="first"), 4, labels=["deepest","q2","q3","shallowest"])
    out["all breaks by depth quartile"] = B2.groupby("dq").apply(summ)
    out["all breaks by coin"] = B.groupby("coin").apply(summ)
    out["breaks: regime vs not"] = B.groupby("reg").apply(summ)
    out["usual 5-bar sd by coin"] = pd.Series(usual)
    out["drift by coin"] = pd.Series(drift)
    return out
