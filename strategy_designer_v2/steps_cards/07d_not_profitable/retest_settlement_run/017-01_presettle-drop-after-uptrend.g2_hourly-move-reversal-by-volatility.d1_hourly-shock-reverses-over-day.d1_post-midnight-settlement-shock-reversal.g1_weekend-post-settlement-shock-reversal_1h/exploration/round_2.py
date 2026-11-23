def explore(data):
    import numpy as np, pandas as pd
    out = {}
    bars = data["bars"]
    rows = []
    for c in bars:
        for w, b in bars[c].items():
            b = b.reset_index(drop=True)
            ts = pd.to_datetime(b["timestamp"])
            a = b["postRebalance_current_allocation"].fillna(0)
            r = b["close"].shift(-1)/b["close"]-1
            g = a*r
            df = pd.DataFrame({"coin":c,"wn":int(w[1:]),"day":ts.dt.floor("D"),
                               "gl":np.where(a>0,g,0.0),"gs":np.where(a<0,g,0.0),
                               "inl":(a>0).astype(float),"ins":(a<0).astype(float)})
            rows.append(df)
    G = pd.concat(rows).dropna()
    Dc = G.groupby(["coin","wn","day"]).agg(gl=("gl","sum"),gs=("gs","sum")).reset_index()
    Dd = Dc.groupby(["wn","day"])[["gl","gs"]].mean().reset_index().sort_values(["wn","day"])
    Dd["tot"] = Dd["gl"]+Dd["gs"]
    def calm(x):
        v=(1+x).cumprod(); dd=(v/v.cummax()-1).min()
        yr=v.iloc[-1]**(365/len(x))-1
        return pd.Series({"mean":x.mean(),"sharpe":x.mean()/x.std()*np.sqrt(365),"yearly":yr,"maxdd":dd,"calmar":yr/abs(dd)})
    out["side_books_gross"] = pd.DataFrame({k:calm(Dd[k]) for k in ["gl","gs","tot"]})
    # cost-adjusted rough: subtract 0.19% per trade per side share; skip, use gross
    Dd["year"]=pd.to_datetime(Dd["day"]).dt.year
    out["side_by_year"] = Dd.groupby("year")[["gl","gs"]].sum()
    out["side_by_window_w12_w20"] = Dd[Dd["wn"].between(12,20)].groupby("wn")[["gl","gs"]].sum()
    # cases: weekend 00:00, long-side signal vs unconditional long on all weekend 00:00 / all 00:00
    C=[]
    for c in bars:
        for w,b in bars[c].items():
            b=b.reset_index(drop=True); ts=pd.to_datetime(b["timestamp"])
            r1=b["close"].pct_change(); v24=r1.rolling(24).std()
            fwd=b["close"].shift(-24)/b["close"]-1
            ret168=b["close"]/b["close"].shift(168)-1
            v720=r1.rolling(720,min_periods=200).std()
            df=pd.DataFrame({"coin":c,"hr":ts.dt.hour,"wd":ts.dt.weekday,"z":r1/v24,"fwd":fwd,
                             "r168":ret168,"vr":v24/v720})
            C.append(df[df["hr"]==0])
    C=pd.concat(C).dropna(subset=["fwd","z"])
    C["wk"]=C["wd"].isin([5,6])
    def s(x):
        return pd.Series({"n":len(x),"mean_fwd":x.mean(),"t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out["fwd_all_00_bars_by_weekend"] = C.groupby("wk")["fwd"].apply(s).unstack()
    W=C[C["wk"]].copy()
    W["dn"]=W["z"]<0
    out["wkend_fwd_by_downhour"]=W.groupby("dn")["fwd"].apply(s).unstack()
    W["zb"]=pd.cut(W["z"],[-99,-2,-1,-0.5,0,0.5,1,2,99])
    out["wkend_fwd_by_zbin"]=W.groupby("zb")["fwd"].apply(s).unstack()
    # down hour, by prior 7d trend sign
    D_=W[W["dn"]].copy(); D_["up168"]=D_["r168"]>0
    out["down_hour_by_7d_trend"]=D_.groupby("up168")["fwd"].apply(s).unstack()
    U_=W[~W["dn"]].copy(); U_["up168"]=U_["r168"]>0
    out["up_hour_short_capture_by_7d_trend"]=(-U_["fwd"]).groupby(U_["up168"]).apply(s).unstack()
    out["coin_mean_24h_fwd_all00"]=C.groupby("coin")["fwd"].mean()
    return out
