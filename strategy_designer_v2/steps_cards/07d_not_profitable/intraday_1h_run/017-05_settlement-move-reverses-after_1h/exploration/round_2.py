def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    feerows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b.close.values; n = len(b)
            tpv = b.total_portfolio_value.values; prv = b.postRebalance_total_value.values
            fee = (tpv - prv) / tpv
            pos = b.postRebalance_current_allocation.values
            r1 = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            feerows.append({"coin":c,"bars":n,"fee_sum":np.nansum(fee),"gain_sum":np.nansum(pos*r1)})
            lr = np.log(cl)
            vol24 = pd.Series(np.r_[np.nan, np.diff(lr)]).rolling(24).std().values
            vol720 = pd.Series(np.r_[np.nan, np.diff(lr)]).rolling(720, min_periods=200).std().values
            idx = np.where((b.regime=="mean_reversion") & (b.forecast!=0))[0]
            for i in idx:
                r = {"coin":c,"w":w,"f":b.forecast.values[i],
                     "pre2":cl[i]/cl[i-2]-1 if i>=2 else np.nan,
                     "pre24":cl[i]/cl[i-24]-1 if i>=24 else np.nan,
                     "vr":vol24[i]/vol720[i] if vol720[i]>0 else np.nan,
                     "vol24":vol24[i]}
                for h in (1,2,4,8):
                    r[f"r{h}"] = cl[i+h]/cl[i]-1 if i+h<n else np.nan
                rows.append(r)
    fr = pd.DataFrame(feerows)
    out["book_gain_vs_fee_per_bar_bps"] = pd.Series({"gain":fr.gain_sum.sum()/fr.bars.sum()*1e4*24,
        "fee":fr.fee_sum.sum()/fr.bars.sum()*1e4*24}).rename("per_day_bps")
    s = pd.DataFrame(rows); sg = np.sign(s.f)
    for h in (1,2,4,8):
        s[f"s{h}"] = sg*s[f"r{h}"]
    out["signed_fwd_bps_h"] = pd.DataFrame({k:[s[k].mean()*1e4, stats.ttest_1samp(s[k].dropna(),0).statistic] for k in ["s1","s2","s4","s8"]}, index=["bps","t"]).T
    # giveback as share of pre move
    s["gb2"] = -s.r2/s.pre2
    s["q"] = pd.qcut(s.pre2.abs(),5,labels=False)
    out["slope_r2_on_pre2"] = pd.Series(stats.linregress(s.dropna(subset=["pre2","r2"]).pre2, s.dropna(subset=["pre2","r2"]).r2)._asdict())
    s["vq"] = pd.qcut(s.vr,3,labels=["lowvr","midvr","highvr"])
    out["by_vol_ratio"] = s.groupby("vq").agg(n=("s2","size"),s2=("s2",lambda x:x.mean()*1e4),
        t=("s2",lambda x: stats.ttest_1samp(x.dropna(),0).statistic), s1=("s1",lambda x:x.mean()*1e4))
    s["vlev"] = pd.qcut(s.vol24,3,labels=["lowvol","midvol","highvol"])
    out["by_vol_level"] = s.groupby("vlev").agg(n=("s2","size"),s2=("s2",lambda x:x.mean()*1e4),
        t=("s2",lambda x: stats.ttest_1samp(x.dropna(),0).statistic), s2_in_vol=("s2",lambda x: (x/s.loc[x.index,"vol24"]).mean()))
    # pre2 against 24h trend
    s["agree"] = np.where(np.sign(s.pre2)==np.sign(s.pre24),"pre2_with_24h","pre2_against_24h")
    out["by_trend_agree"] = s.groupby("agree").agg(n=("s2","size"),s2=("s2",lambda x:x.mean()*1e4),
        t=("s2",lambda x: stats.ttest_1samp(x.dropna(),0).statistic))
    s["year"] = None
    out["by_window_s2_spread"] = s.groupby("w").s2.mean().mul(1e4).describe()
    return out
