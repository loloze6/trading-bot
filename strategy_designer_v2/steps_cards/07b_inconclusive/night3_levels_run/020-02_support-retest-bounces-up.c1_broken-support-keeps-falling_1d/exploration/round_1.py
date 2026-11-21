def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1,3,5,10,20]
    rows = []
    # normal drift per coin per horizon, non-overlapping grids
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl)-h, h)
                rs += list(cl[idx+h]/cl[idx]-1)
            drift[(c,h)] = np.mean(rs); usual[(c,h)] = np.std(rs)
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            raw = b["debug_info.components.support_above.last_history_value"].values
            cl = b["close"].values
            ts = pd.to_datetime(b["timestamp"])
            n = len(cl)
            # trailing 60-bar return for regime
            tr = pd.Series(cl).pct_change(60).values
            ref = 0.0; bets = []
            for i in range(n):
                s = -f[i] if f[i] < 0 else 0.0
                if s <= 0:
                    ref = 0.0; continue
                if s - ref >= 2:
                    bets.append(i); ref = s
                else:
                    ref = min(ref, s)
            seen = set()
            for i in bets:
                cell = i // 5
                if cell in seen: continue
                seen.add(cell)
                rec = {"coin": c, "window": w, "year": ts[i].year, "absf": -f[i],
                       "raw": raw[i], "tr60": tr[i]}
                for h in H:
                    if i+h < n:
                        tot = cl[i+h]/cl[i]-1
                        rec[f"u{h}"] = -(tot - drift[(c,h)])
                        rec[f"s{h}"] = rec[f"u{h}"]/usual[(c,h)]
                    else:
                        rec[f"u{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["by_horizon"] = pd.DataFrame({h: summ(d, f"u{h}") for h in H}).T
    out["by_coin"] = d.groupby("coin").apply(summ)
    out["by_year"] = d.groupby("year").apply(summ)
    d["fq"] = pd.qcut(d["absf"], 4, labels=False, duplicates="drop")
    out["by_absf_quartile"] = d.groupby("fq").apply(summ)
    d["rq"] = pd.qcut(d["raw"], 4, labels=False, duplicates="drop")
    out["by_raw_quartile"] = d.groupby("rq").apply(summ)
    d["trq"] = pd.qcut(d["tr60"], 4, labels=False, duplicates="drop")
    out["by_trend60_quartile"] = d.groupby("trq").apply(summ)
    out["by_trend60_quartile_u10"] = d.groupby("trq").apply(lambda g: summ(g,"u10"))
    out["trend_q_edges"] = d.groupby("trq")["tr60"].agg(["min","max"])
    out["n_cases"] = len(d)
    return out
