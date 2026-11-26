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
            f = df["forecast"].astype(float)
            for h in (7, 14, 28):
                fwd = c.shift(-h) / c - 1
                for i in range(0, len(df), h):
                    if pd.isna(fwd.iloc[i]):
                        continue
                    rows.append(dict(coin=coin, w=w, h=h, inprof=df["regime"].iloc[i] == "unknown",
                                     mult=mult.iloc[i], fc=f.iloc[i], fwd=fwd.iloc[i],
                                     core=coin in ("BTCUSD","ETHUSD","LTCUSD","XMRUSD","XRPUSD","ZECUSD"),
                                     year=pd.Timestamp(df["timestamp"].iloc[i]).year))
    d = pd.DataFrame(rows)
    d["cm"] = d.groupby(["coin", "h"])["fwd"].transform("mean")
    d["ex"] = d["fwd"] - d["cm"]
    out = {}
    def reg(g, x):
        g = g[g[x].notna()]
        if len(g) < 8:
            return pd.Series(dict(n=len(g)))
        s = stats.linregress(g[x], g["ex"])
        return pd.Series(dict(n=len(g), slope=s.slope, t=s.slope / s.stderr,
                              corr=s.rvalue, mean_ex=g["ex"].mean()))
    nz = d[d["fc"] != 0]
    out["step5-like: ex on forecast, nonzero fc"] = nz.groupby("h").apply(lambda g: reg(g, "fc"))
    out["ex on raw mult, nonzero fc"] = nz.groupby("h").apply(lambda g: reg(g, "mult"))
    out["corr forecast vs raw mult (nonzero fc)"] = nz[["fc", "mult"]].corr().iloc[0, 1]
    out["share fc sign == sign(mult-1)"] = float((np.sign(nz["fc"]) == np.sign(nz["mult"] - 1)).mean())
    out["nonzero fc not in profile share"] = float((~nz["inprof"]).mean())
    p = d[d.inprof]
    out["in profile, core vs other, raw mult"] = p.groupby(["h", "core"]).apply(lambda g: reg(g, "mult"))
    # rises only, total move per bucket (fwd, not demeaned) and ex for rise strength
    pr = p[p["mult"] > 0].copy()
    pr["q"] = pd.cut(pr["mult"], [0, 0.5, 1, 1.5, 2.5, 99])
    def desc(g):
        n = len(g)
        t = g["ex"].mean() / (g["ex"].std() / np.sqrt(n)) if n > 2 else np.nan
        return pd.Series(dict(n=n, mean_ex=g["ex"].mean(), t=t, mean_fwd=g["fwd"].mean()))
    out["rises, by strength, per horizon"] = pr.groupby(["h", "q"]).apply(desc)
    out["in profile by year 14d raw mult"] = p[p.h == 14].groupby("year").apply(lambda g: reg(g, "mult"))
    out["in profile by year 7d raw mult"] = p[p.h == 7].groupby("year").apply(lambda g: reg(g, "mult"))
    return out
