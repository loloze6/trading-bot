def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, ws in bars.items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            r6 = c / c.shift(6) - 1
            usual = r1.rolling(180, min_periods=60).std() * np.sqrt(6)
            rng = b["high"].rolling(6).max() / b["low"].rolling(6).min() - 1
            urng = rng.rolling(180, min_periods=60).mean()
            z6 = r6 / usual; rr = rng / urng
            ts = pd.to_datetime(b["timestamp"])
            n = len(b)
            for h in (6, 18):
                f = c.shift(-h) / c - 1
                for i in range(0, n - h, h):
                    rows.append((coin, w, h, f.iloc[i], z6.iloc[i], rr.iloc[i], ts.iloc[i].year, ts.iloc[i].weekday()))
    D = pd.DataFrame(rows, columns=["coin","w","h","fwd","z6","rr","yr","wd"])
    D["un"] = D["fwd"] - D.groupby(["coin","h"])["fwd"].transform("mean")
    def summ(g):
        x = g["un"].dropna(); n = len(x)
        return pd.Series({"n": n, "mean_un": x.mean(), "t": x.mean()/(x.std()/np.sqrt(n)) if n > 2 else np.nan})
    out = {}
    D["zb"] = pd.cut(D["z6"], [-99,-2.5,-1.5,-0.75,0,0.75,1.5,2.5,99])
    out["z6 bins x h"] = D.groupby(["h","zb"]).apply(summ).reset_index()
    L = D[D["z6"] < -0.75].copy()
    out["z6<-0.75 by coin h6"] = L[L.h==6].groupby("coin").apply(summ).reset_index()
    out["z6<-0.75 by year h6"] = L[L.h==6].groupby("yr").apply(summ).reset_index()
    L["rrq"] = L.groupby("h")["rr"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["falls by range tertile x h"] = L.groupby(["h","rrq"]).apply(summ).reset_index()
    E = D[D.h==6].dropna(subset=["z6"])
    out["corr z6 vs un h6 by coin"] = E.groupby("coin").apply(lambda g: pd.Series({"corr": g["z6"].corr(g["un"]), "n": len(g)})).reset_index()
    out["friday by coin h6"] = E[E.wd==4].groupby("coin").apply(summ).reset_index()
    out["friday by year h6"] = E[E.wd==4].groupby("yr").apply(summ).reset_index()
    return out
