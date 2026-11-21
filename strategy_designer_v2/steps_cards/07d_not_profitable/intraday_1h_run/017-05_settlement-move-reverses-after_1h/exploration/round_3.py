def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    rows = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            cl = b.close.values; n = len(b)
            lr = np.r_[np.nan, np.diff(np.log(cl))]
            vol24 = pd.Series(lr).rolling(24).std().values
            idx = np.where((b.regime=="mean_reversion") & (b.forecast!=0))[0]
            for i in idx:
                r = {"coin":c,"f":b.forecast.values[i],
                     "pre2":cl[i]/cl[i-2]-1 if i>=2 else np.nan,
                     "pre24":cl[i]/cl[i-24]-1 if i>=24 else np.nan,
                     "vol24":vol24[i]}
                for h in (2,8,16):
                    r[f"r{h}"] = cl[i+h]/cl[i]-1 if i+h<n else np.nan
                rows.append(r)
    s = pd.DataFrame(rows); sg = np.sign(s.f)
    for h in (2,8,16):
        s[f"s{h}"] = sg*s[f"r{h}"]
    s["vlev"] = pd.qcut(s.vol24,3,labels=["lowvol","midvol","highvol"])
    s["agree"] = np.where(np.sign(s.pre2)==np.sign(s.pre24),"with24","against24")
    s["mq"] = pd.qcut(s.pre2.abs(),3,labels=["small","mid","large"])
    def agg(g):
        return pd.Series({"n":len(g),"s2":g.s2.mean()*1e4,"t2":stats.ttest_1samp(g.s2.dropna(),0).statistic,
                          "s8":g.s8.mean()*1e4,"t8":stats.ttest_1samp(g.s8.dropna(),0).statistic,
                          "s16":g.s16.mean()*1e4,"absmove":g.pre2.abs().mean()*1e4})
    out["vol_x_agree"] = s.groupby(["vlev","agree"]).apply(agg)
    out["vol_x_movesize"] = s.groupby(["vlev","mq"]).apply(agg)
    hv = s[s.vlev=="highvol"].dropna(subset=["pre2","r8"])
    out["slope_r8_on_pre2_highvol"] = pd.Series(stats.linregress(hv.pre2, hv.r8)._asdict())
    al = s.dropna(subset=["pre2","r8"])
    out["slope_r8_on_pre2_all"] = pd.Series(stats.linregress(al.pre2, al.r8)._asdict())
    return out
