def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    H = pd.Timedelta(hours=1)
    rows = []; hrs = []; days = []
    for coin, wins in data["bars"].items():
        g48 = []
        prep = {}
        for w, df in wins.items():
            d = df[["timestamp", "close", "postRebalance_current_allocation"]].copy()
            d["timestamp"] = pd.to_datetime(d["timestamp"], utc=True)
            d = d.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].values
            ts = d["timestamp"]
            fwd = d["close"].shift(-48) / d["close"] - 1
            ok_f = (ts.shift(-48) - ts) == 48 * H
            fwd = fwd.where(ok_f)
            past = d["close"] / d["close"].shift(48) - 1
            ok_p = (ts - ts.shift(48)) == 48 * H
            past = past.where(ok_p)
            r1 = d["close"].pct_change().where((ts - ts.shift(1)) == H)
            vol = r1.rolling(168, min_periods=100).std()
            d["fwd"] = fwd; d["past"] = past; d["r1"] = r1; d["vol"] = vol
            d["ct"] = ts + H
            d["wd"] = d["ct"].dt.weekday; d["hr"] = d["ct"].dt.hour
            d["yr"] = d["ct"].dt.year
            prep[w] = d
            g = d["close"].iloc[::48].pct_change(fill_method=None).shift(-1).dropna()
            g48.append(g)
        g48 = pd.concat(g48)
        mu, sd = g48.mean(), g48.std()
        allr = pd.concat([p["r1"] for p in prep.values()])
        mu1, sd1 = allr.mean(), allr.std()
        for w, d in prep.items():
            s = d[(d["hr"] == 0)].copy()
            s["ex"] = (s["fwd"] - mu) / sd
            s["ps"] = s["past"] / sd
            s["coin"] = coin; s["w"] = w
            rows.append(s[["coin", "w", "wd", "yr", "ex", "ps", "vol", "fwd", "past"]])
            h = d[["wd", "hr", "r1"]].copy()
            h["z"] = (h["r1"] - mu1) / sd1
            h["coin"] = coin
            hrs.append(h.dropna())
    R = pd.concat(rows).dropna(subset=["ex", "ps"])
    # slope of next-48h excess on past 48h, per weekday of the 00:00 close
    res = []
    for wd, s in R.groupby("wd"):
        lr = stats.linregress(s["ps"], s["ex"])
        up = s[s["ps"] > 0]; dn = s[s["ps"] < 0]
        res.append({"wd": wd, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr,
                    "ex_after_up": up["ex"].mean(), "ex_after_dn": dn["ex"].mean(),
                    "t_up_minus_dn": stats.ttest_ind(up["ex"], dn["ex"], equal_var=False).statistic})
    out["48h_reversal_by_weekday_close00"] = pd.DataFrame(res)
    # Friday cases: by past quintile (all, rises and falls)
    F = R[R["wd"] == 4].copy()
    F["q"] = pd.qcut(F["ps"], 5, labels=False)
    out["fri_by_past_quintile"] = F.groupby("q").agg(n=("ex", "size"), ps=("ps", "mean"), ex=("ex", "mean"),
                                                      fwd_raw=("fwd", "mean"))
    F["vq"] = F.groupby("coin")["vol"].transform(lambda x: pd.qcut(x, 3, labels=False, duplicates="drop"))
    vv = []
    for vq, s in F.groupby("vq"):
        lr = stats.linregress(s["ps"], s["ex"]); vv.append({"volq": vq, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["fri_slope_by_vol_tercile"] = pd.DataFrame(vv)
    yy = []
    for y, s in F.groupby("yr"):
        if len(s) > 20:
            lr = stats.linregress(s["ps"], s["ex"]); yy.append({"yr": y, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["fri_slope_by_year"] = pd.DataFrame(yy)
    cc = []
    for cn, s in F.groupby("coin"):
        lr = stats.linregress(s["ps"], s["ex"]); cc.append({"coin": cn, "n": len(s), "slope": lr.slope, "t": lr.slope / lr.stderr})
    out["fri_slope_by_coin"] = pd.DataFrame(cc)
    Hh = pd.concat(hrs)
    out["hourly_z_by_weekday"] = Hh.groupby("wd")["z"].agg(["mean", "count", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    out["hourly_z_by_hour"] = Hh.groupby("hr")["z"].agg(["mean", lambda x: x.mean() / x.std() * np.sqrt(len(x))])
    # book by weekday
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            x = d.copy(); x["wd"] = pd.to_datetime(x["day"]).dt.weekday; D.append(x)
    D = pd.concat(D).dropna(subset=["book_return"])
    out["book_by_weekday"] = D.groupby("wd").agg(book=("book_return", "mean"), coin=("coin_return", "mean"), n=("book_return", "size"))
    q = D["book_return"].quantile([0.02, 0.98])
    out["book_extremes_weekday"] = pd.DataFrame({"big_gain": D[D["book_return"] >= q.iloc[1]]["wd"].value_counts(),
                                                 "big_loss": D[D["book_return"] <= q.iloc[0]]["wd"].value_counts()})
    return out
