def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            nxt = c.shift(-1) / c - 1
            prev_run = np.zeros(len(b), int); runfall = np.zeros(len(b)); cnt = 0; cum = 0.0
            for i in range(len(b)):
                prev_run[i] = cnt; runfall[i] = cum
                ri = r.iloc[i]
                if ri < 0: cnt += 1; cum += np.log1p(ri)
                elif ri >= 0: cnt = 0; cum = 0.0
            tr = c / c.shift(60) - 1
            tr20 = c / c.shift(20) - 1
            vol = r.rolling(30).std()
            vrank = vol.rolling(len(b), min_periods=30).rank(pct=True)
            df = pd.DataFrame({"coin": coin, "w": w, "ts": pd.to_datetime(b["timestamp"]),
                               "r": r, "nxt": nxt, "prun": prev_run, "rfall": runfall,
                               "tr": tr, "tr20": tr20, "vol": vol, "vrank": vrank,
                               "alloc": b["postRebalance_current_allocation"]})
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    D["day"] = D["ts"].dt.floor("D")
    drift = D.groupby("coin")["nxt"].mean()
    D["dev"] = D["nxt"] - D["coin"].map(drift)
    D["trend"] = np.where(D["tr"] > 0.10, "rising", np.where(D["tr"] < -0.10, "falling", "choppy"))
    D.loc[D["tr"].isna(), "trend"] = "na"
    D["agit"] = np.where(D["vrank"] > 0.5, "agit", "calm")
    D.loc[D["vrank"].isna(), "agit"] = "na"
    D["up"] = D["r"] > 0
    D["zr"] = D["r"] / D["vol"]
    D["zfall"] = -D["rfall"] / D["vol"]

    def stat(g, col="dev", sign=-1):
        g = g.dropna(subset=[col])
        if len(g) < 5: return pd.Series({"n": len(g), "mean": np.nan, "t": np.nan, "days": 0})
        x = sign * g[col]; m = x.mean()
        s = (x - m).groupby(g["day"]).sum(); G = len(s)
        se = np.sqrt((s**2).sum() * G / max(G - 1, 1)) / len(x)
        return pd.Series({"n": len(x), "mean": m, "t": m / se if se > 0 else np.nan, "days": G})

    out = {}
    U = D[D["up"]].copy()
    U["runc"] = U["prun"].clip(upper=3)
    out["upday short by trend x agit"] = U.groupby(["trend", "agit"]).apply(stat)
    out["upday short by trend x agit x run(0,1,2,3+)"] = U[U["trend"].isin(["falling","choppy"])].groupby(["trend","agit","runc"]).apply(stat)
    FA = U[(U["trend"] == "falling") & (U["agit"] == "agit") & (U["prun"] >= 1)].copy()
    FA["zq"] = pd.qcut(FA["zr"], 3, labels=False, duplicates="drop")
    out["falling agit run-break by up-size tercile"] = FA.groupby("zq").apply(stat)
    FA["fq"] = pd.qcut(FA["zfall"], 3, labels=False, duplicates="drop")
    out["falling agit run-break by run-fall/vol tercile"] = FA.groupby("fq").apply(stat)
    FA["y"] = FA["ts"].dt.year
    out["falling agit run-break by year"] = FA.groupby("y").apply(stat)
    out["falling agit run-break by window"] = FA.groupby("w").apply(stat)
    # 20-day trend as alternative
    U["t20"] = np.where(U["tr20"] < -0.05, "fall20", np.where(U["tr20"] > 0.05, "rise20", "flat20"))
    out["upday run>=1 short by 20d trend x agit"] = U[U["prun"] >= 1].groupby(["t20", "agit"]).apply(stat)
    # spearman grading in falling agit
    from scipy.stats import spearmanr
    g = FA.dropna(subset=["dev", "zfall"])
    out["spearman falling agit: zfall vs short dev"] = float(spearmanr(g["zfall"], -g["dev"])[0])
    out["spearman falling agit: zr vs short dev"] = float(spearmanr(g["zr"], -g["dev"])[0])
    out["spearman falling agit: prun vs short dev"] = float(spearmanr(g["prun"], -g["dev"])[0])
    # book's position days agitation split
    P = D[D["alloc"].abs() > 1e-6].copy()
    P["gain"] = P["alloc"] * P["nxt"]
    out["book bar gain by agit"] = P.groupby("agit")["gain"].agg(["count", "mean", "std"])
    return out
