def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows = []
    drift = {}
    for coin, ws in data["bars"].items():
        r3 = []
        for w, b in ws.items():
            c = b["close"].values
            idx = np.arange(0, len(c) - 3, 3)
            r3 += list(c[idx + 3] / c[idx] - 1)
        drift[coin] = (np.mean(r3), np.std(r3))
        for w, b in ws.items():
            d = b[["timestamp", "close", "volume", "forecast"]].copy().reset_index(drop=True)
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce") if not np.issubdtype(d["timestamp"].dtype, np.number) else pd.to_datetime(d["timestamp"], unit="ms", utc=True)
            d["wd"] = d["ts"].dt.dayofweek
            d["year"] = d["ts"].dt.year
            d["r1"] = d["close"].pct_change()
            d["vol20"] = d["r1"].rolling(20).std()
            d["z"] = d["r1"] / d["vol20"]
            d["z2"] = (d["close"] / d["close"].shift(2) - 1) / (d["vol20"] * np.sqrt(2))
            d["rv"] = d["volume"] / d["volume"].rolling(20).mean()
            d["rv2"] = (d["volume"] + d["volume"].shift(1)) / (2 * d["volume"].rolling(20).mean())
            d["r20"] = d["close"] / d["close"].shift(20) - 1
            for h in (1, 2, 3):
                d[f"f{h}"] = d["close"].shift(-h) / d["close"] - 1
            d["x3"] = d["f3"] - drift[coin][0]
            d["s3"] = d["x3"] / drift[coin][1]
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z", "f3"])
    out = {}
    # 1: by weekday, slope of next-3d excess on scaled return
    g = []
    for wd, s in D.groupby("wd"):
        rr = stats.pearsonr(s["z"], s["s3"])
        up = s[s["z"] > 0]; dn = s[s["z"] < 0]
        g.append(dict(wd=wd, n=len(s), corr=rr[0], p=rr[1],
                      up_x3=up["x3"].mean(), up_t=stats.ttest_1samp(up["x3"], 0)[0],
                      dn_x3=dn["x3"].mean(), dn_t=stats.ttest_1samp(dn["x3"], 0)[0],
                      next1_mean=s["f1"].mean(), next1_t=stats.ttest_1samp(s["f1"], 0)[0]))
    out["by_weekday_z_vs_next3"] = pd.DataFrame(g).round(4)
    # 2: Sunday quintiles of z
    S = D[D["wd"] == 6].copy()
    S["q"] = pd.qcut(S["z"], 5, labels=False)
    out["sunday_z_quintiles"] = S.groupby("q").agg(n=("x3", "size"), zmean=("z", "mean"), x3=("x3", "mean"),
        x3_t=("x3", lambda v: stats.ttest_1samp(v, 0)[0]), f1=("f1", "mean"), s3=("s3", "mean")).round(4)
    # weekend 2-day move (Fri close -> Sun close)
    S["q2"] = pd.qcut(S["z2"], 5, labels=False)
    out["sunday_weekend2d_quintiles"] = S.groupby("q2").agg(n=("x3", "size"), z2=("z2", "mean"), x3=("x3", "mean"),
        x3_t=("x3", lambda v: stats.ttest_1samp(v, 0)[0])).round(4)
    # 3: Sunday rises by relative weekend volume tercile
    Su = S[S["z"] > 0].dropna(subset=["rv2"]).copy()
    Su["vt"] = pd.qcut(Su["rv2"], 3, labels=False)
    out["sunday_rise_by_wkndvol"] = Su.groupby("vt").agg(n=("x3", "size"), rv2=("rv2", "mean"), x3=("x3", "mean"),
        x3_t=("x3", lambda v: stats.ttest_1samp(v, 0)[0]), corr_z=("z", lambda v: np.corrcoef(v, Su.loc[v.index, "s3"])[0, 1])).round(4)
    # 4: Sunday rises by 20-day trend tercile
    Su2 = S[S["z"] > 0].dropna(subset=["r20"]).copy()
    Su2["tt"] = pd.qcut(Su2["r20"], 3, labels=False)
    out["sunday_rise_by_trend20"] = Su2.groupby("tt").agg(n=("x3", "size"), r20=("r20", "mean"), x3=("x3", "mean"),
        x3_t=("x3", lambda v: stats.ttest_1samp(v, 0)[0])).round(4)
    # 5: Sunday rises by year
    out["sunday_rise_by_year"] = S[S["z"] > 0].groupby("year").agg(n=("x3", "size"), x3=("x3", "mean"),
        x3_t=("x3", lambda v: stats.ttest_1samp(v, 0)[0])).round(4)
    # 6: all Sundays (any sign): Monday-Tuesday-Wednesday path
    out["sunday_rise_path"] = pd.Series({"f1": S[S.z > 0]["f1"].mean(), "f2": S[S.z > 0]["f2"].mean(), "f3": S[S.z > 0]["f3"].mean(),
                                          "fall_f1": S[S.z < 0]["f1"].mean(), "fall_f3": S[S.z < 0]["f3"].mean()}).round(5)
    # 7: book daily returns by weekday
    bk = []
    for coin, ws in data["days"].items():
        for w, d in ws.items():
            d = d.copy(); d["wd"] = pd.to_datetime(d["day"]).dt.dayofweek; bk.append(d)
    B = pd.concat(bk).dropna(subset=["book_return"])
    out["book_by_weekday"] = B.groupby("wd").agg(n=("book_return", "size"), book=("book_return", "mean"),
        coin=("coin_return", "mean"), coin_t=("coin_return", lambda v: stats.ttest_1samp(v, 0)[0])).round(5)
    return out
