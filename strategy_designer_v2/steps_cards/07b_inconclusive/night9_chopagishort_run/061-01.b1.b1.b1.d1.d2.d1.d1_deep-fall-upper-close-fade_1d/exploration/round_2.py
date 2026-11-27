def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = [1, 2, 3, 5]
    drift = {}
    for coin, ws in bars.items():
        r = {h: [] for h in H}
        for w, df in ws.items():
            c = df["close"].values
            for h in H:
                idx = np.arange(0, len(c) - h, h)
                r[h] += list(c[idx + h] / c[idx] - 1)
        drift[coin] = {h: np.mean(r[h]) for h in H}
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; hi = df["high"].values; lo = df["low"].values
            n = len(c)
            loc = np.where(hi > lo, (c - lo) / (hi - lo), np.nan)
            ret5 = pd.Series(c).pct_change(5).values
            day = pd.to_datetime(df["timestamp"]).dt.floor("D").values
            year = pd.to_datetime(df["timestamp"]).dt.year.values
            reg = df["regime"].astype(str).values
            for h in [2, 5]:
                for t in range(0, n - h, h):
                    if reg[t] == "chop":
                        continue
                    rows.append(dict(h=h, coin=coin, w=w, year=year[t], day=day[t], loc=loc[t], ret5=ret5[t],
                                     u=-(c[t + h] / c[t] - 1 - drift[coin][h]), tot=-(c[t + h] / c[t] - 1)))
    ab = pd.DataFrame(rows)

    def tpool(d, col="u"):
        d = d.dropna(subset=[col])
        if len(d) < 3: return pd.Series(dict(n=len(d), days=d["day"].nunique() if len(d) else 0, mean=np.nan, t=np.nan))
        m = d[col].mean()
        g = (d[col] - m).groupby(d["day"]).sum()
        D = len(g)
        se = np.sqrt((g ** 2).sum() * D / (D - 1)) / len(d)
        return pd.Series(dict(n=len(d), days=D, mean=m, t=m / se))
    out = {}
    for h in [2, 5]:
        d = ab[ab.h == h].copy()
        d["lq"] = pd.cut(d["loc"], [0, 0.25, 0.5, 0.75, 0.9, 1.01], right=False)
        out[f"h{h}_by_loc"] = d.groupby("lq").apply(tpool)
        out[f"h{h}_by_loc_ex_w16"] = d[d.w != "w16"].groupby("lq").apply(tpool)
        top = d[d["loc"] >= 0.75]
        out[f"h{h}_top_by_window"] = top.groupby("w").apply(tpool)
        out[f"h{h}_top_by_coin"] = top.groupby("coin").apply(tpool)
        top = top.copy(); top["neg5"] = top["ret5"] < 0
        out[f"h{h}_top_by_neg5"] = top.groupby("neg5").apply(tpool)
        dd = d.dropna(subset=["loc", "u"])
        out[f"h{h}_corr_loc_u"] = pd.Series(dict(spearman=dd["loc"].corr(dd["u"], method="spearman"), n=len(dd)))
    return out
