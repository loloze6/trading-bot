def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    bars = data["bars"]; H = 72
    rows = []; hr = []; bk = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            cl = b["close"].values.astype(float)
            r1 = np.r_[np.nan, cl[1:]/cl[:-1]-1]
            n = len(cl)
            for i in range(H, n-H, H):
                past = cl[i]/cl[i-H]-1; fwd = cl[i+H]/cl[i]-1
                rr = r1[i-H+1:i+1]
                g = np.sort(rr[rr>0])[::-1]; l = np.sort(rr[rr<0])
                rows.append(dict(coin=c, w=w, past=past, fwd=fwd,
                    t3g=g[:3].sum() if len(g) else 0, t3l=l[:3].sum() if len(l) else 0))
            ts = pd.to_datetime(b["timestamp"])
            f = np.r_[cl[1:]/cl[:-1]-1, np.nan]
            hr.append(pd.DataFrame({"coin":c,"yr":ts.dt.year.values,"h":ts.dt.hour.values,"wd":ts.dt.weekday.values,"r":f}))
            pos = b["postRebalance_current_allocation"].values.astype(float)
            tv = b["total_portfolio_value"].values.astype(float); pv = b["postRebalance_total_value"].values.astype(float)
            fee = (tv-pv)/tv
            gross = pos*f
            bk.append(pd.DataFrame({"coin":c,"w":w,"fee":fee,"gross":gross,"turn":np.abs(b["allocation_change"].values.astype(float)) if "allocation_change" in b else np.nan}))
    g = pd.DataFrame(rows); g["ex"] = g.fwd - g.groupby("coin").fwd.transform("mean")
    def reg(d, x):
        d = d.dropna(subset=[x,"ex"])
        r = stats.linregress(d[x], d["ex"]); return pd.Series({"slope":r.slope,"t":r.slope/r.stderr,"n":len(d)})
    dn = g[g.past<0].copy(); dn["ls"] = dn.t3l/dn.past
    out["falls: ex on top3-loss share, by coin"] = dn.groupby("coin").apply(lambda d: reg(d,"ls"))
    out["falls: ex on top3-loss share, pooled"] = reg(dn,"ls")
    dn["half"] = (dn.w.str[1:].astype(int) > 12).astype(int)
    out["falls: by window half"] = dn.groupby("half").apply(lambda d: reg(d,"ls"))
    out["falls: ex on ls controlling past (resid)"] = reg(dn.assign(ls2=dn.ls - np.poly1d(np.polyfit(dn.past,dn.ls,1))(dn.past)),"ls2")
    up = g[g.past>0].copy(); up["gs"] = up.t3g/up.past
    out["rises: ex on top3-gain share, by coin"] = up.groupby("coin").apply(lambda d: reg(d,"gs"))
    hr = pd.concat(hr).dropna()
    hr["late"] = hr.h.isin([20,21]).astype(int); hr["fri"] = (hr.wd==4).astype(int)
    def diff(d, col):
        a = d[d[col]==1].r; b_ = d[d[col]==0].r
        return pd.Series({"diff":a.mean()-b_.mean(),"t":stats.ttest_ind(a,b_,equal_var=False)[0],"n":len(a)})
    out["hour20-21 minus rest, by coin"] = hr.groupby("coin").apply(lambda d: diff(d,"late"))
    out["hour20-21 minus rest, by year"] = hr.groupby("yr").apply(lambda d: diff(d,"late"))
    out["friday minus rest, by coin"] = hr.groupby("coin").apply(lambda d: diff(d,"fri"))
    out["friday minus rest, by year"] = hr.groupby("yr").apply(lambda d: diff(d,"fri"))
    bk = pd.concat(bk)
    out["book per bar: gross, fee, turnover"] = bk[["gross","fee","turn"]].mean()
    return out
