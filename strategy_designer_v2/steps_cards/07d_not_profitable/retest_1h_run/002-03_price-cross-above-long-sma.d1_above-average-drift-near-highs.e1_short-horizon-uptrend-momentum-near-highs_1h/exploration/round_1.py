def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; bins=[]; runs=[]; daily=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"].values
            al=b["postRebalance_current_allocation"].fillna(0).values
            r1=np.append(c[1:]/c[:-1]-1,np.nan)
            gross=al*r1
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"]).values/b["total_portfolio_value"].values
            turn=np.abs(al-b["previous_allocation"].fillna(0).values)
            f=b["forecast"].fillna(0).values
            rows.append(dict(coin=coin,w=w,bars=len(b),gross=np.nansum(gross),fee=np.nansum(fee),
                             turn=turn.sum(),active=(al>0).mean(),fpos=(f>0).mean(),trend=(b["regime"]=="trending").mean()))
            on=(f>0).astype(int); ch=np.diff(np.r_[0,on,0])
            st=np.where(ch==1)[0]; en=np.where(ch==-1)[0]
            runs+=list(en-st)
            for h in [6,24,72,336]:
                idx=np.arange(0,len(c)-h,h)
                fr=c[idx+h]/c[idx]-1
                for i,x in zip(idx,fr):
                    bins.append((h,f[i],x,b["regime"].iloc[i]=="trending"))
    R=pd.DataFrame(rows)
    tot=R[["gross","fee","turn","bars"]].sum()
    out={}
    out["totals"]=pd.Series({"gross_sum_per_day":tot.gross/tot.bars*24,"fee_sum_per_day":tot.fee/tot.bars*24,
        "turnover_per_day":tot.turn/tot.bars*24,"active_share":R.active.mean(),"fpos_share":R.fpos.mean(),"trend_share":R.trend.mean()})
    out["by_coin"]=R.groupby("coin")[["gross","fee","turn"]].sum()
    runs=np.array(runs)
    out["run_len_hours"]=pd.Series({"n":len(runs),"median":np.median(runs),"mean":runs.mean(),"share_le3":(runs<=3).mean()})
    B=pd.DataFrame(bins,columns=["h","f","r","tr"])
    B=B[B.tr]
    B["grp"]=np.where(B.f<=0,"zero",pd.qcut(B.f.where(B.f>0),3,labels=["lo","mid","hi"]).astype(str))
    out["fwd_by_forecast"]=B.groupby(["h","grp"]).r.agg(["mean","count"]).unstack(0)
    return out
