def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []; base = []
    H = [1,3,5,10,20]
    for coin, wins in bars.items():
        # coin mean h-return on grid
        means = {}
        for h in H:
            rs = []
            for w, df in wins.items():
                c = df["close"].values
                idx = np.arange(0, len(c)-h, h)
                rs += list(c[idx+h]/c[idx]-1)
            means[h] = np.mean(rs) if rs else np.nan
        for w, df in wins.items():
            c = df["close"].values; f = df["forecast"].fillna(0).values
            n = len(c)
            yr = pd.to_datetime(df["timestamp"]).dt.year.values
            brk = df.get("debug_info.components.break.last_history_value")
            brk = brk.values if brk is not None else np.full(n, np.nan)
            r10 = df.get("debug_info.components.run10.post_pipeline_value")
            r10 = r10.values if r10 is not None else np.full(n, np.nan)
            ref = 0.0; sig = np.zeros(n, bool)
            for i in range(n):
                if f[i] <= 0: ref = 0.0; continue
                if f[i]-ref >= 2: sig[i] = True; ref = f[i]
                else: ref = min(ref, f[i]) if ref > 0 else f[i]
            c60 = pd.Series(c).pct_change(60).values
            vol = pd.Series(c).pct_change().rolling(30).std().values
            seen = set()
            for i in np.where(sig)[0]:
                cell = i//5
                if cell in seen: continue
                seen.add(cell)
                r = {"coin": coin, "win": int(w[1:]), "year": yr[i], "f": f[i], "brk": brk[i], "r10": r10[i], "vol": vol[i]}
                for h in H:
                    r[f"x{h}"] = c[i+h]/c[i]-1-means[h] if i+h < n else np.nan
                rows.append(r)
            for i in range(60, n-5, 5):
                if c60[i] > 0:
                    base.append({"coin": coin, "x5": c[i+5]/c[i]-1-means[5], "case": cell_any(sig, i)})
    d = pd.DataFrame(rows); b = pd.DataFrame(base)
    def tt(s):
        s = s.dropna(); return pd.Series({"n": len(s), "mean": s.mean(), "t": s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan})
    out = {}
    out["n_cases"] = len(d)
    out["by_h"] = pd.DataFrame({h: tt(d[f"x{h}"]) for h in H}).T
    out["by_coin"] = d.groupby("coin")["x5"].apply(tt).unstack()
    out["by_year"] = d.groupby("year")["x5"].apply(tt).unstack()
    for k in ["f", "brk", "r10", "vol"]:
        q = pd.qcut(d[k].rank(method="first"), 4, labels=False)
        out[f"by_{k}_q"] = d.groupby(q)[["x5","x10","x20"]].mean().assign(n=d.groupby(q).size(), t5=d.groupby(q)["x5"].apply(lambda s: tt(s)["t"]))
    out["base_r60pos_noncase"] = tt(b.loc[~b["case"], "x5"])
    out["median_x5"] = d["x5"].median()
    out["share_pos_x5"] = (d["x5"] > 0).mean()
    return out

def cell_any(sig, i):
    return bool(sig[i:i+5].any())
