def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H = 18
    rows = []
    drift = {}; usual = {}
    for coin, wins in data["bars"].items():
        allr = []
        for w, b in wins.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - H, H)
            allr.append(c[idx + H] / c[idx] - 1)
        allr = np.concatenate(allr)
        drift[coin] = allr.mean(); usual[coin] = allr.std()
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"]; v = b["volume"]
            n = len(b)
            fwd = c.shift(-H) / c - 1
            r1d = c / c.shift(6) - 1
            r30 = c / c.shift(180) - 1
            vol = np.log(c).diff().rolling(180, min_periods=60).std()
            dn = (c < c.shift(1)).astype(int).values
            up = (c > c.shift(1)).astype(int).values
            sd = np.zeros(n, int); su = np.zeros(n, int)
            for i in range(1, n):
                sd[i] = sd[i-1] + 1 if dn[i] else 0
                su[i] = su[i-1] + 1 if up[i] else 0
            # volume slope over current streak (sign of last vol minus first vol of streak as proxy)
            lv = np.log(v.replace(0, np.nan)).values
            vslope = np.full(n, np.nan)
            for i in range(n):
                L = max(sd[i], su[i])
                if L >= 2:
                    y = lv[i-L+1:i+1]
                    if np.isfinite(y).all():
                        vslope[i] = np.polyfit(np.arange(L), y, 1)[0]
            vrel = v / v.rolling(180, min_periods=60).mean()
            idx = np.arange(0, n - H, H)
            df = pd.DataFrame({
                "coin": coin, "win": w, "fwd": fwd.values[idx], "r1d": r1d.values[idx],
                "r30": r30.values[idx], "vol": vol.values[idx], "sd": sd[idx], "su": su[idx],
                "vslope": vslope[idx], "vrel": vrel.values[idx],
                "fc": b["forecast"].values[idx], "alloc": b["postRebalance_current_allocation"].values[idx],
                "hour": pd.to_datetime(b["timestamp"]).dt.hour.values[idx],
                "wd": pd.to_datetime(b["timestamp"]).dt.weekday.values[idx]})
            df["u"] = (df["fwd"] - drift[coin]) / usual[coin]
            df["ex"] = df["fwd"] - drift[coin]
            rows.append(df)
    G = pd.concat(rows).dropna(subset=["fwd"])
    def summ(g):
        x = g["ex"].dropna()
        return pd.Series({"n": len(x), "mean_ex%": 100*x.mean(), "t": x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                          "strength": g["u"].mean()})
    out = {}
    out["drift_usual"] = pd.DataFrame({"drift%": pd.Series(drift)*100, "usual%": pd.Series(usual)*100})
    G["q1d"] = G.groupby("coin")["r1d"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_1d_return_quintile"] = G.groupby("q1d").apply(summ)
    G["q30"] = G.groupby("coin")["r30"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_30d_return_quintile"] = G.groupby("q30").apply(summ)
    G["qv"] = G.groupby("coin")["vol"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_vol_quintile"] = G.groupby("qv").apply(summ)
    G["streak"] = np.where(G["sd"] > 0, -G["sd"].clip(upper=5), G["su"].clip(upper=5))
    out["by_streak(neg=down)"] = G.groupby("streak").apply(summ)
    G["fade"] = np.where(G["vslope"] < 0, "fade", np.where(G["vslope"] > 0, "rise", "none"))
    G["streakdir"] = np.where(G["sd"] >= 2, "down2+", np.where(G["su"] >= 2, "up2+", "short"))
    out["streak_x_volume"] = G.groupby(["streakdir", "fade"]).apply(summ)
    G["qvr"] = G.groupby("coin")["vrel"].transform(lambda s: pd.qcut(s, 5, labels=False, duplicates="drop"))
    out["by_relvolume_quintile"] = G.groupby("qvr").apply(summ)
    out["by_hour"] = G.groupby("hour").apply(summ)
    out["by_weekday"] = G.groupby("wd").apply(summ)
    out["by_coin"] = G.groupby("coin").apply(summ)
    out["by_forecast_bucket"] = G.assign(fb=pd.cut(G["fc"], [-21, -0.01, 0.01, 2, 5, 10, 21])).groupby("fb").apply(summ)
    # book
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            D.append(d.assign(coin=coin, win=w))
    D = pd.concat(D)
    daily = D.groupby(["win", "day"])[["book_return", "coin_return"]].mean().dropna()
    out["book_daily"] = pd.Series({"mean_book%": 100*daily.book_return.mean(), "mean_coin%": 100*daily.coin_return.mean(),
                                   "sharpe_book": daily.book_return.mean()/daily.book_return.std()*np.sqrt(365),
                                   "corr": daily.book_return.corr(daily.coin_return), "ndays": len(daily)})
    daily["yr"] = pd.to_datetime(daily.index.get_level_values("day")).year
    out["book_by_year"] = daily.groupby("yr").agg(n=("book_return", "size"), book=("book_return", "mean"), coin=("coin_return", "mean"))*[1,100,100]
    return out
