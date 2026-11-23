def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    hourly = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b[["timestamp","close"]].copy()
            b["timestamp"] = pd.to_datetime(b["timestamp"], utc=True)
            b = b.set_index("timestamp").sort_index()
            r1 = b["close"].pct_change()
            vol = r1.rolling(720, min_periods=240).std()
            hh = pd.DataFrame({"r": r1, "wd": b.index.weekday, "hr": b.index.hour, "coin": coin})
            hourly.append(hh.dropna())
            # daily closes at hour 23
            d = b[b.index.hour == 23].copy()
            d["vol"] = vol.reindex(d.index) * np.sqrt(24)
            d["day"] = d.index.floor("D")
            d = d.set_index("day")
            full = pd.date_range(d.index.min(), d.index.max(), freq="D", tz="UTC")
            d = d.reindex(full)
            c = d["close"]
            dd = pd.DataFrame(index=full)
            dd["ret1"] = c / c.shift(1) - 1
            dd["ret2"] = c / c.shift(2) - 1
            dd["prev1"] = c.shift(1)/c.shift(2)-1
            dd["f48"] = c.shift(-2) / c - 1
            dd["f24"] = c.shift(-1) / c - 1
            dd["vol"] = d["vol"]
            dd["wd"] = full.weekday
            dd["coin"] = coin; dd["win"] = w
            dd["year"] = full.year
            rows.append(dd)
    D = pd.concat(rows)
    D = D.dropna(subset=["ret1","f48","vol"])
    # coin mean 48h return (approx non-overlap: every other day)
    m48 = D.groupby("coin")["f48"].apply(lambda s: s.iloc[::2].mean())
    D["x48"] = D["f48"] - D["coin"].map(m48)
    m24 = D.groupby("coin")["f24"].mean()
    D["x24"] = D["f24"] - D["coin"].map(m24)
    D["z"] = D["ret1"] / D["vol"]
    D["z"] = D["z"].clip(-6, 6)
    def reg(sub, x, y):
        s = sub.dropna(subset=[x, y])
        if len(s) < 30: return (np.nan, np.nan, len(s))
        lr = stats.linregress(s[x], s[y])
        return (lr.slope, lr.slope/lr.stderr, len(s))
    tab = []
    names = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    for wd in range(7):
        s = D[D.wd == wd]
        sl, t, n = reg(s, "z", "x48")
        sl2, t2, n2 = reg(s, "z", "x24")
        dirm = (np.sign(s["z"]) * s["x48"]).mean()
        tab.append({"day": names[wd], "slope48": sl, "t48": t, "n": n, "slope24": sl2, "t24": t2, "signmean48": dirm})
    out["day-return z -> next 48h/24h excess, by weekday of the day"] = pd.DataFrame(tab)
    # Saturday quintiles
    s = D[D.wd == 5].copy()
    s["q"] = pd.qcut(s["z"], 5, labels=False)
    out["Sat z quintile -> Mon-Tue x48"] = s.groupby("q").agg(z=("z","mean"), x48=("x48","mean"), sd=("x48","std"), n=("x48","size"))
    # Sunday as predictor of Mon-Tue
    s6 = D[D.wd == 6].copy()
    s6["q"] = pd.qcut(s6["z"], 5, labels=False)
    out["Sun z quintile -> Mon-Tue x48"] = s6.groupby("q").agg(z=("z","mean"), x48=("x48","mean"), n=("x48","size"))
    # Sat by vol tercile (vol relative to coin median)
    s["vrel"] = s["vol"] / s.groupby("coin")["vol"].transform("median")
    s["vt"] = pd.qcut(s["vrel"], 3, labels=False)
    vt = []
    for k, g in s.groupby("vt"):
        sl, t, n = reg(g, "z", "x48"); vt.append({"vol_tercile": k, "slope": sl, "t": t, "n": n})
    out["Sat slope by vol tercile"] = pd.DataFrame(vt)
    yt = []
    for k, g in s.groupby("year"):
        sl, t, n = reg(g, "z", "x48"); yt.append({"year": k, "slope": sl, "t": t, "n": n})
    out["Sat slope by year"] = pd.DataFrame(yt)
    ct = []
    for k, g in s.groupby("coin"):
        sl, t, n = reg(g, "z", "x48"); ct.append({"coin": k, "slope": sl, "t": t, "n": n})
    out["Sat slope by coin"] = pd.DataFrame(ct)
    # hourly seasonality
    H = pd.concat(hourly)
    H["rx"] = H["r"] - H.groupby("coin")["r"].transform("mean")
    g = H.groupby("wd")["rx"]
    out["hourly excess return by weekday (bp)"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size())), "n": g.size()})
    g = H.groupby("hr")["rx"]
    out["hourly excess return by hour (bp)"] = pd.DataFrame({"mean_bp": g.mean()*1e4, "t": g.mean()/(g.std()/np.sqrt(g.size()))})
    # book days
    bd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); d["coin"] = coin
            bd.append(d)
    B = pd.concat(bd).dropna(subset=["book_return"])
    B["wd"] = pd.to_datetime(B["day"]).dt.weekday
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book coin-day return by weekday (bp)"] = B.groupby("wd")["book_return"].agg(lambda x: x.mean()*1e4)
    out["book coin-day mean by year (bp)"] = B.groupby("year")["book_return"].agg(lambda x: x.mean()*1e4)
    return out
