def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    h = 14
    rows = []
    for coin, ws in data["bars"].items():
        for w, b in ws.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].values
            f = b["forecast"].values
            n = len(b)
            ret60 = pd.Series(c).pct_change(60).values
            ret14 = pd.Series(c).pct_change(14).values
            vr = pd.Series(v).rolling(14).mean() / pd.Series(v).rolling(30).mean() - 1
            vr = vr.values
            yr = pd.to_datetime(b["timestamp"]).dt.year.values
            alloc = b["postRebalance_current_allocation"].values
            for i in range(0, n - h, h):
                rows.append(dict(coin=coin, w=w, yr=yr[i], f=f[i], fr=c[i+h]/c[i]-1,
                                 r60=ret60[i], r14=ret14[i], vr=vr[i], al=alloc[i],
                                 day=str(b["timestamp"].iloc[i])[:10]))
    d = pd.DataFrame(rows)
    d["mu"] = d.groupby("coin")["fr"].transform("mean")
    d["ex"] = d["fr"] - d["mu"]
    d["side"] = np.sign(d["f"])
    d["dex"] = d["side"] * d["ex"]
    d["dtot"] = d["side"] * d["fr"]
    def summ(g):
        x = g["dex"].dropna()
        return pd.Series(dict(n=len(x), dex=x.mean(), t=x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan,
                              dtot=g["dtot"].mean(), fr=g["fr"].mean()))
    out = {}
    out["by_side"] = d[d.side!=0].groupby("side").apply(summ)
    d["fq"] = pd.qcut(d["f"].abs(), 4, labels=False, duplicates="drop")
    out["by_absf_quart_side"] = d[d.side!=0].groupby(["side","fq"]).apply(summ)
    d["r60s"] = np.sign(d["r60"])
    out["by_side_r60sign"] = d[d.side!=0].dropna(subset=["r60"]).groupby(["side","r60s"]).apply(summ)
    # condition alone: fr excess by r60 sign
    out["r60sign_alone_ex"] = d.dropna(subset=["r60"]).groupby("r60s")["ex"].agg(["count","mean"])
    d["r14s"] = np.sign(d["r14"])
    out["by_side_r14sign"] = d[d.side!=0].dropna(subset=["r14"]).groupby(["side","r14s"]).apply(summ)
    out["by_year"] = d[d.side!=0].groupby("yr").apply(summ)
    # book daily
    bd = []
    for coin, ws in data["days"].items():
        for w, dd in ws.items():
            x = dd[["day","book_return","coin_return"]].copy(); x["coin"]=coin; x["w"]=w
            bd.append(x)
    bd = pd.concat(bd)
    port = bd.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    port["wn"] = port["w"].str[1:].astype(int)
    port = port.sort_values(["wn","day"])
    port = port.dropna()
    v = (1+port["book_return"]).cumprod()
    dd_ = v/v.cummax()-1
    out["book_maxdd"] = float(dd_.min())
    port["dd"]=dd_.values
    out["book_by_window"] = port.groupby("wn").agg(book=("book_return","sum"), hold=("coin_return","sum"), mindd=("dd","min"))
    return out
