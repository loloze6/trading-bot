def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    def clust_t(x,days):
        m=x.mean(); d=pd.DataFrame({"x":x.values,"d":days.values})
        g=d.groupby("d").x.agg(["sum","size"])
        se=np.sqrt(((g["sum"]-g["size"]*m)**2).sum())/len(d)
        return m, (m/se if se>0 else np.nan), g.shape[0]
    summary={}
    for H in (3,5,7,10):
        drift={}
        for coin,wins in data["bars"].items():
            g=[]
            for w,b in wins.items():
                c=b["close"].values; idx=np.arange(0,len(c)-H,H)
                g+=list(c[idx+H]/c[idx]-1)
            drift[coin]=np.mean(g)
        rows=[]
        for coin,wins in data["bars"].items():
            for w,b in wins.items():
                b=b.reset_index(drop=True); c=b["close"].values; n=len(c)
                rec=b.get("debug_info.components.fall30.last_history_value")
                rc=pd.Series(c).pct_change(30).values*100
                for i in range(0,n-H,H):
                    if b.loc[i,"regime"]!="unknown": continue
                    v=rec.iloc[i] if rec is not None and pd.notna(rec.iloc[i]) else rc[i]
                    if pd.isna(v): continue
                    rows.append({"coin":coin,"win":w,"year":pd.Timestamp(b.loc[i,"timestamp"]).year,
                        "day":str(b.loc[i,"timestamp"])[:10],"r30":v,"fc":b.loc[i,"forecast"],
                        "ret":c[i+H]/c[i]-1,"ex":c[i+H]/c[i]-1-drift[coin]})
        df=pd.DataFrame(rows)
        fa=df[df.fc<0].copy()
        fa["sx"]=-fa.ex; fa["w"]=-fa.fc/10; fa["wsx"]=fa.w*fa.sx
        m,t,nd=clust_t(fa.wsx,fa.day); mu,tu,_=clust_t(fa.sx,fa.day)
        mt,tt,_=clust_t(-fa.ret,fa.day)
        s=fa.sort_values(fa.fc.abs().name if False else "w",kind="stable"); k=len(s)//2
        s2=fa.sort_values("r30"); 
        summary[H]={"cases":len(fa),"days":nd,"w_mean":m,"w_t":t,"unw_mean":mu,"unw_t":tu,
            "total_mean":mt,"total_t":tt,
            "bigfc_minus_smallfc":s.sx.iloc[-k:].mean()-s.sx.iloc[:k].mean(),
            "deep_minus_shallow_r30":s2.sx.iloc[:k].mean()-s2.sx.iloc[-k:].mean(),
            "spearman_fc_r30":stats.spearmanr(fa.fc,fa.r30)[0]}
        ri=df[df.r30>0].copy()
        if len(ri)>2:
            mr,tr,ndr=clust_t(ri.ex,ri.day)
            summary[H].update({"rise_cases":len(ri),"rise_ex_mean":mr,"rise_t":tr})
        if H==5:
            out["H5_by_year"]=fa.groupby("year").sx.agg(["count","mean"])
            out["H5_by_coin"]=fa.groupby("coin").sx.agg(["count","mean"])
            fa["q"]=pd.qcut(fa.w.rank(method="first"),3,labels=["small_fc","mid_fc","big_fc"])
            out["H5_by_fc_tercile"]=fa.groupby("q").sx.agg(["count","mean"])
            fa["pos"]=np.where(fa.ret<0,"fell","rose")
            out["H5_share_fell"]=float((fa.ret<0).mean())
    out["summary_by_H"]=pd.DataFrame(summary)
    return out
