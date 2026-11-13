def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            df = df.reset_index(drop=True)
            cl = df["close"].values; f = df["forecast"].values
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            vol = pd.Series(r1).rolling(20).std().values
            ret20 = df["debug_info.components.mom20.last_history_value"].values if "debug_info.components.mom20.last_history_value" in df else np.full(len(df), np.nan)
            ts = pd.to_datetime(df["timestamp"])
            for h in (1,20):
                for i in range(0, len(df)-h, h):
                    rows.append((c, w, int(w[1:]), ts.iloc[i].year, h, f[i], ret20[i], cl[i+h]/cl[i]-1, r1[i], vol[i], ts.iloc[i].weekday()))
    R = pd.DataFrame(rows, columns=["coin","win","wn","yr","h","f","raw20","fwd","r1","vol","wd"])
    R["ex"] = R.fwd - R.groupby(["coin","h"]).fwd.transform("mean")
    def ts_(x):
        x = x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"t":x.mean()/x.std()*np.sqrt(len(x)) if len(x)>2 else np.nan})
    s = R[R.h==20].copy()
    s["q"] = pd.qcut(s.f.rank(method="first"),5,labels=False)
    out["ex20_by_q"] = s.groupby("q").ex.apply(ts_).unstack()
    s["absf"] = s.f.abs()
    lr = stats.linregress(s.absf, s.ex); out["ex20_on_absf_slope_t"] = float(lr.slope/lr.stderr)
    s["ext"] = (s.f.abs()>=15)
    out["ex20_extreme_vs_not"] = s.groupby("ext").ex.apply(ts_).unstack()
    out["ex20_bottomq_by_coin"] = s[s.q==0].groupby("coin").ex.apply(ts_).unstack()
    out["ex20_bottomq_by_yr"] = s[s.q==0].groupby("yr").ex.apply(ts_).unstack()
    out["ex20_topq_by_coin"] = s[s.q==4].groupby("coin").ex.apply(ts_).unstack()
    d = R[R.h==1].copy()
    d["z"] = d.r1/d.vol
    dn = d[d.z<=-1]
    out["ex1_after_down1sd_by_coin"] = dn.groupby("coin").ex.apply(ts_).unstack()
    out["ex1_after_down1sd_by_yr"] = dn.groupby("yr").ex.apply(ts_).unstack()
    out["ex1_after_down1sd_vs_rest"] = d.assign(dn=d.z<=-1).groupby("dn").ex.apply(ts_).unstack()
    # down day after weak 20-day trend vs strong
    dn2 = dn.assign(fneg=dn.f<0)
    out["ex1_after_down_by_fsign"] = dn2.groupby("fneg").ex.apply(ts_).unstack()
    out["ex1_wd_by_yr_thu_fri"] = d[d.wd.isin([3,4])].groupby("yr").ex.apply(ts_).unstack()
    out["ex1_wd"] = d.groupby("wd").ex.apply(ts_).unstack()
    out["ex1_wd_by_coin_thufri"] = d[d.wd.isin([3,4])].groupby("coin").ex.apply(ts_).unstack()
    return out
