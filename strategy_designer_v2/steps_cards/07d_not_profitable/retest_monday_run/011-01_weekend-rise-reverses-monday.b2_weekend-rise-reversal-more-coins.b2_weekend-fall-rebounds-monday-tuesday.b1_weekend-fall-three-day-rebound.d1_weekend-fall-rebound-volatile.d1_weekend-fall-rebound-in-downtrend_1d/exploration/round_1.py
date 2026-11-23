def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily returns per window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"]).agg(book=("book_return","mean"), hold=("coin_return","mean"), n=("coin","count")).reset_index().dropna()
    B = B.sort_values(["wn","day"])
    v = (1+B["book"]).cumprod()
    peak = v.cummax(); dd = v/peak-1
    B["dd"] = dd.values
    B["year"] = pd.to_datetime(B["day"]).dt.year
    out["book_by_window"] = B.groupby("wn").agg(book_sum=("book","sum"), hold_sum=("hold","sum"), mindd=("dd","min"), days=("book","count"))
    out["book_by_year"] = B.groupby("year").agg(book_sum=("book","sum"), hold_sum=("hold","sum"), mindd=("dd","min"))
    out["maxdd"] = float(dd.min())
    # worst book days
    w = B.nsmallest(15, "book")[["wn","book","hold","n"]]
    out["worst_days"] = w.reset_index(drop=True)
    # cases
    cases = []
    for c, ws in data["bars"].items():
        for wn, b in ws.items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            n = len(b)
            r1 = pd.Series(cl).pct_change().values
            r20 = pd.Series(cl).pct_change(20).values
            r60 = pd.Series(cl).pct_change(60).values
            lr = np.log(pd.Series(cl)).diff()
            vol20 = lr.rolling(20).std().values
            vol60 = lr.rolling(60).std().values
            vrat = (b["volume"]/b["volume"].rolling(20).mean()).values
            mx20 = pd.Series(cl).rolling(20).max().values
            for i in range(n-3):
                if ts[i].dayofweek == 6 and b["forecast"].iloc[i] > 0:
                    cases.append(dict(coin=c, wn=int(wn[1:]), year=ts[i].year, r1=r1[i], r20=r20[i], r60=r60[i], vol20=vol20[i], vrat=vrat[i],
                                      volr=vol20[i]/vol60[i] if vol60[i] else np.nan, dfm=cl[i]/mx20[i]-1,
                                      fwd=cl[i+3]/cl[i]-1, f1=cl[i+1]/cl[i]-1, alloc=b["postRebalance_current_allocation"].iloc[i],
                                      worst=np.min(cl[i+1:i+4])/cl[i]-1, fc=b["forecast"].iloc[i]))
    C = pd.DataFrame(cases)
    C["pnl"] = C["fwd"]*C["alloc"]
    out["n_cases"] = len(C)
    out["fwd_quantiles"] = C["fwd"].quantile([.01,.05,.1,.25,.5,.75,.9]).to_frame()
    def g(col, q=5):
        C["_b"] = pd.qcut(C[col], q, duplicates="drop")
        r = C.groupby("_b", observed=True).agg(n=("fwd","count"), mean=("fwd","mean"), sd=("fwd","std"), p05=("fwd",lambda x: x.quantile(.05)), pnl=("pnl","mean"), alloc=("alloc","mean"))
        r["t"] = r["mean"]/(r["sd"]/np.sqrt(r["n"]))
        return r.reset_index().astype({"_b": str})
    for col in ["r1","r20","r60","vol20","vrat","volr","dfm","fc","alloc"]:
        out["by_"+col] = g(col)
    out["by_year"] = C.groupby("year").agg(n=("fwd","count"), mean=("fwd","mean"), pnl=("pnl","mean"))
    out["worst_cases"] = C.nsmallest(15,"pnl")[["coin","wn","r1","r20","r60","vol20","vrat","fwd","alloc","pnl"]].reset_index(drop=True)
    return out
