def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = pd.Series(df["close"].values.astype(float))
            n = len(c)
            r7 = c.pct_change(7).values
            r30 = c.pct_change(30).values
            r60 = c.pct_change(60).values
            d1 = c.pct_change()
            vr = (d1.rolling(10).std() / d1.rolling(30).std()).values
            z30 = ((c.pct_change(30) - c.pct_change(30).rolling(60).mean()) / c.pct_change(30).rolling(60).std()).values
            fc = df["forecast"].values
            for h in (3, 5, 7, 10):
                for i in range(0, n - h, h):
                    rows.append(dict(coin=coin, w=w, h=h, ts=df["timestamp"].iloc[i], ret=c[i+h]/c[i]-1,
                                     fc=fc[i], reg=df["regime"].iloc[i], r7=r7[i], r30=r30[i], r60=r60[i], vr=vr[i], z=z30[i]))
    g = pd.DataFrame(rows)
    g["mu"] = g.groupby(["coin","h"])["ret"].transform("mean")
    g["ex"] = g["ret"] - g["mu"]
    g["day"] = pd.to_datetime(g["ts"]).dt.floor("D")
    g["year"] = pd.to_datetime(g["ts"]).dt.year
    def summ(d):
        if len(d) < 5: return pd.Series(dict(n=len(d)))
        def tcl(x):
            s = (x - x.mean()).groupby(d["day"]).sum(); G = len(s)
            se = np.sqrt((s**2).sum() * G/(G-1)) / len(x)
            return x.mean()/se if se > 0 else np.nan
        return pd.Series(dict(n=len(d), days=d["day"].nunique(), raw_short=-d["ret"].mean(), ex_short=-d["ex"].mean(),
                              t_raw_cl=tcl(-d["ret"]), t_ex_cl=tcl(-d["ex"])))
    out = {}
    chop = g[g.reg=="unknown"]
    sig = chop[chop.fc < 0].copy()
    nos = chop[chop.fc == 0]
    # deep part of signal, by h
    sig["deep"] = sig["fc"] <= sig.groupby("h")["fc"].transform(lambda x: x.quantile(1/3))
    out["signal deep third by h"] = sig[sig.deep].groupby("h").apply(summ)
    out["signal by h (clustered)"] = sig.groupby("h").apply(summ)
    # vol rising condition: with signal vs without
    out["vol rising, signal, by h"] = sig[sig.vr > 1].groupby("h").apply(summ)
    out["vol rising, no signal, by h"] = nos[nos.vr > 1].groupby("h").apply(summ)
    out["r7 down & deep, by h"] = sig[(sig.r7 <= 0) & sig.deep].groupby("h").apply(summ)
    # r30 < 0 in falling / rising markets (outside choppy), raw short
    oth = g[g.reg != "unknown"].copy()
    oth["tr"] = np.where(oth.r60 < -0.10, "falling", np.where(oth.r60 > 0.10, "rising", "x"))
    oth = oth[oth.r30 < 0]
    out["r30<0 outside choppy, h5, by trend"] = oth[oth.h==5].groupby("tr").apply(summ)
    out["signal h5 by year"] = sig[sig.h==5].groupby("year").apply(summ)
    out["signal h5 by window"] = sig[sig.h==5].groupby("w").apply(summ)[["n","raw_short","ex_short"]]
    # trades by entry forecast depth and duration
    tr = []
    for coin, wins in data["trades"].items():
        for w, df in wins.items():
            if len(df): tr.append(df.assign(w=w, coin=coin))
    tr = pd.concat(tr)
    tr["dur_d"] = tr["duration_minutes"]/1440
    tr["fq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 3, labels=["deep","mid","shallow"])
    out["trades by entry forecast tercile"] = tr.groupby("fq").agg(n=("dur_d","size"), fc=("entry_forecast","mean"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur=("dur_d","mean"))
    tr["db"] = pd.cut(tr["dur_d"], [0, 3.5, 6, 15, 1000])
    out["trades by duration"] = tr.groupby("db").agg(n=("dur_d","size"), gross=("profit_loss_percent","mean"),
        net=("net_profit_loss_percent","mean"))
    out["trades exit forecast zero share"] = float((tr["exit_forecast"] == 0).mean())
    # turnover: bars with allocation change in position
    ac = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            a = df["postRebalance_current_allocation"].fillna(0); p = df["previous_allocation"].fillna(0)
            ac.append(pd.DataFrame(dict(inpos=(a != 0), chg=(a - p).abs())))
    ac = pd.concat(ac)
    out["mean abs alloc change on bars in position"] = float(ac[ac.inpos]["chg"].mean())
    out["share of in-position bars with a rebalance"] = float((ac[ac.inpos]["chg"] > 1e-6).mean())
    return out
