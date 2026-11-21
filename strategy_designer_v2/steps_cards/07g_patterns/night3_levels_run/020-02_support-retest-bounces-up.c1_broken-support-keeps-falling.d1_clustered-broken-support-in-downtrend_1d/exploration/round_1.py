def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 5
    rows = []
    for coin, wins in data["bars"].items():
        recs = []
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            n = len(c)
            fwd = c.shift(-H) / c - 1
            r1 = c.pct_change()
            past5 = c / c.shift(5) - 1
            past20 = c / c.shift(20) - 1
            sma50 = c.rolling(50).mean()
            dist50 = c / sma50 - 1
            vol20 = r1.rolling(20).std()
            vol_rel = vol20 / r1.rolling(60).std()
            hi20 = c / c.rolling(20).max() - 1
            lo20 = c / c.rolling(20).min() - 1
            # swing highs (2 each side) in prior 60 bars, count within 2% above close of nearest
            h = b["high"].astype(float).values; l = b["low"].astype(float).values
            sh = np.zeros(n, bool); sl = np.zeros(n, bool)
            for i in range(2, n - 2):
                if h[i] == max(h[i-2:i+3]): sh[i] = True
                if l[i] == min(l[i-2:i+3]): sl[i] = True
            hc = np.full(n, np.nan); lcb = np.full(n, np.nan)
            for i in range(62, n):
                cc = c.iloc[i]
                idx = np.arange(i - 60, i - 2)
                hh = h[idx][sh[idx]]
                ab = hh[hh >= cc]
                hc[i] = ((ab >= cc) & (ab <= cc * 1.03)).sum()
                ll = l[idx][sl[idx]]
                be = ll[ll <= cc]
                lcb[i] = ((be <= cc) & (be >= cc * 0.97)).sum()
            raw = b.get("debug_info.components.low_cluster.last_history_value")
            df = pd.DataFrame({
                "coin": coin, "win": w, "pos": np.arange(n), "fwd": fwd, "past5": past5,
                "past20": past20, "dist50": dist50, "vol_rel": vol_rel, "hi20": hi20, "lo20": lo20,
                "hiclust": hc, "loclust_below": lcb,
                "fc": b["forecast"].astype(float),
                "alloc": b["postRebalance_current_allocation"].astype(float),
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday,
                "raw": raw.astype(float) if raw is not None else np.nan,
            })
            recs.append(df)
        d = pd.concat(recs)
        g = d[(d["pos"] % H == 0) & d["fwd"].notna()]
        drift = g["fwd"].mean(); sd = g["fwd"].std()
        d["un"] = d["fwd"] - drift; d["st"] = d["un"] / sd
        rows.append(d)
    A = pd.concat(rows)
    G = A[(A["pos"] % H == 0) & A["fwd"].notna()].copy()
    out = {}
    out["base"] = pd.Series({"n": len(G), "mean_fwd": G["fwd"].mean(), "sd": G["fwd"].std()})
    def by(col, q=5, data=G):
        x = data[data[col].notna()].copy()
        try:
            x["b"] = pd.qcut(x[col].rank(method="first"), q, labels=False)
        except Exception:
            x["b"] = x[col]
        r = x.groupby("b").agg(n=("un", "size"), lo=(col, "min"), hi=(col, "max"),
                               un=("un", "mean"), st=("st", "mean"),
                               t=("st", lambda s: s.mean() / (s.std() / np.sqrt(len(s)))))
        return r.round(4)
    for col in ["past5", "past20", "dist50", "vol_rel", "hi20", "lo20"]:
        out[col] = by(col)
    out["hiclust"] = by("hiclust", 4)
    out["loclust_below"] = by("loclust_below", 4)
    out["wd"] = G.groupby("wd").agg(n=("un", "size"), un=("un", "mean"), st=("st", "mean"))
    out["fc_below0"] = by("fc", 4, G[G["fc"] < 0])
    # interaction: past5 within below vs above SMA50
    for nm, sub in [("p5_below50", G[G["dist50"] < 0]), ("p5_above50", G[G["dist50"] >= 0])]:
        out[nm] = by("past5", 4, sub)
    # per coin correlation strength vs past5, dist50
    pc = {}
    for coin, s in G.groupby("coin"):
        s = s.dropna(subset=["past5", "dist50"])
        pc[coin] = {"rho_p5": stats.spearmanr(s["past5"], s["st"])[0],
                    "rho_d50": stats.spearmanr(s["dist50"], s["st"])[0], "n": len(s)}
    out["percoin"] = pd.DataFrame(pc).T.round(3)
    return out
