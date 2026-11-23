def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []; hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.set_index("timestamp").sort_index()
            r1 = b["close"].pct_change()
            vol = r1.rolling(720, min_periods=240).std()
            hh = pd.DataFrame({"r": r1, "hr": b.index.hour, "year": b.index.year, "coin": coin})
            hourly.append(hh.dropna())
            d = b[b.index.hour == 23].copy()
            d["vol"] = vol.reindex(d.index) * np.sqrt(24)
            d.index = d.index.floor("D")
            full = pd.date_range(d.index.min(), d.index.max(), freq="D", tz="UTC")
            d = d.reindex(full)
            c = d["close"]
            dd = pd.DataFrame(index=full)
            dd["r_today"] = c / c.shift(1) - 1
            dd["r_yday"] = c.shift(1) / c.shift(2) - 1
            dd["r_2d"] = c / c.shift(2) - 1
            dd["f48"] = c.shift(-2) / c - 1
            dd["vol"] = d["vol"]
            dd["wd"] = full.weekday
            dd["coin"] = coin; dd["year"] = full.year
            rows.append(dd)
    D = pd.concat(rows).dropna(subset=["r_today","r_yday","f48","vol"])
    m48 = D.groupby("coin")["f48"].apply(lambda s: s.iloc[::2].mean())
    D["x48"] = D["f48"] - D["coin"].map(m48)
    for k in ["r_today","r_yday","r_2d"]:
        D["z_"+k] = (D[k] / D["vol"]).clip(-6, 6)
    def reg(s, x, y="x48"):
        s = s.dropna(subset=[x, y])
        if len(s) < 30: return (np.nan, np.nan, len(s))
        lr = stats.linregress(s[x], s[y]); return (lr.slope, lr.slope/lr.stderr, len(s))
    names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    # row at day wd: today's return, yesterday's return, 2-day return -> next 48h
    tab = []
    for wd in range(7):
        s = D[D.wd == wd]
        a = reg(s, "z_r_today"); b_ = reg(s, "z_r_yday"); c_ = reg(s, "z_r_2d")
        tab.append({"close_day": names[wd], "sl_today": a[0], "t_today": a[1], "sl_yday": b_[0], "t_yday": b_[1], "sl_2d": c_[0], "t_2d": c_[1], "n": a[2]})
    out["at close of day: today/yesterday/2d z -> next 48h excess"] = pd.DataFrame(tab)
    S = D[D.wd == 6].copy()   # Sunday close: Mon-Tue ahead
    # multivariate: Sat and Sun z together
    X = np.column_stack([np.ones(len(S)), S["z_r_yday"], S["z_r_today"]])
    beta, res, *_ = np.linalg.lstsq(X, S["x48"].values, rcond=None)
    e = S["x48"].values - X @ beta
    cov = np.linalg.inv(X.T @ X) * (e @ e) / (len(S) - 3)
    out["Sun close: x48 ~ Sat z + Sun z"] = pd.DataFrame({"beta": beta, "t": beta/np.sqrt(np.diag(cov))}, index=["const","Sat_z","Sun_z"])
    S["q"] = pd.qcut(S["z_r_today"], 5, labels=False)
    out["Sun z quintile -> Mon-Tue x48 (non-overlap, weekly)"] = S.groupby("q").agg(z=("z_r_today","mean"), x48=("x48","mean"), n=("x48","size"))
    S["q2"] = pd.qcut(S["z_r_2d"], 5, labels=False)
    out["weekend 2d z quintile -> Mon-Tue x48"] = S.groupby("q2").agg(z=("z_r_2d","mean"), x48=("x48","mean"), n=("x48","size"))
    yt = []
    for k, g in S.groupby("year"):
        a = reg(g, "z_r_today"); yt.append({"year": k, "slope": a[0], "t": a[1], "n": a[2]})
    out["Sun z -> Mon-Tue slope by year"] = pd.DataFrame(yt)
    ct = []
    for k, g in S.groupby("coin"):
        a = reg(g, "z_r_today"); ct.append({"coin": k, "slope": a[0], "t": a[1], "n": a[2]})
    out["Sun z -> Mon-Tue slope by coin"] = pd.DataFrame(ct)
    S["vrel"] = S["vol"] / S.groupby("coin")["vol"].transform("median")
    S["vt"] = pd.qcut(S["vrel"], 3, labels=False)
    vt = []
    for k, g in S.groupby("vt"):
        a = reg(g, "z_r_today"); vt.append({"vol_tercile": k, "slope": a[0], "t": a[1], "n": a[2]})
    out["Sun z -> Mon-Tue slope by vol tercile"] = pd.DataFrame(vt)
    # Sunday size effect: mean |x48| in direction -sign(Sun)
    S["dirmean"] = -np.sign(S["z_r_today"]) * S["x48"]
    g = S["dirmean"]
    out["Sun reversal sign-mean (x48 in -sign(Sun))"] = pd.Series({"mean": g.mean(), "t": g.mean()/(g.std()/np.sqrt(len(g))), "n": len(g), "sd48_usual": D["f48"].iloc[::2].std()})
    # hour 21-22 stability by year
    H = pd.concat(hourly)
    H["rx"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    H["h2122"] = H["hr"].isin([21,22])
    yy = H[H.h2122].groupby("year")["rx"].agg(["mean","std","size"])
    yy["t"] = yy["mean"]/(yy["std"]/np.sqrt(yy["size"])); yy["mean_bp"] = yy["mean"]*1e4
    out["hours 21-22 excess by year"] = yy[["mean_bp","t","size"]]
    cc = H[H.h2122].groupby("coin")["rx"].agg(["mean","std","size"])
    cc["t"] = cc["mean"]/(cc["std"]/np.sqrt(cc["size"])); cc["mean_bp"] = cc["mean"]*1e4
    out["hours 21-22 excess by coin"] = cc[["mean_bp","t","size"]]
    # book: trades by side and entry forecast size
    T = []
    for coin, wins in data["trades"].items():
        for w, t in wins.items():
            t = t.copy(); t["coin"] = coin; T.append(t)
    T = pd.concat(T)
    T["fq"] = pd.qcut(T["entry_forecast"].abs(), 4, labels=False, duplicates="drop")
    out["trades by side"] = T.groupby("side")["net_profit_loss_percent"].agg(["mean","count"])
    out["trades by |entry forecast| quartile"] = T.groupby("fq")["net_profit_loss_percent"].agg(["mean","count"])
    return out
