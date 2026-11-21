def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"], utc=True)
            c = b["close"].astype(float).values
            n = len(c)
            lr = pd.Series(np.log(c)).diff()
            sd1 = lr.rolling(480, min_periods=200).std().values
            yr = ts.dt.year.values
            for i in range(48, n - 72, 24):
                if not sd1[i] > 0: continue
                z12 = (c[i]/c[i-12]-1)/(sd1[i]*np.sqrt(12))
                z24 = (c[i]/c[i-24]-1)/(sd1[i]*np.sqrt(24))
                z48 = (c[i]/c[i-48]-1)/(sd1[i]*np.sqrt(48))
                f24 = c[i+24]/c[i]-1; f48 = c[i+48]/c[i]-1; f72 = c[i+72]/c[i]-1
                f24n = f24/(sd1[i]*np.sqrt(24))
                rows.append((coin, w, yr[i], z12, z24, z48, f24, f48, f72, f24n))
    R = pd.DataFrame(rows, columns=["coin","w","year","z12","z24","z48","f24","f48","f72","f24n"])
    for col in ["f24","f48","f72"]:
        R[col+"u"] = R[col] - R.groupby("coin")[col].transform("mean")
    def tt(s): return s.mean()/(s.std()/np.sqrt(s.count()))
    # finer bins of z24 (pooled percentiles)
    q = R["z24"].rank(pct=True)
    bins = pd.cut(q, [0,0.02,0.05,0.10,0.20,0.40,0.60,0.80,0.90,0.95,0.98,1.0])
    g = R.groupby(bins, observed=True)
    out["z24_fine_bins"] = pd.DataFrame({"z": g["z24"].mean(), "f24u_bps": g["f24u"].mean()*1e4,
        "t24": g["f24u"].apply(tt), "f48u_bps": g["f48u"].mean()*1e4, "t48": g["f48u"].apply(tt),
        "f72u_bps": g["f72u"].mean()*1e4, "strength24": g["f24n"].mean(), "n": g["z24"].count()}).round(2)
    low = R[q <= 0.10]
    gc = low.groupby("coin")
    out["bottom_decile_by_coin"] = pd.DataFrame({"f24u_bps": gc["f24u"].mean()*1e4, "t24": gc["f24u"].apply(tt),
        "f72u_bps": gc["f72u"].mean()*1e4, "n": gc["f24u"].count()}).round(2)
    gy = low.groupby("year")
    out["bottom_decile_by_year"] = pd.DataFrame({"f24u_bps": gy["f24u"].mean()*1e4, "t24": gy["f24u"].apply(tt),
        "n": gy["f24u"].count()}).round(2)
    wn = low["w"].str[1:].astype(int)
    gw = low.groupby(pd.cut(wn, [0,6,12,18,24]))
    out["bottom_decile_by_window_quarter"] = pd.DataFrame({"f24u_bps": gw["f24u"].mean()*1e4,
        "t24": gw["f24u"].apply(tt), "n": gw["f24u"].count()}).round(2)
    # other lookbacks bottom decile
    res = {}
    for zc in ["z12","z24","z48"]:
        qq = R[zc].rank(pct=True)
        lo = R[qq<=0.10]; hi = R[qq>=0.90]
        res[zc] = {"low_f24u_bps": lo["f24u"].mean()*1e4, "low_t": tt(lo["f24u"]),
                   "high_f24u_bps": hi["f24u"].mean()*1e4, "high_t": tt(hi["f24u"])}
    out["lookbacks_tails"] = pd.DataFrame(res).T.round(2)
    # within the falls only (z24<0): rank correlation of -z with f24u
    neg = R[R.z24 < 0]
    from scipy import stats
    out["spearman_neg_z24_vs_f24u"] = round(stats.spearmanr(-neg["z24"], neg["f24u"])[0], 4)
    out["n_neg"] = int(len(neg))
    # days: Saturday by year
    D = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            d = d.copy(); D.append(d)
    D = pd.concat(D).dropna(subset=["coin_return"])
    dd = pd.to_datetime(D["day"]); D["wd"] = dd.dt.weekday; D["year"] = dd.dt.year
    sat = D[D.wd == 5]
    out["saturday_by_year_bps"] = (sat.groupby("year")["coin_return"].mean()*1e4).round(1)
    return out
