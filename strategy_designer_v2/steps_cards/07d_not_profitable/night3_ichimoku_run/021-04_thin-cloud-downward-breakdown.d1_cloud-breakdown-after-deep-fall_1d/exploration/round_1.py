def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    bars=data["bars"]; H=26
    rows=[]; drift={}; up_rows=[]
    for c in bars:
        rets=[]
        for w,df in bars[c].items():
            cl=df["close"].values
            for i in range(0,len(cl)-H,H): rets.append(cl[i+H]/cl[i]-1)
        drift[c]=np.mean(rets)
        for w,df in bars[c].items():
            df=df.reset_index(drop=True); cl=df["close"]; hi=df["high"]; lo=df["low"]
            ten=(hi.rolling(9).max()+lo.rolling(9).min())/2
            kij=(hi.rolling(26).max()+lo.rolling(26).min())/2
            sa=((ten+kij)/2).shift(26); sb=((hi.rolling(52).max()+lo.rolling(52).min())/2).shift(26)
            top=np.maximum(sa,sb); bot=np.minimum(sa,sb)
            state=np.where(cl>top,1,np.where(cl<bot,-1,0)).astype(float); state[top.isna().values]=np.nan
            last=None
            for i in range(len(df)):
                s=state[i]
                if np.isnan(s): continue
                prev=last
                if s!=0: last=s
                if i+H>=len(df) or i<60: continue
                fwd=cl[i+H]/cl[i]-1; r26=cl[i]/cl[i-26]-1; r60=cl[i]/cl[i-60]-1
                thick=(top[i]-bot[i])/cl[i]
                if s==-1 and prev==1:
                    rows.append(dict(c=c,w=w,fwd=fwd,un=-(fwd-drift[c]),r26=r26,r60=r60,thick=thick,cloudslope=sa[i]-sa[i-5]>0))
                if s==1 and prev==-1:
                    up_rows.append(dict(c=c,w=w,fwd=fwd,un=fwd-drift[c],r26=r26,r60=r60,thick=thick))
    d=pd.DataFrame(rows); u=pd.DataFrame(up_rows)
    out={}
    def summ(x):
        return pd.Series(dict(n=len(x),fwd_mean=x.fwd.mean(),t_fwd=stats.ttest_1samp(x.fwd,0).statistic if len(x)>2 else np.nan,un_mean=x.un.mean()))
    out["down_all"]=summ(d)
    d["r26q"]=pd.qcut(d.r26,4,labels=False); out["down_by_r26q"]=d.groupby("r26q").apply(summ)
    d["r60q"]=pd.qcut(d.r60,4,labels=False); out["down_by_r60q"]=d.groupby("r60q").apply(summ)
    d["thq"]=pd.qcut(d.thick,3,labels=False); out["down_by_thick"]=d.groupby("thq").apply(summ)
    out["down_by_coin"]=d.groupby("c").apply(summ)
    out["corr_down"]=d[["fwd","r26","r60","thick"]].corr()["fwd"]
    out["up_all"]=summ(u)
    u["r26q"]=pd.qcut(u.r26,4,labels=False); out["up_by_r26q"]=u.groupby("r26q").apply(summ)
    u["thq"]=pd.qcut(u.thick,3,labels=False); out["up_by_thick"]=u.groupby("thq").apply(summ)
    out["corr_up"]=u[["fwd","r26","r60","thick"]].corr()["fwd"]
    out["drift26"]=pd.Series(drift)
    # book
    br=[]
    for c in data["days"]:
        for w,df in data["days"][c].items():
            br.append(df.assign(c=c,w=w))
    B=pd.concat(br); g=B.groupby(["w"])[["book_return","coin_return"]].mean()
    out["book_by_window_sum"]=B.groupby("w")[["book_return","coin_return"]].sum().sort_values("book_return").head(10)
    tr=pd.concat([t.assign(c=c) for c in data["trades"] for w,t in data["trades"][c].items()])
    out["trades"]=pd.Series(dict(n=len(tr),mean_pl=tr.profit_loss_percent.mean(),mean_net=tr.net_profit_loss_percent.mean(),win=(tr.profit_loss_percent>0).mean()))
    return out
