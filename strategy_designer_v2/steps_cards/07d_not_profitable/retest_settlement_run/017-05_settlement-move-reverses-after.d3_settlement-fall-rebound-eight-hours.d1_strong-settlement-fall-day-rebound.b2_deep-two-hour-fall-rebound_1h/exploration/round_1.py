def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    out = {}
    # book daily returns: mean over coins per (window, day)
    rows = []
    for c in days:
        for w, d in days[c].items():
            dd = d[["day","book_return","coin_return"]].copy(); dd["coin"]=c; dd["w"]=w
            rows.append(dd)
    D = pd.concat(rows)
    D["wn"] = D["w"].str[1:].astype(int)
    B = D.groupby(["wn","day"])[["book_return","coin_return"]].mean().dropna().sort_index()
    v = (1+B["book_return"]).cumprod(); dd_ = v/v.cummax()-1
    h = (1+B["coin_return"]).cumprod(); ddh = h/h.cummax()-1
    out["book_maxdd"] = float(dd_.min()); out["hold_maxdd"] = float(ddh.min())
    # per-window book vs hold
    pw = B.groupby(level=0).agg(book=("book_return", lambda x:(1+x).prod()-1), hold=("coin_return", lambda x:(1+x).prod()-1))
    pw["book_mdd"] = B["book_return"].groupby(level=0).apply(lambda x: ((1+x).cumprod()/(1+x).cumprod().cummax()-1).min())
    out["per_window"] = pw.round(3)
    out["corr_book_hold_daily"] = float(B["book_return"].corr(B["coin_return"]))
    # allocation stats and grid-case analysis
    al = []; cases = []
    for c in bars:
        allr = []
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            al.append(b["postRebalance_current_allocation"].values)
            cl = b["close"].values; n=len(cl)
            r2 = pd.Series(cl).pct_change(2).values
            r24b = pd.Series(cl).pct_change(24).values
            r168b = pd.Series(cl).pct_change(168).values
            r720b = pd.Series(cl).pct_change(720).values
            vol = pd.Series(np.log(cl)).diff().rolling(168).std().values
            vol720 = pd.Series(np.log(cl)).diff().rolling(720).std().values
            f = b["forecast"].values
            alloc = b["postRebalance_current_allocation"].values
            for i in range(0, n-24, 24):
                cases.append((c, w, f[i], cl[i+24]/cl[i]-1, r2[i], r24b[i], r168b[i], r720b[i], vol[i]/vol720[i] if vol720[i]>0 else np.nan, alloc[i]))
    al = np.concatenate(al)
    out["alloc_desc"] = pd.Series(al).describe().round(3)
    out["share_alloc_pos"] = float((al>0.01).mean())
    C = pd.DataFrame(cases, columns=["coin","w","f","fwd","r2","r24b","r168b","r720b","volratio","alloc"])
    drift = C.groupby("coin")["fwd"].mean()
    C["ex"] = C["fwd"] - C["coin"].map(drift)
    C["sig"] = C["f"]>0
    def summ(g):
        return pd.Series({"n":len(g),"mean_fwd":g["fwd"].mean(),"mean_ex":g["ex"].mean(),"t_ex":stats.ttest_1samp(g["ex"],0).statistic if len(g)>2 else np.nan})
    out["by_signal"] = C.groupby("sig").apply(summ).round(4)
    C["fq"] = pd.qcut(C["f"].where(C["sig"]), 5, labels=False, duplicates="drop")
    out["by_fq"] = C[C.sig].groupby("fq").apply(summ).round(4)
    C["trend168"] = np.where(C["r168b"]>0,"up7d","down7d")
    C["trend720"] = np.where(C["r720b"]>0,"up30d","down30d")
    out["sig_x_trend168"] = C.groupby(["sig","trend168"]).apply(summ).round(4)
    out["sig_x_trend720"] = C.groupby(["sig","trend720"]).apply(summ).round(4)
    C["vr"] = pd.qcut(C["volratio"],3,labels=["lowvol","midvol","highvol"])
    out["sig_x_vol"] = C.groupby(["sig","vr"]).apply(summ).round(4)
    return out
