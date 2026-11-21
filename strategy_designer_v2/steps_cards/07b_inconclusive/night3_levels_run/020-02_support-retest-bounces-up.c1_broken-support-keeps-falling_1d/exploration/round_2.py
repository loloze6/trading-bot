def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [5,10]
    drift = {}; usual = {}
    for c in bars:
        for h in H:
            rs = []
            for w, b in bars[c].items():
                cl = b["close"].values
                idx = np.arange(0, len(cl)-h, h)
                rs += list(cl[idx+h]/cl[idx]-1)
            drift[(c,h)] = np.mean(rs); usual[(c,h)] = np.std(rs)
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            f = b["forecast"].fillna(0).values
            cl = b["close"].values; lo = b["low"].values
            ts = pd.to_datetime(b["timestamp"]); n = len(cl)
            s = pd.Series(cl)
            ma120 = s.rolling(120, min_periods=60).mean().values
            r30 = s.pct_change(30).values
            vol = s.pct_change().rolling(30).std().values
            ref = 0.0; bets = []
            for i in range(n):
                sv = -f[i] if f[i] < 0 else 0.0
                if sv <= 0: ref = 0.0; continue
                if sv - ref >= 2: bets.append(i); ref = sv
                else: ref = min(ref, sv)
            seen = set()
            for i in bets:
                cell = i // 5
                if cell in seen: continue
                seen.add(cell)
                # distance to nearest confirmed swing low above close in past 90 bars
                dist = np.nan
                cands = []
                for j in range(max(2, i-90), i-1):
                    if j+2 <= i and lo[j] <= lo[j-2:j+3].min() and lo[j] >= cl[i]:
                        cands.append(lo[j])
                if cands: dist = min(cands)/cl[i]-1
                rec = {"coin": c, "year": ts[i].year, "dist": dist,
                       "above_ma": (cl[i] > ma120[i]) if not np.isnan(ma120[i]) else np.nan,
                       "r30": r30[i], "vol": vol[i]}
                for h in H:
                    if i+h < n:
                        tot = cl[i+h]/cl[i]-1
                        rec[f"u{h}"] = -(tot - drift[(c,h)])
                        rec[f"t{h}"] = -tot
                    else: rec[f"u{h}"] = np.nan; rec[f"t{h}"] = np.nan
                rows.append(rec)
    d = pd.DataFrame(rows)
    def summ(g, col="u5"):
        x = g[col].dropna()
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out = {}
    out["by_above_ma120_u5"] = d.groupby("above_ma").apply(summ)
    out["by_above_ma120_u10"] = d.groupby("above_ma").apply(lambda g: summ(g,"u10"))
    d["dq"] = pd.qcut(d["dist"], 4, labels=False, duplicates="drop")
    out["by_dist_q_u5"] = d.groupby("dq").apply(summ)
    out["dist_edges"] = d.groupby("dq")["dist"].agg(["min","max"])
    d["r30q"] = pd.qcut(d["r30"], 4, labels=False, duplicates="drop")
    out["by_r30_q_u5"] = d.groupby("r30q").apply(summ)
    out["r30_edges"] = d.groupby("r30q")["r30"].agg(["min","max"])
    d["vq"] = pd.qcut(d["vol"], 4, labels=False, duplicates="drop")
    out["by_vol_q_u5"] = d.groupby("vq").apply(summ)
    out["by_year_u10"] = d.groupby("year").apply(lambda g: summ(g,"u10"))
    out["by_year_total5"] = d.groupby("year").apply(lambda g: summ(g,"t5"))
    out["dist_missing_share"] = float(d["dist"].isna().mean())
    return out
