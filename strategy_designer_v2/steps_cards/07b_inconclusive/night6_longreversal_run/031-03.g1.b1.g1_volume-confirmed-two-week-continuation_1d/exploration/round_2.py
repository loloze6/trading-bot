def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def tday(df, col):
        g = df.groupby("timestamp")[col].sum()
        if len(g) < 3: return np.nan
        return g.mean() / (g.std(ddof=1) / np.sqrt(len(g)))
    def summ(d, col):
        d = d.dropna(subset=[col])
        return pd.Series({"n": len(d), "mean": d[col].mean(), "t_day": tday(d, col), "days": d.timestamp.nunique()})
    rows = []
    for H in (3, 5, 7, 10, 14):
        for coin, wins in bars.items():
            allr = []
            for w, b in wins.items():
                c = b["close"].values
                idx = np.arange(0, len(c) - H, H)
                allr += list(c[idx + H] / c[idx] - 1)
            mu = np.mean(allr) if allr else np.nan
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].values; v = b["volume"].values
                for i in np.arange(0, len(c) - H, H):
                    if i < 29: continue
                    r = c[i + H] / c[i] - 1
                    r14 = c[i] / c[i - 14] - 1
                    r7 = c[i] / c[i - 7] - 1
                    vr = v[i-13:i+1].mean() / v[i-29:i+1].mean()
                    rows.append(dict(H=H, coin=coin, timestamp=b["timestamp"].iat[i],
                                     year=pd.Timestamp(b["timestamp"].iat[i]).year,
                                     r=r, mu=mu, r14=r14, r7=r7, vr=vr, f=b["forecast"].iat[i],
                                     cont=np.sign(r14) * (r - mu),
                                     cont7=np.sign(r7) * (r - mu)))
    df = pd.DataFrame(rows)
    df["vrq"] = df.groupby("H")["vr"].transform(lambda s: pd.qcut(s, 5, labels=False))
    out["cont14_by_H_vrq"] = df.groupby(["H", "vrq"]).apply(lambda d: summ(d, "cont")).unstack("vrq")["mean"]
    out["cont14_t_by_H_vrq"] = df.groupby(["H", "vrq"]).apply(lambda d: summ(d, "cont")).unstack("vrq")["t_day"]
    top = df[df.vrq == 4].copy()
    top["side"] = np.where(top.r14 > 0, "up", "down")
    out["top_vr_cont_by_H_side"] = top.groupby(["H", "side"]).apply(lambda d: summ(d, "cont"))
    d7 = df[df.H == 7].copy()
    d7["above"] = d7.vr >= 1
    out["H7_cont_by_vol_side"] = d7.groupby(["above", np.where(d7.r14 > 0, "up", "down")]).apply(lambda d: summ(d, "cont"))
    # graded: signal = r14 scaled x (vr-1) on vr>=1
    for H in (7, 14):
        d = df[(df.H == H) & (df.vr >= 1)].copy()
        d["s"] = np.sign(d.r14) * (d.vr - 1)
        d["gq"] = pd.qcut(d.vr, 4, labels=False)
        out[f"H{H}_volup_cont_by_vrq4"] = d.groupby("gq").apply(lambda x: summ(x, "cont"))
        out[f"H{H}_volup_cont_by_year"] = d.groupby("year").apply(lambda x: summ(x, "cont"))
    return out
