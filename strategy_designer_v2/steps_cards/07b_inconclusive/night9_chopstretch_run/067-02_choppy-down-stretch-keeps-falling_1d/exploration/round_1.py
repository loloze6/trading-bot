def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].astype(float)
            r = c.pct_change()
            sma = c.rolling(20).mean()
            sd = r.rolling(20).std()
            raw = (c / sma - 1) / sd
            rec = b.get("debug_info.components.stretch_below.last_history_value")
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (3, 5, 10, 20):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], fc=b["forecast"][i],
                                     reg=b["regime"][i], raw=raw[i],
                                     rec=(rec[i] if rec is not None else np.nan),
                                     fwd=fwd[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    ch = d[d.reg == "unknown"].copy()

    def reg(x, col):
        x = x.dropna(subset=[col, "un"])
        if len(x) < 10:
            return pd.Series(dict(n=len(x)))
        s = stats.linregress(x[col], x["un"])
        return pd.Series(dict(n=len(x), slope=s.slope, t=s.slope / s.stderr,
                              mean_un=x.un.mean(), mean_fwd=x.fwd.mean()))

    out = {}
    out["choppy, by horizon and side of the raw stretch"] = ch.assign(
        side=np.where(ch.raw < 0, "below", "above")
    ).groupby(["h", "side"]).apply(lambda x: reg(x, "raw"))
    out["choppy, both sides pooled, raw stretch"] = ch.groupby("h").apply(lambda x: reg(x, "raw"))
    out["all bars, by horizon, raw stretch"] = d.groupby("h").apply(lambda x: reg(x, "raw"))
    s10 = ch[(ch.h == 10) & (ch.fc < 0)].copy()
    s10["mag"] = -s10.fc
    out["h10 short cases: forecast slope"] = reg(s10, "mag").to_frame().T
    out["h10 short cases: raw stretch slope"] = reg(s10, "raw").to_frame().T
    out["h10 short cases, by coin"] = s10.groupby("coin").apply(lambda x: reg(x, "mag"))
    out["h10 short cases, by year"] = s10.groupby("yr").apply(lambda x: reg(x, "mag"))
    s10["q"] = pd.qcut(s10.raw, 4, labels=False, duplicates="drop")
    out["h10 short cases, by raw-stretch quartile"] = s10.groupby("q").agg(
        n=("un", "size"), raw=("raw", "mean"), un=("un", "mean"), fwd=("fwd", "mean"))
    c10 = ch[ch.h == 10].copy()
    c10["q"] = pd.qcut(c10.raw, 5, labels=False, duplicates="drop")
    out["choppy h10, all cases by raw-stretch quintile"] = c10.groupby("q").agg(
        n=("un", "size"), raw=("raw", "mean"), un=("un", "mean"), fwd=("fwd", "mean"))
    out["corr forecast vs raw stretch"] = float(s10[["fc", "raw"]].corr().iloc[0, 1])
    return out
