def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]
    H = 336
    # --- grid cells at 336 bars, with 30d return, 7d return, 30d vol, forecast
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            n = len(c)
            lr = np.log(c)
            r1 = np.diff(lr, prepend=np.nan)
            vol30 = pd.Series(r1).rolling(720, min_periods=300).std().values
            f = df["forecast"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, n - H, H):
                r30 = c[i]/c[i-720]-1 if i >= 720 else np.nan
                r7 = c[i]/c[i-168]-1 if i >= 168 else np.nan
                r1d = c[i]/c[i-24]-1 if i >= 24 else np.nan
                rows.append(dict(coin=coin, w=w, year=ts.iloc[i].year, fc=f[i], r30=r30, r7=r7, r1d=r1d,
                                 vol=vol30[i], f336=c[i+H]/c[i]-1, f168=c[i+168]/c[i]-1, f72=c[i+72]/c[i]-1))
    g = pd.DataFrame(rows)
    for col in ["f336", "f168", "f72"]:
        g[col+"x"] = g[col] - g.groupby("coin")[col].transform("mean")
    def summ(grp, col):
        a = grp.agg(n=(col, "size"), mean=(col, "mean"), sd=(col, "std"))
        a["t"] = a["mean"]/(a["sd"]/np.sqrt(a["n"]))
        return a.drop(columns="sd").round(4)
    g["fc_b"] = pd.cut(g["fc"], [-1, 0, 0.5, 1, 1.5, 2.5, 25], labels=["0", "0-.5", ".5-1", "1-1.5", "1.5-2.5", ">2.5"])
    out["f336x by forecast bucket"] = summ(g.groupby("fc_b"), "f336x")
    g["r30q"] = g.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["f336x by r30 quintile (per coin)"] = summ(g.groupby("r30q"), "f336x")
    out["f168x by r30 quintile"] = summ(g.groupby("r30q"), "f168x")
    g["r7q"] = g.groupby("coin")["r7"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["f336x by r7 quintile"] = summ(g.groupby("r7q"), "f336x")
    g["volq"] = g.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 3, labels=False, duplicates="drop"))
    out["f336x by vol tercile"] = summ(g.groupby("volq"), "f336x")
    out["f336x r30q x volq"] = g.groupby(["volq", "r30q"])["f336x"].mean().unstack().round(4)
    out["f336x by year, fc>0 vs 0"] = g.assign(pos=g.fc > 0).groupby(["year", "pos"])["f336x"].mean().unstack().round(4)
    out["f336x by coin, fc>0"] = summ(g[g.fc > 0].groupby("coin"), "f336x")
    # --- daily-scale: large 1-day moves, next 3 days (72-bar grid)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            ts = pd.to_datetime(df["timestamp"])
            hr = ts.dt.hour.values; wd = ts.dt.weekday.values
            r = c[1:]/c[:-1]-1
            for i in range(0, len(c)-1):
                pass
            # hourly returns by hour/weekday
            rows.append(pd.DataFrame(dict(coin=coin, hr=hr[:-1], wd=wd[:-1], r=r)))
    hb = pd.concat(rows)
    hb["rx"] = hb["r"] - hb.groupby("coin")["r"].transform("mean")
    a = hb.groupby("hr")["rx"].agg(["mean", "std", "size"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["size"]))
    out["hourly excess ret by hour (bps), t"] = pd.DataFrame({"bps": a["mean"]*1e4, "t": a["t"]}).round(2)
    a = hb.groupby("wd")["rx"].agg(["mean", "std", "size"]); a["t"] = a["mean"]/(a["std"]/np.sqrt(a["size"]))
    out["hourly excess ret by weekday (bps), t"] = pd.DataFrame({"bps": a["mean"]*1e4, "t": a["t"]}).round(2)
    # --- 72-bar grid: 1-day return z-score vs next 3 days
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            c = df["close"].values.astype(float)
            r24 = pd.Series(c).pct_change(24)
            sd = r24.rolling(720, min_periods=300).std()
            for i in range(720, len(c)-72, 72):
                rows.append(dict(coin=coin, z=r24.iloc[i]/sd.iloc[i], f72=c[i+72]/c[i]-1))
    d = pd.DataFrame(rows).dropna()
    d["f72x"] = d["f72"] - d.groupby("coin")["f72"].transform("mean")
    d["zb"] = pd.cut(d["z"], [-99, -2, -1, 0, 1, 2, 99])
    out["f72x by 1-day move z"] = summ(d.groupby("zb"), "f72x")
    # --- book
    dd = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            x = df[["day", "book_return", "coin_return"]].copy(); x["coin"] = coin; x["w"] = w; dd.append(x)
    dd = pd.concat(dd)
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    by = dd.groupby("year")[["book_return", "coin_return"]].mean()*1e4
    out["daily bps book vs coin by year"] = by.round(2)
    # trades
    tr = pd.concat([t.assign(coin=c) for c, ws in data["trades"].items() for t in ws.values()])
    tr["efb"] = pd.qcut(tr["entry_forecast"], 4, duplicates="drop")
    out["trades by entry forecast q"] = tr.groupby("efb")["net_profit_loss_percent"].agg(["size", "mean", "median"]).round(3)
    tr["dur_d"] = tr["duration_minutes"]/1440
    out["trades duration days"] = tr["dur_d"].describe().round(2)
    return out
