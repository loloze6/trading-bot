def explore(data):
    import numpy as np, pandas as pd
    out={}
    T=[]
    for c,wd in data["trades"].items():
        for w,t in wd.items():
            t=t.copy(); t["c"]=c; t["w"]=w; T.append(t)
    T=pd.concat(T)
    T["dur_d"]=T["duration_minutes"]/1440
    T["durq"]=pd.cut(T["dur_d"],[0,2,3.5,6,12,30,1e9])
    out["trades_by_duration_days"]=T.groupby("durq").agg(n=("profit_loss_percent","count"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("profit_loss_percent",lambda x:(x>0).mean()),efc=("entry_forecast","mean"))
    T["fq"]=pd.qcut(T["entry_forecast"].rank(method="first"),4,labels=False)
    out["trades_by_entry_forecast_q(0=most_negative)"]=T.groupby("fq").agg(n=("profit_loss_percent","count"),fc=("entry_forecast","mean"),gross=("profit_loss_percent","mean"),dur_d=("dur_d","mean"))
    # bar-level: position held and gain, in-regime vs out of regime
    rows=[]
    for c,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; lo=b["low"]
            pos=b["postRebalance_current_allocation"]
            g=pos*(cl.shift(-1)/cl-1)
            lo12=lo.shift(1).rolling(12).min()
            brk=(cl<lo12)
            # bars since last break
            idx=pd.Series(np.where(brk,np.arange(len(b)),np.nan)).ffill()
            since=np.arange(len(b))-idx
            r180=cl/cl.shift(180)-1
            rows.append(pd.DataFrame({"pos":pos,"g":g,"since":since,"fc":b["forecast"],"r180":r180,"reg":b["regime"]}))
    Bb=pd.concat(rows).dropna(subset=["g"])
    Bb["sinceq"]=pd.cut(Bb["since"],[-1,0,6,18,36,72,1e9])
    act=Bb[Bb.pos<0]
    out["held_short_bars_by_bars_since_last_break"]=act.groupby("sinceq").agg(n=("g","count"),pos=("pos","mean"),gain_bps=("g",lambda x:x.mean()*1e4),fc_zero_share=("fc",lambda x:(x==0).mean()))
    out["share_short_bars_with_fc0"]=float((act.fc==0).mean())
    out["short_bars_r180_pos_share"]=float((act.r180>0).mean())
    # narrow down breaks: forward horizons, pos r180
    H=18; res=[]
    for c,wd in data["bars"].items():
        for w,b in wd.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; lo=b["low"]; hi=b["high"]
            lo12=lo.shift(1).rolling(12).min(); hi12=hi.shift(1).rolling(12).max()
            ratio=(hi12-lo12)/(hi-lo).shift(1).rolling(180).mean()
            r180=cl/cl.shift(180)-1
            d=pd.DataFrame({"cell":np.arange(len(b))//H,"dn":cl<lo12,"ratio":ratio,"r180":r180,
              "f6":-(cl.shift(-6)/cl-1),"f18":-(cl.shift(-18)/cl-1),"f36":-(cl.shift(-36)/cl-1),"f72":-(cl.shift(-72)/cl-1)})
            d=d.dropna(subset=["ratio","r180","f18"])
            res.append(d[d.dn].groupby("cell").first())
    R=pd.concat(res)
    R["nq"]=pd.qcut(R["ratio"],5,labels=False)
    R["pos"]=R.r180>0
    out["down_break_short_by_narrow_q_and_r180sign"]=R.groupby(["nq","pos"]).agg(n=("f18","count"),f6=("f6","mean"),f18=("f18","mean"),t18=("f18",lambda x:x.mean()/(x.std()/np.sqrt(len(x)))),f36=("f36","mean"),f72=("f72","mean"))
    return out
