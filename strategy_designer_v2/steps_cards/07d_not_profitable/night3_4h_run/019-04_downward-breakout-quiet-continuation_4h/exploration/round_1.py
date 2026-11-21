def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    H=18
    rows=[]; drift={}
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
            dn=c<lo12; up=c>hi12
            depth_dn=(lo12-c)/mbr; depth_up=(c-hi12)/mbr
            ret12=c/c.shift(12)-1
            ret36=c/c.shift(36)-1
            ret180=c/c.shift(180)-1
            df=pd.DataFrame({"f":f,"ratio":ratio,"dn":dn,"up":up,"ddn":depth_dn,"dup":depth_up,
                             "r36":ret36,"r180":ret180,"cell":np.arange(len(b))//H})
            df["coin"]=coin;df["win"]=w
            df["year"]=pd.to_datetime(b["timestamp"]).dt.year
            rows.append(df)
        drift[coin]=pd.concat(nonov).mean()
    A=pd.concat(rows).dropna(subset=["f","ratio"])
    A["adj"]=A["f"]-A["coin"].map(drift)
    def first(m):
        s=A[m]; return s.groupby(["coin","win","cell"]).head(1)
    def summ(s,col,sign):
        g=s.groupby(col)["adj"]
        return pd.DataFrame({"n":g.size(),"mean_adj_dir":sign*g.mean(),
                             "t":sign*g.mean()/(g.std()/np.sqrt(g.size()))})
    out={}
    out["drift18_by_coin"]=pd.Series(drift)
    D=first(A["dn"]).copy(); U=first(A["up"]).copy()
    G=A.groupby(["coin","win","cell"]).head(1).copy()
    for s in (D,U,G):
        s["rq"]=pd.qcut(s["ratio"],5,labels=False)
    out["down_break_long_by_width_q"]=summ(D,"rq",1)
    out["up_break_long_by_width_q"]=summ(U,"rq",1)
    out["all_grid_absmove_by_width_q"]=G.groupby("rq")["f"].apply(lambda x:x.abs().mean())
    D["dq"]=pd.qcut(D["ddn"],5,labels=False); U["dq"]=pd.qcut(U["dup"],5,labels=False)
    out["down_break_long_by_depth_q"]=summ(D,"dq",1)
    out["up_break_long_by_depth_q"]=summ(U,"dq",1)
    D["tq"]=pd.qcut(D["r180"],5,labels=False)
    out["down_break_long_by_30d_ret_q"]=summ(D.dropna(subset=["r180"]),"tq",1)
    out["down_break_long_by_year"]=summ(D,"year",1)
    out["down_break_long_by_coin"]=summ(D,"coin",1)
    # book
    dd=[];
    for coin,ws in data["days"].items():
        for w,d in ws.items(): dd.append(d.assign(coin=coin,win=w))
    Dd=pd.concat(dd)
    out["book_daily_mean_by_coin"]=Dd.groupby("coin")[["book_return","coin_return"]].mean()
    tr=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=tr.groupby("side")[["profit_loss_percent","net_profit_loss_percent","duration_minutes"]].agg(["mean","count"])
    return out
