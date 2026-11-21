def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    H=18
    for coin, wins in data["bars"].items():
        fr=[]
        for w,b in wins.items():
            c=b["close"].values
            idx=np.arange(0,len(c)-H,H)
            fr+=list(c[idx+H]/c[idx]-1)
        drift=np.mean(fr) if fr else 0; usual=np.std(fr) if fr else np.nan
        for w,b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"]; h=b["high"]; l=b["low"]
            lo12=l.shift(1).rolling(12).min(); hi12=h.shift(1).rolling(12).max()
            span=(hi12-lo12)/c
            mbr=((h-l)/c).shift(1).rolling(180,min_periods=60).mean()
            narrow=span/mbr
            r30=c/c.shift(180)-1
            r3d=c/c.shift(18)-1
            n=len(b)
            dn=c<lo12
            grid=np.arange(n)//H
            fc=b["forecast"]
            wv=b["debug_info.components.width.last_history_value"] if "debug_info.components.width.last_history_value" in b else pd.Series(np.nan,index=b.index)
            wp=b["debug_info.components.width.post_pipeline_value"] if "debug_info.components.width.post_pipeline_value" in b else pd.Series(np.nan,index=b.index)
            df=pd.DataFrame({"g":grid,"dn":dn,"narrow":narrow,"r30":r30,"r3d":r3d,
                             "f6":c.shift(-6)/c-1,"f18":c.shift(-18)/c-1,"f36":c.shift(-36)/c-1,
                             "fc":fc,"wv":wv,"wp":wp,"alloc":b["postRebalance_current_allocation"]})
            s=df[df["dn"]].dropna(subset=["narrow","r30","f18"]).groupby("g").head(1)
            rows.append(s.assign(coin=coin,win=w,drift=drift,usual=usual))
    A=pd.concat(rows)
    A["u18"]=A["f18"]-A["drift"]
    A["str"]=-A["u18"]/A["usual"]
    A["r30pos"]=A["r30"]>0
    A["nq"]=pd.qcut(A["narrow"],5,labels=False)
    A["r3neg"]=A["r3d"]<A["r3d"].median()
    def agg(g):
        m=g["u18"].mean(); s=g["u18"].std(); n=len(g)
        return pd.Series({"n":n,"mean_u18":m,"t":m/(s/np.sqrt(n)) if n>1 else np.nan,"mean_f18":g["f18"].mean(),"mean_f36":g["f36"].mean(),"short_strength":g["str"].mean()})
    out={}
    out["nq_x_r30pos"]=A.groupby(["r30pos","nq"]).apply(agg)
    A["r3q"]=pd.qcut(A["r3d"],3,labels=False)
    out["nq_x_r3d_tercile"]=A.groupby(["r3q","nq"]).apply(agg)
    N0=A[A.nq<=1]
    out["narrow2q_by_window_sign"]=pd.Series({"windows":N0.groupby("win")["u18"].mean().shape[0],"share_neg":(N0.groupby("win")["u18"].mean()<0).mean()})
    out["narrow2q_by_coin_share_neg"]=pd.Series({"share_neg":(N0.groupby("coin")["u18"].mean()<0).mean(),"coins":N0["coin"].nunique()})
    act=A[A.fc<0]
    out["book_active_cases"]=pd.Series({"n":len(act),"corr_narrow_fc":act[["narrow","fc"]].corr().iloc[0,1],
        "corr_narrow_wv":act[["narrow","wv"]].corr().iloc[0,1],"corr_narrow_wp":act[["narrow","wp"]].corr().iloc[0,1],
        "fc_mean":act["fc"].mean(),"wv_med":act["wv"].median(),"wp_med":act["wp"].median(),"alloc_mean":act["alloc"].mean()})
    out["book_active_by_nq"]=act.groupby("nq").apply(agg)
    return out
