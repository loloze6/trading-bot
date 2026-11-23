def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    def tstat(x):
        x = np.asarray(x, float); x = x[~np.isnan(x)]
        if len(x) < 3: return np.nan
        return x.mean() / (x.std(ddof=1) / np.sqrt(len(x)))
    # prepare
    prep = {}
    for c in bars:
        prep[c] = {}
        for w, df in bars[c].items():
            d = df[["timestamp", "close", "volume", "forecast", "postRebalance_current_allocation"]].copy()
            d["ts"] = pd.to_datetime(d["timestamp"], utc=True, errors="coerce")
            d["hour"] = d["ts"].dt.hour
            d["r1"] = d["close"].pct_change()
            d["r24p"] = d["close"] / d["close"].shift(24) - 1
            d["s24"] = d["r1"].rolling(24).std()
            d["vr"] = d["s24"] / d["s24"].rolling(720, min_periods=200).mean()
            d["fwd1"] = d["close"].shift(-1) / d["close"] - 1
            prep[c][w] = d.reset_index(drop=True)
    # A/B: hour of day, next-bar return against 24h trend
    rows = []
    for c in prep:
        for w, d in prep[c].items():
            x = d[["hour", "fwd1", "r24p", "volume"]].dropna().copy()
            x["against"] = -np.sign(x["r24p"]) * x["fwd1"]
            x["vrel"] = x["volume"] / x["volume"].rolling(24, center=True, min_periods=12).mean()
            x["coin"] = c
            rows.append(x)
    H = pd.concat(rows)
    # bar with timestamp hour h covers h..h+1; return measured close(t)->close(t+1) is bar hour+1
    H["fwd_hour"] = (H["hour"] + 1) % 24
    g = H.groupby("fwd_hour")
    out["by_hour_of_return_bp"] = pd.DataFrame({
        "mean_bp": g["fwd1"].mean() * 1e4,
        "t": g["fwd1"].apply(tstat),
        "against_trend_bp": g["against"].mean() * 1e4,
        "t_against": g["against"].apply(tstat),
        "rel_volume": g["vrel"].mean(),
        "n": g.size()}).round(3)
    pre = H[H["fwd_hour"].isin([7, 15, 23])]["against"]
    post = H[H["fwd_hour"].isin([0, 8, 16])]["against"]
    oth = H[~H["fwd_hour"].isin([7, 15, 23, 0, 8, 16])]["against"]
    out["settle_groups_against_bp"] = pd.DataFrame({
        "mean_bp": [pre.mean()*1e4, post.mean()*1e4, oth.mean()*1e4],
        "t": [tstat(pre), tstat(post), tstat(oth)],
        "n": [len(pre), len(post), len(oth)]}, index=["pre", "post", "other"]).round(3)
    # C: past L-hour return vs forward Hh return, non-overlapping grid of H
    drift = {}
    res = []
    for Hh in [24, 72, 168]:
        cases = []
        for c in prep:
            allf = []
            for w, d in prep[c].items():
                cl = d["close"].values
                idx = np.arange(0, len(cl) - Hh, Hh)
                allf.append(cl[idx + Hh] / cl[idx] - 1)
            allf = np.concatenate(allf); mu = np.nanmean(allf); sd = np.nanstd(allf)
            for w, d in prep[c].items():
                cl = d["close"].values
                idx = np.arange(0, len(cl) - Hh, Hh)
                fw = cl[idx + Hh] / cl[idx] - 1 - mu
                for L in [1, 24, 72, 168]:
                    if L > Hh * 7: continue
                    past = np.full(len(idx), np.nan)
                    ok = idx >= L
                    past[ok] = cl[idx[ok]] / cl[idx[ok] - L] - 1
                    vr = d["vr"].values[idx]
                    s24 = d["s24"].values[idx]
                    z = past / (s24 * np.sqrt(L))
                    cases.append(pd.DataFrame({"L": L, "z": z, "fw": fw / sd, "fwraw": fw, "vr": vr}))
        C = pd.concat(cases).dropna()
        for L, q in C.groupby("L"):
            s = np.sign(q["z"]) * q["fw"]
            big = q[q["z"].abs() >= q["z"].abs().quantile(2/3)]
            res.append({"H_h": Hh, "L_h": L, "n": len(q),
                        "mean_sign_strength": s.mean(), "t": tstat(s),
                        "bigthird_sign_ret_%": (np.sign(big["z"]) * big["fwraw"]).mean() * 100,
                        "t_big": tstat(np.sign(big["z"]) * big["fwraw"]),
                        "corr_z_fw": np.corrcoef(q["z"].clip(-6, 6), q["fw"])[0, 1]})
    out["past_vs_future_(+ = momentum)"] = pd.DataFrame(res).round(4)
    # D: weekday daily coin returns
    dr = []
    for c in days:
        for w, d in days[c].items():
            x = d[["day", "coin_return", "book_return"]].copy()
            x["wd"] = pd.to_datetime(x["day"]).dt.dayofweek
            dr.append(x.dropna())
    D = pd.concat(dr)
    gw = D.groupby("wd")
    out["weekday_%"] = pd.DataFrame({"coin_mean_%": gw["coin_return"].mean()*100,
                                     "t": gw["coin_return"].apply(tstat),
                                     "book_mean_%": gw["book_return"].mean()*100,
                                     "t_book": gw["book_return"].apply(tstat), "n": gw.size()}).round(3)
    # E: book days extremes vs coin
    D["bq"] = pd.qcut(D["book_return"], 10, labels=False, duplicates="drop")
    gb = D.groupby("bq")
    out["book_deciles"] = pd.DataFrame({"book_%": gb["book_return"].mean()*100,
                                        "coin_%": gb["coin_return"].mean()*100,
                                        "abs_coin_%": gb["coin_return"].apply(lambda s: s.abs().mean()*100),
                                        "n": gb.size()}).round(3)
    return out
