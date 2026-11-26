def explore(data):
    import numpy as np, pandas as pd
    bars, days = data["bars"], data["days"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            b["ts"] = pd.to_datetime(b["timestamp"])
            b["day"] = b["ts"].dt.floor("D")
            b["pos"] = b["postRebalance_current_allocation"].shift(1)
            b["r1"] = b["close"].pct_change()
            b["ret30"] = b["close"] / b["close"].shift(30) - 1
            b["ret30_prev"] = b["ret30"].shift(1)
            b["fc_prev"] = b["forecast"].shift(1)
            b["bk"] = b["postRebalance_total_value"].pct_change()
            b["coin"] = c; b["win"] = w
            rows.append(b[["coin","win","day","pos","r1","ret30","ret30_prev","fc_prev","bk","close","forecast"]])
    B = pd.concat(rows, ignore_index=True)
    mu = B.groupby("coin")["r1"].mean()
    B["mu"] = B["coin"].map(mu)
    B["mkt"] = B["pos"] * B["mu"]
    B["timing"] = B["bk"] - B["mkt"]
    B["year"] = B["day"].dt.year
    D = B.dropna(subset=["bk"])
    daily = D.groupby(["win","day"]).agg(bk=("bk","mean"), mkt=("mkt","mean"), tim=("timing","mean"), hold=("r1","mean"))
    s = lambda x: x.mean()/x.std()*np.sqrt(365)
    out["decomp"] = pd.Series({"book_mean": daily.bk.mean(), "mkt_part": daily.mkt.mean(), "timing_part": daily.tim.mean(),
        "t_timing": daily.tim.mean()/(daily.tim.std()/np.sqrt(len(daily))), "sharpe_book": s(daily.bk), "sharpe_timing": s(daily.tim), "ndays": len(daily)})
    # per coin contribution
    n = len(daily)
    cc = D.groupby("coin").agg(sum_bk=("bk","sum"), sum_tim=("timing","sum"), n=("bk","size"), meanpos=("pos","mean"))
    # contribution approx: each coin's days weighted by 1/ncoins of the day
    nc = D.groupby(["win","day"])["coin"].transform("size")
    D2 = D.assign(wbk=D.bk/nc, wtim=D.timing/nc)
    cc["contrib_share"] = D2.groupby("coin")["wbk"].sum()/D2["wbk"].sum()
    cc["timing_contrib_share"] = D2.groupby("coin")["wtim"].sum()/D2["wtim"].sum()
    out["by_coin"] = cc.round(4)
    dy = daily.reset_index(); dy["year"] = pd.to_datetime(dy.day).dt.year
    out["by_year"] = dy.groupby("year").agg(bk=("bk","mean"), mkt=("mkt","mean"), tim=("tim","mean"), hold=("hold","mean"), n=("bk","size"))
    out["by_window"] = dy.groupby("win").agg(bk=("bk","mean"), tim=("tim","mean"), hold=("hold","mean"), n=("bk","size")).sort_values("tim")
    # state of the day: in position with ret30 & fc
    Dp = D[D.pos.abs()>1e-9]
    Dp = Dp.assign(r30q=pd.qcut(Dp.ret30_prev, 4, labels=False, duplicates="drop"))
    out["in_pos_by_ret30_quartile"] = Dp.groupby("r30q").agg(bk=("bk","mean"), r1=("r1","mean"), tim=("timing","mean"), n=("bk","size"), r30=("ret30_prev","median"))
    # forward returns at horizons, groups
    res = []
    for h in [1,3,5,10,20]:
        rr = []
        for (c,w), g in B.groupby(["coin","win"]):
            g = g.reset_index(drop=True)
            fwd = g["close"].shift(-h)/g["close"]-1
            idx = np.arange(0, len(g), h)
            sub = pd.DataFrame({"coin":c,"day":g.day.iloc[idx].values,"fwd":fwd.iloc[idx].values,
                                "ret30":g.ret30.iloc[idx].values,"fc":g.forecast.iloc[idx].values})
            rr.append(sub)
        R = pd.concat(rr).dropna()
        dr = R.groupby("coin")["fwd"].mean()
        R["ab"] = R.fwd - R.coin.map(dr)
        R["grp"] = np.where(R.ret30<=0, "ret30<=0", np.where(R.fc>0, "ret30>0_streak", "ret30>0_nostreak"))
        for gname, g in R.groupby("grp"):
            pd_ = g.groupby("day")["ab"].sum(); Dn = len(pd_)
            m = g.ab.mean(); se = np.sqrt((pd_**2).sum()*Dn/(Dn-1))/len(g)
            res.append({"h":h,"grp":gname,"n":len(g),"days":Dn,"mean_ab":m,"t":m/se,"mean_tot":g.fwd.mean()})
        # graded by ret30 among ret30>0
        pos = R[R.ret30>0].copy()
        pos["q"] = pd.qcut(pos.ret30, 3, labels=["lo","mid","hi"])
        for q, g in pos.groupby("q", observed=True):
            pd_ = g.groupby("day")["ab"].sum(); Dn=len(pd_)
            m=g.ab.mean(); se=np.sqrt((pd_**2).sum()*Dn/(Dn-1))/len(g)
            res.append({"h":h,"grp":"ret30>0 tercile "+q,"n":len(g),"days":Dn,"mean_ab":m,"t":m/se,"mean_tot":g.fwd.mean()})
    out["fwd"] = pd.DataFrame(res).round(4)
    # trades concentration
    T = pd.concat([t.assign(coin=c) for c in data["trades"] for w,t in data["trades"][c].items()], ignore_index=True)
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n":len(p),"sum":p.sum(),"top10_sum":p.head(10).sum(),"top5pct_sum":p.head(int(len(p)*0.05)).sum(),"winrate":(p>0).mean(),"median":p.median(), "mean_dur_days":T.duration_minutes.mean()/1440})
    return out
