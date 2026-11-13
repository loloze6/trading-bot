def explore(data):
    import pandas as pd, numpy as np
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            r=b["close"].pct_change()
            a=b["postRebalance_current_allocation"].shift(1)
            bv=b["postRebalance_total_value"].pct_change()
            f=b["forecast"].shift(1)
            ma=b["close"].rolling(20).mean()
            trend20=b["close"]/b["close"].shift(20)-1
            vol=r.rolling(20).std()
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year,
                            "r":r,"a":a,"f":f,"book":bv,"gross":a*r,"trend20":trend20.shift(1),"vol":vol.shift(1),
                            "fwd10":b["close"].shift(-10)/b["close"]-1})
            d["fwd10"]=d["fwd10"].shift(1)
            rows.append(d.iloc[1:])
    D=pd.concat(rows,ignore_index=True)
    D["fee"]=D["gross"]-D["book"]
    act=D[D["a"].abs()>1e-9]
    out={}
    out["overall"]=pd.Series({"bars":len(D),"active_share":len(act)/len(D),"mean_gross_all":D["gross"].mean(),
        "mean_book_all":D["book"].mean(),"mean_fee_all":D["fee"].mean(),"mean_abs_alloc_active":act["a"].abs().mean(),
        "mean_coin_ret_active":act["r"].mean(),"mean_coin_ret_flat":D[D["a"].abs()<=1e-9]["r"].mean(),
        "t_gross":D["gross"].mean()/D["gross"].std()*np.sqrt(len(D))})
    act=act.copy()
    act["fbin"]=pd.cut(act["f"],[-20.1,-15,-10,-5,-2,-1e-9],labels=["<-15","-15..-10","-10..-5","-5..-2","-2..0"])
    out["by_forecast"]=act.groupby("fbin").agg(n=("r","size"),coin_ret=("r","mean"),gross=("gross","mean"),fee=("fee","mean"),book=("book","mean"),alloc=("a","mean"))
    out["by_coin"]=D.groupby("coin").agg(gross=("gross","mean"),book=("book","mean"),fee=("fee","mean"),active=("a",lambda x:(x.abs()>1e-9).mean()),coin_ret=("r","mean"))
    out["by_year"]=D.groupby("year").agg(n=("r","size"),gross=("gross","mean"),book=("book","mean"),fee=("fee","mean"),active=("a",lambda x:(x.abs()>1e-9).mean()),coin_ret=("r","mean"))
    act["trend"]=np.where(act["trend20"]>0,"up20","down20")
    act["vt"]=pd.qcut(act["vol"],3,labels=["calm","mid","volatile"])
    out["active_by_trend_vol"]=act.groupby(["trend","vt"]).agg(n=("r","size"),coin_ret=("r","mean"),gross=("gross","mean"),book=("book","mean"))
    T=[]
    for coin,ws in data["trades"].items():
        for w,t in ws.items():
            if len(t): T.append(t.assign(coin=coin))
    T=pd.concat(T,ignore_index=True)
    T["days"]=T["duration_minutes"]/1440
    out["trades"]=T.groupby("side").agg(n=("days","size"),med_days=("days","median"),mean_days=("days","mean"),gross_pct=("profit_loss_percent","mean"),net_pct=("net_profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()),comm=("total_commission","mean"))
    T["dbin"]=pd.cut(T["days"],[0,1.5,3.5,10.5,30.5,1e5],labels=["1d","2-3d","4-10d","11-30d",">30d"])
    out["trades_by_dur"]=T.groupby("dbin").agg(n=("days","size"),gross_pct=("profit_loss_percent","mean"),net_pct=("net_profit_loss_percent","mean"),sum_gross=("profit_loss_percent","sum"))
    # rebalance turnover
    D["turn"]=D.groupby(["coin","w"])["a"].diff().abs()
    out["turnover"]=pd.Series({"mean_abs_alloc_change_per_bar":D["turn"].mean(),"share_bars_change":(D["turn"]>1e-9).mean()})
    return out
