def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # coin mean daily return over all windows
    rows = []
    side_rows = []
    fee_rows = []
    fwd_rows = []
    for c in bars:
        allret = []
        for w, b in bars[c].items():
            r = b["close"].pct_change().shift(-1)
            allret.append(r.dropna())
        mu = pd.concat(allret).mean()
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            pos = b["postRebalance_current_allocation"].fillna(0)
            r1 = b["close"].shift(-1)/b["close"]-1
            g = pos*r1
            fee = (b["total_portfolio_value"] - b["postRebalance_total_value"])/b["total_portfolio_value"]
            side = np.where(pos>0.001,"long",np.where(pos<-0.001,"short","flat"))
            df = pd.DataFrame({"coin":c,"w":w,"side":side,"gain":g,"timing":pos*(r1-mu),"drift":pos*mu,"fee":fee,"reg":b["regime"],"fc":b["forecast"],"absdpos":(pos-b["previous_allocation"].fillna(0)).abs()})
            side_rows.append(df)
            # forward returns at several horizons, non-overlapping per h, trending
            for h in [1,3,7,14]:
                idx = np.arange(0,len(b)-h,h)
                fr = b["close"].values[idx+h]/b["close"].values[idx]-1
                fwd_rows.append(pd.DataFrame({"coin":c,"h":h,"fc":b["forecast"].values[idx],"reg":b["regime"].values[idx],"fr":fr,"z":b["debug_info.components.zday.last_history_value"].values[idx]}))
    S = pd.concat(side_rows)
    agg = S.groupby("side").agg(n=("gain","size"),gain_mean=("gain","mean"),drift=("drift","mean"),timing=("timing","mean"),fee=("fee","mean"))
    out["by side per bar"] = agg
    out["overall per bar"] = pd.Series({"gain":S.gain.mean(),"fee":S.fee.mean(),"net":(S.gain-S.fee).mean(),"drift":S.drift.mean(),"timing":S.timing.mean(),"turnover":S.absdpos.mean()})
    out["by coin"] = S.groupby("coin").agg(gain=("gain","mean"),fee=("fee","mean"),drift=("drift","mean"),timing=("timing","mean"))
    F = pd.concat(fwd_rows)
    F = F[F.reg=="trending"].dropna(subset=["fr"])
    res = []
    for h, g in F.groupby("h"):
        g = g.copy()
        g["ex"] = g.fr - g.groupby("coin").fr.transform("mean")
        sl = stats.linregress(g.fc, g.ex)
        pos = g[g.fc>0]; neg = g[g.fc<0]
        res.append({"h":h,"n":len(g),"slope":sl.slope,"t":sl.slope/sl.stderr,"mean_fr_fc>0":pos.fr.mean(),"mean_fr_fc<0":neg.fr.mean(),"n_pos":len(pos),"n_neg":len(neg),"corr_fc_z":np.corrcoef(g.fc.fillna(0),g.z.fillna(0))[0,1]})
    out["trending fwd by horizon"] = pd.DataFrame(res)
    # forecast quintiles at h=7
    g = F[F.h==7].copy()
    g["q"] = pd.qcut(g.fc.rank(method="first"),5,labels=False)
    out["h7 by fc quintile"] = g.groupby("q").agg(n=("fr","size"),fc=("fc","mean"),fr=("fr","mean"))
    # regime share & book by regime
    out["by regime"] = S.groupby("reg").agg(n=("gain","size"),gain=("gain","mean"),fee=("fee","mean"))
    D = pd.concat([d.assign(coin=c) for c in days for d in days[c].values()])
    out["days"] = pd.Series({"book_mean":D.book_return.mean(),"coin_mean":D.coin_return.mean()})
    return out
