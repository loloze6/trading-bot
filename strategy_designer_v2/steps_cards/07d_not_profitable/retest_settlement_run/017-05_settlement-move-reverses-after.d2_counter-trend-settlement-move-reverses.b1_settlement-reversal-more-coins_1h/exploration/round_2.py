def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            ts=pd.to_datetime(b["timestamp"],utc=True)
            c=b["close"].astype(float)
            nh=(ts+pd.Timedelta(hours=1)).dt.hour
            r1=c.pct_change()
            vol=r1.rolling(240,min_periods=100).std()
            r2=c/c.shift(2)-1; r24=c/c.shift(24)-1
            d=pd.DataFrame({"coin":coin,"nh":nh,"r2":r2,"r24":r24,"vol":vol})
            for h in (1,2,3,4,8):
                d[f"f{h}"]=c.shift(-h)/c-1
            d=d[d.nh%4==0]
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    for h in (1,2,3,4,8):
        D[f"d{h}"]=D[f"f{h}"]-D.groupby("coin")[f"f{h}"].transform("mean")
    D["settle"]=D.nh.isin([0,8,16])
    D["against"]=(D.r2*D.r24<0)
    D["z2"]=D.r2.abs()/(D.vol*np.sqrt(2))
    D["z24"]=D.r24.abs()/(D.vol*np.sqrt(24))
    D["sgn"]=np.sign(D.r24)
    D["dec2"]=D.groupby("settle")["z2"].transform(lambda s: pd.qcut(s,10,labels=False,duplicates="drop"))
    def summ(g,h):
        x=(g["sgn"]*g[f"d{h}"]).dropna(); tot=(g["sgn"]*g[f"f{h}"]).dropna()
        return pd.Series({"n":len(x),"unusual_pct":100*x.mean(),"total_pct":100*tot.mean(),
                          "t":x.mean()/(x.std()/np.sqrt(len(x)))})
    out={}
    A=D[D.against]
    for h in (2,4,8):
        out[f"against_by_z2decile_settle_h{h}"]=A.groupby(["settle","dec2"]).apply(lambda g: summ(g,h)).reset_index()
    T=A[A.dec2>=9]
    out["against_top_decile_by_hour_h2"]=T.groupby("nh").apply(lambda g: summ(g,2))
    out["against_top_decile_by_hour_h4"]=T.groupby("nh").apply(lambda g: summ(g,4))
    S=A[A.settle].copy()
    S["p"]=S.z2*S.z24
    S["qp"]=pd.qcut(S.p,20,labels=False,duplicates="drop")
    out["settle_top5pct_product"]=pd.DataFrame({f"h{h}":summ(S[S.qp==19],h) for h in (1,2,3,4,8)}).T
    out["settle_top_decile_premove_all_h"]=pd.DataFrame({f"h{h}":summ(A[A.settle&(A.dec2>=9)],h) for h in (1,2,3,4,8)}).T
    # pre-move with trend (not against): revert premove at settlement, top decile
    W=D[D.settle&(~D.against)&(D.dec2>=9)].copy(); W["sgn"]=-np.sign(W.r2)
    out["settle_withtrend_top_decile_revert_premove"]=pd.DataFrame({f"h{h}":summ(W,h) for h in (1,2,4,8)}).T
    usual=D.groupby("coin")["f2"].std().mean()
    out["usual_2h_move_pct"]=100*usual
    return out
