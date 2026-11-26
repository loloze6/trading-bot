def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            for h in [1, 3, 5, 10, 20]:
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, i=i,
                        day=str(df["timestamp"].iloc[i])[:10],
                        year=str(df["timestamp"].iloc[i])[:4],
                        ret=c[i+h]/c[i]-1,
                        fc=df["forecast"].iloc[i],
                        reg=df["regime"].iloc[i],
                        raw=df.get("debug_info.components.quiet_fall.last_history_value", pd.Series([np.nan]*n)).iloc[i],
                        r30=(c[i]/c[i-30]-1) if i >= 30 else np.nan))
    R = pd.DataFrame(rows)
    R["drift"] = R.groupby(["coin", "h"])["ret"].transform("mean")
    R["short_unusual"] = -(R["ret"] - R["drift"])  # gain of a short beyond drift
    R["short_total"] = -R["ret"]
    def tday(s, d):
        g = pd.DataFrame({"v": s.values, "d": d.values}).groupby("d")["v"].sum()
        n = len(s)
        if len(g) < 3: return np.nan
        return s.mean() / (g.std(ddof=1) * np.sqrt(len(g)) / n)
    out = {}
    sig = R[R.fc < 0]
    # by horizon
    hz = []
    for h, g in sig.groupby("h"):
        hz.append(dict(h=h, n=len(g), days=g.day.nunique(), unusual=g.short_unusual.mean(), t=tday(g.short_unusual, g.day), total=g.short_total.mean()))
    out["signal by horizon (short gain)"] = pd.DataFrame(hz)
    # other falling-calm-passed bars with forecast 0 (regime unknown)
    oth = R[(R.fc == 0) & (R.reg == "unknown")]
    hz = []
    for h, g in oth.groupby("h"):
        hz.append(dict(h=h, n=len(g), unusual=g.short_unusual.mean(), t=tday(g.short_unusual, g.day)))
    out["profile bars with no signal (short gain)"] = pd.DataFrame(hz)
    s5 = sig[sig.h == 5].copy()
    def summ(g):
        return pd.Series(dict(n=len(g), unusual=g.short_unusual.mean(), t=tday(g.short_unusual, g.day) if len(g) > 3 else np.nan))
    out["h5 by coin"] = s5.groupby("coin").apply(summ)
    out["h5 by window"] = s5.groupby("w").apply(summ)
    out["h5 by year"] = s5.groupby("year").apply(summ)
    s5["fq"] = pd.qcut(-s5.fc, 4, labels=False, duplicates="drop")
    out["h5 by |forecast| quartile"] = s5.groupby("fq").apply(summ)
    s5["rq"] = pd.qcut(s5.r30, 4, labels=False, duplicates="drop")
    out["h5 by 30d return quartile (0=deepest)"] = s5.groupby("rq").apply(summ)
    s5["vr"] = s5.raw / s5.r30.replace(0, np.nan)  # proxy for volume ratio * scale
    s5["vq"] = pd.qcut(s5.vr, 4, labels=False, duplicates="drop")
    out["h5 by raw/r30 quartile (volume lightness proxy, 3=lightest)"] = s5.groupby("vq").apply(summ)
    s10 = sig[sig.h == 10].copy()
    s10["fq"] = pd.qcut(-s10.fc, 4, labels=False, duplicates="drop")
    out["h10 by |forecast| quartile"] = s10.groupby("fq").apply(summ)
    return out
