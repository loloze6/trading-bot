def explore(data):
    import pandas as pd, numpy as np
    from scipy import stats
    out = {}
    # book daily by window
    rows=[]
    for c,ws in data["days"].items():
        for w,d in ws.items():
            d=d.dropna(subset=["book_return"])
            rows.append(pd.DataFrame({"w":w,"c":c,"day":d["day"].values,"br":d["book_return"].values,"cr":d["coin_return"].values}))
    D=pd.concat(rows)
    bd=D.groupby(["w","day"]).agg(br=("br","mean"),cr=("cr","mean")).reset_index()
    g=bd.groupby("w").agg(n=("br","size"),book_mean_bp=("br",lambda x:x.mean()*1e4),book_sum=("br","sum"),coin_mean_bp=("cr",lambda x:x.mean()*1e4))
    out["book_by_window"]=g.round(3)
    # grid cases
    recs=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"].values; n=len(cl)
            r=pd.Series(cl).pct_change()
            vol30=r.rolling(30).std().values
            ret30=pd.Series(cl).pct_change(30).values*100
            for h in (5,10,20):
                pass
            for i in range(0,n,10):
                rec={"c":c,"w":w,"i":i,"regime":b["regime"].iloc[i],"fc":b["forecast"].iloc[i],
                     "alloc":b["postRebalance_current_allocation"].iloc[i],
                     "f30":b["debug_info.components.fall30.last_history_value"].iloc[i] if "debug_info.components.fall30.last_history_value" in b else np.nan,
                     "r30":ret30[i],"vol30":vol30[i],"yr":pd.Timestamp(b["timestamp"].iloc[i]).year}
                for h in (5,10,20):
                    rec[f"f{h}"]=cl[i+h]/cl[i]-1 if i+h<n else np.nan
                recs.append(rec)
    G=pd.DataFrame(recs)
    G["drift10"]=G.groupby("c")["f10"].transform("mean")
    G["vmed"]=G.groupby("c")["vol30"].transform("median")
    G["agit"]=G["vol30"]>G["vmed"]
    G["u10"]=-(G["f10"]-G["drift10"])
    G["t10"]=-G["f10"]
    chop=G[G.regime=="chop"].copy()
    chop["fall"]=chop["f30"].where(chop["f30"].notna(),chop["r30"])
    def summ(x):
        x=x.dropna(subset=["f10"])
        if len(x)<3: return pd.Series({"n":len(x)})
        return pd.Series({"n":len(x),"tot_short_10":x.t10.mean()*100,"t_tot":stats.ttest_1samp(x.t10,0).statistic,
                          "unus_10":x.u10.mean()*100,"tot_short_20":(-x.f20).mean()*100,"tot_short_5":(-x.f5).mean()*100})
    chop["fbin"]=pd.cut(chop["fall"],[-200,-25,-15,-8,-3,0,3,8,15,200])
    out["chop_by_fall30_bin"]=chop.groupby("fbin").apply(summ).round(3)
    sh=chop[chop.fc<=-2]
    out["short_signal_by_agit"]=sh.groupby("agit").apply(summ).round(3)
    out["chop_fall_noSignal_by_agit"]=chop[(chop.fall<0)&(chop.fc>-2)].groupby("agit").apply(summ).round(3)
    sh=sh.copy(); sh["q"]=pd.qcut(sh.fc.abs().rank(method="first"),3,labels=["small","mid","large"])
    out["short_signal_by_tercile"]=sh.groupby("q").apply(summ).round(3)
    out["short_signal_by_window"]=sh.groupby("w").apply(summ).round(3)
    out["short_signal_by_coin"]=sh.groupby("c").apply(summ).round(3)
    out["allgrid_by_agit"]=G.groupby("agit").apply(summ).round(3)
    # trades
    T=pd.concat([t.assign(c=c,w=w) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"]=T.groupby("side").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_d=("duration_minutes",lambda x:x.mean()/1440),win=("net_profit_loss_percent",lambda x:(x>0).mean())).round(3)
    T["q"]=pd.qcut(T.entry_forecast.abs().rank(method="first"),3,labels=["small","mid","large"])
    out["trades_by_entryfc"]=T.groupby("q").agg(n=("net_profit_loss_percent","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),dur_d=("duration_minutes",lambda x:x.mean()/1440)).round(3)
    return out
