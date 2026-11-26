def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    drift = {}
    for coin, ws in bars.items():
        rr = []
        for w, df in ws.items():
            c = df["close"].values
            for i in range(0, len(c) - 14, 14):
                rr.append(c[i + 14] / c[i] - 1)
        drift[coin] = np.mean(rr) if rr else np.nan
        for w, df in ws.items():
            c = df["close"].values
            f = df["forecast"].fillna(0).values
            n = len(c)
            for g in range(0, n, 14):
                idx = [i for i in range(g, min(g + 14, n)) if f[i] >= 2]
                if not idx:
                    continue
                i = idx[0]
                if i + 14 >= n:
                    continue
                r = {"coin": coin, "win": w, "fc": f[i],
                     "u14": c[i + 14] / c[i] - 1 - drift[coin],
                     "r7": c[i] / c[i - 7] - 1 if i >= 7 else np.nan,
                     "r30": c[i] / c[i - 30] - 1 if i >= 30 else np.nan,
                     "r60": c[i] / c[i - 60] - 1 if i >= 60 else np.nan,
                     "hi30": c[i] / c[max(0, i - 30):i + 1].max() if i >= 30 else np.nan}
                # window's own 14-bar grid return of the coin, for the market's drowning
                rows.append(r)
    d = pd.DataFrame(rows)
    def summ(g):
        x = g["u14"].dropna()
        if len(x) < 3:
            return pd.Series({"n": len(x), "mean": x.mean(), "t": np.nan})
        return pd.Series({"n": len(x), "mean": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out = {}
    for col in ["r7", "r30", "r60", "hi30"]:
        x = d.dropna(subset=[col])
        try:
            x = x.assign(q=pd.qcut(x[col], 3, labels=["low", "mid", "high"]))
            out[f"by_{col}_tercile"] = x.groupby("q").apply(summ)
        except Exception as e:
            out[f"by_{col}_tercile"] = str(e)
    x = d.dropna(subset=["r60"])
    out["by_r60_sign"] = x.assign(s=np.where(x["r60"] > 0, "r60>0", "r60<=0")).groupby("s").apply(summ)
    out["by_at_30d_high"] = d.dropna(subset=["hi30"]).assign(s=lambda z: np.where(z["hi30"] >= 0.999, "at_high", "below")).groupby("s").apply(summ)
    out["core6_vs_other"] = d.assign(s=d["coin"].isin(["BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"]).map({True:"core", False:"other"})).groupby("s").apply(summ)
    return out
