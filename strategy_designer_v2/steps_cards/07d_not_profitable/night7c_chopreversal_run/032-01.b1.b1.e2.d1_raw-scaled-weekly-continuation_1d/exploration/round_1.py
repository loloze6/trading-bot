def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    bars = data["bars"]; days = data["days"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True).copy()
            cl = b["close"].astype(float)
            b["r1"] = cl.shift(-1)/cl - 1
            b["alloc"] = b["postRebalance_current_allocation"].astype(float)
            b["gain"] = b["alloc"]*b["r1"]
            b["fwd7"] = cl.shift(-7)/cl - 1
            b["ret7"] = cl/cl.shift(7) - 1
            b["ret30"] = cl/cl.shift(30) - 1
            d = cl.diff().abs()
            b["er"] = (cl - cl.shift(30)).abs()/d.rolling(30).sum()
            lr = np.log(cl).diff()
            b["vol30"] = lr.rolling(30).std()
            b["vol_ratio"] = lr.rolling(7).std()/lr.rolling(60, min_periods=30).std()
            b["scaled"] = b["ret7"]/(b["vol30"]*np.sqrt(7))
            b["grid"] = (np.arange(len(b)) % 7 == 0)
            b["coin"] = c; b["win"] = w
            b["year"] = pd.to_datetime(b["timestamp"]).dt.year
            rows.append(b)
    B = pd.concat(rows, ignore_index=True)
    drift = B[B.grid].groupby("coin")["fwd7"].mean()
    B["ex7"] = B["fwd7"] - B["coin"].map(drift)
    out = {}
    # side contribution
    B["side"] = np.sign(B["alloc"]).map({1:"long",-1:"short",0:"flat"})
    out["gain_by_side"] = B.groupby("side")["gain"].agg(["count","mean","sum"])
    # grid cases: forecast nonzero
    G = B[B.grid & (B["forecast"].fillna(0)!=0) & B["fwd7"].notna()].copy()
    G["sgn"] = np.sign(G["forecast"])
    G["dir_ex"] = G["sgn"]*G["ex7"]; G["dir_tot"] = G["sgn"]*G["fwd7"]
    G["absf"] = G["forecast"].abs()
    G["fq"] = pd.qcut(G["absf"], 4, labels=False, duplicates="drop")
    G["sq"] = pd.qcut(G["scaled"].abs(), 4, labels=False, duplicates="drop")
    def agg(g):
        return pd.Series({"n":len(g),"dir_ex":g.dir_ex.mean(),"dir_tot":g.dir_tot.mean(),
                          "t":g.dir_ex.mean()/(g.dir_ex.std()/np.sqrt(len(g))) if len(g)>2 else np.nan})
    out["cases_by_side"] = G.groupby("sgn").apply(agg)
    out["cases_by_absforecast_q"] = G.groupby("fq").apply(agg)
    out["cases_by_absscaled_q"] = G.groupby("sq").apply(agg)
    G["trend_agree"] = np.sign(G["ret30"])==G["sgn"]
    out["cases_by_30d_agree"] = G.groupby("trend_agree").apply(agg)
    G["erq"] = pd.qcut(G["er"], 3, labels=False, duplicates="drop")
    out["cases_by_er_tercile"] = G.groupby("erq").apply(agg)
    G["vq"] = pd.qcut(G["vol_ratio"], 3, labels=False, duplicates="drop")
    out["cases_by_volratio_tercile"] = G.groupby("vq").apply(agg)
    out["cases_by_year"] = G.groupby("year").apply(agg)
    # regime-less: all grid bars, scaled move sign, by er tercile (is condition its own effect)
    A = B[B.grid & B["scaled"].notna() & B["fwd7"].notna()].copy()
    A["sgn"]=np.sign(A["scaled"]); A["dir_ex"]=A.sgn*A.ex7; A["dir_tot"]=A.sgn*A.fwd7
    A["inreg"] = A["er"]<=0.3
    A["sq"] = pd.qcut(A["scaled"].abs(), 4, labels=False, duplicates="drop")
    out["all_bars_by_regime_sq"] = A.groupby(["inreg","sq"]).apply(agg)
    # book daily
    Dl=[]
    for c in days:
        for w,d in days[c].items():
            d=d.copy(); d["coin"]=c; d["win"]=w; Dl.append(d)
    D=pd.concat(Dl)
    P = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index()
    P = P.sort_values(["win","day"]).dropna()
    P["eq"]=(1+P.book_return).cumprod(); P["dd"]=P.eq/P.eq.cummax()-1
    out["book_by_window"]=P.groupby("win").agg(book=("book_return","mean"),hold=("coin_return","mean"),
        bsd=("book_return","std"),n=("book_return","count"))
    out["maxdd"]=float(P.dd.min())
    # drawdown episodes: identify days in worst 10% dd and what book held
    B["day"]=pd.to_datetime(B["timestamp"]).dt.floor("D")
    P["day"]=pd.to_datetime(P["day"])
    P["in_dd_deep"]=P.dd< P.dd.quantile(0.1)
    m = B.merge(P[["win","day","dd","in_dd_deep"]], on=["win","day"], how="left")
    m["agree30"]=np.sign(m["ret30"])==np.sign(m["alloc"])
    out["deepdd_vs_rest"]=m[m.alloc!=0].groupby("in_dd_deep").agg(gain=("gain","mean"),
        long_share=("alloc",lambda x:(x>0).mean()),absalloc=("alloc",lambda x:x.abs().mean()),
        er=("er","mean"),agree30=("agree30","mean"),volratio=("vol_ratio","mean"))
    # gain by year side
    out["gain_year_side"]=B[B.alloc!=0].groupby(["year","side"])["gain"].mean().unstack()
    out["share_inregime_bars"]=float((B["regime"]=="mean_reversion").mean())
    return out
