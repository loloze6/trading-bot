def explore(data):
    import numpy as np, pandas as pd
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"]); cl = b["close"].values; n = len(b)
            lr = np.r_[np.nan, np.diff(np.log(cl))]
            vol = pd.Series(lr).rolling(720, min_periods=200).std().values
            wd = ts.dt.weekday.values; hr = ts.dt.hour.values
            for i in np.where(hr == 23)[0]:
                if i+48 >= n or i-168 < 0 or not np.isfinite(vol[i]): continue
                wk = cl[i]/cl[i-48]-1; pr = cl[i-48]/cl[i-168]-1
                if not (wk < 0 and pr > 0): continue
                rows.append(dict(coin=c, win=w, yr=ts[i].year, sunday=(wd[i]==6),
                                 wkz=wk/(vol[i]*np.sqrt(48)), prz=pr/(vol[i]*np.sqrt(120)),
                                 vol=vol[i]*np.sqrt(24), f48=cl[i+48]/cl[i]-1,
                                 alloc=b["postRebalance_current_allocation"].iloc[i]))
    S = pd.DataFrame(rows)
    S["tot48"] = -S["f48"]
    def summ(x):
        return pd.Series({"n": len(x), "tot48": x.tot48.mean(),
                          "t": x.tot48.mean()/(x.tot48.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["sunday_vs_weekday_daily_grid"] = S.groupby("sunday").apply(summ)
    for lab, sub in [("sun", S[S.sunday]), ("wkday", S[~S.sunday])]:
        sub = sub.copy()
        sub["wkzq"] = pd.qcut(sub["wkz"], 4, labels=False)
        sub["przq"] = pd.qcut(sub["prz"], 4, labels=False)
        sub["volq"] = pd.qcut(sub["vol"], 4, labels=False)
        out[lab+"_by_weekendfall_z_q"] = sub.groupby("wkzq").apply(summ)
        out[lab+"_by_prior_rise_z_q"] = sub.groupby("przq").apply(summ)
        out[lab+"_by_vol_q"] = sub.groupby("volq").apply(summ)
    Su = S[S.sunday].copy()
    Su["ratio"] = -Su["wkz"]/Su["prz"]
    Su["rq"] = pd.qcut(Su["ratio"], 4, labels=False)
    out["sun_by_fall_over_rise_q"] = Su.groupby("rq").apply(summ)
    # book drawdown per coin chained
    dd = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            r = d["book_return"].fillna(0).values
            v = np.cumprod(1+r); m = np.maximum.accumulate(v)
            dd.append(dict(coin=c, win=w, ret=v[-1]-1, mdd=(v/m-1).min()))
    DD = pd.DataFrame(dd)
    out["worst_windows"] = DD.sort_values("ret").head(10).set_index(["coin","win"])
    # trade durations
    tr = pd.concat([t for ws in data["trades"].values() for t in ws.values() if t is not None and len(t)])
    out["trade_dur_h_quantiles"] = (tr["duration_minutes"]/60).quantile([.1,.25,.5,.75,.9])
    return out
