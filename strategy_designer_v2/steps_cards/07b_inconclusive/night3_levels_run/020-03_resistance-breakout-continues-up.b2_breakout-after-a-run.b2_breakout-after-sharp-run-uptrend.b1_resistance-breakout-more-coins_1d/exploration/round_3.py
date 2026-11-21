def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        rs = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c)-5, 5)
            rs += list(c[idx+5]/c[idx]-1)
        m5 = np.mean(rs); sd5 = np.std(rs)
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values; n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            col = "debug_info.components.break.last_history_value"
            brk = df[col].values if col in df else np.full(n, np.nan)
            col2 = "debug_info.components.run10.post_pipeline_value"
            r10 = df[col2].values if col2 in df else np.full(n, np.nan)
            col3 = "debug_info.components.break.post_pipeline_value"
            bz = df[col3].values if col3 in df else np.full(n, np.nan)
            r60 = pd.Series(c).pct_change(60).values
            r10raw = pd.Series(c).pct_change(10).values
            ref = 0.0; sig = np.zeros(n, bool)
            for i in range(n):
                if f[i] <= 0: ref = 0.0; continue
                if f[i]-ref >= 2: sig[i] = True; ref = f[i]
                else: ref = min(ref, f[i]) if ref > 0 else f[i]
            seen = set()
            for i in np.where(sig)[0]:
                if i//5 in seen: continue
                seen.add(i//5)
                if i+5 >= n: continue
                rows.append({"coin": coin, "win": int(w[1:]), "year": yr[i], "f": f[i], "brk": brk[i], "bz": bz[i],
                             "r10z": r10[i], "r10raw": r10raw[i], "r60": r60[i],
                             "x5": c[i+5]/c[i]-1-m5, "s5": (c[i+5]/c[i]-1-m5)/sd5})
    d = pd.DataFrame(rows)
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s)))})
    out = {}
    for k in ["r60", "r10raw", "bz", "r10z"]:
        q = pd.qcut(d[k].rank(method="first"), 4, labels=False)
        g = d.groupby(q)
        out[f"by_{k}_q"] = g["x5"].apply(tt).unstack().assign(s5=g["s5"].mean(), med=g[k].median())
    d["fq"] = pd.qcut(d["f"].rank(method="first"), 4, labels=False)
    top = d[d.fq == 3]
    out["topf_odd_even_win"] = top.groupby(top.win % 2)["x5"].apply(tt).unstack()
    out["topf_by_r60_half"] = top.groupby(top.r60 > d.r60.median())["x5"].apply(tt).unstack()
    out["share_r10z_zero"] = (d["r10z"] <= 0).mean()
    both = d[(d.bz > d.bz.median()) & (d.r10z > d.r10z.median())]
    out["both_strong"] = tt(both["x5"])
    out["both_strong_by_year"] = both.groupby("year")["x5"].apply(tt).unstack()
    out["spearman_bz_x5"] = d[["bz", "x5"]].corr(method="spearman").iloc[0, 1]
    out["spearman_r10raw_x5"] = d[["r10raw", "x5"]].corr(method="spearman").iloc[0, 1]
    return out
