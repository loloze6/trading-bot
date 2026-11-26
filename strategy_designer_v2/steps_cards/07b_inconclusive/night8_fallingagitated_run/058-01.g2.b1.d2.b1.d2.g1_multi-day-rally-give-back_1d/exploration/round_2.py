import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]
    out = {}
    def tday(x, days):
        s = pd.Series(x).reset_index(drop=True); d = pd.Series(days).reset_index(drop=True)
        ok = s.notna(); s = s[ok]; d = d[ok]
        m = s.mean(); dev = (s - m).groupby(d).sum(); D = len(dev)
        se = np.sqrt((dev**2).sum() * D/(D-1)) / len(s) if D > 1 else np.nan
        return m, (m/se if se else np.nan), len(s), D
    res = {}; half = {}; yr = {}
    for h in [1, 2, 3, 4]:
        rows = []; allr = []
        for coin, wins in bars.items():
            for w, b in wins.items():
                b = b.reset_index(drop=True)
                c = b["close"].astype(float).values; n = len(c)
                fc = b["forecast"].astype(float).values
                ts = pd.to_datetime(b["timestamp"])
                for i in range(0, n - h, h):
                    allr.append((coin, c[i+h]/c[i]-1))
                    if fc[i] < 0:
                        rows.append((coin, w, ts.iloc[i].year, ts.iloc[i].normalize(), abs(fc[i]), c[i+h]/c[i]-1))
        a = pd.DataFrame(allr, columns=["coin","r"]); dr = a.groupby("coin")["r"].mean()
        df = pd.DataFrame(rows, columns=["coin","win","year","day","afc","r"])
        df["u"] = -(df["r"] - df["coin"].map(dr)); df["tot"] = -df["r"]
        res[h] = tday(df["u"], df["day"]) + (df["tot"].mean(),)
        med = df["afc"].median()
        hi = df[df["afc"] > med]; lo = df[df["afc"] <= med]
        th = tday(hi["u"], hi["day"]); tl = tday(lo["u"], lo["day"])
        half[h] = [th[0], th[1], th[2], tl[0], tl[1], tl[2]]
        if h == 1:
            yr = df.groupby("year")["u"].agg(["mean","count"])
            out["h1 by coin"] = df.groupby("coin")["u"].agg(["mean","count"])
            df["q"] = pd.qcut(df["afc"].rank(method="first"), 4, labels=["q1","q2","q3","q4"])
            out["h1 by |fc| quartile"] = df.groupby("q")["u"].agg(["mean","count"])
            out["h1 by year"] = yr
            out["h1 by window"] = df.groupby("win")["u"].agg(["mean","count"])
    out["horizon grid h: mean u, t, n, days, total"] = pd.DataFrame(res, index=["mean","t","n","days","total"]).T
    out["upper vs lower half by h"] = pd.DataFrame(half, index=["hi mean","hi t","hi n","lo mean","lo t","lo n"]).T
    return out
