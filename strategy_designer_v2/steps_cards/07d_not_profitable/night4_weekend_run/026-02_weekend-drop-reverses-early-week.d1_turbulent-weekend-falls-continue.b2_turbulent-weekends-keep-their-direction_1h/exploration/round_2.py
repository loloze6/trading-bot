def explore(data):
    import numpy as np, pandas as pd
    rows = []
    for coin, ws in data["bars"].items():
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
            pv = b["postRebalance_total_value"].values
            m = (ts.dt.weekday == 6) & (ts.dt.hour == 23)
            for i in np.where(m.values)[0]:
                if i + 48 >= len(c) or i < 216:
                    continue
                f = b["forecast"].iat[i]
                if not np.isfinite(f) or f == 0:
                    continue
                wk = c[i] / c[i - 48] - 1
                sdw = r1.iloc[i - 47:i + 1].std(); sdp = r1.iloc[i - 215:i - 47].std()
                vr = sdw / sdp
                fr = c[i + 48] / c[i] - 1
                sg = np.sign(f)
                wkz = wk / (sdp * np.sqrt(48))
                book = pv[i + 48] / pv[i - 1] - 1 if i >= 1 else np.nan
                rows.append(dict(coin=coin, w=w, sg=sg, f=abs(f), vr=vr, wk=abs(wk), wkz=abs(wkz),
                                 un=sg * (fr - d48), str_=sg * (fr - d48) / s48, book=book,
                                 alloc=abs(b["postRebalance_current_allocation"].iat[i]),
                                 sgv=np.sign(wk) * sg))
    df = pd.DataFrame(rows)
    def g(x):
        return pd.Series(dict(n=len(x), un=x.un.mean(), t=x.un.mean() / x.un.std() * np.sqrt(len(x)),
                              strength=x.str_.mean(), book=x.book.mean(), alloc=x.alloc.mean()))
    out = {}
    df["vq"] = pd.qcut(df.vr, 3, labels=False)
    df["wq"] = pd.qcut(df.wkz, 3, labels=False)
    out["vr tercile x |weekend ret in prior-week sd| tercile"] = df.groupby(["vq", "wq"]).apply(g)
    df["vq5"] = pd.qcut(df.vr, 5, labels=False)
    out["vr quintile: book per case, alloc, strength"] = df.groupby("vq5").apply(g)
    out["sign of forecast vs weekend ret"] = df.groupby("sgv").apply(g)
    out["corr |f| with vr, wkz"] = pd.Series({"vr": df.f.corr(df.vr, method="spearman"), "wkz": df.f.corr(df.wkz, method="spearman")})
    # worst cases contributing to drawdowns
    df["bq"] = pd.qcut(df.book.rank(method="first"), 10, labels=False)
    out["book decile: vr mean, wkz mean"] = df.groupby("bq")[["book", "vr", "wkz", "alloc"]].mean()
    return out
