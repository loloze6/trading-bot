def explore(data):
    import numpy as np, pandas as pd
    out = {}
    days = data["days"]; bars = data["bars"]
    # book daily: mean over coins per (window, day)
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy()
            dd["coin"] = c; dd["w"] = w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().reset_index().sort_values(["wn","day"])
    B = B.dropna(subset=["book_return"])
    v = (1+B["book_return"]).cumprod().values
    peak = np.maximum.accumulate(v); dd = v/peak-1
    B["dd"] = dd
    i = int(np.argmin(dd)); pk = int(np.argmax(v[:i+1]))
    out["deepest fall"] = f"{dd[i]:.4f}, from row {pk} (w{B.iloc[pk]['wn']}) to row {i} (w{B.iloc[i]['wn']}), length {i-pk} days"
    # per-window book stats
    g = B.groupby("wn")
    out["by window"] = pd.DataFrame({"book_sum": g["book_return"].sum(), "coin_sum": g["coin_return"].sum(),
                                     "min_dd": g["dd"].min(), "n": g.size()})
    # find drawdown episodes: top 5 by depth
    ep = []; start = 0
    for k in range(1, len(v)):
        if v[k] >= peak[k] and dd[k-1] < 0:
            seg = dd[start:k]; ep.append((seg.min(), start, start+int(np.argmin(seg))))
        if v[k] >= peak[k]: start = k
    ep.append((dd[start:].min(), start, start+int(np.argmin(dd[start:]))))
    ep = sorted(ep)[:5]
    out["top falls"] = pd.DataFrame([{"depth": e[0], "len": e[2]-e[1], "window": B.iloc[e[2]]["wn"]} for e in ep])
    # bar-level: position gain by side, by ret20 depth, by agitation, by vol ratio
    R = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.copy()
            cl = b["close"]; vol = b["volume"]
            b["r1"] = cl.shift(-1)/cl-1
            b["ret20"] = cl/cl.shift(20)-1
            b["ret60"] = cl/cl.shift(60)-1
            b["ret5p"] = cl/cl.shift(5)-1
            b["vr"] = np.log(vol.rolling(30).mean()/vol.shift(30).rolling(30).mean())
            lr = np.log(cl).diff()
            s30 = lr.rolling(30).std()
            b["agit"] = s30.rolling(365, min_periods=120).apply(lambda x: (x<=x[-1]).mean(), raw=True)
            b["fwd5"] = cl.shift(-5)/cl-1
            b["pos"] = b["postRebalance_current_allocation"]
            b["gain"] = b["pos"]*b["r1"]
            b["coin"] = c; b["wn"] = int(w[1:])
            R.append(b[["coin","wn","pos","gain","r1","ret20","ret60","ret5p","vr","agit","fwd5","forecast"]])
    R = pd.concat(R)
    H = R[R["pos"].abs()>1e-9].copy()
    H["side"] = np.where(H["pos"]>0,"long","short")
    out["gain by side"] = H.groupby("side")["gain"].agg(["count","mean","sum","std"])
    H["d20"] = pd.cut(H["ret20"], [-1,-0.4,-0.3,-0.2,-0.15,-0.1,1])
    out["gain by side x ret20"] = H.groupby(["side","d20"],observed=True)["gain"].agg(["count","mean","sum"])
    H["ag"] = np.where(H["agit"]>0.5,"agitated","calm")
    out["gain by side x agitation"] = H.groupby(["side","ag"])["gain"].agg(["count","mean","sum"])
    H["p5"] = pd.cut(H["ret5p"], [-1,-0.15,-0.05,0,0.05,1])
    out["gain by side x past5d"] = H.groupby(["side","p5"],observed=True)["gain"].agg(["count","mean","sum"])
    out["gain by coin side"] = H.groupby(["coin","side"])["gain"].agg(["count","mean","sum"])
    return out
