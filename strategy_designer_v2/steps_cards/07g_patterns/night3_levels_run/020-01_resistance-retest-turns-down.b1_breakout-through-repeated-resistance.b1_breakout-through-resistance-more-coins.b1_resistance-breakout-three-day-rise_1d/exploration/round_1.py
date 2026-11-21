def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    def nonover(df, h):
        c = df["close"].values
        idx = np.arange(0, len(c)-h, h)
        return idx, c[idx+h]/c[idx]-1
    # coin drift and usual move per horizon
    H = [1,3,5,10,20]
    drift = {}; usual = {}
    for coin, ws in bars.items():
        for h in H:
            r = np.concatenate([nonover(df,h)[1] for df in ws.values()] or [np.array([])])
            drift[(coin,h)] = np.nanmean(r) if len(r) else np.nan
            usual[(coin,h)] = np.nanstd(r) if len(r) else np.nan
    # 1. break cases: horizon profile (fresh rise of forecast from 0)
    rows = []
    for coin, ws in bars.items():
        for w, df in ws.items():
            f = df["forecast"].fillna(0).values; c = df["close"].values
            n = len(c)
            for i in range(1, n):
                if f[i] >= 2 and f[i-1] < 2:
                    d = {"coin": coin, "f": f[i], "cell3": i//3}
                    for h in H:
                        if i+h < n:
                            ex = c[i+h]/c[i]-1 - drift[(coin,h)]
                            d[f"ex{h}"] = ex; d[f"s{h}"] = ex/usual[(coin,h)]
                    d["pre1"] = c[i]/c[i-1]-1 - drift[(coin,1)]
                    rows.append(d)
    cs = pd.DataFrame(rows)
    prof = []
    for h in H:
        x = cs[f"ex{h}"].dropna(); s = cs[f"s{h}"].dropna()
        prof.append({"h_days": h, "n": len(x), "mean_ex": x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))), "strength": s.mean()})
    out["break_horizon_profile"] = pd.DataFrame(prof)
    out["break_signal_day_excess_mean"] = cs["pre1"].mean()
    cs["fq"] = pd.qcut(cs["f"].rank(method="first"), 5, labels=False)
    out["break_by_forecast_quintile"] = cs.groupby("fq").agg(n=("ex3","count"), f=("f","mean"), ex3=("ex3","mean"), ex10=("ex10","mean"), s10=("s10","mean"))
    # 2. bars: past-move vs future (non-overlapping grid of h), strength units
    def grid_cond(h_past, h_fut, name):
        rr = []
        for coin, ws in bars.items():
            for w, df in ws.items():
                c = df["close"].values; n = len(c)
                hi = pd.Series(c).rolling(20, min_periods=20).max().values
                lr = np.log(c[1:]/c[:-1]); vol = pd.Series(np.r_[np.nan, lr]).rolling(20).std().values
                vol60 = pd.Series(np.r_[np.nan, lr]).rolling(60, min_periods=40).std().values
                for i in range(0, n-h_fut, h_fut):
                    if i-h_past < 0: continue
                    past = (c[i]/c[i-h_past]-1)/usual.get((coin,h_past) if (coin,h_past) in usual else (coin,20))
                    fut = c[i+h_fut]/c[i]-1 - drift[(coin,h_fut)]
                    rr.append({"coin": coin, "past": past, "fut": fut, "sfut": fut/usual[(coin,h_fut)],
                               "dist": c[i]/hi[i]-1 if not np.isnan(hi[i]) else np.nan,
                               "vr": vol[i]/vol60[i] if vol60[i]==vol60[i] and vol60[i]>0 else np.nan,
                               "wd": pd.Timestamp(df["timestamp"].iloc[i]).weekday(),
                               "year": pd.Timestamp(df["timestamp"].iloc[i]).year})
        return pd.DataFrame(rr)
    def tab(g, key, q=5):
        g = g.dropna(subset=[key]).copy()
        g["b"] = g.groupby("coin")[key].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        a = g.groupby("b").agg(n=("fut","count"), key=(key,"mean"), fut=("fut","mean"), sfut=("sfut","mean"), sd=("fut","std"))
        a["t"] = a["fut"]/(a["sd"]/np.sqrt(a["n"]))
        return a.drop(columns="sd")
    g1 = grid_cond(1, 1, "1d")
    out["past1d_next1d"] = tab(g1, "past")
    g3 = grid_cond(3, 3, "3d")
    out["past3d_next3d"] = tab(g3, "past")
    out["dist20high_next3d"] = tab(g3, "dist")
    out["volratio_next3d"] = tab(g3, "vr")
    g5 = grid_cond(20, 5, "20d")
    out["past20d_next5d"] = tab(g5, "past")
    out["dist20high_next5d"] = tab(g5, "dist")
    wd = g1.groupby("wd").agg(n=("fut","count"), fut=("fut","mean"), sd=("fut","std")); wd["t"]=wd["fut"]/(wd["sd"]/np.sqrt(wd["n"]))
    out["weekday_next1d"] = wd.drop(columns="sd")
    # 3. book: by year, gain on in vs out days
    dd = []
    for coin, ws in data["days"].items():
        for w, df in ws.items():
            x = df[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["w"]=w; dd.append(x)
    dd = pd.concat(dd).dropna()
    dd["year"] = pd.to_datetime(dd["day"]).dt.year
    daily = dd.groupby("day").agg(book=("book_return","mean"), hold=("coin_return","mean"))
    daily["year"] = pd.to_datetime(daily.index).year
    yy = daily.groupby("year").agg(n=("book","count"), book=("book","mean"), hold=("hold","mean"), bsd=("book","std"), hsd=("hold","std"))
    yy["book_sharpe"] = yy["book"]/yy["bsd"]*np.sqrt(365); yy["hold_sharpe"]=yy["hold"]/yy["hsd"]*np.sqrt(365)
    out["book_by_year"] = yy.drop(columns=["bsd","hsd"])
    # 4. trades
    tr = []
    for coin, ws in data["trades"].items():
        for w, df in ws.items():
            if len(df): x = df.copy(); x["coin"]=coin; tr.append(x)
    tr = pd.concat(tr)
    tr["dd"] = tr["duration_minutes"]/1440
    tr["db"] = pd.cut(tr["dd"], [0,1.5,3.5,6.5,10.5,1e9])
    out["trades_by_duration"] = tr.groupby("db").agg(n=("net_profit_loss_percent","count"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    tr["eq"] = pd.qcut(tr["entry_forecast"].rank(method="first"), 5, labels=False)
    out["trades_by_entry_forecast"] = tr.groupby("eq").agg(n=("net_profit_loss_percent","count"), f=("entry_forecast","mean"), gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"), dur=("dd","mean"))
    return out
