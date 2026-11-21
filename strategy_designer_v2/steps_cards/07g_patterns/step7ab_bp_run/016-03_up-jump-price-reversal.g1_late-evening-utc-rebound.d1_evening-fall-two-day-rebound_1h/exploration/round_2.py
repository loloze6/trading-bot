def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    rows = []
    for coin in bars:
        for w, df in bars[coin].items():
            d = df.sort_values("timestamp").reset_index(drop=True)
            c = d["close"].astype(float).values
            ts = pd.to_datetime(d["timestamp"])
            r = np.r_[np.nan, c[1:]/c[:-1]-1]
            n = len(c)
            for H in (24, 48, 120):
                for off in (0, H//2):
                    for t in range(off, n, H):
                        if t < 168 or t+H >= n: continue
                        rr = r[t-71:t+1]
                        eff = abs(np.log(c[t]/c[t-72]))/np.nansum(np.abs(np.log1p(rr)))
                        rows.append(dict(coin=coin, w=w, H=H, off=off, fwd=c[t+H]/c[t]-1,
                            p24=c[t]/c[t-24]-1, p72=c[t]/c[t-72]-1, p168=c[t]/c[t-168]-1,
                            eff=eff, vol168=np.nanstd(r[t-167:t+1]),
                            hour=ts[t].hour, yr=ts[t].year))
    X = pd.DataFrame(rows)
    out = {}
    def tstat(s): return s.mean()/s.std()*np.sqrt(len(s))
    for H in (24,48,120):
        for off in (0, H//2):
            S = X[(X.H==H)&(X.off==off)].copy()
            S["mu"] = S.groupby("coin")["fwd"].transform("mean")
            S["sd"] = S.groupby("coin")["fwd"].transform("std")
            S["ex"] = S["fwd"]-S["mu"]
            res = {}
            for p in ("p24","p72","p168"):
                S["z"] = S[p]/S.groupby("coin")[p].transform("std")
                sl = stats.linregress(S["z"], S["ex"]/S["sd"])
                S["q"] = S.groupby("coin")[p].transform(lambda s: pd.qcut(s,5,labels=False))
                lo = S[S.q==0]; hi = S[S.q==4]
                res[p] = pd.Series({"slope_sd": sl.slope, "t": sl.slope/sl.stderr, "n": len(S),
                    "q0_ex_bps": lo["ex"].mean()*1e4, "q0_t": tstat(lo["ex"]),
                    "q4_ex_bps": hi["ex"].mean()*1e4, "q4_t": tstat(hi["ex"]),
                    "q0_tot_bps": lo["fwd"].mean()*1e4, "q4_tot_bps": hi["fwd"].mean()*1e4,
                    "usual_bps": S["sd"].mean()*1e4})
            out[f"H{H}_off{off}"] = pd.DataFrame(res)
            if off == 0 and H in (48,120):
                p = "p24" if H==48 else "p72"
                S["z"] = S[p]/S.groupby("coin")[p].transform("std")
                g = lambda G: pd.Series({"t": (lambda l: l.slope/l.stderr)(stats.linregress(G["z"], G["ex"]/G["sd"])), "n": len(G)})
                out[f"H{H}_{p}_bycoin"] = S.groupby("coin").apply(g)
                out[f"H{H}_{p}_byyear"] = S.groupby("yr").apply(g)
                S["vq"] = S.groupby("coin")["vol168"].transform(lambda s: pd.qcut(s,3,labels=False))
                out[f"H{H}_{p}_byvol3"] = S.groupby("vq").apply(g)
    return out
