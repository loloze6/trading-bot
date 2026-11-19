def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars = data["bars"]
    out = {}
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            ts = pd.to_datetime(b["timestamp"])
            cl = b["close"].values
            s = pd.Series(cl)
            lr = np.log(s).diff()
            df = pd.DataFrame({
                "coin": c, "w": w, "hour": ts.dt.hour.values, "year": ts.dt.year.values,
                "pos": np.arange(len(b)),
                "r1": np.r_[cl[1:]/cl[:-1]-1, np.nan],
                "r2": s.shift(-2).values/cl-1,
                "r24f": s.shift(-24).values/cl-1,
                "r72f": s.shift(-72).values/cl-1,
                "p24": cl/s.shift(24).values-1,
                "p72": cl/s.shift(72).values-1,
                "vol24": lr.rolling(24).std().values,
                "vol168": lr.rolling(168).std().values,
            })
            rows.append(df)
    A = pd.concat(rows, ignore_index=True)
    def tt(x): x=x.dropna(); return pd.Series({"bps": x.mean()*1e4, "t": x.mean()/(x.std()/np.sqrt(len(x))), "n": len(x)})
    # 2h return from 20:00 close (bar stamped 19) : r2 on bars hour==19, by coin and by year
    H = A[A.hour==19]
    out["r2_from20_by_coin"] = H.groupby("coin")["r2"].apply(tt).unstack()
    out["r2_from20_by_year"] = H.groupby("year")["r2"].apply(tt).unstack()
    # share of windows with positive mean
    wm = H.groupby(["coin","w"])["r2"].mean()
    out["r2_from20_share_windows_pos"] = f"{(wm>0).mean():.3f} of {len(wm)}"
    # compare against all other 2h slots on even grid
    E = A[A.pos%2==0]
    out["r2_by_starthour_evenpos_top"] = E.groupby("hour")["r2"].apply(tt).unstack().sort_values("t").iloc[[0,1,2,-3,-2,-1]]
    # regression at hour19: r2 on p24 controlling? simple: slope and in fall vs rise halves
    x = H.dropna(subset=["p24","r2"])
    sl = stats.linregress(x.p24, x.r2)
    out["h19_slope_r2_on_p24"] = f"slope {sl.slope:.4f} t {sl.slope/sl.stderr:.2f} n {len(x)}"
    xo = E[E.hour!=19].dropna(subset=["p24","r2"]); xo = xo[xo.hour%2==1]
    sl2 = stats.linregress(xo.p24, xo.r2)
    out["otherodd_slope_r2_on_p24"] = f"slope {sl2.slope:.4f} t {sl2.slope/sl2.stderr:.2f} n {len(xo)}"
    # 24h reversal: grid every 24 bars, quintile of p24 within coin -> r24f, per coin slope, per year
    G = A[A.pos%24==0].dropna(subset=["p24","r24f"]).copy()
    G["q"] = G.groupby("coin")["p24"].transform(lambda v: pd.qcut(v,5,labels=False))
    out["r24f_by_p24_quintile"] = G.groupby("q")["r24f"].apply(tt).unstack()
    res=[]
    for c,xx in G.groupby("coin"):
        s_=stats.linregress(xx.p24,xx.r24f); res.append((c,s_.slope,s_.slope/s_.stderr,len(xx)))
    for y,xx in G.groupby("year"):
        s_=stats.linregress(xx.p24,xx.r24f); res.append((str(y),s_.slope,s_.slope/s_.stderr,len(xx)))
    out["r24f_on_p24_slope_by_coin_year"] = pd.DataFrame(res,columns=["grp","slope","t","n"]).set_index("grp")
    # 72h: grid every 72
    G3 = A[A.pos%72==0].dropna(subset=["p72","r72f"])
    s3 = stats.linregress(G3.p72,G3.r72f)
    out["r72f_on_p72"] = f"slope {s3.slope:.4f} t {s3.slope/s3.stderr:.2f} n {len(G3)}"
    # vol: 24h forward return by vol24 relative to vol168 quintile
    G["vr"] = (A.loc[G.index,"vol24"]/A.loc[G.index,"vol168"]).values
    Gv = G.dropna(subset=["vr"]).copy()
    Gv["vq"] = Gv.groupby("coin")["vr"].transform(lambda v: pd.qcut(v,5,labels=False))
    out["r24f_by_volratio_quintile"] = Gv.groupby("vq")["r24f"].apply(tt).unstack()
    # interaction: 24h reversal in high vs low vol ratio
    res=[]
    for vq,xx in Gv.groupby("vq"):
        s_=stats.linregress(xx.p24,xx.r24f); res.append((vq,s_.slope,s_.slope/s_.stderr,len(xx)))
    out["r24f_on_p24_by_volratio_q"] = pd.DataFrame(res,columns=["vq","slope","t","n"]).set_index("vq")
    return out
