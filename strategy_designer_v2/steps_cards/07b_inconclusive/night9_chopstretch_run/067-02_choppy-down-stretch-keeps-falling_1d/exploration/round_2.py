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
            stdz = (raw - raw.rolling(60, min_periods=20).mean()) / raw.rolling(60, min_periods=20).std()
            sd30 = r.rolling(30).std()
            yr = pd.to_datetime(b["timestamp"]).dt.year
            for h in (5, 10):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(b) - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, yr=yr[i], fc=b["forecast"][i],
                                     reg=b["regime"][i], raw=raw[i], stdz=stdz[i],
                                     sd30=sd30[i], fwd=fwd[i]))
    d = pd.DataFrame(rows)
    d["drift"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["un"] = d["fwd"] - d["drift"]
    d["agit"] = d.groupby("coin")["sd30"].transform(lambda s: s > s.median())
    ch = d[d.reg == "unknown"].copy()

    def reg(x, col):
        x = x.dropna(subset=[col, "un"])
        if len(x) < 8:
            return pd.Series(dict(n=len(x)))
        s = stats.linregress(x[col], x["un"])
        sp = stats.spearmanr(x[col], x["un"])
        return pd.Series(dict(n=len(x), slope=s.slope, t=s.slope / s.stderr,
                              rho=sp.correlation, mean_un=x.un.mean()))

    out = {}
    for h in (5, 10):
        b = ch[(ch.h == h) & (ch.raw < 0)]
        out[f"h{h} choppy below: raw vs standardised stretch"] = pd.DataFrame(
            {"raw": reg(b, "raw"), "stdz": reg(b, "stdz")}).T
        out[f"h{h} choppy below raw, by year"] = b.groupby("yr").apply(lambda x: reg(x, "raw"))
        out[f"h{h} choppy below raw, by agitation"] = b.groupby("agit").apply(lambda x: reg(x, "raw"))
        out[f"h{h} choppy below raw, by coin"] = b.groupby("coin").apply(lambda x: reg(x, "raw"))
        bw = b[(b.un.abs() < b.un.abs().quantile(0.95))]
        out[f"h{h} choppy below raw, top 5% |move| removed"] = reg(bw, "raw").to_frame().T
        ab = ch[(ch.h == h) & (ch.raw > 0)]
        out[f"h{h} choppy above raw, by agitation"] = ab.groupby("agit").apply(lambda x: reg(x, "raw"))
        allb = d[(d.h == h) & (d.raw < 0)]
        out[f"h{h} all profiles below raw"] = reg(allb, "raw").to_frame().T
    s10 = ch[(ch.h == 10) & (ch.fc < 0)]
    out["h10 short cases: corr stdz vs raw, fc vs stdz"] = pd.Series(
        dict(raw_stdz=s10[["raw", "stdz"]].corr().iloc[0, 1], fc_stdz=s10[["fc", "stdz"]].corr().iloc[0, 1]))
    return out
