def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values; n = len(df); h = 5
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, day=str(df["timestamp"].iloc[i])[:10],
                    year=str(df["timestamp"].iloc[i])[:4], ret=c[i+h]/c[i]-1,
                    fc=df["forecast"].iloc[i], reg=df["regime"].iloc[i],
                    r30=(c[i]/c[i-30]-1) if i >= 30 else np.nan,
                    r60=(c[i]/c[i-60]-1) if i >= 60 else np.nan))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby("coin")["ret"].transform("mean")
    R["dev"] = R["ret"] - R["drift"]
    def tday(s, d):
        g = pd.DataFrame({"v": s.values, "d": d.values}).groupby("d")["v"].sum()
        if len(g) < 3: return np.nan
        return s.mean() / (g.std(ddof=1) * np.sqrt(len(g)) / len(s))
    def summ(g, col="dev"):
        return pd.Series(dict(n=len(g), days=g.day.nunique(), mean=g[col].mean(), t=tday(g[col], g.day)))
    out = {}
    s = R[R.fc < 0].copy()
    s["main"] = s.dev * (-s.fc / 10)
    out["main measure recomputed (dev x -fc/10), and plain dev"] = pd.DataFrame(
        [summ(s, "main"), summ(s, "dev")], index=["weighted", "plain"])
    out["corr(fc, dev) in signal cases"] = float(np.corrcoef(s.fc, s.dev)[0, 1])
    s["side"] = np.where(s.year.isin(["2018", "2019"]), "2018-19", "2020-21")
    out["main by year group"] = s.groupby("side").apply(lambda g: summ(g, "main"))
    # momentum of the 30-day return, by regime (unknown = falling calm passed)
    a = R.dropna(subset=["r30"]).copy()
    a["fall"] = a.r30 < 0
    out["dev by regime x 30d fall"] = a.groupby(["reg", "fall"]).apply(summ)
    # falling (60d < -10%) but outside the profile = agitated falls
    b = a.dropna(subset=["r60"])
    b = b[(b.r60 < -0.10) & (b.r30 < 0)]
    out["falling, 30d fall, by regime (chop=agitated here)"] = b.groupby("reg").apply(summ)
    b = b.copy()
    b["q"] = pd.qcut(b.r30, 3, labels=False, duplicates="drop")
    out["falling & 30d fall: dev by 30d return tercile (0 deepest)"] = b.groupby(["reg", "q"]).apply(summ)
    return out
