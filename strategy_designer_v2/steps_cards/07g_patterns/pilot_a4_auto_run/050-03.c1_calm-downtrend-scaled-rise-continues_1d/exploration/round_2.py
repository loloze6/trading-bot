def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; out = {}
    res = []
    for H in [3, 7, 14]:
        rows = []
        for coin, ws in bars.items():
            allr = []
            for w, b in ws.items():
                c = b["close"].values
                for i in range(0, len(c) - H, H):
                    allr.append(c[i+H]/c[i]-1)
            dr = np.mean(allr)
            for w, b in ws.items():
                b = b.reset_index(drop=True)
                c = b["close"]; hi = b["high"]; lo = b["low"]
                mrr = ((hi-lo)/c).rolling(30).mean()
                sd = c.pct_change().rolling(30).std()
                f = pd.DataFrame({
                    "inprof": (b["regime"]=="unknown").values,
                    "s14": (c.pct_change(14)/mrr).values,
                    "s7": (c.pct_change(7)/mrr).values,
                    "s7sd": (c.pct_change(7)/sd).values,
                    "dlo20": (c/lo.rolling(20).min()-1).values,
                    "dlo20s": ((c/lo.rolling(20).min()-1)/mrr).values,
                    "exc": (c.shift(-H)/c-1-dr).values,
                    "day": pd.to_datetime(b["timestamp"]).dt.floor("D").values,
                })
                f["grid"] = np.arange(len(f)) % H == 0
                rows.append(f)
        df = pd.concat(rows, ignore_index=True)
        p = df[df.grid & df.inprof].dropna(subset=["exc"])
        for col in ["s14","s7","s7sd","dlo20","dlo20s"]:
            d = p.dropna(subset=[col])
            if len(d) < 10: continue
            lr = stats.linregress(d[col], d["exc"])
            r = stats.spearmanr(d[col], d["exc"]).correlation
            up = d[d[col] > 0] if col.startswith("s") else d[d[col] > d[col].median()]
            res.append({"H": H, "x": col, "n": len(d), "slope_t": lr.slope/lr.stderr,
                        "spearman": r, "upper_mean": up["exc"].mean(), "upper_n": len(up),
                        "upper_t": stats.ttest_1samp(up["exc"],0).statistic})
    out["slopes"] = pd.DataFrame(res)
    return out
