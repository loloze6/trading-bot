def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, df in bars[c].items():
            d = df.reset_index(drop=True).copy()
            cl = d["close"].astype(float)
            d["coin"] = c; d["win"] = w
            d["fwr3"] = cl.shift(-3)/cl - 1
            d["fwr1"] = cl.shift(-1)/cl - 1
            d["fwr5"] = cl.shift(-5)/cl - 1
            d["r1"] = cl.pct_change()
            d["r5"] = cl/cl.shift(5) - 1
            d["r20"] = cl/cl.shift(20) - 1
            v = d["volume"].astype(float)
            d["vr"] = v / v.rolling(30, min_periods=10).mean()
            d["near"] = cl / cl.rolling(30, min_periods=10).max()  # nearness to 30d high
            d["vol20"] = d["r1"].rolling(20, min_periods=10).std()
            d["rng"] = (d["high"]-d["low"])/cl
            d["pos"] = np.arange(len(d))
            d["wd"] = pd.to_datetime(d["timestamp"]).dt.weekday
            d["yr"] = pd.to_datetime(d["timestamp"]).dt.year
            rows.append(d)
    A = pd.concat(rows, ignore_index=True)
    # demean fwr3 by coin mean over all windows
    for h in ["fwr1","fwr3","fwr5"]:
        A[h+"_dm"] = A[h] - A.groupby("coin")[h].transform("mean")
    g3 = A[A["pos"] % 3 == 0].dropna(subset=["fwr3_dm"])
    g5 = A[A["pos"] % 5 == 0].dropna(subset=["fwr5_dm"])
    out = {}
    def qtab(df, col, y, q=5):
        x = df.dropna(subset=[col, y]).copy()
        x["q"] = x.groupby("coin")[col].transform(lambda s: pd.qcut(s.rank(method="first"), q, labels=False))
        t = x.groupby("q")[y].agg(["mean","count","std"])
        t["t"] = t["mean"]/(t["std"]/np.sqrt(t["count"]))
        return t.drop(columns="std")
    def slope(df, col, y):
        x = df.dropna(subset=[col, y])
        r = stats.linregress(x[col], x[y]); return pd.Series({"slope": r.slope, "t": r.slope/r.stderr, "n": len(x)})
    out["fc_q_fwr3"] = qtab(g3, "forecast", "fwr3_dm")
    out["vr_q_fwr3"] = qtab(g3, "vr", "fwr3_dm")
    out["near_q_fwr3"] = qtab(g3, "near", "fwr3_dm")
    out["r5_q_fwr5"] = qtab(g5, "r5", "fwr5_dm")
    out["r20_q_fwr5"] = qtab(g5, "r20", "fwr5_dm")
    out["vol20_q_fwr5"] = qtab(g5, "vol20", "fwr5_dm")
    out["r1_q_fwr3"] = qtab(g3, "r1", "fwr3_dm")
    out["slopes"] = pd.DataFrame({k: slope(g3, k, "fwr3_dm") for k in ["forecast","vr","near","r1","rng","vol20"]}).T
    g1 = A.dropna(subset=["fwr1_dm"])
    out["weekday_fwr1"] = g1.groupby("wd")["fwr1_dm"].agg(["mean","count", lambda s: s.mean()/(s.std()/np.sqrt(len(s)))])
    # vr slope by coin
    out["vr_slope_by_coin"] = pd.DataFrame({c: slope(g3[g3.coin==c], "vr", "fwr3_dm") for c in g3.coin.unique()}).T
    out["near_slope_by_coin"] = pd.DataFrame({c: slope(g3[g3.coin==c], "near", "fwr3_dm") for c in g3.coin.unique()}).T
    # vr interacted with day's sign
    x = g3.dropna(subset=["vr","r1"]).copy()
    x["up"] = np.sign(x["r1"])
    x["vr_signed"] = (x["vr"]-1)*x["up"]
    out["vr_signed_slope"] = slope(x, "vr_signed", "fwr3_dm")
    out["vr_q_by_daysign"] = x.assign(q=pd.qcut(x["vr"].rank(method="first"),5,labels=False)).groupby(["up","q"])["fwr3_dm"].agg(["mean","count"])
    # book
    D = []
    for c in days:
        for w, df in days[c].items():
            dd = df.copy(); dd["coin"]=c; dd["win"]=w; D.append(dd)
    D = pd.concat(D, ignore_index=True)
    out["book_by_coin"] = D.groupby("coin")[["book_return","coin_return"]].mean()
    out["book_by_year"] = D.assign(yr=pd.to_datetime(D["day"]).dt.year).groupby("yr")[["book_return","coin_return"]].mean()
    out["alloc_mean"] = A.groupby("coin")["postRebalance_current_allocation"].mean()
    out["share_short"] = float((A["postRebalance_current_allocation"]<0).mean())
    return out
