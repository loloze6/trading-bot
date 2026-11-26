def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wd in bars.items():
        for w, b in wd.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r1 = c.pct_change()
            r7 = c / c.shift(7) - 1
            mabs = r7.abs().rolling(30, min_periods=20).mean()
            s7 = r7 / mabs
            sd30 = r1.rolling(30, min_periods=20).std()
            z1 = r1 / sd30.shift(1)
            tr60 = c / c.shift(60) - 1
            clv = (c - b["low"]) / (b["high"] - b["low"]).replace(0, np.nan)
            n = len(b)
            df = pd.DataFrame({"coin": coin, "w": w, "pos": np.arange(n),
                               "inprof": (b["regime"] == "unknown").astype(int),
                               "s7": s7, "z1": z1, "clv": clv, "tr60": tr60,
                               "day": pd.to_datetime(b["timestamp"]).dt.floor("D")})
            for h in (1, 3, 7):
                df[f"f{h}"] = c.shift(-h) / c - 1
            rows.append(df)
    D = pd.concat(rows, ignore_index=True)
    for h in (1, 3, 7):
        g = D[D.pos % h == 0]
        dr = g.groupby("coin")[f"f{h}"].mean()
        D[f"u{h}"] = D[f"f{h}"] - D.coin.map(dr)
    def prof(r):
        if pd.isna(r.tr60): return "na"
        if r.tr60 > 0.10: return "rising"
        if r.tr60 < -0.10: return "falling"
        return "choppy calm" if r.inprof == 1 else "choppy agitated"
    D["prof"] = D.apply(prof, axis=1)
    out = {"profile counts": D.prof.value_counts()}
    def ctab(sub, key, h, q=5, by=None):
        g = sub[sub.pos % h == 0].dropna(subset=[key, f"u{h}"]).copy()
        g["b"] = pd.qcut(g[key], q, labels=False, duplicates="drop")
        res = []
        for bb, gg in g.groupby("b"):
            dsum = gg.groupby("day")[f"u{h}"].sum()
            m = gg[f"u{h}"].mean(); nd = len(dsum)
            # day-clustered t of mean
            se = np.sqrt(((dsum - gg.groupby("day").size() * m) ** 2).sum()) / len(gg)
            res.append({"b": bb, "lo": gg[key].min(), "hi": gg[key].max(), "n": len(gg),
                        "days": nd, "mean": m, "t_day": m / se if se > 0 else np.nan})
        return pd.DataFrame(res).set_index("b")
    for p in ["rising", "falling", "choppy agitated", "choppy calm"]:
        sub = D[D.prof == p]
        out[f"{p}: z1 -> u1"] = ctab(sub, "z1", 1)
        out[f"{p}: clv -> u1"] = ctab(sub, "clv", 1)
        out[f"{p}: s7 -> u3"] = ctab(sub, "s7", 3)
    # windows consistency of low-clv next-day rebound and low-z1
    g = D[D.pos % 1 == 0].dropna(subset=["clv", "u1", "z1"]).copy()
    g["lowclv"] = g.clv < 0.25
    g["lowz"] = g.z1 < -0.64
    out["low clv minus rest u1 by window"] = g.groupby("w").apply(
        lambda x: x[x.lowclv].u1.mean() - x[~x.lowclv].u1.mean())
    out["low z1 minus rest u1 by window"] = g.groupby("w").apply(
        lambda x: x[x.lowz].u1.mean() - x[~x.lowz].u1.mean())
    return out
