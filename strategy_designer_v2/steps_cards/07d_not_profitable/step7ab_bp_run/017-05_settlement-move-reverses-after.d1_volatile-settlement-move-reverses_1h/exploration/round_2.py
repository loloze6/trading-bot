def explore(data):
    import numpy as np, pandas as pd
    res={}
    rows=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.reset_index(drop=True)
            c=b["close"].astype(float)
            nxt=c.shift(-1)/c-1
            a=b["postRebalance_current_allocation"].astype(float)
            pa=b["previous_allocation"].astype(float)
            f=b["forecast"].astype(float)
            hr=pd.to_datetime(b["timestamp"]).dt.hour
            hclose=(hr+1)%24
            hs=hclose%8  # hours since settlement close
            tv=b["total_portfolio_value"].astype(float); pv=b["postRebalance_total_value"].astype(float)
            fee=(tv-pv)/tv
            d=pd.DataFrame({"coin":coin,"w":w,"hs":hs,"a":a,"pa":pa,"f":f,"gain":a*nxt*1e4,"fee":fee*1e4,
                            "turn":(a-pa).abs(),"absa":a.abs(),"sgn_agree":np.sign(a)*np.sign(f)})
            # last nonzero forecast sign carried
            lf=f.where(f!=0).ffill()
            d["agree_last"]=np.sign(a)*np.sign(lf)
            d["regime"]=b["regime"].values
            rows.append(d)
    D=pd.concat(rows)
    g=D.groupby("hs")
    res["by_hours_since_settlement"]=pd.DataFrame({"gain_bps":g["gain"].mean(),"fee_bps":g["fee"].mean(),"turn":g["turn"].mean(),"absa":g["absa"].mean(),"agree_last":g["agree_last"].mean(),"share_flat":g["absa"].apply(lambda x:(x<1e-6).mean())})
    res["totals_bps_per_bar"]=pd.Series({"gain":D["gain"].mean(),"fee":D["fee"].mean(),"turn":D["turn"].mean(),"absa":D["absa"].mean()})
    # at settlement bars with forecast: allocation vs forecast
    S=D[(D["hs"]==0)&(D["f"]!=0)]
    res["sett_bars"]=pd.Series({"n":len(S),"agree_sign_alloc_f":(np.sign(S["a"])==np.sign(S["f"])).mean(),"mean_absa":S["absa"].mean(),"mean_turn":S["turn"].mean(),"prev_absa":S["pa"].abs().mean()})
    # trades: duration distribution and side vs entry forecast
    tr=[]
    for coin,wins in data["trades"].items():
        for w,t in wins.items():
            if len(t): tt=t.copy(); tt["coin"]=coin; tr.append(tt)
    T=pd.concat(tr)
    T["dur_h"]=T["duration_minutes"]/60
    T["side_f_agree"]=np.where(T["side"]=="LONG",1,-1)*np.sign(T["entry_forecast"])
    T["durb"]=pd.cut(T["dur_h"],[-1,1,4,8,9,16,48,1e6])
    res["trades_by_dur"]=T.groupby("durb").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),agree=("side_f_agree","mean"))
    res["trades_entry_hour"]=T.assign(eh=(pd.to_datetime(T["entry_time"]).dt.hour)%8).groupby("eh").agg(n=("side","size"),gross=("profit_loss_percent","mean"),agree=("side_f_agree","mean"))
    # book daily
    dd=[]
    for coin,wins in data["days"].items():
        for w,x in wins.items():
            dd.append(pd.DataFrame({"w":w,"br":x["book_return"],"cr":x["coin_return"]}))
    DD=pd.concat(dd)
    res["book_by_window"]=DD.groupby("w")[["br","cr"]].mean()*1e4
    return res
