def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # 1. weekday effect per coin, daily returns (coin_return), each coin separately
    dl = []
    for coin, wins in days.items():
        for w, d in wins.items():
            d = d.copy(); d["coin"]=coin; d["w"]=w; dl.append(d)
    D = pd.concat(dl)
    D["wd"] = pd.to_datetime(D["day"]).dt.weekday
    D["yr"] = pd.to_datetime(D["day"]).dt.year
    def tt(s):
        s = s.dropna(); return s.mean()/(s.std()/np.sqrt(len(s))) if len(s)>2 else np.nan
    D["coin_mean"] = D.groupby("coin")["coin_return"].transform("mean")
    D["ex1"] = D["coin_return"] - D["coin_mean"]
    out["sat_minus_other_t_by_coin"] = D.groupby("coin").apply(lambda d: pd.Series({
        "sat_mean": d.loc[d.wd==5,"coin_return"].mean(),
        "other_mean": d.loc[d.wd!=5,"coin_return"].mean(),
        "welch_t": stats.ttest_ind(d.loc[d.wd==5,"coin_return"].dropna(), d.loc[d.wd!=5,"coin_return"].dropna(), equal_var=False).statistic}))
    # Saturday by year, pooled (cross-coin mean per day first, to avoid inflating)
    M = D.groupby(["w","day","wd","yr"])["ex1"].mean().reset_index()
    out["sat_ex_by_year_coinavg"] = M[M.wd==5].groupby("yr")["ex1"].agg(["count","mean", tt])
    out["weekday_ex_coinavg"] = M.groupby("wd")["ex1"].agg(["count","mean", tt])
    # 2. Non-overlapping: after a daily move sized by vol, next 5 days, per coin grid of 5
    rows = []
    for coin, wins in bars.items():
        for w, df in wins.items():
            c = df["close"].astype(float).values; n = len(c)
            lr = np.diff(np.log(c))
            dh = df["debug_info.components.dist_high.last_history_value"].astype(float).values
            for h in (5, 10, 20):
                for i in range(0, n-h, h):
                    if i < 31: continue
                    sd = np.std(lr[i-31:i-1])
                    z1 = lr[i-1]/sd if sd>0 else np.nan
                    z5 = np.log(c[i]/c[i-5])/(sd*np.sqrt(5)) if sd>0 else np.nan
                    rows.append(dict(coin=coin, w=w, h=h, z1=z1, z5=z5, r=c[i+h]/c[i]-1, dh=dh[i]))
    G = pd.DataFrame(rows)
    G["ex"] = G["r"] - G.groupby(["coin","h"])["r"].transform("mean")
    G["exz"] = G["ex"]/G.groupby(["coin","h"])["r"].transform("std")
    res = []
    for h in (5,10,20):
        for col in ("z1","z5"):
            d = G[(G.h==h)].dropna(subset=[col,"exz"])
            sl = stats.linregress(d[col], d["exz"])
            res.append(dict(h=h, x=col, n=len(d), slope=sl.slope, t=sl.slope/sl.stderr,
                            absx_t=stats.linregress(d[col].abs(), d["exz"]).slope/stats.linregress(d[col].abs(), d["exz"]).stderr))
    out["reg_nonoverlap"] = pd.DataFrame(res)
    # per coin sign of z1 slope at h=20 and h=5
    pc = []
    for h in (5,20):
        for coin, d in G[G.h==h].dropna(subset=["z1","exz"]).groupby("coin"):
            sl = stats.linregress(d["z1"], d["exz"]); pc.append(dict(h=h, coin=coin, n=len(d), t=sl.slope/sl.stderr))
    out["z1_slope_by_coin"] = pd.DataFrame(pc)
    # 3. distance from high bins (raw dist), 20d
    d = G[G.h==20].dropna(subset=["dh"]).copy()
    d["b"] = pd.cut(d["dh"], [-1e9,-40,-25,-15,-8,-3,0,1e9])
    out["dist_high_bins_20d"] = d.groupby("b").agg(n=("ex","size"), mean_ex=("ex","mean"), mean_exz=("exz","mean"))
    out["dist_high_raw_desc"] = d["dh"].describe()
    # 4. book: what precedes largest book loss days
    B = D.groupby(["w","day"]).agg(book=("book_return","mean"), coin=("coin_return","mean")).dropna().reset_index()
    out["book_vs_coin_corr"] = float(B["book"].corr(B["coin"]))
    q = B["book"].quantile([0.02,0.98])
    out["book_tails_coin_mean"] = pd.Series({"worst2pct_coin": B.loc[B.book<=q.iloc[0],"coin"].mean(),
                                            "best2pct_coin": B.loc[B.book>=q.iloc[1],"coin"].mean(),
                                            "n_tail": int((B.book<=q.iloc[0]).sum())})
    return out
