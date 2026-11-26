def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    col = "debug_info.components.week_multiple.last_history_value"
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float)
            r7 = c / c.shift(7) - 1
            base = r7.abs().rolling(30).mean()
            mult = r7 / base
            if col in df:
                m = df[col].astype(float)
                mult = m.where(m.notna(), mult - 1) + 1
            for h in (7, 14, 28):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if pd.isna(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, inprof=df["regime"].iloc[i] == "unknown",
                                     mult=mult.iloc[i], fwd=fwd.iloc[i],
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    out = {}
    # coin mean per horizon over all bars
    d["cm"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["cm"]
    p = d[d.inprof & d["mult"].notna()]
    def reg(g):
        if len(g) < 10:
            return pd.Series(dict(n=len(g)))
        s = stats.linregress(g["mult"], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              mean_ex=g["ex"].mean(), mean_fwd=g["fwd"].mean()))
    out["slope by horizon (in profile)"] = p.groupby("h").apply(reg)
    out["slope by horizon (all bars)"] = d[d["mult"].notna()].groupby("h").apply(reg)
    p28 = p[p.h == 28].copy()
    p28["bucket"] = pd.cut(p28["mult"], [-99, -1, 0, 1, 2, 99])
    def desc(g):
        t = g["ex"].mean() / (g["ex"].std() / np.sqrt(len(g))) if len(g) > 2 else np.nan
        return pd.Series(dict(n=len(g), mean_ex=g["ex"].mean(), t=t, mean_fwd=g["fwd"].mean()))
    out["28d by multiple bucket"] = p28.groupby("bucket").apply(desc)
    for h in (7, 14):
        ph = p[p.h == h].copy()
        ph["bucket"] = pd.cut(ph["mult"], [-99, -1, 0, 1, 2, 99])
        out[f"{h}d by multiple bucket"] = ph.groupby("bucket").apply(desc)
    out["28d by year"] = p28.groupby("year").apply(reg)
    out["28d by coin"] = p28.groupby("coin").apply(reg)
    out["28d rises only (mult>0)"] = reg(p28[p28["mult"] > 0])
    out["28d falls only (mult<0)"] = reg(p28[p28["mult"] < 0])
    out["7d rises only"] = reg(p[(p.h == 7) & (p["mult"] > 0)])
    out["14d rises only"] = reg(p[(p.h == 14) & (p["mult"] > 0)])
    out["share in profile"] = d[d.h == 28]["inprof"].mean()
    return out
