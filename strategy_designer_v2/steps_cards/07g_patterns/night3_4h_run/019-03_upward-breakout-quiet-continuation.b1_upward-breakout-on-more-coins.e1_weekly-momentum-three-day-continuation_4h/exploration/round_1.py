def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    H = [18, 36, 42]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float).values
            hi = df["high"].astype(float).values; lo = df["low"].astype(float).values
            n = len(c)
            if n < 250: continue
            r1 = np.r_[np.nan, c[1:] / c[:-1] - 1]
            s = pd.Series(r1)
            vol30 = s.rolling(180, min_periods=120).std().values
            vol7 = s.rolling(42, min_periods=42).std().values
            vol2 = s.rolling(12, min_periods=12).std().values
            hh = pd.Series(hi).rolling(42).max().shift(1).values
            ll = pd.Series(lo).rolling(42).min().shift(1).values
            rng = (hh - ll) / c
            ret7 = np.r_[np.full(42, np.nan), c[42:] / c[:-42] - 1]
            ret1d = np.r_[np.full(6, np.nan), c[6:] / c[:-6] - 1]
            ts = pd.to_datetime(df["timestamp"])
            fc = df["forecast"].astype(float).values
            for h in H:
                idx = np.arange(0, n - h, h)
                fr = c[idx + h] / c[idx] - 1
                for j, t in enumerate(idx):
                    rows.append((coin, w, h, t, fr[j], fc[t], vol30[t], vol7[t] / vol30[t] if vol30[t] else np.nan,
                                 vol2[t] / vol30[t] if vol30[t] else np.nan,
                                 rng[t] / (vol30[t] * np.sqrt(42)) if vol30[t] else np.nan,
                                 (c[t] - (hh[t] + ll[t]) / 2) / ((hh[t] - ll[t]) / 2) if hh[t] > ll[t] else np.nan,
                                 r1[t] / vol30[t] if vol30[t] else np.nan,
                                 ret7[t] / (vol30[t] * np.sqrt(42)) if vol30[t] else np.nan,
                                 ret1d[t] / (vol30[t] * np.sqrt(6)) if vol30[t] else np.nan,
                                 ts[t].hour, ts[t].weekday(), ts[t].year))
    d = pd.DataFrame(rows, columns=["coin", "w", "h", "t", "fr", "fc", "vol30", "comp7", "comp2", "rng", "brk",
                                    "r1z", "r7z", "r1dz", "hour", "wd", "year"])
    g = d.groupby(["coin", "h"])["fr"]
    d["drift"] = g.transform("mean"); d["usd"] = g.transform("std")
    d["un"] = d["fr"] - d["drift"]; d["st"] = d["un"] / d["usd"]
    d["absz"] = d["fr"].abs() / d["usd"]
    out = {}
    def tab(sub, col, target, q=5):
        sub = sub.dropna(subset=[col, target]).copy()
        sub["q"] = pd.qcut(sub[col].rank(method="first"), q, labels=False)
        a = sub.groupby("q")[target].agg(["mean", "std", "count"])
        a["t"] = a["mean"] / (a["std"] / np.sqrt(a["count"]))
        a["un_pct"] = sub.groupby("q")["un"].mean() * 100
        return a.drop(columns="std").round(4)
    for h in H:
        sub = d[d.h == h]
        out[f"fc_q h{h} strength"] = tab(sub, "fc", "st")
    s18 = d[d.h == 18]
    out["compression7 -> abs move h18"] = tab(s18, "comp7", "absz")
    out["range7 -> abs move h18"] = tab(s18, "rng", "absz")
    out["breakout pos -> strength h18"] = tab(s18, "brk", "st")
    s18q = s18[s18.rng <= s18.rng.quantile(0.3)]
    out["breakout pos in quiet 30pct -> strength h18"] = tab(s18q, "brk", "st")
    out["1d move z -> strength h18"] = tab(s18, "r1dz", "st")
    out["4h bar z -> strength h18"] = tab(s18, "r1z", "st")
    out["vol level (vol30 rank within coin) -> strength h18"] = tab(
        s18.assign(vr=s18.groupby("coin")["vol30"].rank(pct=True)), "vr", "st")
    s42 = d[d.h == 42]
    out["r7z -> strength h42"] = tab(s42, "r7z", "st")
    out["comp7 -> abs move h42"] = tab(s42, "comp7", "absz")
    # signed-strength product by year for momentum
    s18 = s18.assign(p=np.sign(s18.fc) * s18.st)
    out["momentum sign x strength by year h18"] = s18.groupby("year")["p"].agg(["mean", "count"]).round(4)
    out["strength by weekday h18"] = s18.groupby("wd")["st"].agg(["mean", "count"]).round(4)
    # book daily
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            x = df.dropna(subset=["book_return"]).copy(); x["coin"] = coin; dd.append(x)
    dd = pd.concat(dd)
    dd["wd"] = pd.to_datetime(dd["day"]).dt.weekday
    out["book ret by weekday (bps)"] = (dd.groupby("wd")[["book_return", "coin_return"]].mean() * 1e4).round(2)
    out["book ret by coin (bps)"] = (dd.groupby("coin")[["book_return", "coin_return"]].mean() * 1e4).round(2)
    return out
