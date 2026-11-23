def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    def tt(v):
        v = pd.Series(v).dropna()
        return stats.ttest_1samp(v, 0)[0] if len(v) > 2 else np.nan
    def tod(s):
        if pd.api.types.is_numeric_dtype(s):
            return pd.to_datetime(s, unit="ms", utc=True)
        return pd.to_datetime(s, utc=True, errors="coerce")
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
            d = b[["timestamp", "close", "volume", "forecast", "postRebalance_current_allocation"]].copy().reset_index(drop=True)
            d["ts"] = tod(d["timestamp"])
            d["wd"] = d["ts"].dt.dayofweek
            d["year"] = d["ts"].dt.year
            d["r1"] = d["close"].pct_change()
            d["vol20"] = d["r1"].rolling(20).std()
            d["z"] = d["r1"] / d["vol20"]
            d["z2"] = (d["close"] / d["close"].shift(2) - 1) / (d["vol20"] * np.sqrt(2))
            d["rv2"] = (d["volume"] + d["volume"].shift(1)) / (2 * d["volume"].rolling(20).mean())
            d["r20"] = d["close"] / d["close"].shift(20) - 1
            d["volrank"] = d["vol20"] / d["vol20"].rolling(120, min_periods=40).mean()
            for h in (1, 2, 3):
                d[f"f{h}"] = d["close"].shift(-h) / d["close"] - 1
            d["x3"] = d["f3"] - drift[coin][0]
            d["s3"] = d["x3"] / drift[coin][1]
            d["coin"] = coin; d["win"] = w
            rows.append(d)
    D = pd.concat(rows).dropna(subset=["z", "f3"])
    out = {}
    try:
        g = []
        for wd, s in D.groupby("wd"):
            rr = stats.pearsonr(s["z"], s["s3"])
            up = s[s["z"] > 0]; dn = s[s["z"] < 0]
            big = s[s["z"] > 1]
            g.append(dict(wd=wd, n=len(s), corr=rr[0], p=rr[1],
                          up_x3=up["x3"].mean(), up_t=tt(up["x3"]),
                          bigup_n=len(big), bigup_x3=big["x3"].mean(), bigup_t=tt(big["x3"]),
                          dn_x3=dn["x3"].mean(), dn_t=tt(dn["x3"]),
                          next1=s["f1"].mean(), next1_t=tt(s["f1"])))
        out["by_weekday_z_vs_next3"] = pd.DataFrame(g).round(4)
    except Exception as e:
        out["e1"] = str(e)
    S = D[D["wd"] == 6].copy()
    try:
        S["q"] = pd.qcut(S["z"], 5, labels=False)
        out["sunday_z_quintiles"] = S.groupby("q").agg(n=("x3", "size"), zmean=("z", "mean"), x3=("x3", "mean"),
            x3_t=("x3", tt), f1=("f1", "mean"), f1_t=("f1", tt)).round(4)
        S["q2"] = pd.qcut(S["z2"], 5, labels=False)
        out["sunday_weekend2d_quintiles"] = S.groupby("q2").agg(n=("x3", "size"), z2=("z2", "mean"), x3=("x3", "mean"),
            x3_t=("x3", tt)).round(4)
    except Exception as e:
        out["e2"] = str(e)
    try:
        Su = S[S["z"] > 0].dropna(subset=["rv2"]).copy()
        Su["vt"] = pd.qcut(Su["rv2"], 3, labels=False)
        out["sunday_rise_by_wkndvol"] = Su.groupby("vt").agg(n=("x3", "size"), rv2=("rv2", "mean"), x3=("x3", "mean"),
            x3_t=("x3", tt)).round(4)
        Su2 = S[S["z"] > 0].dropna(subset=["r20"]).copy()
        Su2["tt"] = pd.qcut(Su2["r20"], 3, labels=False)
        out["sunday_rise_by_trend20"] = Su2.groupby("tt").agg(n=("x3", "size"), r20=("r20", "mean"), x3=("x3", "mean"),
            x3_t=("x3", tt)).round(4)
        Su3 = S[S["z"] > 0].dropna(subset=["volrank"]).copy()
        Su3["vr"] = pd.qcut(Su3["volrank"], 3, labels=False)
        out["sunday_rise_by_vollevel"] = Su3.groupby("vr").agg(n=("x3", "size"), vr=("volrank", "mean"), x3=("x3", "mean"),
            x3_t=("x3", tt)).round(4)
        out["sunday_rise_by_year"] = S[S["z"] > 0].groupby("year").agg(n=("x3", "size"), x3=("x3", "mean"),
            x3_t=("x3", tt)).round(4)
        out["sunday_rise_by_coin"] = S[S["z"] > 0].groupby("coin").agg(n=("x3", "size"), x3=("x3", "mean"),
            x3_t=("x3", tt)).round(4)
        out["sunday_path"] = pd.Series({"rise_f1": S[S.z > 0]["f1"].mean(), "rise_f2": S[S.z > 0]["f2"].mean(),
            "rise_f3": S[S.z > 0]["f3"].mean(), "fall_f1": S[S.z < 0]["f1"].mean(), "fall_f3": S[S.z < 0]["f3"].mean(),
            "all_f1_any_day": D["f1"].mean(), "all_f3_any_day": D["f3"].mean()}).round(5)
    except Exception as e:
        out["e3"] = str(e)
    try:
        bk = []
        for coin, ws in data["days"].items():
            for w, d in ws.items():
                d = d.copy(); d["wd"] = tod(d["day"]).dt.dayofweek; bk.append(d)
        B = pd.concat(bk).dropna(subset=["book_return", "coin_return"])
        out["book_by_weekday"] = B.groupby("wd").agg(n=("book_return", "size"), book=("book_return", "mean"),
            book_t=("book_return", tt), coin=("coin_return", "mean"), coin_t=("coin_return", tt)).round(5)
        q = B["book_return"].quantile([0.01, 0.99])
        out["book_extremes_weekday"] = pd.DataFrame({
            "worst1pct": B[B.book_return <= q.iloc[0]].groupby("wd").size(),
            "best1pct": B[B.book_return >= q.iloc[1]].groupby("wd").size()}).fillna(0)
    except Exception as e:
        out["e4"] = str(e)
    return out
