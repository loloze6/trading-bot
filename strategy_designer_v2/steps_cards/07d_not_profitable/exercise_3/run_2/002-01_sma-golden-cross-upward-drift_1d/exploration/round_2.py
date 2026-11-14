import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy().reset_index(drop=True)
            cl=b["close"]
            r=cl.shift(-1)/cl-1
            a=b["postRebalance_current_allocation"].astype(float)
            sp=b["debug_info.components.sma_cross.last_history_value"]
            d=pd.DataFrame({"coin":c,"w":w,"fc":b["forecast"],"alloc":a,"r":r,"g":a*r,
                "sp":sp,"dsp10":sp-sp.shift(10),
                "dd20":cl/cl.rolling(20,min_periods=20).max()-1,
                "ret20":cl/cl.shift(20)-1,"ret5":cl/cl.shift(5)-1,
                "vol20":cl.pct_change().rolling(20).std()})
            d["r10"]=cl.shift(-10)/cl-1
            d["pos"]=np.arange(len(d))
            rows.append(d)
    D=pd.concat(rows).dropna(subset=["r"])
    act=D[D.alloc.abs()>1e-9].copy()
    out={}
    out["alloc_vs_fc"]=act.groupby(pd.cut(act.fc,[0,5,10,15,20.01])).alloc.agg(["mean","min","max"]).round(3)
    def summ(x,k):
        g=x.groupby(k)
        return g.agg(n=("g","size"),mean_g=("g","mean"),sd_g=("g","std"),mean_r=("r","mean"),
                     worst5=("g",lambda s:s.quantile(0.05)),
                     sum_g=("g","sum")).assign(shr=lambda t:(t.mean_g/t.sd_g*np.sqrt(365))).round(4)
    act["dd20q"]=pd.qcut(act.dd20,5,labels=False,duplicates="drop")
    out["by_dd20"]=summ(act,"dd20q").join(act.groupby("dd20q").dd20.agg(lo="min",hi="max").round(3))
    act["vq"]=pd.qcut(act.vol20,5,labels=False)
    out["by_vol"]=summ(act,"vq")
    act["state"]=np.where(act.dsp10<0,"spread_falling","spread_rising")+np.where(act.ret20<0,"_px_down","_px_up")
    out["by_state"]=summ(act.dropna(subset=["dsp10","ret20"]),"state")
    # non-overlapping 10-bar fwd, active, by dsp10 sign & ret20 sign
    nb=act[(act.pos%10==0)].dropna(subset=["r10","dsp10","ret20"])
    hm=D[D.pos%10==0].groupby("coin").r10.mean()
    nb=nb.assign(ex=nb.r10-nb.coin.map(hm))
    out["nonoverlap10_state"]=nb.groupby("state").ex.agg(n="size",mean="mean",t=lambda s:s.mean()/s.std()*np.sqrt(len(s))).round(4)
    # pooled book worst days: states held
    act["dayloss"]=act.g
    worst=act[act.g<=act.g.quantile(0.02)]
    out["worst2pct_states"]=pd.Series({"n":len(worst),"mean_alloc":worst.alloc.mean(),"all_alloc":act.alloc.mean(),
        "share_spread_falling":(worst.dsp10<0).mean(),"all_spread_falling":(act.dsp10<0).mean(),
        "share_px_down20":(worst.ret20<0).mean(),"all_px_down20":(act.ret20<0).mean(),
        "mean_vol20":worst.vol20.mean(),"all_vol20":act.vol20.mean(),
        "mean_dd20":worst.dd20.mean(),"all_dd20":act.dd20.mean()}).round(4)
    # window 11-18 vs rest
    act["wn"]=act.w.str[1:].astype(int)
    act["era"]=np.where(act.wn<=10,"w1-10",np.where(act.wn<=18,"w11-18","w19-24"))
    out["by_era"]=summ(act,"era")
    return out
