import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            r=b["close"].shift(-1)/b["close"]-1
            a=b["postRebalance_current_allocation"].astype(float)
            sp=b["debug_info.components.sma_cross.last_history_value"]
            d=pd.DataFrame({"coin":c,"w":w,"fc":b["forecast"],"alloc":a,"r":r,"g":a*r,
                "sp":sp,"dsp10":sp-sp.shift(10),"ret20":b["close"]/b["close"].shift(20)-1,
                "vol20":b["close"].pct_change().rolling(20).std(),"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["r"])
    out={}
    # pooled book by window
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            x=x.copy(); x["coin"]=c; x["w"]=w; dd.append(x)
    Dy=pd.concat(dd)
    P=Dy.groupby(["w","day"])[["book_return","coin_return"]].mean().reset_index()
    P["wn"]=P["w"].str[1:].astype(int)
    P=P.sort_values(["wn","day"])
    pw=P.groupby("wn").agg(book=("book_return",lambda s:(1+s.fillna(0)).prod()-1),
                          hold=("coin_return",lambda s:(1+s.fillna(0)).prod()-1),
                          n=("book_return","count"))
    eq=(1+P["book_return"].fillna(0)).cumprod().values
    dd_=eq/np.maximum.accumulate(eq)-1
    P["dd"]=dd_
    pw["min_dd_in_w"]=P.groupby("wn")["dd"].min()
    out["per_window"]=pw.round(4)
    out["total_dd"]=float(dd_.min())
    act=D[D.alloc.abs()>1e-9]
    out["active_share"]=float(len(act)/len(D))
    # gain by forecast bucket, active only
    act=act.copy()
    act["fb"]=pd.cut(act.fc,[0,5,10,15,20.01])
    out["by_fc"]=act.groupby("fb").agg(n=("r","size"),mean_r=("r","mean"),mean_g=("g","mean"),sd=("r","std")).round(5)
    out["hold_mean_r"]=float(D.r.mean())
    out["flat_mean_r"]=float(D[D.alloc.abs()<=1e-9].r.mean())
    for k in ["dsp10","ret20","vol20","sp"]:
        x=act.dropna(subset=[k]).copy()
        x["q"]=pd.qcut(x[k],5,labels=False,duplicates="drop")
        out["act_by_"+k]=x.groupby("q").agg(n=("r","size"),lo=(k,"min"),hi=(k,"max"),mean_r=("r","mean"),t=("r",lambda s:s.mean()/s.std()*np.sqrt(len(s)))).round(5)
    out["act_by_coin"]=act.groupby("coin").agg(n=("r","size"),mean_r=("r","mean")).round(5)
    out["act_by_yr"]=act.groupby("yr").agg(n=("r","size"),mean_r=("r","mean")).round(5)
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items()])
    out["trades"]=pd.Series({"n":len(T),"mean_net":T.net_profit_loss_percent.mean(),"mean_gross":T.profit_loss_percent.mean(),"mean_comm":T.total_commission.mean(),"med_dur_days":T.duration_minutes.median()/1440})
    return out
