import pandas as pd, numpy as np

def explore(data):
    bars = data["bars"]; days = data["days"]
    out = {}
    drift = {}; usual = {}
    for c in bars:
        rs = []
        for w, b in bars[c].items():
            cl = b["close"].values
            for g in range(0, len(cl)-84, 84):
                rs.append(cl[g+84]/cl[g]-1)
        drift[c] = float(np.mean(rs)); usual[c] = float(np.std(rs))
    out["drift_usual"] = pd.DataFrame({"drift":drift,"usual":usual})
    # book: share of daily mean from active days, market part
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            try:
                d = days[c][w]
                ts = pd.to_datetime(b["timestamp"], utc=True).dt.floor("D")
                a = b["postRebalance_current_allocation"].groupby(ts.values).mean()
                dd = pd.to_datetime(d["day"], utc=True).dt.floor("D")
                al = pd.Series(a.reindex(dd.values).values, index=d.index)
                rows.append(pd.DataFrame({"coin":c,"br":d["book_return"].values,"cr":d["coin_return"].values,"al":al.values}))
            except Exception as e:
                out["err"] = str(e)[:80]
    if rows:
        M = pd.concat(rows)
        M["in"] = M["al"].abs()>1e-9
        cm = M.groupby("coin")["cr"].mean()
        M["mkt"] = M["al"].fillna(0)*M["coin"].map(cm)
        out["book_split"] = pd.Series({"book_mean":M["br"].mean(),"market_part":M["mkt"].mean(),
            "share_days_in":M["in"].mean(),"mean_on_in_days":M.loc[M["in"],"br"].mean(),"n_days":len(M)})
    # panic cases, all trends, graded
    recs = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            rng = (b["high"]-b["low"])/b["close"]
            ratio = (rng.rolling(6).mean()/rng.rolling(180).mean()).values
            f6 = (b["close"]/b["close"].shift(6)-1)
            us6 = f6.abs().rolling(180).mean().values
            f6 = f6.values
            r540 = (b["close"]/b["close"].shift(540)-1).values
            r84 = (b["close"]/b["close"].shift(84)-1).values
            cl = b["close"].values; n=len(b)
            for g0 in range(0, n-84, 84):
                for k in [2,2.5,3]:
                    idx = np.where((ratio[g0:g0+84]>=k)&(f6[g0:g0+84]<0))[0]
                    if len(idx)==0: continue
                    i = g0+idx[0]
                    for H,lab in [(42,"7d"),(84,"14d")]:
                        if i+H>=n: continue
                        recs.append(dict(coin=c,k=k,H=lab,fall=-f6[i]/us6[i] if us6[i]>0 else np.nan,
                            ratio=ratio[i],r540=r540[i],r84=r84[i],
                            unus=cl[i+H]/cl[i]-1-drift[c]*H/84,
                            st=(cl[i+H]/cl[i]-1-drift[c]*H/84)/usual[c]))
    R = pd.DataFrame(recs).dropna(subset=["unus","fall"])
    def summ(g):
        n=len(g); m=g["unus"].mean(); s=g["unus"].std()
        return pd.Series({"n":n,"mean_unus":m,"t":m/(s/np.sqrt(n)) if n>2 else np.nan,
                          "strength":g["st"].mean(),"corr_fall":g["unus"].corr(g["fall"])})
    out["panics_all_trends"] = R.groupby(["k","H"]).apply(summ)
    R2 = R[(R.k==2)&(R.H=="14d")].copy()
    R2["fallq"]=pd.qcut(R2["fall"].rank(method="first"),4,labels=False)
    out["k2_14d_fall_q"] = R2.groupby("fallq").apply(summ)
    R2["r84q"]=pd.qcut(R2["r84"].rank(method="first"),4,labels=False)
    out["k2_14d_prior14d_q"] = R2.groupby("r84q").apply(summ)
    R2["r540q"]=pd.qcut(R2["r540"].dropna().rank(method="first"),4,labels=False) if R2["r540"].notna().sum()>8 else np.nan
    out["k2_14d_90d_q"] = R2.dropna(subset=["r540q"]).groupby("r540q").apply(summ)
    out["k2_14d_coin"] = R2.groupby("coin").apply(summ)
    return out
