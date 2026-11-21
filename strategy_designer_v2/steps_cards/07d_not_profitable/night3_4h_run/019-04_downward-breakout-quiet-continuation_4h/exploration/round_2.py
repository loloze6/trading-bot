def explore(data):
    import numpy as np, pandas as pd
    H=18
    rows=[]; drift={}; bk=[]
    for coin,ws in data["bars"].items():
        nonov=[]
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; hi=b["high"]; lo=b["low"]
            f=c.shift(-H)/c-1
            nonov.append(f.iloc[::H].dropna())
            lo12=lo.shift(1).rolling(12).min(); hi12=hi.shift(1).rolling(12).max()
            mbr=(hi-lo).rolling(180,min_periods=90).mean()
            ratio=(hi12-lo12)/mbr
            r180=c/c.shift(180)-1
            df=pd.DataFrame({"f":f,"ratio":ratio,"dn":c<lo12,"up":c>hi12,"r180":r180,
                             "cell":np.arange(len(b))//H})
            df["coin"]=coin;df["win"]=w
            rows.append(df)
            pos=b["postRebalance_current_allocation"]; g=c.shift(-1)/c-1
            bk.append(pd.DataFrame({"coin":coin,"pos":pos,"g":g,"short":pos<0}))
        drift[coin]=pd.concat(nonov).mean()
    A=pd.concat(rows).dropna(subset=["f","ratio"])
    A["adj"]=A["f"]-A["coin"].map(drift)
    out={}
    def summ(s,col):
        g=s.groupby(col)["adj"]; f=s.groupby(col)["f"]
        return pd.DataFrame({"n":g.size(),"mean_adj_long":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size())),"mean_total_long":f.mean()})
    D=A[A["dn"]].groupby(["coin","win","cell"]).head(1).copy()
    U=A[A["up"]].groupby(["coin","win","cell"]).head(1).copy()
    D["rq"]=pd.qcut(D["ratio"],5,labels=False); U["rq"]=pd.qcut(U["ratio"],5,labels=False)
    D=D.dropna(subset=["r180"]); D["tr"]=np.where(D["r180"]>0,"up30","down30")
    out["down_break_by_width_q_and_30d_sign"]=summ(D,["tr","rq"])
    out["down_break_widest_q_by_coin"]=summ(D[D["rq"]==4],"coin")
    out["down_break_narrowest_q_by_coin"]=summ(D[D["rq"]==0],"coin")
    U=U.dropna(subset=["r180"]); U["tr"]=np.where(U["r180"]>0,"up30","down30")
    out["up_break_by_width_q_and_30d_sign"]=summ(U,["tr","rq"])
    B=pd.concat(bk).dropna()
    B["mkt"]=B["pos"]*B["coin"].map({k:v/H for k,v in drift.items()})
    B["tot"]=B["pos"]*B["g"]
    out["book_bar_decomp_bps"]=(B.groupby("coin")[["tot","mkt"]].mean()*1e4).assign(timing=lambda x:x.tot-x.mkt, share_bars_short=B.groupby("coin")["short"].mean())
    return out
