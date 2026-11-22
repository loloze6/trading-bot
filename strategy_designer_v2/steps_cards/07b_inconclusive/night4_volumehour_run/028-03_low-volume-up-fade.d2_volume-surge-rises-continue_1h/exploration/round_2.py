def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float); v = b["volume"].astype(float)
            r = c.pct_change()
            sd = r.rolling(720, min_periods=240).std().shift(1)
            vm = v.rolling(720, min_periods=240).mean().shift(1)
            df = pd.DataFrame({"z": r / sd, "vr": v / vm,
                               "year": pd.to_datetime(b["timestamp"]).dt.year})
            for h in (6, 12, 24):
                df[f"f{h}"] = c.shift(-h) / c - 1
            df["coin"] = coin; df["win"] = w; df["pos"] = np.arange(len(df))
            rows.append(df)
    d = pd.concat(rows, ignore_index=True)
    usual = {}
    for h in (6, 12, 24):
        g = d[d["pos"] % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean(); sdv = g.groupby("coin")[f"f{h}"].std()
        d[f"u{h}"] = d[f"f{h}"] - d["coin"].map(dr)
        d[f"s{h}"] = d[f"u{h}"] / d["coin"].map(sdv)
    out = {}
    def summ(e, h, label):
        e = e.copy(); e["cell"] = e["pos"] // h
        g = e.groupby(["coin", "win", "cell"]).head(1)
        x = g[f"u{h}"].dropna(); s = g.loc[x.index, f"s{h}"]
        return {"grp": label, "h": h, "n": len(x), "mean_bp": round(x.mean()*1e4, 2),
                "t": round(x.mean()/(x.std()/np.sqrt(len(x))), 2), "strength": round(s.mean(), 3)}
    res = []
    for zmin in (2, 2.5, 3):
        for vmin in (0, 2, 3):
            e = d[(d["z"] >= zmin) & (d["vr"] >= vmin)]
            for h in (6, 12, 24):
                res.append(summ(e, h, f"up z>={zmin} vr>={vmin}"))
    out["pooled up events, one per h-cell"] = pd.DataFrame(res)
    # grading inside up z>=2.5: correlation of unusual move with log vr and with z*vr
    e = d[(d["z"] >= 2.5)].copy()
    gr = []
    for h in (6, 24):
        e2 = e.copy(); e2["cell"] = e2["pos"] // h
        g = e2.groupby(["coin", "win", "cell"]).head(1).dropna(subset=[f"u{h}", "vr"])
        for col in ("vr", "z"):
            rho, p = stats.spearmanr(np.log(g[col]) if col == "vr" else g[col], g[f"u{h}"])
            gr.append({"h": h, "x": col, "n": len(g), "spearman": round(rho, 3), "p": round(p, 3)})
        q = pd.qcut(g["vr"], 4, labels=False)
        for k in range(4):
            x = g.loc[q == k, f"u{h}"]
            gr.append({"h": h, "x": f"vr quartile {k}", "n": len(x), "spearman": round(x.mean()*1e4, 2),
                       "p": round(x.mean()/(x.std()/np.sqrt(len(x))), 2)})
    out["grading in up z>=2.5 (quartile rows: mean_bp, t)"] = pd.DataFrame(gr)
    # stability: up z>=2.5 vr>=2 at 24h by year halves and coin
    e = d[(d["z"] >= 2.5) & (d["vr"] >= 2)]
    res = []
    for lab, m in [("2018-2021", e["year"] <= 2021), ("2022-2025", e["year"] >= 2022)]:
        for coin in ("BTCUSD", "ETHUSD"):
            for h in (6, 24):
                res.append(summ(e[m & (e["coin"] == coin)], h, f"{lab} {coin}"))
    out["stability up z>=2.5 vr>=2"] = pd.DataFrame(res)
    # base rate: all up hours z in (1,2.5), 24h, to see if any big up hour continues
    res = []
    for lo, hi in ((1, 2), (2, 3), (3, 100)):
        for vlo, vhi in ((0, 1.5), (1.5, 1e9)):
            e = d[(d["z"] >= lo) & (d["z"] < hi) & (d["vr"] >= vlo) & (d["vr"] < vhi)]
            res.append(summ(e, 24, f"z[{lo},{hi}) vr[{vlo},{vhi})"))
    out["24h by z x vr, up"] = pd.DataFrame(res)
    return out
