def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    out = {}
    gross=[];fee=[];allocs=[];rows=[]
    daily=[]
    cm={}
    for c in data["bars"]:
        dr=[]
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].fillna(0)
            g=(a*r)
            f=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            gross.append(g.sum()); fee.append(f.sum()); allocs.append(a.mean())
            ts=pd.to_datetime(b["timestamp"])
            # grid 72
            for h in [0]:
                idx=np.arange(0,len(b)-72,72)
                cl=b["close"].values
                ret72=cl[idx+72]/cl[idx]-1
                ret24=cl[idx+24]/cl[idx]-1
                past72=np.full(len(idx),np.nan); past24=np.full(len(idx),np.nan)
                ok=idx>=72
                past72[ok]=cl[idx[ok]]/cl[idx[ok]-72]-1
                ok2=idx>=24
                past24[ok2]=cl[idx[ok2]]/cl[idx[ok2]-24]-1
                for i,j in enumerate(idx):
                    rows.append((c,w,b["forecast"].iloc[j],b["regime"].iloc[j],ret72[i],ret24[i],past72[i],past24[i],ts.iloc[j].year))
        d=data["days"][c]
        for w,dd in d.items():
            dr.append(dd[["book_return","coin_return"]].assign(w=w))
        dr=pd.concat(dr); cm[c]=dr["coin_return"].mean()
        daily.append(dr.assign(coin=c))
    out["gross_sum_vs_fee_sum"]=pd.Series({"gross":np.sum(gross),"fee":np.sum(fee),"mean_alloc":np.mean(allocs)})
    D=pd.concat(daily)
    out["per_coin_book"]=D.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"),sd=("book_return","std"))
    G=pd.DataFrame(rows,columns=["coin","w","fc","reg","r72","r24","p72","p24","yr"])
    G["ex72"]=G["r72"]-G.groupby("coin")["r72"].transform("mean")
    G["ex24"]=G["r24"]-G.groupby("coin")["r24"].transform("mean")
    G["late"]=(1+G["r72"])/(1+G["r24"])-1
    G["exlate"]=G["late"]-G.groupby("coin")["late"].transform("mean")
    M=G[G.reg=="mean_reversion"].copy()
    M["fb"]=pd.cut(M["fc"],[-0.1,0.001,5,10,15,20.1])
    out["fc_bucket"]=M.groupby("fb").agg(n=("ex72","size"),ex72=("ex72","mean"),ex24=("ex24","mean"),exlate=("exlate","mean"))
    M["p72q"]=pd.qcut(M["p72"],4)
    out["by_p72_depth"]=M.groupby("p72q").agg(n=("ex72","size"),ex72=("ex72","mean"),ex24=("ex24","mean"))
    out["by_year_regime"]=G.groupby(["yr","reg"]).agg(n=("ex72","size"),ex72=("ex72","mean"))
    G["p24q"]=pd.qcut(G["p24"],5)
    out["all_grid_by_p24"]=G.groupby(["reg","p24q"]).agg(n=("ex72","size"),ex72=("ex72","mean"),ex24=("ex24","mean"))
    T=[]
    for c in data["trades"]:
        for w,t in data["trades"][c].items(): T.append(t)
    T=pd.concat(T)
    out["trades"]=pd.Series({"n":len(T),"med_dur_h":T["duration_minutes"].median()/60,"mean_pl":T["profit_loss_percent"].mean(),"mean_net":T["net_profit_loss_percent"].mean(),"mean_comm":T["total_commission"].mean()})
    return out
