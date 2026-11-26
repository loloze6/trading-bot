def explore(data):
    import pandas as pd, numpy as np
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
    B["side"] = np.sign(B["alloc"]).map({1.0:"long",-1.0:"short",0.0:"flat"})
    out["gain_by_side"] = B.groupby("side")["gain"].agg(["count","mean","sum"])
    G = B[B.grid & (B["forecast"].fillna(0)!=0) & B["fwd7"].notna()].copy()
    G["sgn"] = np.sign(G["forecast"])
    G["dir_ex"] = G["sgn"]*G["ex7"]; G["dir_tot"] = G["sgn"]*G["fwd7"]
    def agg(g):
        n=len(g); s=g.dir_ex.std()
        return pd.Series({"n":n,"dir_ex":g.dir_ex.mean(),"dir_tot":g.dir_tot.mean(),
                          "t":g.dir_ex.mean()/(s/np.sqrt(n)) if n>2 and s>0 else np.nan})
    out["cases_by_side"] = G.groupby("sgn").apply(agg)
    G["fq"] = pd.qcut(G["forecast"].abs(), 4, labels=False, duplicates="drop")
    out["cases_by_absforecast_q"] = G.groupby("fq").apply(agg)
    G["sq"] = pd.qcut(G["scaled"].abs(), 4, labels=False, duplicates="drop")
    out["cases_by_absscaled_q"] = G.groupby("sq").apply(agg)
    G["trend_agree"] = (np.sign(G["ret30"])==G["sgn"]).astype(int)
    out["cases_by_30d_agree"] = G.groupby("trend_agree").apply(agg)
    G["vq"] = pd.qcut(G["vol_ratio"], 3, labels=False, duplicates="drop")
    out["cases_by_volratio_tercile"] = G.groupby("vq").apply(agg)
    out["cases_by_year"] = G.groupby("year").apply(agg)
    # all grid bars, raw scaled sign: in regime vs not, by |scaled| quartile
    A = B[B.grid & B["scaled"].notna() & B["fwd7"].notna() & B["er"].notna()].copy()
    A["sgn"]=np.sign(A["scaled"]); A["dir_ex"]=A.sgn*A.ex7; A["dir_tot"]=A.sgn*A.fwd7
    A["inreg"] = (A["er"]<=0.3).astype(int)
    A["sq"] = pd.qcut(A["scaled"].abs(), 4, labels=False, duplicates="drop")
    out["all_bars_by_regime_sq"] = A.groupby(["inreg","sq"]).apply(agg)
    A["vq"] = pd.qcut(A["vol_ratio"], 3, labels=False, duplicates="drop")
    out["all_bars_by_regime_volratio"] = A.groupby(["inreg","vq"]).apply(agg)
    # book daily
    Dl=[]
    for c in days:
        for w,d in days[c].items():
            d=d.copy(); d["coin"]=c; d["win"]=w; Dl.append(d)
    D=pd.concat(Dl)
    P = D.groupby(["win","day"])[["book_return","coin_return"]].mean().reset_index().dropna()
    P["wn"]=P["win"].str[1:].astype(int)
    P = P.sort_values(["wn","day"]).reset_index(drop=True)
    P["eqv"]=(1+P["book_return"]).cumprod(); P["ddv"]=P["eqv"]/P["eqv"].cummax()-1
    out["book_by_window"]=P.groupby("win").agg(book=("book_return","mean"),hold=("coin_return","mean"),
        bsd=("book_return","std"),n=("book_return","count"),mindd=("ddv","min"))
    out["maxdd"]=float(P["ddv"].min())
    # deepest-fall days: falling days within deepest 10% drawdown
    B["day"]=pd.to_datetime(B["timestamp"]).dt.floor("D")
    P["day"]=pd.to_datetime(P["day"])
    if P["day"].dt.tz is not None and B["day"].dt.tz is None:
        B["day"]=B["day"].dt.tz_localize(P["day"].dt.tz)
    elif P["day"].dt.tz is None and B["day"].dt.tz is not None:
        B["day"]=B["day"].dt.tz_localize(None)
    P["deep"]=(P["ddv"]<P["ddv"].quantile(0.1)).astype(int)
    m = B.merge(P[["win","day","deep"]], on=["win","day"], how="left")
    m["agree30"]=(np.sign(m["ret30"])==np.sign(m["alloc"])).astype(int)
    m["inreg"]=(m["regime"]=="mean_reversion").astype(int)
    out["deep_vs_rest"]=m[m.alloc!=0].groupby("deep").agg(n=("gain","count"),gain=("gain","mean"),
        long_share=("alloc",lambda x:(x>0).mean()),absalloc=("alloc",lambda x:x.abs().mean()),
        er=("er","mean"),agree30=("agree30","mean"),volratio=("vol_ratio","mean"),inreg=("inreg","mean"))
    # gain held while regime off vs on
    out["gain_by_inreg_side"]=m[m.alloc!=0].groupby(["inreg","side"])["gain"].agg(["count","mean"])
    out["gain_year_side"]=B[B.alloc!=0].groupby(["year","side"])["gain"].mean().unstack()
    out["share_inregime_bars"]=float((B["regime"]=="mean_reversion").mean())
    out["trades_mean_net_by_side"]=pd.concat([t.assign(coin=c) for c in data["trades"] for t in data["trades"][c].values()]).groupby("side")[["profit_loss_percent","net_profit_loss_percent"]].agg(["count","mean"])
    return out
