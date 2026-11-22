def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, ws in data["bars"].items():
        allc = []
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            allc.append(b["close"].values)
        drift = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 48, 48)
            drift.extend(list(c[idx + 48] / c[idx] - 1))
        d48 = np.nanmean(drift); s48 = np.nanstd(drift)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            c = b["close"].values
            r1 = pd.Series(c).pct_change()
            m = (ts.dt.weekday == 6) & (ts.dt.hour == 23)
            for i in np.where(m.values)[0]:
                if i + 48 >= len(c) or i < 216:
                    continue
                f = b["forecast"].iat[i]
                if not np.isfinite(f) or f == 0:
                    continue
                wk = c[i] / c[i - 48] - 1
                pw = c[i - 48] / c[i - 216] - 1
                p30 = c[i - 48] / c[i - min(i, 720)] - 1 if i >= 720 else np.nan
                vr = r1.iloc[i - 47:i + 1].std() / r1.iloc[i - 215:i - 47].std()
                fr = c[i + 48] / c[i] - 1
                f24 = c[i + 24] / c[i] - 1
                fr96 = c[i + 96] / c[i] - 1 if i + 96 < len(c) else np.nan
                sg = np.sign(f)
                rows.append(dict(coin=coin, w=w, year=ts.iat[i].year, f=f, sg=sg,
                                 alloc=b["postRebalance_current_allocation"].iat[i],
                                 wk=wk, pw=pw, p30=p30, vr=vr,
                                 un=sg * (fr - d48), tot=sg * fr, d1=sg * f24,
                                 d2=sg * (fr - f24), x96=sg * (fr96 - fr),
                                 pwal=np.sign(pw) * sg, p30al=np.sign(p30) * sg))
    df = pd.DataFrame(rows)
    def g(x):
        return pd.Series(dict(n=len(x), un=x.un.mean(), t=x.un.mean() / x.un.std() * np.sqrt(len(x)), tot=x.tot.mean()))
    out = {}
    out["by coin"] = df.groupby("coin").apply(g)
    out["by year"] = df.groupby("year").apply(g)
    out["by side"] = df.groupby("sg").apply(g)
    df["fq"] = pd.qcut(df.f.abs(), 5, labels=False)
    out["by |f| quintile"] = df.groupby("fq").apply(g)
    df["vq"] = pd.qcut(df.vr, 5, labels=False)
    out["by volratio quintile"] = df.groupby("vq").apply(g)
    df["wq"] = pd.qcut(df.wk.abs(), 5, labels=False)
    out["by |weekend ret| quintile"] = df.groupby("wq").apply(g)
    out["by prior-week aligned"] = df.groupby("pwal").apply(g)
    out["by prior-30d aligned"] = df.groupby("p30al").apply(g)
    out["day1 day2 day3-4 signed mean,t"] = pd.DataFrame({k: [df[k].mean(), df[k].mean() / df[k].std() * np.sqrt(df[k].notna().sum())] for k in ["d1", "d2", "x96"]}, index=["mean", "t"])
    out["mean |alloc|"] = float(df.alloc.abs().mean())
    # book
    dl = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day", "book_return", "coin_return"]].copy(); dd["w"] = w; dd["coin"] = coin
            dl.append(dd)
    D = pd.concat(dl)
    B = D.groupby(["w", "day"])[["book_return", "coin_return"]].mean().reset_index()
    B["wn"] = B.w.str[1:].astype(int); B = B.sort_values(["wn", "day"])
    B["wd"] = pd.to_datetime(B.day).dt.weekday
    out["book by weekday"] = B.groupby("wd")[["book_return", "coin_return"]].agg(["mean", "std", "count"])
    eq = (1 + B.book_return.fillna(0)).cumprod()
    dd = eq / eq.cummax() - 1
    out["max dd"] = float(dd.min())
    B["year"] = pd.to_datetime(B.day).dt.year
    out["book by year"] = B.groupby("year")[["book_return", "coin_return"]].mean()
    out["book by window"] = B.groupby("wn")[["book_return", "coin_return"]].agg(["mean"])
    return out
