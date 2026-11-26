def explore(data):
    import pandas as pd, numpy as np
    bars = data["bars"]; days = data["days"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            sd30 = r1.rolling(30).std()
            ret30 = c / c.shift(30) - 1
            ret60 = c / c.shift(60) - 1
            ret5p = c / c.shift(5) - 1
            z30 = ret30 / (sd30 * np.sqrt(30))
            z5 = ret5p / (sd30 * np.sqrt(5))
            z1 = r1 / sd30.shift(1)
            vz5 = v.rolling(5).mean() / v.rolling(30).mean().shift(5)
            fwd5 = c.shift(-5) / c - 1
            ts = pd.to_datetime(df["timestamp"])
            for i in range(0, len(df), 5):
                if i + 5 >= len(df):
                    break
                rows.append(dict(coin=coin, w=w, regime=df["regime"].iloc[i], ret30=ret30.iloc[i],
                                 ret60=ret60.iloc[i], z30=z30.iloc[i], z5=z5.iloc[i], z1=z1.iloc[i],
                                 vz5=vz5.iloc[i], sd30=sd30.iloc[i], fwd5=fwd5.iloc[i],
                                 year=ts.iloc[i].year, day=ts.iloc[i].normalize()))
    g = pd.DataFrame(rows)
    g["ex5"] = g["fwd5"] - g.groupby("coin")["fwd5"].transform("mean")
    g["sdc"] = g.groupby("coin")["sd30"].transform("median")
    g["agit"] = np.where(g.sd30 > g.sdc, "agit", "calm")

    def summ(sub, col="ex5"):
        s = sub.dropna(subset=[col])
        n = len(s)
        if n < 5:
            return pd.Series(dict(n=n))
        m = s[col].mean()
        dev = (s[col] - m).groupby(s["day"]).sum()
        G = len(dev)
        se = np.sqrt((dev ** 2).sum() * G / max(G - 1, 1)) / n
        return pd.Series(dict(n=n, days=G, mean=m, t_day=m / se if se > 0 else np.nan))

    out = {}
    s = g[g.ret60.notna() & g.z30.notna()].copy()
    s["trend"] = np.where(s.ret60 > 0.1, "rising", np.where(s.ret60 < -0.1, "falling", "choppy"))
    s["z30b"] = pd.cut(s.z30, [-np.inf, -1.5, -0.75, 0, 0.75, 1.5, np.inf])
    out["trend_x_z30"] = s.groupby(["trend", "z30b"]).apply(summ).round(4)
    ch = s[s.trend == "choppy"]
    out["choppy_z30_x_agit"] = ch.groupby(["agit", pd.cut(ch.z30, [-np.inf, -1, 0, 1, np.inf])]).apply(summ).round(4)
    chl = ch[ch.z30 < -1]
    out["choppy_lowz30_by_year"] = chl.groupby("year").apply(summ).round(4)
    out["choppy_lowz30_by_coin"] = chl.groupby("coin").apply(summ).round(4)
    out["choppy_lowz30_by_vz5"] = chl.groupby(pd.qcut(chl.vz5, 2, labels=["lowvol", "highvol"])).apply(summ).round(4)
    # 5-day momentum, day-clustered
    s5 = g[g.z5.notna()].copy()
    s5["z5b"] = pd.cut(s5.z5, [-np.inf, -1.5, -0.75, 0, 0.75, 1.5, np.inf])
    out["z5_all_dayt"] = s5.groupby("z5b").apply(summ).round(4)
    out["z5_by_agit"] = s5.groupby(["agit", "z5b"]).apply(summ).round(4)
    s5["side"] = np.sign(s5.z5)
    s5["sx"] = s5.ex5 * s5.side
    ext = s5[s5.z5.abs() > 1.5]
    out["z5_ext_signed_by_year"] = ext.groupby("year").apply(lambda x: summ(x, "sx")).round(4)
    out["z5_ext_signed_by_coin"] = ext.groupby("coin").apply(lambda x: summ(x, "sx")).round(4)
    # Saturday check by year
    dd = []
    for coin, wins in days.items():
        for w, df in wins.items():
            d = df.copy(); d["coin"] = coin; d["w"] = w; dd.append(d)
    D = pd.concat(dd)
    D["dt"] = pd.to_datetime(D["day"]); D["wd"] = D.dt.dt.weekday; D["year"] = D.dt.dt.year
    D["cx"] = D.coin_return - D.groupby("coin")["coin_return"].transform("mean")
    sat = D[D.wd == 5]
    out["sat_by_year"] = sat.groupby("year")["cx"].agg(["count", "mean"]).round(5)
    thu = D[D.wd == 3]
    out["thu_by_year"] = thu.groupby("year")["cx"].agg(["count", "mean"]).round(5)
    return out
