def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []; hr = []
    for coin in bars:
        for w, df in bars[coin].items():
            df = df.reset_index(drop=True)
            c = df["close"].values.astype(float); n = len(c)
            ts = pd.to_datetime(df["timestamp"])
            lr = np.r_[np.nan, np.diff(np.log(c))]
            vol168 = pd.Series(lr).rolling(168, min_periods=84).std()
            vrel = (vol168 / vol168.rolling(720, min_periods=240).median()).values
            vol168 = vol168.values
            ret24p = np.full(n, np.nan); ret24p[24:] = c[24:]/c[:-24]-1
            f24 = np.full(n, np.nan); f24[:-24] = c[24:]/c[:-24]-1
            r1 = np.full(n, np.nan); r1[:-1] = c[1:]/c[:-1]-1
            alloc = df["postRebalance_current_allocation"].values
            gain = alloc*r1
            tv = df["total_portfolio_value"].values.astype(float); pv = df["postRebalance_total_value"].values.astype(float)
            fee = (tv-pv)/tv
            for i in range(0, n, 24):
                rows.append(dict(coin=coin, w=w, z=ret24p[i]/(vol168[i]*np.sqrt(24)) if vol168[i]>0 else np.nan,
                                 vrel=vrel[i], vol=vol168[i], f24=f24[i], f24n=f24[i]/(vol168[i]*np.sqrt(24)) if vol168[i]>0 else np.nan, year=ts.iloc[i].year))
            hr.append(pd.DataFrame(dict(coin=coin, w=w, hour=ts.dt.hour.values, wd=ts.dt.weekday.values, year=ts.dt.year.values,
                                        r1n=r1/vol168, r1=r1, gain=gain, fee=fee)))
    g = pd.DataFrame(rows).dropna(subset=["f24","z"])
    g["ex"] = g["f24"] - g.groupby("coin")["f24"].transform("mean")
    g["exn"] = g["f24n"] - g.groupby("coin")["f24n"].transform("mean")
    def sl(s, x, y):
        r = stats.linregress(s[x], s[y]); return dict(n=len(s), slope=r.slope, t=r.slope/r.stderr)
    gv = g.dropna(subset=["vrel"]).copy()
    gv["vq"] = pd.qcut(gv["vrel"], 5, labels=False)
    out["revslope_rawret_by_relvol_quint"] = pd.DataFrame([dict(vq=k, vrel=s["vrel"].mean(), **sl(s.assign(mz=-s["z"]), "mz", "ex")) for k, s in gv.groupby("vq")])
    out["revslope_normret_by_relvol_quint"] = pd.DataFrame([dict(vq=k, **sl(s.assign(mz=-s["z"]), "mz", "exn")) for k, s in gv.groupby("vq")])
    # interaction: -z * vrel as predictor vs -z alone
    gv["mz"] = -gv["z"]; gv["mzv"] = -gv["z"]*gv["vrel"]
    out["pred_mz"] = pd.Series(sl(gv, "mz", "ex"))
    out["pred_mz_x_vrel"] = pd.Series(sl(gv, "mzv", "ex"))
    # asymmetry: after falls vs after rises
    out["sign_split"] = pd.DataFrame([dict(side=k, **sl(s.assign(mz=-s["z"]), "mz", "ex")) for k, s in g.assign(side=np.where(g["z"]<0,"after_fall","after_rise")).groupby("side")])
    out["highrelvol_by_year"] = pd.DataFrame([dict(year=k, **sl(s, "mz", "ex")) for k, s in gv[gv["vq"]==4].groupby("year")])
    H = pd.concat(hr)
    H["blk"] = (H["hour"]//4)
    # hour 20-21 stability
    H["h2021"] = H["hour"].isin([20,21])
    out["h2021_by_year"] = H[H.h2021].groupby("year").agg(r1n_mean=("r1n","mean"), t=("r1n", lambda x: x.mean()/x.std()*np.sqrt(x.count())), n=("r1n","count"))
    out["h2021_by_coin"] = H[H.h2021].groupby("coin").agg(r1n_mean=("r1n","mean"), t=("r1n", lambda x: x.mean()/x.std()*np.sqrt(x.count())))
    out["h2021_by_wd"] = H[H.h2021].groupby("wd").agg(r1n_mean=("r1n","mean"), t=("r1n", lambda x: x.mean()/x.std()*np.sqrt(x.count())))
    out["funding_hours_norm"] = H.groupby("hour").agg(r1n=("r1n","mean"), t=("r1n", lambda x: x.mean()/x.std()*np.sqrt(x.count()))).loc[[22,23,0,1,6,7,8,9,14,15,16,17]]
    out["book_costs"] = pd.Series(dict(gain_per_bar=H["gain"].mean(), fee_per_bar=H["fee"].mean(), gain_per_day=H["gain"].mean()*24, fee_per_day=H["fee"].mean()*24))
    return out
