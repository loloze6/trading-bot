import numpy as np, pandas as pd

def explore(data):
    bars = data["bars"]
    H = [1, 2, 5]
    drift = {}
    for c, ws in bars.items():
        for h in H:
            rs = []
            for w, df in ws.items():
                cl = df["close"].values
                idx = np.arange(0, len(cl) - h, h)
                rs.extend(cl[idx + h] / cl[idx] - 1)
            drift[(c, h)] = np.mean(rs) if rs else 0.0
    rows = []
    for c, ws in bars.items():
        for w, df in ws.items():
            df = df.reset_index(drop=True)
            cl = df["close"]; hi = df["high"]; lo = df["low"]
            loc = (cl - lo) / (hi - lo)
            pe5 = cl / cl.shift(5) - 1
            r1 = cl.pct_change()
            v30 = r1.rolling(30).std()
            vpct = v30.rolling(min(365, len(df)), min_periods=60).apply(lambda a: (a <= a[-1]).mean(), raw=True)
            f = df["forecast"].fillna(0)
            sig = (f <= -2) & ((f.shift(1).fillna(0) - f) >= 2)
            n = len(df); seen = set()
            for i in np.where(sig.values)[0]:
                cell = i // 5
                if cell in seen: continue
                seen.add(cell)
                if i + 5 >= n: continue
                rec = dict(coin=c, window=w, day=str(df["timestamp"].iloc[i])[:10], pe5=pe5.iloc[i],
                           f=abs(f.iloc[i]), vp=vpct.iloc[i], loc=loc.iloc[i])
                for h in H:
                    rec[f"u{h}"] = -(cl.iloc[i + h] / cl.iloc[i] - 1 - drift[(c, h)])
                rows.append(rec)
    d = pd.DataFrame(rows)

    def ct(x, days):
        m = x.notna(); x = x[m]; days = days[m]; n = len(x)
        if n < 3: return dict(mean=np.nan, n=n, days=0, t=np.nan)
        mu = x.mean(); S = (x - mu).groupby(days).sum(); G = len(S)
        se = np.sqrt((S ** 2).sum() * G / (G - 1)) / n
        return dict(mean=mu, n=n, days=G, t=mu / se)

    out = {}
    d["agit"] = np.where(d["vp"] > 0.5, "agitated", np.where(d["vp"].notna(), "calm", "na"))
    res = {}
    for k, g in d.groupby("agit"):
        for h in H:
            res[f"{k}_h{h}"] = ct(g[f"u{h}"], g["day"])
    out["by_agitation"] = pd.DataFrame(res).T
    sl = {}
    for h in H:
        x = d["f"]; y = d[f"u{h}"]
        b = np.polyfit(x, y, 1)[0]
        sl[f"h{h}"] = dict(slope=b, corr=np.corrcoef(x, y)[0, 1])
    out["slope_by_h"] = pd.DataFrame(sl).T
    d["fq"] = pd.qcut(d["f"], 3, labels=False)
    res = {}
    for k, g in d.groupby("fq"):
        for h in H:
            res[f"fq{k}_h{h}"] = ct(g[f"u{h}"], g["day"])
    out["by_forecast_tercile"] = pd.DataFrame(res).T
    out["share_positive_u5"] = float((d["u5"] > 0).mean())
    out["median_u5"] = float(d["u5"].median())
    return out
