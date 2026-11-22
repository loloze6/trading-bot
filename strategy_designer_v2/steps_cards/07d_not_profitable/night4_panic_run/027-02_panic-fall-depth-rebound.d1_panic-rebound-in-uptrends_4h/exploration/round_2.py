import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    # drift per coin: non-overlapping 84-bar returns over all windows
    drift = {}; usual = {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for g in range(0, len(cl)-84, 84):
                rs.append(cl[g+84]/cl[g]-1)
        drift[c] = np.mean(rs); usual[c] = np.std(rs)
    out["drift_usual"] = pd.DataFrame({"drift":drift,"usual":usual})
    # book: mean daily return, in vs out, market part
    dl = []
    for c in days:
        for w, d in days[c].items():
            dd = d.copy(); dd["coin"]=c; dd["win"]=w; dl.append(dd)
    D = pd.concat(dl)
    # daily allocation from bars (mean of the day)
    al = []
    for c in bars:
        for w, b in bars[c].items():
            bb = b[["timestamp","postRebalance_current_allocation"]].copy()
            bb["day"] = pd.to_datetime(bb["timestamp"]).dt.floor("D")
            a = bb.groupby("day")["postRebalance_current_allocation"].mean().reset_index()
            a["coin"]=c; a["win"]=w; al.append(a)
    A = pd.concat(al)
    D["day"] = pd.to_datetime(D["day"]).dt.floor("D") if not np.issubdtype(D["day"].dtype, np.datetime64) else D["day"].dt.floor("D")
    A["day"] = pd.to_datetime(A["day"])
    try:
        A["day"] = A["day"].dt.tz_localize(None)
        D["day"] = D["day"].dt.tz_localize(None)
    except Exception: pass
    M = D.merge(A, on=["coin","win","day"], how="left")
    M["in"] = M["postRebalance_current_allocation"].abs()>1e-9
    out["book_day_in_vs_out"] = M.groupby("in")["book_return"].agg(["count","mean"])
    cm = M.groupby("coin")["coin_return"].mean()
    M["mkt_part"] = M["postRebalance_current_allocation"]*M["coin"].map(cm)
    out["book_mean_split"] = pd.Series({"book_mean":M["book_return"].mean(),"market_part":M["mkt_part"].mean(),
        "share_days_in":M["in"].mean()})
    # cases: first bar in each 84-cell with ratio>=k and fall<0, graded
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            rng = (b["high"]-b["low"])/b["close"]
            ratio = rng.rolling(6).mean()/rng.rolling(180).mean()
            fall6 = b["close"]/b["close"].shift(6)-1
            us6 = fall6.abs().rolling(180).mean()
            r540 = b["close"]/b["close"].shift(540)-1
            r84b = b["close"]/b["close"].shift(84)-1
            cl = b["close"].values; n=len(b)
            for H,lab in [(84,"14d"),(42,"7d")]:
                for g0 in range(0, n-84, 84):
                    for k in [2,3]:
                        idx = np.where((ratio.values[g0:g0+84]>=k)&(fall6.values[g0:g0+84]<0))[0]
                        if len(idx)==0: continue
                        i = g0+idx[0]
                        if i+H>=n: continue
                        recs.append(dict(coin=c,H=lab,k=k,fall=-fall6.iloc[i]/us6.iloc[i],ratio=ratio.iloc[i],
                            r540=r540.iloc[i], r84b=r84b.iloc[i],
                            unus=cl[i+H]/cl[i]-1-drift[c]*(H/84)))
    R = pd.DataFrame(recs).dropna(subset=["unus","fall"])
    def summ(g):
        n=len(g); m=g["unus"].mean(); s=g["unus"].std()
        return pd.Series({"n":n,"mean_unus":m,"t":m/(s/np.sqrt(n)) if n>2 else np.nan,
                          "corr_fall":g["unus"].corr(g["fall"]),"corr_ratio":g["unus"].corr(g["ratio"])})
    out["panics_all_trends"] = R.groupby(["k","H"]).apply(summ)
    R2 = R[(R.k==2)&(R.H=="14d")].copy()
    R2["fallq"]=pd.qcut(R2["fall"],4,labels=False)
    out["k2_14d_by_fall_quartile"] = R2.groupby("fallq").apply(summ)
    R2["r540q"]=pd.qcut(R2["r540"].rank(method="first"),4,labels=False)
    out["k2_14d_by_90d_quartile"] = R2.groupby("r540q").apply(summ)
    R2["r84q"]=pd.qcut(R2["r84b"].rank(method="first"),4,labels=False)
    out["k2_14d_by_prior14d_quartile"] = R2.groupby("r84q").apply(summ)
    R3 = R[(R.k==3)&(R.H=="14d")]
    out["k3_14d_by_coin"] = R3.groupby("coin").apply(summ)
    return out
