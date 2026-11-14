def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]; trs=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy(); c=b["close"].astype(float)
            b["ret"]=c.pct_change()
            for h in (1,2,3,5):
                b[f"r{h}"]=c.shift(-h)/c-1
            b["r2only"]=c.shift(-2)/c.shift(-1)-1
            b["vol20"]=b["ret"].rolling(20).std()
            b["vol100"]=b["ret"].rolling(100,min_periods=40).std()
            b["vrel"]=b["vol20"]/b["vol100"]
            b["f"]=b["forecast"].astype(float)
            b["fprev"]=b["f"].shift(1)
            b["alloc"]=b["postRebalance_current_allocation"].astype(float)
            bv=b["postRebalance_total_value"].astype(float)
            b["bret"]=bv.shift(-1)/bv-1
            b["dd"]=bv/bv.cummax()-1
            b["coin"]=coin; b["w"]=w
            rows.append(b)
        for w,t in data["trades"][coin].items():
            t=t.copy(); t["coin"]=coin; trs.append(t)
    B=pd.concat(rows)
    T=pd.concat(trs)
    out={}
    E=B[(B.f>=16)&(B.fprev<16)].dropna(subset=["r1"])  # first big-drop bars
    def st(x):
        x=x.dropna(); return pd.Series({"n":len(x),"mean":x.mean(),"hit":(x>0).mean(),"t":x.mean()/x.std()*np.sqrt(len(x))})
    out["after_bigdrop_horizons"]=pd.DataFrame({k:st(E[k]) for k in ["r1","r2only","r2","r3","r5"]}).T
    S=B[(B.f>=16)].dropna(subset=["r1"])
    S=S.assign(cons=np.where(S.fprev>=16,"repeat_bigdrop","first_bigdrop"))
    out["first_vs_repeat"]=S.groupby("cons")["r1"].apply(st).unstack()
    A=B[B.f>0].dropna(subset=["r1","vol20"]).copy()
    A["vq"]=pd.qcut(A["vol20"],3,labels=["low","mid","high"])
    A["fq"]=np.where(A.f>=8,"f>=8","f<8")
    out["vol_x_f"]=A.groupby(["vq","fq"])["r1"].apply(st).unstack()
    A2=A.dropna(subset=["vrel"]).copy()
    A2["vr"]=pd.qcut(A2["vrel"],3,labels=["vol_falling","vol_flat","vol_rising"])
    out["bigf_by_vrel"]=A2[A2.f>=8].groupby("vr")["r1"].apply(st).unstack()
    out["maxdd_by_coin"]=B.groupby("coin")["dd"].min()
    out["maxdd_by_window_worst"]=B.groupby("w")["dd"].min().sort_values().head(8).reset_index(drop=True)
    T["dur_d"]=(T.duration_minutes/1440).round()
    T["db"]=pd.cut(T.dur_d,[-1,1,2,4,1000])
    out["trades_by_dur"]=T.groupby("db").agg(n=("profit_loss_percent","size"),gross=("profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()),fee=("total_commission","mean"))
    out["worst_day_losses"]=pd.Series({"bret_q01":B.bret.quantile(0.01),"share_neg_from_f>=16":B.loc[(B.bret<0)&(B.f>=16),"bret"].sum()/B.loc[B.bret<0,"bret"].sum(),
       "share_pos_from_f>=16":B.loc[(B.bret>0)&(B.f>=16),"bret"].sum()/B.loc[B.bret>0,"bret"].sum(),"r1_sd_f>=16":S.r1.std(),"r1_q05_f>=16":S.r1.quantile(0.05)})
    return out
