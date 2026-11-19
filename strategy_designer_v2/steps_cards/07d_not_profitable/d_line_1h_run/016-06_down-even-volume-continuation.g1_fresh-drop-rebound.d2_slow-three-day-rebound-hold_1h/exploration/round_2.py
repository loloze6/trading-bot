def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out={}
    rows=[];gr=[];hold=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b["close"].values
            r=pd.Series(cl).shift(-1)/pd.Series(cl)-1
            a=b["postRebalance_current_allocation"].fillna(0)
            f=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            ac=(a-b["previous_allocation"].fillna(0)).abs()
            ndays=len(b)/24
            rows.append((c,w,(a*r).sum()/ndays,f.sum()/ndays,ac.sum()/ndays,a.mean(),(a!=0).mean(),
                         ((b["forecast"]>0)&(b["forecast"].shift(1)<=0)).sum()/ndays))
            # grid-held version: allocation fixed at grid bar for 72 bars
            idx=np.arange(0,len(b)-72,72)
            for j in idx:
                fc=b["forecast"].iloc[j]
                hold.append((c,fc,cl[j+72]/cl[j]-1,a.iloc[j]))
    R=pd.DataFrame(rows,columns=["coin","w","gross_pd","fee_pd","turn_pd","mean_alloc","share_in","entries_pd"])
    out["per_day_means"]=R[["gross_pd","fee_pd","turn_pd","mean_alloc","share_in","entries_pd"]].mean()
    H=pd.DataFrame(hold,columns=["coin","fc","r72","a"])
    H["ex"]=H["r72"]-H.groupby("coin")["r72"].transform("mean")
    act=H[H.fc>0]
    out["grid_held_gross_per72"]=pd.Series({"n":len(act),"mean_a_x_r72":(act.a*act.r72).mean(),
        "t":stats.ttest_1samp(act.a*act.r72,0).statistic,"mean_r72":act.r72.mean(),"mean_ex":act.ex.mean()})
    top=H[H.fc>=15]; mid=H[(H.fc>0)&(H.fc<15)]
    out["top_vs_mid_ex72"]=pd.Series({"n_top":len(top),"top_ex":top.ex.mean(),"n_mid":len(mid),"mid_ex":mid.ex.mean(),
        "welch_t":stats.ttest_ind(top.ex,mid.ex,equal_var=False).statistic})
    # forecast persistence
    pers=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            fc=b["forecast"].values
            on=fc>0
            # run lengths of on
            runs=[];k=0
            for v in on:
                if v:k+=1
                elif k>0: runs.append(k);k=0
            if k: runs.append(k)
            pers+=runs
    out["on_run_hours"]=pd.Series(pers).describe()
    return out
