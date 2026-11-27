def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    btc = {}
    for w, b in bars["BTCUSD"].items():
        bb = b.reset_index(drop=True)
        btc[w] = dict(zip(bb["timestamp"].astype(str), bb["close"].pct_change().shift(-1)))
    for coin, ws in bars.items():
        rr = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 1)
            rr.extend(list(c[idx + 1] / c[idx] - 1))
        d = np.mean(rr); s = np.std(rr, ddof=1)
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"]; r1 = c.pct_change()
            sd20 = r1.rolling(20).std(); zr = r1 / sd20
            ret20 = c / c.shift(20) - 1
            ret60 = c / c.shift(60) - 1
            ret5 = c / c.shift(5) - 1
            rng = (b["high"] - b["low"]).replace(0, np.nan)
            cl = (c - b["low"]) / rng
            body = (c - b["open"]) / rng
            vol = b["volume"]; vrel = vol / vol.rolling(20).mean()
            nxt_open = b["open"].shift(-1)
            yr = pd.to_datetime(b["timestamp"]).dt.year
            f = b["forecast"]
            for i in range(0, len(b) - 1):
                if f.iloc[i] <= -2:
                    ret = c.iloc[i + 1] / c.iloc[i] - 1
                    rb = btc.get(w, {}).get(str(b["timestamp"].iloc[i]), np.nan)
                    rows.append(dict(coin=coin, day=str(b["timestamp"].iloc[i])[:10], year=yr.iloc[i],
                                     zr=zr.iloc[i], ret20=ret20.iloc[i], ret60=ret60.iloc[i], ret5=ret5.iloc[i],
                                     cl=cl.iloc[i], body=body.iloc[i], vrel=vrel.iloc[i],
                                     unusual=-(ret - d), strength=-(ret - d) / s,
                                     btcnext=rb, isbtc=coin == "BTCUSD"))
    df = pd.DataFrame(rows)
    def tday(g):
        g = g.dropna(subset=["unusual"])
        dd = g.groupby("day")["unusual"].sum(); n = len(dd)
        m = g["unusual"].mean()
        se = dd.std(ddof=1) * np.sqrt(n) / len(g) if n > 1 else np.nan
        return pd.Series(dict(n=len(g), days=n, mean=m, t=m / se if se else np.nan,
                              strength=g["strength"].mean()))
    out = {"all_every_bar": tday(df)}
    for col in ["ret20", "ret60", "ret5", "cl", "body", "vrel"]:
        x = df.dropna(subset=[col]).copy()
        x["q"] = pd.qcut(x[col], 3, labels=["lo", "mid", "hi"], duplicates="drop")
        r = x.groupby("q").apply(tday)
        r["colmean"] = x.groupby("q")[col].mean()
        out["by_" + col] = r
    x = df[~df.isbtc].dropna(subset=["btcnext"]).copy()
    if len(x) > 10:
        b_ = np.polyfit(-x["btcnext"], x["unusual"], 1)
        x["resid"] = x["unusual"] - b_[0] * (-x["btcnext"])
        dd = x.groupby("day")["resid"].sum()
        out["vs_btc"] = pd.Series(dict(n=len(x), beta=b_[0], corr=np.corrcoef(-x["btcnext"], x["unusual"])[0, 1],
                                       resid_mean=x["resid"].mean(),
                                       resid_t=x["resid"].mean() / (dd.std(ddof=1) * np.sqrt(len(dd)) / len(x)),
                                       btc_short_mean=(-x["btcnext"]).mean()))
    return out
