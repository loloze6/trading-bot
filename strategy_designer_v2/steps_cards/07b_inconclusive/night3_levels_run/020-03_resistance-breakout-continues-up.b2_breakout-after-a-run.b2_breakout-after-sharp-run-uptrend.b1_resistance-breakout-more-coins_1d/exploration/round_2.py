def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [5, 10, 20]
    rows = []
    for coin, wins in bars.items():
        means = {}; sds = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                rs += list(c[idx+h]/c[idx]-1)
            means[h] = np.mean(rs); sds[h] = np.std(rs)
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values; n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            col = "debug_info.components.break.last_history_value"
            brk = df[col].values if col in df else np.full(n, np.nan)
            ref = 0.0; sig = np.zeros(n, bool)
            for i in range(n):
                if f[i] <= 0: ref = 0.0; continue
                if f[i]-ref >= 2: sig[i] = True; ref = f[i]
                else: ref = min(ref, f[i]) if ref > 0 else f[i]
            seen5 = set(); seen20 = set()
            for i in np.where(sig)[0]:
                r = {"coin": coin, "year": yr[i], "f": f[i], "brk": brk[i],
                     "first5": (i//5) not in seen5, "first20": (i//20) not in seen20}
                seen5.add(i//5); seen20.add(i//20)
                for h in H:
                    r[f"x{h}"] = c[i+h]/c[i]-1-means[h] if i+h < n else np.nan
                    r[f"s{h}"] = r[f"x{h}"]/sds[h]
                rows.append(r)
    d = pd.DataFrame(rows)
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    out = {}
    d5 = d[d.first5].copy()
    d20 = d[d.first20].copy()
    out["h20_nonoverlap"] = tt(d20["x20"])
    out["h20_strength"] = d20["s20"].mean()
    d5["fq"] = pd.qcut(d5["f"].rank(method="first"), 4, labels=False)
    d5["bq"] = pd.qcut(d5["brk"].rank(method="first"), 4, labels=False)
    top = d5[d5.fq == 3]
    out["topf_x5"] = tt(top["x5"]); out["topf_strength5"] = top["s5"].mean()
    out["topf_by_year"] = top.groupby("year")["x5"].apply(tt).unstack()
    out["topf_coins_pos_share"] = (top.groupby("coin")["x5"].mean() > 0).mean()
    out["topf_median_x5"] = top["x5"].median()
    out["f_q_by_h"] = d5.groupby("fq")[["x5", "s5"]].mean().assign(t5=d5.groupby("fq")["x5"].apply(lambda s: tt(s)["t"]))
    d20["fq"] = pd.qcut(d20["f"].rank(method="first"), 4, labels=False)
    out["h20_by_fq"] = d20.groupby("fq")["x20"].apply(tt).unstack()
    out["corr_f_x5_spearman"] = d5[["f", "x5"]].corr(method="spearman").iloc[0, 1]
    out["topb_by_year"] = d5[d5.bq == 3].groupby("year")["x5"].apply(tt).unstack()
    out["f_cut_q3"] = d5["f"].quantile(0.75)
    return out
