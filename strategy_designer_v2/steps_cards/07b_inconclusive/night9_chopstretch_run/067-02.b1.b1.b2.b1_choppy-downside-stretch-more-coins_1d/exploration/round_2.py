def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    H = 5
    drift = {}
    for coin, ws in bars.items():
        rets = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - H, H):
                rets.append(c[i + H] / c[i] - 1)
        drift[coin] = np.mean(rets) if rets else np.nan
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            c = df["close"]
            sma = c.rolling(20).mean()
            r1 = c.pct_change()
            sd = r1.rolling(20).std()
            raw = (c - sma) / sma / sd
            below = (c < sma).astype(float)
            # consecutive days below the average
            run = below.groupby((below != below.shift()).cumsum()).cumcount() + 1
            run = run.where(below == 1, 0)
            tr60 = c / c.shift(60) - 1
            r5p = c / c.shift(5) - 1
            sdrank = sd.expanding(40).apply(lambda x: (x <= x[-1]).mean(), raw=True)
            n = len(df)
            for i in range(0, n - H, H):
                rows.append(dict(coin=coin, w=w, ts=df["timestamp"].iloc[i],
                    fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                    raw=raw.iloc[i], run=run.iloc[i], tr60=tr60.iloc[i],
                    r5p=r5p.iloc[i], sdrank=sdrank.iloc[i],
                    r=c.iloc[i + H] / c.iloc[i] - 1))
    d = pd.DataFrame(rows)
    d["day"] = pd.to_datetime(d["ts"]).dt.floor("D")
    d["ex"] = d["r"] - d["coin"].map(drift)
    s = d[(d.reg == "unknown") & (d.fc < 0)].copy()
    s["sx"] = -s["ex"]; s["wgt"] = s["fc"].abs()
    def tpool(sub, col="sx", wcol=None):
        if len(sub) < 3: return pd.Series(dict(n=len(sub), days=np.nan, mean=np.nan, t=np.nan))
        wv = sub[wcol] if wcol else pd.Series(1.0, index=sub.index)
        m = (sub[col] * wv).sum() / wv.sum()
        dd = ((sub[col] - m) * wv).groupby(sub["day"]).sum()
        D = len(dd)
        se = np.sqrt((dd ** 2).sum() * D / (D - 1)) / wv.sum() if D > 1 else np.nan
        return pd.Series(dict(n=len(sub), days=D, mean=m, t=m / se if se else np.nan))
    out = {}
    out["weighted_vs_unweighted"] = pd.DataFrame({"weighted": tpool(s, wcol="wgt"), "unweighted": tpool(s)}).T
    s["runq"] = pd.cut(s["run"], [0, 2, 5, 10, 100], labels=["1-2", "3-5", "6-10", ">10"])
    out["by_days_below_avg"] = s.groupby("runq").apply(lambda x: tpool(x))
    t = s.dropna(subset=["tr60"]).copy()
    t["trs"] = np.where(t.tr60 < 0, "choppy_down", "choppy_up")
    out["by_60d_trend_sign"] = t.groupby("trs").apply(lambda x: tpool(x))
    a = s.dropna(subset=["sdrank"]).copy()
    a["ag"] = np.where(a.sdrank > 0.5, "swing_high", "swing_low")
    out["by_swing_rank"] = a.groupby("ag").apply(lambda x: tpool(x))
    p = s.dropna(subset=["r5p"]).copy()
    p["r5q"] = pd.qcut(p["r5p"], 3, labels=["fell_most", "mid", "fell_least"])
    out["by_prior5d_return"] = p.groupby("r5q").apply(lambda x: pd.concat([tpool(x), pd.Series(dict(r5p=x.r5p.mean(), raw=x.raw.mean()))]))
    s["fh"] = np.where(s.wgt > s.wgt.median(), "larger", "smaller")
    out["size_halves"] = s.groupby("fh").apply(lambda x: tpool(x))
    out["corr_wgt_sx_spearman"] = float(s[["wgt", "sx"]].corr(method="spearman").iloc[0, 1])
    return out
