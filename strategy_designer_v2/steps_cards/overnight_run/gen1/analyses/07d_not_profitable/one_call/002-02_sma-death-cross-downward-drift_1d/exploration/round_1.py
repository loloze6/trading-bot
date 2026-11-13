import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]; trs=[]
    for coin, wins in data["bars"].items():
        for w, b in wins.items():
            b=b.sort_values("timestamp").copy()
            alloc=pd.to_numeric(b["postRebalance_current_allocation"],errors="coerce").fillna(0)
            fc=pd.to_numeric(b["forecast"],errors="coerce").fillna(0)
            c=b["close"].astype(float)
            nxt=c.shift(-1)/c-1
            v=b["postRebalance_total_value"].astype(float)
            bret=v.shift(-1)/v-1
            r20=c/c.shift(20)-1
            vol=c.pct_change().rolling(20).std()
            fwd10=c.shift(-10)/c-1
            d=pd.DataFrame({"coin":coin,"w":w,"year":pd.to_datetime(b["timestamp"]).dt.year.values,
                "alloc":alloc.values,"fc":fc.values,"nxt":nxt.values,"bret":bret.values,
                "r20":r20.values,"vol":vol.values,"fwd10":fwd10.values,"raw":pd.to_numeric(b["debug_info.components.sma_cross_down.last_history_value"],errors="coerce").values})
            rows.append(d)
            t=data["trades"][coin][w].copy(); t["coin"]=coin; t["w"]=w; trs.append(t)
    D=pd.concat(rows,ignore_index=True).dropna(subset=["nxt","bret"])
    D["gross"]=D["alloc"]*D["nxt"]; D["fee"]=D["gross"]-D["bret"]
    A=D[D.fc<0].copy()
    out={}
    out["overall"]=pd.Series({"bars":len(D),"share_short":(D.fc<0).mean(),"mean_alloc_when_short":A.alloc.mean(),
        "gross_daily_all":D.gross.mean(),"book_daily_all":D.bret.mean(),"fee_daily_all":D.fee.mean(),
        "coin_daily_all":D.nxt.mean(),"coin_daily_when_short":A.nxt.mean(),"coin_daily_when_flat":D[D.fc==0].nxt.mean(),
        "corr_alloc_fc":D[["alloc","fc"]].corr().iloc[0,1]})
    A["q"]=pd.qcut(A.fc.abs(),3,labels=["low","mid","high"])
    out["by_fc_tercile"]=A.groupby("q").agg(n=("nxt","size"),coin_nxt=("nxt","mean"),gross=("gross","mean"),book=("bret","mean"),fwd10=("fwd10","mean"),alloc=("alloc","mean"))
    out["by_coin"]=D.groupby("coin").agg(gross=("gross","mean"),book=("bret","mean"),fee=("fee","mean"),coin=("nxt","mean"),short_share=("fc",lambda x:(x<0).mean()))
    out["by_year"]=D.groupby("year").agg(gross=("gross","sum"),book=("bret","sum"),coin=("nxt","mean"),short_share=("fc",lambda x:(x<0).mean()))
    out["by_window"]=D.groupby("w").agg(gross=("gross","sum"),book=("bret","sum"),coin=("nxt","mean"),short_share=("fc",lambda x:(x<0).mean()))
    A["trend20"]=np.where(A.r20>0,"up20","down20")
    A["volq"]=pd.qcut(A.vol,3,labels=["calm","mid","volatile"])
    out["short_by_trend20"]=A.groupby("trend20").agg(n=("nxt","size"),gross=("gross","mean"),coin=("nxt","mean"))
    out["short_by_vol"]=A.groupby("volq").agg(n=("nxt","size"),gross=("gross","mean"),coin=("nxt","mean"))
    A["rawq"]=pd.qcut(A.raw,4)
    out["short_by_raw_spread"]=A.groupby("rawq").agg(n=("nxt","size"),gross=("gross","mean"),fwd10=("fwd10","mean"))
    T=pd.concat(trs,ignore_index=True)
    T["days"]=T.duration_minutes/1440
    out["trades"]=T.groupby("side").agg(n=("days","size"),med_days=("days","median"),mean_days=("days","mean"),gross_mean=("profit_loss_percent","mean"),net_mean=("net_profit_loss_percent","mean"),gross_sum=("profit_loss_percent","sum"),net_sum=("net_profit_loss_percent","sum"),win=("profit_loss_percent",lambda x:(x>0).mean()))
    T["dq"]=pd.cut(T.days,[0,1,3,10,30,1e5])
    out["trades_by_dur"]=T.groupby("dq").agg(n=("days","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"))
    return out
