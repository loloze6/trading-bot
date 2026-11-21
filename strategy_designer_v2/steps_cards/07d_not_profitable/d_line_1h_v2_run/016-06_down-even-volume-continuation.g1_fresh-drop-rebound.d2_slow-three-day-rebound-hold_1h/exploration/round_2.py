def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    G = []
    for c in data["bars"]:
        cm = []
        for w, b in data["bars"][c].items():
            b = b.reset_index(drop=True)
            s = b["close"]; n = len(s)
            r24p = s/s.shift(24)-1; r72p = s/s.shift(72)-1
            lr = np.log(s).diff()
            volratio = lr.rolling(24).std()/lr.rolling(720).std()
            vr24 = (b["volume"]/b["volume"].rolling(720,min_periods=100).mean()).rolling(24).mean()
            z24 = (r24p - r24p.rolling(60*24, min_periods=200).mean())/r24p.rolling(60*24,min_periods=200).std()
            f72 = s.shift(-72)/s-1
            idx = np.arange(0, n, 72)
            G.append(pd.DataFrame({"coin":c,"win":w,"fc":b["forecast"].values[idx],
                "alloc":b["postRebalance_current_allocation"].fillna(0).values[idx],
                "r24p":r24p.values[idx],"r72p":r72p.values[idx],"z24":z24.values[idx],
                "volratio":volratio.values[idx],"vr24":vr24.values[idx],"f72":f72.values[idx]}))
    G = pd.concat(G)
    G["ex72"] = G.f72 - G.groupby("coin").f72.transform("mean")
    A = G[(G.fc>0)].dropna(subset=["ex72","vr24","volratio"]).copy()
    def summ(g):
        return pd.Series({"n":len(g),"ex72":g.ex72.mean(),"t":stats.ttest_1samp(g.ex72,0).statistic if len(g)>2 else np.nan})
    A["fhi"] = (A.fc >= A.fc.median()).astype(int)
    A["vhi"] = (A.vr24 >= A.vr24.median()).astype(int)
    A["volhi"] = (A.volratio >= A.volratio.median()).astype(int)
    out["fc_half_x_volume_half"] = A.groupby(["fhi","vhi"]).apply(summ)
    out["fc_half_x_volatility_half"] = A.groupby(["fhi","volhi"]).apply(summ)
    # graded combination: 1-day fall size times volume ratio
    A["combo"] = (-A.r24p).clip(lower=0)*A.vr24
    A["cq"] = pd.qcut(A.combo, 5, labels=False, duplicates="drop")
    out["by_fall_x_volume_quint"] = A.groupby("cq").apply(summ)
    out["corr_ex72_with"] = pd.Series({"fc":stats.spearmanr(A.fc,A.ex72).correlation,
        "-r24p":stats.spearmanr(-A.r24p,A.ex72).correlation,
        "vr24":stats.spearmanr(A.vr24,A.ex72).correlation,
        "volratio":stats.spearmanr(A.volratio,A.ex72).correlation,
        "combo":stats.spearmanr(A.combo,A.ex72).correlation})
    # all grid bars with r72p<0 and r24p<0 regardless of forecast, by volume quartile
    B = G[(G.r72p<0)&(G.r24p<0)].dropna(subset=["ex72","vr24"]).copy()
    B["vq"] = pd.qcut(B.vr24,4,labels=False)
    out["all_down_by_volume_quart"] = B.groupby("vq").apply(summ)
    # book: market-rise part vs timing
    rows=[]
    for c in data["days"]:
        for w,d in data["days"][c].items():
            b = data["bars"][c][w]
            al = b.groupby(pd.to_datetime(b["timestamp"]).dt.floor("D"))["postRebalance_current_allocation"].mean().fillna(0)
            d = d.copy(); d["coin"]=c; d["al"]=al.reindex(pd.to_datetime(d["day"]).dt.floor("D")).values
            rows.append(d)
    D = pd.concat(rows)
    D["mu"] = D.groupby("coin").coin_return.transform("mean")
    D["mkt"] = D.al*D.mu
    out["book_mean_vs_market_part"] = pd.Series({"book_mean":D.book_return.mean(),"market_part":D.mkt.mean(),"timing":D.book_return.mean()-D.mkt.mean(),"mean_alloc":D.al.mean()})
    return out
