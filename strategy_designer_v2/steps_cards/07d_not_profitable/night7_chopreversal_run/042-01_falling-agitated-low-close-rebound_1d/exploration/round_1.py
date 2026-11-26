def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    # book daily: mean over coins per day within window
    rows = []
    for c, ws in data["days"].items():
        for w, d in ws.items():
            t = d[["day","book_return","coin_return"]].copy()
            t["coin"]=c; t["w"]=w
            rows.append(t)
    D = pd.concat(rows)
    B = D.groupby(["w","day"]).agg(br=("book_return","mean"), cr=("coin_return","mean")).reset_index()
    B["wn"]=B.w.str[1:].astype(int)
    B = B.sort_values(["wn","day"]).dropna(subset=["br"])
    v = (1+B.br).cumprod(); B["v"]=v.values
    peak = B.v.cummax(); B["dd"]=B.v/peak-1
    out["maxdd"]=float(B.dd.min())
    out["book_by_window"]=B.groupby("w").agg(br_sum=("br","sum"), cr_sum=("cr","sum"), mindd=("dd","min"), n=("br","size"))
    # bar level analysis
    rs=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.copy()
            b["ret1"]=b.close.shift(-1)/b.close-1
            b["dayret"]=b.close/b.close.shift(1)-1
            b["rng"]=(b.high-b.low)/b.close
            b["raw"]=(b.high-b.close)/(b.high-b.low)
            b["r5"]=b.close/b.close.shift(5)-1
            b["coin"]=c; b["w"]=w
            b["alloc"]=b.postRebalance_current_allocation
            b["gain"]=b.alloc*b.ret1
            rs.append(b[["coin","w","timestamp","ret1","dayret","rng","raw","r5","regime","alloc","gain","forecast"]])
    X=pd.concat(rs)
    mu = X.groupby("coin").ret1.mean()
    X["ex"]=X.ret1-X.coin.map(mu)
    P = X[X.regime=="unknown"].dropna(subset=["ret1","raw"])
    P["rawq"]=pd.cut(P.raw,[-0.01,0.2,0.4,0.6,0.8,1.01])
    g=P.groupby("rawq").agg(n=("ex","size"),ex=("ex","mean"),ret=("ret1","mean"),alloc=("alloc","mean"),gain=("gain","mean"),gainsum=("gain","sum"))
    out["inprofile_by_raw"]=g
    # by day's own return quintile among in-profile
    P["dq"]=pd.qcut(P.dayret,5,labels=False)
    out["by_dayret_q"]=P.groupby("dq").agg(n=("ex","size"),ex=("ex","mean"),dr=("dayret","mean"),gain=("gain","sum"))
    P["low"]=P.raw>=0.6
    out["dayret_x_low"]=P.groupby(["dq","low"]).agg(n=("ex","size"),ex=("ex","mean")).unstack()
    P["rq"]=pd.qcut(P.rng,4,labels=False)
    out["rng_x_low"]=P.groupby(["rq","low"]).agg(n=("ex","size"),ex=("ex","mean")).unstack()
    P["r5q"]=pd.qcut(P.r5,4,labels=False)
    out["r5_x_low"]=P.groupby(["r5q","low"]).agg(n=("ex","size"),ex=("ex","mean")).unstack()
    out["by_window_gain"]=P.groupby("w").agg(n=("gain","size"),gain=("gain","sum"),ex=("ex","mean"))
    # gain in worst dd period: find trough and peak
    tr = B.dd.idxmin(); 
    i_tr = B.index.get_loc(tr) if False else None
    Bs=B.reset_index(drop=True)
    it=Bs.dd.idxmin(); ip=Bs.v.iloc[:it+1].idxmax()
    out["worst_dd_span"]=f"{Bs.w.iloc[ip]} to {Bs.w.iloc[it]}, days {it-ip}, dd {Bs.dd.iloc[it]:.3f}, coin mean sum {Bs.cr.iloc[ip:it+1].sum():.3f}"
    return out
