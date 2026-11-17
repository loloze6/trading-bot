def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.reset_index(drop=True).copy()
            cl = d["close"].astype(float)
            d["coin"] = c; d["win"] = w
            d["fwr3"] = cl.shift(-3)/cl - 1
            d["fwr1"] = cl.shift(-1)/cl - 1
            d["fwr7"] = cl.shift(-7)/cl - 1
            d["r1"] = cl.pct_change()
            v = d["volume"].astype(float)
            d["vr"] = v / v.rolling(30, min_periods=10).mean()
            d["pos"] = np.arange(len(d))
            ts = pd.to_datetime(d["timestamp"])
            d["wd"] = ts.dt.weekday; d["yr"] = ts.dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    for h in ["fwr1","fwr3","fwr7"]:
        A[h+"_dm"] = A[h] - A.groupby("coin")[h].transform("mean")
    out = {}
    def slope(x, col, y):
        x = x.dropna(subset=[col, y])
        if len(x) < 30: return pd.Series({"slope": np.nan, "t": np.nan, "n": len(x)})
        r = stats.linregress(x[col], x[y]); return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(x)})
    g3 = A[A["pos"] % 3 == 0].dropna(subset=["fwr3_dm","vr","r1"]).copy()
    g7 = A[A["pos"] % 7 == 0].dropna(subset=["fwr7_dm","vr","r1"]).copy()
    dn3 = g3[g3.r1 < 0]; up3 = g3[g3.r1 > 0]
    out["slope_vr_down_vs_up_h3"] = pd.DataFrame({"down": slope(dn3,"vr","fwr3_dm"), "up": slope(up3,"vr","fwr3_dm"),
        "down_h7": slope(g7[g7.r1<0],"vr","fwr7_dm"), "up_h7": slope(g7[g7.r1>0],"vr","fwr7_dm")}).T
    out["down_vr_by_coin"] = pd.DataFrame({c: slope(dn3[dn3.coin==c],"vr","fwr3_dm") for c in g3.coin.unique()}).T
    out["up_vr_by_coin"] = pd.DataFrame({c: slope(up3[up3.coin==c],"vr","fwr3_dm") for c in g3.coin.unique()}).T
    out["down_vr_by_year"] = pd.DataFrame({y: slope(dn3[dn3.yr==y],"vr","fwr3_dm") for y in sorted(g3.yr.unique())}).T
    # graded: down days, combined size*vr
    dn3 = dn3.copy(); dn3["sv"] = dn3["vr"] * (-dn3["r1"])
    out["down_sv_slope"] = slope(dn3,"sv","fwr3_dm")
    out["down_vr_q"] = dn3.assign(q=pd.qcut(dn3.vr.rank(method="first"),5,labels=False)).groupby("q")["fwr3_dm"].agg(["mean","count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # weekday by year halves & by coin
    g1 = A.dropna(subset=["fwr1_dm"]).copy()
    g1["half"] = np.where(g1.yr <= 2021, "early", "late")
    out["wd_by_half"] = g1.groupby(["wd","half"])["fwr1_dm"].mean().unstack()
    out["wd_by_coin"] = g1.groupby(["wd","coin"])["fwr1_dm"].mean().unstack()
    # vr robustness: excluding top 1% vr
    cut = g3.vr.quantile(0.99)
    out["vr_slope_trim"] = slope(g3[g3.vr < cut], "vr", "fwr3_dm")
    out["vr_slope_rank"] = slope(g3.assign(rk=g3.groupby("coin").vr.rank(pct=True)), "rk", "fwr3_dm")
    return out
