import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    bars = data["bars"]
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            df = df.reset_index(drop=True)
            c = df["close"].values
            n = len(df)
            r1 = np.r_[np.nan, c[1:]/c[:-1]-1]
            vol20 = pd.Series(r1).rolling(20, min_periods=15).std().values
            for h in (1, 3, 10):
                pass
            for i in range(n):
                rows.append(dict(coin=coin, win=w, pos=i, n=n,
                    f28=df["debug_info.components.fall28.last_history_value"].iloc[i],
                    nl60=df["debug_info.components.near_low60.last_history_value"].iloc[i],
                    fc=df["forecast"].iloc[i], alloc=df["postRebalance_current_allocation"].iloc[i],
                    r1=r1[i], vol20=vol20[i], svol=df["sizing_realised_vol"].iloc[i],
                    wd=pd.Timestamp(df["timestamp"].iloc[i]).weekday(),
                    f1=(c[i+1]/c[i]-1) if i+1<n else np.nan,
                    f3=(c[i+3]/c[i]-1) if i+3<n else np.nan,
                    f10=(c[i+10]/c[i]-1) if i+10<n else np.nan))
    d = pd.DataFrame(rows)
    out = {}
    for h, col in ((10,"f10"),(3,"f3"),(1,"f1")):
        g = d[d["pos"] % h == 0].copy()
        drift = g.groupby("coin")[col].transform("mean")
        g["u"+col] = g[col] - drift
        d.loc[g.index, "u"+col] = g["u"+col]
        d.loc[g.index, "grid"+str(h)] = 1
    g10 = d[d["grid10"]==1].dropna(subset=["uf10"])
    # 28-day return quintiles (both signs) per coin, pooled
    g10["q28"] = g10.groupby("coin")["f28"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["f10_by_q28"] = g10.groupby("q28").agg(mean_f28=("f28","mean"), mean_u=("uf10","mean"), n=("uf10","size"),
        t=("uf10", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    g10["qnl"] = g10.groupby("coin")["nl60"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["f10_by_qnl60"] = g10.groupby("qnl").agg(mean_nl=("nl60","mean"), mean_u=("uf10","mean"), n=("uf10","size"),
        t=("uf10", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    g10["qv"] = g10.groupby("coin")["vol20"].transform(lambda s: pd.qcut(s.rank(method="first"),5,labels=False))
    out["f10_by_vol"] = g10.dropna(subset=["qv"]).groupby("qv").agg(mean_v=("vol20","mean"), mean_u=("uf10","mean"), mean_raw=("f10","mean"), n=("uf10","size"),
        t=("uf10", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    # per-coin slope of uf10 on standardized f28
    res = []
    for coin, gg in g10.groupby("coin"):
        x = (gg["f28"]-gg["f28"].mean())/gg["f28"].std()
        s = stats.linregress(x, gg["uf10"]); 
        x2 = (gg["nl60"]-gg["nl60"].mean())/gg["nl60"].std()
        s2 = stats.linregress(x2, gg["uf10"])
        res.append(dict(coin=coin, n=len(gg), slope28=s.slope, t28=s.slope/s.stderr, slopeNL=s2.slope, tNL=s2.slope/s2.stderr))
    out["per_coin_slopes"] = pd.DataFrame(res)
    # 1-day return quintiles -> next 3 days and next 1 day
    for h, col in ((3,"uf3"),(1,"uf1")):
        g = d[d["grid"+str(h)]==1].dropna(subset=[col,"r1","vol20"]).copy()
        g["z1"] = g["r1"]/g["vol20"]
        g["qz"] = pd.qcut(g["z1"].rank(method="first"),5,labels=False)
        out["next%d_by_r1z" % h] = g.groupby("qz").agg(mean_z=("z1","mean"), mean_u=(col,"mean"), n=(col,"size"),
            t=(col, lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    g1 = d[d["grid1"]==1].dropna(subset=["uf1"])
    out["next1_by_weekday"] = g1.groupby("wd").agg(mean_u=("uf1","mean"), n=("uf1","size"),
        t=("uf1", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))))
    # book days: before/after largest gains/losses
    dd = []
    for coin, wins in data["days"].items():
        for w, df in wins.items():
            df = df.reset_index(drop=True).copy()
            df["coin"]=coin; df["win"]=w
            df["next_coin"] = df["coin_return"].shift(-1)
            df["next_book"] = df["book_return"].shift(-1)
            dd.append(df)
    D = pd.concat(dd).dropna(subset=["book_return"])
    lo, hi = D["book_return"].quantile([0.02,0.98])
    D["tail"] = np.where(D["book_return"]<=lo,"loss2pct",np.where(D["book_return"]>=hi,"gain2pct","mid"))
    out["book_tails"] = D.groupby("tail").agg(book=("book_return","mean"), coin=("coin_return","mean"),
        next_coin=("next_coin","mean"), next_book=("next_book","mean"), n=("book_return","size"))
    # by window sign of coin 10-day drift: book vs coin by year
    D["year"] = pd.to_datetime(D["day"]).dt.year
    out["by_year"] = D.groupby("year").agg(book=("book_return","mean"), coin=("coin_return","mean"), n=("book_return","size"))
    # active vs flat days
    out["alloc_share_long"] = float((d["alloc"]>0).mean())
    return out
