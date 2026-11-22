def explore(data):
    import numpy as np, pandas as pd
    H = 18
    rows = []; hrows = []
    for coin, wins in data["bars"].items():
        r18_all = []
        for w, df in wins.items():
            c = df["close"].values
            idx = np.arange(0, len(c) - H, H)
            r18_all.extend(list(c[idx + H] / c[idx] - 1))
        r18_all = np.array(r18_all)
        if len(r18_all) < 10:
            continue
        drift = r18_all.mean(); usual = r18_all.std()
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].astype(float); v = df["volume"].astype(float)
            r1 = c.pct_change()
            cv = c.values; vv = v.values
            usual1 = r1.abs().rolling(180, min_periods=60).mean().values
            lv = np.log(v.replace(0, np.nan))
            vz = ((lv - lv.rolling(180, min_periods=60).mean()) / lv.rolling(180, min_periods=60).std()).values
            ts = pd.to_datetime(df["timestamp"])
            n = len(c)
            r6 = (c / c.shift(6) - 1).values
            # volume-weighted 1-day move vs plain: sum of signed returns weighted by vz over last 6 bars
            nxt = (c.shift(-1) / c - 1).values
            for i in range(0, n - 1):
                if not np.isnan(nxt[i]) and not np.isnan(usual1[i]):
                    hrows.append((coin, w, ts.iloc[i].year, ts.iloc[i].hour, nxt[i] / usual1[i]))
            for i in range(0, n - H, H):
                if i < 7 or np.isnan(usual1[i]) or np.isnan(vz[i]):
                    continue
                fr = cv[i + H] / cv[i] - 1
                d6 = r6[i] / (usual1[i] * np.sqrt(6))
                vz6 = np.nanmean(vz[i-5:i+1])
                rows.append(dict(coin=coin, win=w, year=ts.iloc[i].year, wd=ts.iloc[i].weekday(),
                                 d6=d6, vz=vz[i], vz6=vz6, b1=r1.values[i] / usual1[i],
                                 un=fr - drift, st=(fr - drift) / usual))
    G = pd.DataFrame(rows)
    def summ(g):
        x = g["un"].dropna()
        return pd.Series({"n": len(x), "mean_un%": 100 * x.mean(),
                          "t": x.mean() / (x.std() / np.sqrt(len(x))) if len(x) > 2 else np.nan,
                          "strength": g["st"].mean()})
    out = {}
    # 1-day move direction x 1-day volume level
    G["dir"] = np.where(G["d6"] < 0, "down", "up")
    G["dq"] = G.groupby("dir")["d6"].transform(lambda s: pd.qcut(s.abs(), 3, labels=False, duplicates="drop"))
    G["vq"] = pd.qcut(G["vz6"], 3, labels=False)
    out["dir_x_size_x_vol6"] = G.groupby(["dir", "dq", "vq"]).apply(summ)
    # down 1-day moves: graded by size*volume ; per coin sign
    dn = G[G.dir == "down"].copy()
    dn["score"] = (-dn["d6"]) * np.exp(dn["vz6"].clip(-3, 3))
    dn["sq"] = pd.qcut(dn["score"], 5, labels=False)
    out["down_score_quint"] = dn.groupby("sq").apply(summ)
    top = dn[dn.sq == 4]
    out["down_top_by_coin"] = top.groupby("coin").apply(summ)
    out["down_top_by_year"] = top.groupby("year").apply(summ)
    # vz at bar alone, split by bar direction
    G["bdir"] = np.where(G["b1"] < 0, "down", "up")
    G["vzq"] = pd.qcut(G["vz"], 4, labels=False)
    out["bar_dir_x_vz"] = G.groupby(["bdir", "vzq"]).apply(summ)
    # hour effect robustness
    Hd = pd.DataFrame(hrows, columns=["coin", "win", "year", "hour", "nu"])
    h = Hd[Hd.hour.isin([0, 16])]
    def s1(g):
        x = g["nu"]; return pd.Series({"n": len(x), "mean_usual": x.mean(), "t": x.mean() / (x.std() / np.sqrt(len(x)))})
    out["hour_all"] = Hd.groupby("hour").apply(s1)
    out["hour16_by_year"] = Hd[Hd.hour == 16].groupby("year").apply(s1)
    out["hour16_by_coin"] = Hd[Hd.hour == 16].groupby("coin").apply(s1)
    out["hour0_by_year"] = Hd[Hd.hour == 0].groupby("year").apply(s1)
    return out
