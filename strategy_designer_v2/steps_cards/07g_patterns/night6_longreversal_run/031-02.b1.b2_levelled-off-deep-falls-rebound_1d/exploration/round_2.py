import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; out = {}
    def tcl(df, col, key="ts"):
        # day-clustered t: sum deviations per day
        m = df[col].mean()
        s = (df[col]-m).groupby(df[key]).sum()
        se = np.sqrt((s**2).sum())/len(df)
        return m/se, df[key].nunique()
    def grid(h, L):
        recs = []
        for c in bars:
            fr = []
            for w, b in bars[c].items():
                cl = b["close"].values
                for i in range(0, len(cl)-h, h):
                    fr.append(cl[i+h]/cl[i]-1)
            fr = np.array(fr); drift = fr.mean(); sd = fr.std()
            for w, b in bars[c].items():
                cl = b["close"].values; ts = pd.to_datetime(b["timestamp"]).values
                lr = np.log(cl[1:]/cl[:-1])
                for i in range(0, len(cl)-h, h):
                    if i < max(L, 20): continue
                    past = cl[i]/cl[i-L]-1
                    v = np.std(lr[i-20:i])
                    pz = np.log(cl[i]/cl[i-L])/(v*np.sqrt(L*1.0))
                    recs.append((c, w, ts[i], past, pz, cl[i+h]/cl[i]-1-drift, pd.Timestamp(ts[i]).year))
        return pd.DataFrame(recs, columns=["coin","win","ts","past","pz","ex","yr"])
    # 1-day reversal, scaled by own 20-day vol
    g = grid(1, 1)
    g["d"] = pd.qcut(g.pz, 10, labels=False)
    tab = g.groupby("d").agg(n=("ex","size"), pz=("pz","mean"), ex=("ex","mean"))
    tab["t_cl"] = [tcl(g[g.d==k], "ex")[0] for k in tab.index]
    out["r1_deciles_volscaled"] = tab
    r = stats.spearmanr(g.pz, g.ex)
    out["r1_rho"] = pd.Series({"rho": r[0], "n": len(g), "days": g.ts.nunique()})
    low = g[g.d<=1]
    out["r1_low20_by_year"] = low.groupby("yr").ex.agg(["size","mean"])
    out["r1_low20_by_coin"] = low.groupby("coin").ex.agg(["size","mean"])
    # slope of ex on pz, day-clustered via daily cross-section means of pz*ex
    # 30-day momentum
    for h, L in [(30,30),(7,30),(14,30)]:
        gg = grid(h, L)
        gg["q"] = pd.qcut(gg.pz, 5, labels=False)
        tb = gg.groupby("q").agg(n=("ex","size"), pz=("pz","mean"), ex=("ex","mean"))
        tb["t_cl"] = [tcl(gg[gg.q==k], "ex")[0] for k in tb.index]
        hi = gg[gg.q==4].ex; lo = gg[gg.q==0].ex
        tb.loc["hi-lo"] = [len(gg), np.nan, hi.mean()-lo.mean(), stats.ttest_ind(hi, lo, equal_var=False).statistic]
        out[f"mom{L}_next{h}"] = tb
        gg["hl"] = np.sign(gg.pz)*gg.ex
        out[f"mom{L}_next{h}_signed_by_year"] = gg.groupby("yr").hl.agg(["size","mean"])
    # weekday with day-clustered t (mean across coins per day)
    dd = []
    for c in data["days"]:
        for w, d in data["days"][c].items():
            x = d.copy(); x["coin"] = c; dd.append(x)
    D = pd.concat(dd).dropna(subset=["coin_return"])
    D["ex"] = D.coin_return - D.groupby("coin").coin_return.transform("mean")
    dm = D.groupby("day").ex.mean().reset_index()
    dm["wd"] = pd.to_datetime(dm["day"]).dt.weekday; dm["yr"] = pd.to_datetime(dm["day"]).dt.year
    out["weekday_daymean"] = dm.groupby("wd").ex.agg(["size","mean", lambda s: stats.ttest_1samp(s,0).statistic])
    out["thu_sat_by_year"] = dm[dm.wd.isin([3,5])].groupby(["yr","wd"]).ex.mean().unstack()
    # shorts in deep falls: trade outcomes by entry forecast
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): tt = t.copy(); tt["coin"] = c; tr.append(tt)
    T = pd.concat(tr)
    T["fq"] = pd.cut(T.entry_forecast, [-21,-10,-5,0,5,21])
    out["trades_by_entry_fc"] = T.groupby("fq").net_profit_loss_percent.agg(["size","mean","median"])
    return out
