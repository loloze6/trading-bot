def explore(data):
    import numpy as np, pandas as pd
    bars = data["bars"]
    out = {}
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df[["timestamp", "close"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d["fwd_hour"] = (d["ts"].dt.hour + 1) % 24
            d["year"] = d["ts"].dt.year
            r1 = d["close"].pct_change()
            d["s24"] = r1.rolling(24).std()
            d["z24"] = (d["close"] / d["close"].shift(24) - 1) / (d["s24"] * np.sqrt(24))
            d["fwd1"] = d["close"].shift(-1) / d["close"] - 1
            d["coin"] = c; d["win"] = w
            rows.append(d.dropna(subset=["fwd1", "z24", "s24"]))
    H = pd.concat(rows)
    H["with"] = np.sign(H["z24"]) * H["fwd1"]
    H["grp"] = np.where(H["fwd_hour"].isin([23]), "h23", np.where(H["fwd_hour"].isin([15, 16]), "h15_16",
               np.where(H["fwd_hour"].isin([21, 22]), "h21_22", "other")))
    H["zq"] = pd.qcut(H["z24"].abs(), 5, labels=False, duplicates="drop")
    g = H.groupby(["grp", "zq"])
    out["with_trend_bp_by_group_and_|z24|_quintile"] = pd.DataFrame({
        "with_bp": g["with"].mean() * 1e4, "t": g["with"].apply(tstat),
        "with_in_s24": g.apply(lambda q: (q["with"] / q["s24"]).mean()), "n": g.size()}).round(3)
    sub = H[H["grp"] == "h23"]
    gy = sub.groupby("year")
    out["h23_with_trend_by_year"] = pd.DataFrame({"with_bp": gy["with"].mean()*1e4, "t": gy["with"].apply(tstat), "n": gy.size()}).round(2)
    gc = sub.groupby("coin")
    out["h23_with_trend_by_coin"] = pd.DataFrame({"with_bp": gc["with"].mean()*1e4, "t": gc["with"].apply(tstat), "n": gc.size()}).round(2)
    s2 = H[H["grp"] == "h21_22"]
    gy2 = s2.groupby("year"); gc2 = s2.groupby("coin")
    out["h21_22_raw_by_year"] = pd.DataFrame({"bp": gy2["fwd1"].mean()*1e4, "t": gy2["fwd1"].apply(tstat), "n": gy2.size()}).round(2)
    out["h21_22_raw_by_coin"] = pd.DataFrame({"bp": gc2["fwd1"].mean()*1e4, "t": gc2["fwd1"].apply(tstat), "n": gc2.size()}).round(2)
    s3 = H[H["grp"] == "h15_16"]
    gy3 = s3.groupby("year")
    out["h15_16_with_trend_by_year"] = pd.DataFrame({"with_bp": gy3["with"].mean()*1e4, "t": gy3["with"].apply(tstat), "n": gy3.size()}).round(2)
    # 7-day momentum over next 7 days, graded and by year
    res = []
    for c in bars:
        allf = []
        for w, df in bars[c].items():
            cl = df["close"].values; idx = np.arange(0, len(cl) - 168, 168)
            allf.append(cl[idx + 168] / cl[idx] - 1)
        mu = np.nanmean(np.concatenate(allf))
        for w, df in bars[c].items():
            cl = df["close"].values; ts = pd.to_datetime(df["timestamp"], utc=True)
            idx = np.arange(0, len(cl) - 168, 168); idx = idx[idx >= 168]
            r1 = pd.Series(cl).pct_change()
            s = r1.rolling(168).std().values[idx]
            past = cl[idx] / cl[idx - 168] - 1
            fw = cl[idx + 168] / cl[idx] - 1 - mu
            res.append(pd.DataFrame({"z": past / (s * np.sqrt(168)), "fw": fw, "year": ts.dt.year.values[idx], "coin": c}))
    M = pd.concat(res).dropna()
    M["sf"] = np.sign(M["z"]) * M["fw"]
    M["q"] = pd.qcut(M["z"].abs(), 4, labels=False)
    gq = M.groupby("q")
    out["7d_mom_by_|z|_quartile"] = pd.DataFrame({"sign_ret_%": gq["sf"].mean()*100, "t": gq["sf"].apply(tstat), "n": gq.size()}).round(3)
    gy4 = M.groupby("year")
    out["7d_mom_by_year"] = pd.DataFrame({"sign_ret_%": gy4["sf"].mean()*100, "t": gy4["sf"].apply(tstat), "n": gy4.size()}).round(3)
    return out
