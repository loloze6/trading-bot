def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["w"] = w; dd["coin"] = c
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B = B.dropna()
    v = (1+B["book_return"]).cumprod()
    peak = v.cummax(); dd = v/peak-1
    B["dd"] = dd.values; B["year"] = pd.to_datetime(B["day"]).dt.year
    out["max_dd"] = float(dd.min())
    # drawdown by window: min dd and book / coin sum
    out["by_window"] = B.groupby("wn").agg(book_sum=("book_return","sum"), coin_sum=("coin_return","sum"), min_dd=("dd","min"), n=("dd","size")).round(4)
    # worst 15 days of book: coin return that day
    worst = B.nsmallest(15,"book_return")[["wn","book_return","coin_return"]]
    out["worst_days"] = worst.round(4).reset_index(drop=True)
    # case-level analysis
    cases = []
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.sort_values("timestamp").reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            r1 = b["close"].pct_change()
            mad = r1.abs().rolling(60, min_periods=20).mean()
            fwd = b["close"].shift(-3)/b["close"]-1
            ret20 = b["close"]/b["close"].shift(20)-1
            ret7 = b["close"]/b["close"].shift(7)-1
            ma50 = b["close"]/b["close"].rolling(50, min_periods=30).mean()-1
            vol10 = r1.rolling(10).std(); vol60 = r1.rolling(60, min_periods=30).std()
            vrel = b["volume"]/b["volume"].rolling(60, min_periods=20).mean()
            # grid drift
            g = b["close"].values[::3]
            dr = list(g[1:]/g[:-1]-1)
            sun = ts.dt.dayofweek == 6
            df = pd.DataFrame({"coin":c,"w":w,"fc":b["forecast"],"r1":r1,"z":r1/mad,"fwd":fwd,"ret20":ret20,"ret7":ret7,
                               "ma50":ma50,"vr":vol10/vol60,"vrel":vrel,"year":ts.dt.year})[sun.values]
            df["drifts"] = [dr]*len(df)
            cases.append(df)
    C = pd.concat(cases).dropna(subset=["fwd","ret20","ma50","vr"])
    drift = {}
    for c in C["coin"].unique():
        allr = []
        for x in C.loc[C.coin==c,"drifts"].iloc[:0]: pass
    # drift per coin: recompute
    for c, ws in data["bars"].items():
        allr=[]
        for w,b in ws.items():
            g=b.sort_values("timestamp")["close"].values[::3]; allr += list(g[1:]/g[:-1]-1)
        drift[c]=np.mean(allr)
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    C = C.drop(columns="drifts")
    sig = C[C.fc>=2]; non = C[C.r1>0]
    def summ(g):
        return pd.Series({"n":len(g),"fwd":g.fwd.mean(),"ex":g.ex.mean(),"t":g.ex.mean()/(g.ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan,"p_neg5":(g.fwd<-0.05).mean()})
    out["sig_all"] = summ(sig).round(4)
    out["sig_by_year"] = sig.groupby("year").apply(summ).round(4)
    for k in ["ret20","ma50","vr","vrel"]:
        q = pd.qcut(C[k], 4, labels=False, duplicates="drop")
        C["q_"+k] = q
        s = C[C.fc>=2].groupby("q_"+k).apply(summ)
        n = C[C.r1>0].groupby("q_"+k).apply(summ)
        out["by_"+k] = pd.concat({"signal":s,"sunday_rise":n},axis=1).round(4)
    out["sig_by_zbin"] = sig.groupby(pd.cut(-sig.z,[0,1,2,3,10])).apply(summ).round(4)
    return out
