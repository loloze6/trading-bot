def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars, days, trades = data["bars"], data["days"], data["trades"]
    out = {}
    # coin mean daily return over windows (visible)
    rows = []; book_rows = []
    for c in days:
        allr = pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu = allr.mean()
        for w in days[c]:
            b = bars[c][w].copy()
            b["d"] = pd.to_datetime(b["timestamp"]).dt.floor("D")
            b["yr"] = pd.to_datetime(b["timestamp"]).dt.year
            b["r1"] = b["close"].shift(-1) / b["close"] - 1
            b["pos"] = b["postRebalance_current_allocation"].fillna(0)
            b["g"] = b["pos"] * b["r1"]
            b["mkt"] = b["pos"] * mu
            b["coin"] = c; b["w"] = w
            rows.append(b[["coin","w","yr","pos","g","mkt","r1"]])
            d = days[c][w][["day","book_return","coin_return"]].copy()
            d["coin"]=c; d["w"]=w; d["yr"]=pd.to_datetime(d["day"]).dt.year
            book_rows.append(d)
    B = pd.concat(rows).dropna(subset=["r1"])
    D = pd.concat(book_rows).dropna()
    out["gain_decomp_by_coin"] = B.groupby("coin").agg(mean_gain=("g","mean"), market_part=("mkt","mean"), share_in=("pos", lambda x:(x!=0).mean()))
    out["gain_decomp_by_window"] = B.groupby("w").agg(mean_gain=("g","mean"), market_part=("mkt","mean"), coin_r=("r1","mean"))
    out["gain_decomp_by_year"] = B.groupby("yr").agg(mean_gain=("g","mean"), market_part=("mkt","mean"), coin_r=("r1","mean"))
    out["total"] = pd.Series({"mean_gain":B.g.mean(),"market_part":B.mkt.mean(),
                              "timing":B.g.mean()-B.mkt.mean()})
    # trades concentration
    T = pd.concat([trades[c][w].assign(coin=c) for c in trades for w in trades[c] if len(trades[c][w])])
    p = T["net_profit_loss_percent"].sort_values(ascending=False)
    out["trades"] = pd.Series({"n":len(p),"mean":p.mean(),"median":p.median(),"win":(p>0).mean(),
        "sum":p.sum(),"top5_sum":p.head(5).sum(),"top10_sum":p.head(10).sum(),
        "mean_days":T["duration_minutes"].mean()/1440})
    # forward returns at horizons, by group: active (forecast>0), chop-regime but forecast 0, others with ret7>0
    res = []
    for c in bars:
        allc = []
        for w in bars[c]:
            b = bars[c][w].reset_index(drop=True)
            cl = b["close"]
            er = (cl - cl.shift(30)).abs() / cl.diff().abs().rolling(30).sum()
            r7 = cl/cl.shift(7)-1; r30 = cl/cl.shift(30)-1
            vol = cl.pct_change().rolling(30).std()
            for h in [1,3,7,14,21]:
                fwd = cl.shift(-h)/cl-1
                idx = np.arange(0, len(b), h)
                df = pd.DataFrame({"h":h,"fwd":fwd.iloc[idx].values,"fc":b["forecast"].iloc[idx].values,
                    "er":er.iloc[idx].values,"r7":r7.iloc[idx].values,"r30":r30.iloc[idx].values,
                    "z7":(r7/(vol*np.sqrt(7))).iloc[idx].values,"coin":c})
                allc.append(df)
        A = pd.concat(allc).dropna(subset=["fwd"])
        for h in [1,3,7,14,21]:
            a = A[A.h==h]; mu = a.fwd.mean(); a = a.assign(u=a.fwd-mu)
            res.append(a)
    R = pd.concat(res)
    def grp(r):
        if r.fc>0: return "active"
        if r.er<=0.3 and r.r30>0 and r.r7>0: return "chop_up_inactive"
        if r.er<=0.3 and r.r7<0: return "chop_down7"
        if r.er>0.3 and r.r7>0 and r.r30>0: return "trend_up"
        if r.er>0.3 and r.r30<0: return "trend_down"
        return "other"
    R["grp"] = R.apply(grp, axis=1)
    g = R.groupby(["h","grp"])["u"].agg(["mean","count",lambda x: x.mean()/x.std()*np.sqrt(len(x))])
    g.columns=["mean_unusual","n","t"]
    out["unusual_by_horizon_group"] = g
    # within chop up regime, unusual 7d by z7 tercile; and active by coin
    a7 = R[(R.h==7)&(R.er<=0.3)&(R.r30>0)&(R.r7>0)].copy()
    a7["q"] = pd.qcut(a7.z7, 3, labels=["lo","mid","hi"])
    out["chopup_7d_by_z7_tercile"] = a7.groupby("q")["u"].agg(["mean","count"])
    out["active_7d_by_coin"] = R[(R.h==7)&(R.grp=="active")].groupby("coin")["u"].agg(["mean","count"])
    # r30 graded: all bars, 7d unusual by r30 quintile
    a = R[R.h==7].dropna(subset=["r30"]).copy()
    a["q30"]=pd.qcut(a.r30,5,labels=False)
    out["all_7d_by_r30_quintile"]=a.groupby("q30")["u"].agg(["mean","count"])
    a["qer"]=pd.qcut(a.er,3,labels=["chop","mid","eff"])
    out["all_7d_by_er_and_r7sign"]=a.groupby(["qer",a.r7>0])["u"].agg(["mean","count"])
    return out
