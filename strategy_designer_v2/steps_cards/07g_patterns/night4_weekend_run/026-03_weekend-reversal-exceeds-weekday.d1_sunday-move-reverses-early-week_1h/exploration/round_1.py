def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]; trades = data["trades"]
    rows = []; hrows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df[["timestamp", "close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("ts").reset_index(drop=True)
            c = d["close"].values
            ts = d["ts"]
            r1 = pd.Series(c).pct_change()
            vol = r1.rolling(720, min_periods=200).std().shift(0)
            def back(k):
                ok = (ts - ts.shift(k)) == pd.Timedelta(hours=k)
                return pd.Series(np.where(ok, c / pd.Series(c).shift(k) - 1, np.nan))
            def fwd(k):
                ok = (ts.shift(-k) - ts) == pd.Timedelta(hours=k)
                return pd.Series(np.where(ok, pd.Series(c).shift(-k) / c - 1, np.nan))
            r24 = back(24); r48 = back(48); f24 = fwd(24); f48 = fwd(48); f24b = f48 - 0
            f2nd = pd.Series(np.where(f48.notna() & f24.notna(), (1 + f48) / (1 + f24) - 1, np.nan))
            sel = ts.dt.hour == 23
            t = pd.DataFrame({"coin": coin, "w": w, "wd": ts.dt.weekday, "r24": r24, "r48": r48,
                              "f24": f24, "f48": f48, "f2nd": f2nd, "vol": vol})[sel]
            rows.append(t)
            hrows.append(pd.DataFrame({"coin": coin, "hr": ts.dt.hour, "wd": ts.dt.weekday,
                                       "z": (r1.shift(-1) / vol)}))
    A = pd.concat(rows).dropna(subset=["r24", "f48", "vol"])
    A["z24"] = A.r24 / (A.vol * np.sqrt(24)); A["z48"] = A.r48 / (A.vol * np.sqrt(48))
    A["y48"] = A.f48 / (A.vol * np.sqrt(48)); A["y24"] = A.f24 / (A.vol * np.sqrt(24))
    A["y2nd"] = A.f2nd / (A.vol * np.sqrt(24))
    def reg(df, x, y):
        df = df[[x, y]].dropna()
        if len(df) < 30: return (np.nan, np.nan, len(df))
        r = stats.linregress(df[x], df[y]); return (r.slope, r.slope / r.stderr, len(df))
    out = {}
    wdres = []
    for wd in range(7):
        s = A[A.wd == wd]
        a = reg(s, "z24", "y48"); b = reg(s, "z48", "y48"); c1 = reg(s, "z24", "y24"); c2 = reg(s, "z24", "y2nd")
        wdres.append({"day_of_24h_move": wd, "slope24_f48": a[0], "t24_f48": a[1], "slope48_f48": b[0], "t48_f48": b[1],
                      "t24_nextday": c1[1], "t24_dayafter": c2[1], "n": a[2]})
    out["reversal_by_weekday_of_move(0=Mon,6=Sun)"] = pd.DataFrame(wdres)
    S = A[A.wd == 6].copy()
    S["vq"] = S.groupby("coin")["vol"].transform(lambda v: pd.qcut(v.rank(method="first"), 3, labels=False))
    out["sunday_by_vol_tercile"] = pd.DataFrame([dict(vq=q, **dict(zip(["slope", "t", "n"], reg(S[S.vq == q], "z24", "y48")))) for q in range(3)])
    out["sunday_by_coin"] = pd.DataFrame([dict(coin=k, **dict(zip(["slope", "t", "n"], reg(g, "z24", "y48")))) for k, g in S.groupby("coin")])
    S["zq"] = pd.qcut(S.z24, 5, labels=False)
    out["sunday_quintile_next48"] = S.groupby("zq").agg(z24=("z24", "mean"), f48=("f48", "mean"), y48=("y48", "mean"), n=("f48", "size"))
    sat = A[A.wd == 5][["coin", "w", "z24"]].reset_index(drop=True)
    H = pd.concat(hrows).dropna()
    hg = H.groupby("hr")["z"].agg(["mean", "std", "count"]); hg["t"] = hg["mean"] / (hg["std"] / np.sqrt(hg["count"]))
    out["hourly_ret_by_hour_z"] = hg[["mean", "t", "count"]]
    D = []
    for coin in days:
        for w, df in days[coin].items():
            x = df.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; x["coin"] = coin; D.append(x)
    D = pd.concat(D)
    dg = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), bsd=("book_return", "std"), n=("book_return", "count"))
    dg["t_book"] = dg.book / (dg.bsd / np.sqrt(dg.n))
    out["daily_by_weekday"] = dg
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c]])
    out["trades_by_side"] = T.groupby("side").agg(n=("net_profit_loss_percent", "size"), gross=("profit_loss_percent", "mean"), net=("net_profit_loss_percent", "mean"), win=("net_profit_loss_percent", lambda v: (v > 0).mean()))
    out["trades_by_coin"] = T.groupby("coin").agg(n=("net_profit_loss_percent", "size"), net=("net_profit_loss_percent", "mean"), dur_h=("duration_minutes", lambda v: v.mean() / 60))
    return out
