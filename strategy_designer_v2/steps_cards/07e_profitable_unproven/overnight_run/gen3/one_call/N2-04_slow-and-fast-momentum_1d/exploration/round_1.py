import numpy as np, pandas as pd
from scipy import stats

def explore(data):
    rows=[]; trades=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            r=b["close"].pct_change().shift(-1)
            a=b["postRebalance_current_allocation"].fillna(0)
            v=b["postRebalance_total_value"]
            br=v.pct_change().shift(-1)
            r60=b["close"].pct_change(60); r20=b["close"].pct_change(20)
            vol=b["close"].pct_change().rolling(20).std()
            yr=pd.to_datetime(b["timestamp"]).dt.year
            d=pd.DataFrame({"coin":c,"w":w,"yr":yr,"r":r,"a":a,"br":br,"fc":b["forecast"],
                            "r60":r60,"r20":r20,"vol":vol})
            rows.append(d)
        for w,t in data["trades"][c].items():
            t=t.copy(); t["coin"]=c; t["w"]=w; trades.append(t)
    D=pd.concat(rows).dropna(subset=["r","br"])
    D["held"]=D["a"].abs()>1e-9
    D["beta_part"]=D["a"]*D["r"]
    out={}
    g=D.groupby("coin").agg(book=("br","sum"),coin_drift=("r","mean"),exposure=("held","mean"),
        held_ret=("beta_part","sum"),coin_sum=("r","sum"),n=("r","size"))
    g["drift_x_exposure"]=g["coin_drift"]*g["exposure"]*g["n"]
    g["timing_excess"]=g["held_ret"]-g["drift_x_exposure"]
    out["by_coin"]=g.round(4)
    gw=D.groupby("w").agg(book=("br","sum"),coin_mean=("r","mean"),exposure=("held","mean"))
    out["by_window"]=gw.round(4)
    gy=D.groupby("yr").agg(book=("br","sum"),coin_mean=("r","mean"),exposure=("held","mean"),n=("r","size"))
    out["by_year"]=gy.round(4)
    # daily return when held vs not held
    out["ret_held_vs_flat"]=D.groupby("held")["r"].agg(["mean","std","count"]).round(5)
    # held days excess vs coin's mean
    D["cm"]=D.groupby("coin")["r"].transform("mean")
    h=D[D.held]; ex=h["r"]-h["cm"]
    out["held_excess_daily_t"]=pd.Series({"mean":ex.mean(),"t":ex.mean()/ex.std()*np.sqrt(len(ex)),"n":len(ex)})
    # vol state among held days
    D["volq"]=D.groupby("coin")["vol"].transform(lambda s: pd.qcut(s.rank(method="first"),3,labels=["lo","mid","hi"]))
    out["held_by_vol"]=h.assign(volq=D.loc[h.index.isin(h.index),"volq"] if False else D[D.held]["volq"]).groupby("volq")["br"].agg(["sum","mean","count"]).round(4)
    D["fcq"]=pd.cut(D["fc"],[-0.01,0,0.5,1,2,100])
    out["by_forecast"]=D.groupby("fcq")["r"].agg(["mean","count"]).round(5)
    T=pd.concat(trades)
    p=T["net_profit_loss_percent"]
    s=p.sort_values(ascending=False)
    out["trades"]=pd.Series({"n":len(p),"sum":p.sum(),"win_rate":(p>0).mean(),"top5_sum":s.head(5).sum(),
        "top10_sum":s.head(10).sum(),"median":p.median(),"mean_dur_days":T["duration_minutes"].mean()/1440})
    out["trades_by_coin"]=T.groupby("coin")["net_profit_loss_percent"].agg(["sum","count","median"]).round(2)
    return out
