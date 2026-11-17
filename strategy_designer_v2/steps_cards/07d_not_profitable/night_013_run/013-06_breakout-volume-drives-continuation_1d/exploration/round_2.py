def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    cases = []
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b = b.reset_index(drop=True)
            c = b["close"].values; v = b["volume"].values
            act = (b["regime"] == "trending").values
            alloc = b["postRebalance_current_allocation"].fillna(0).values
            vr = b.get("debug_info.components.volratio.last_history_value")
            i = 0; last = -10**9
            while i < len(c):
                if act[i] and (i == 0 or not act[i-1]) and i - last >= 30:
                    last = i
                    j = i
                    while j < len(c) and act[j]: j += 1
                    d = dict(coin=coin, runlen=j - i,
                             vr=float(vr.iloc[i]) if vr is not None and pd.notna(vr.iloc[i]) else np.nan)
                    for h in [1, 3, 5, 10, 20, 30, 60]:
                        d[f"r{h}"] = c[i+h]/c[i]-1 if i+h < len(c) else np.nan
                    # book gain over the 30 bars after breakout
                    if i+30 < len(c):
                        g = sum(alloc[k]*(c[k+1]/c[k]-1) for k in range(i, i+30))
                        d["book30"] = g
                    else:
                        d["book30"] = np.nan
                    # path: max drawdown of coin over next 30 bars from breakout close
                    if i+30 < len(c):
                        seg = c[i:i+31]
                        d["mae30"] = seg.min()/c[i]-1
                        d["below_entry_share"] = (seg[1:] < c[i]).mean()
                    cases.append(d)
                i += 1
    C = pd.DataFrame(cases)
    out["n_cases"] = len(C)
    cols = [f"r{h}" for h in [1,3,5,10,20,30,60]]
    m = C[cols].mean(); s = C[cols].std(); n = C[cols].count()
    out["fwd_after_breakout"] = pd.DataFrame({"mean": m, "median": C[cols].median(), "n": n, "t": m/(s/np.sqrt(n))})
    out["book30_vs_coin30"] = C[["book30","r30"]].agg(["mean","median","count"])
    C["vrt"] = pd.qcut(C["vr"].rank(method="first"), 3, labels=["low","mid","high"])
    out["by_vol_tercile"] = C.groupby("vrt")[["r5","r10","r30","r60","book30","mae30","runlen"]].mean()
    out["mae30"] = C[["mae30","below_entry_share"]].describe()
    out["by_coin_r30"] = C.groupby("coin")[["r30","book30","mae30"]].mean()
    out["corr_runlen_r30"] = C[["runlen","r30"]].corr().iloc[0,1]
    # daily book returns: worst days
    dd = []
    for coin, wins in data["days"].items():
        for w, d in wins.items():
            dd.append(d[["book_return","coin_return"]].assign(coin=coin))
    D = pd.concat(dd).dropna()
    nz = D[D["book_return"].abs() > 1e-9]
    out["active_days"] = len(nz)
    out["active_day_stats"] = nz[["book_return","coin_return"]].agg(["mean","std","min"])
    out["worst10_days"] = nz.nsmallest(10, "book_return")[["coin","book_return","coin_return"]].reset_index(drop=True)
    return out
