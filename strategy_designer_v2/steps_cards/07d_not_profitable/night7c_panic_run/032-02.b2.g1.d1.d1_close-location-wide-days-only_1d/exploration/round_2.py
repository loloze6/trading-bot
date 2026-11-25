def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            rng=b.high-b.low
            m20=rng.shift(1).rolling(20).mean()
            b["mult"]=rng/m20
            b["cl"]=(2*b.close-b.high-b.low)/rng.replace(0,np.nan)
            b["nxt"]=b.close.shift(-1)/b.close-1
            for h in (2,3,5):
                b[f"f{h}"]=b.close.shift(-h)/b.close-1
            b["r20"]=b.close/b.close.shift(20)-1
            b["pos"]=b["postRebalance_current_allocation"]
            b["coin"]=coin; b["w"]=w; b["i"]=np.arange(len(b))
            b["day"]=pd.to_datetime(b.timestamp).dt.floor("D")
            rows.append(b)
    d=pd.concat(rows)
    d["drift"]=d.groupby("coin").nxt.transform("mean")
    d["held"]=np.sign(d.pos).fillna(0)
    d["posret"]=d.pos*d.nxt
    out={}
    # condition alone: down20 vs up20 next-day excess, all bars and wide bars
    x=d.dropna(subset=["nxt","r20","mult","cl"]).copy()
    x["ex"]=x.nxt-x.drift
    x["trend"]=np.where(x.r20>0,"up20","down20")
    x["wide"]=x.mult>1
    def tt(s): return pd.Series({"n":len(s),"mean_%":s.mean()*100,"t":s.mean()/(s.std()/np.sqrt(len(s)))})
    out["cond_alone_ex_by_trend_wide"]=x.groupby(["wide","trend"]).ex.apply(tt).unstack()
    # graded long side on wide days: by cl and mult tercile
    xl=x[x.wide&(x.cl<0)].copy()
    xl["clq"]=pd.qcut(-xl.cl,3,labels=False); xl["mq"]=pd.qcut(xl.mult,3,labels=False)
    out["long_ex_by_clq"]=xl.groupby("clq").ex.apply(tt).unstack()
    out["long_ex_by_multq"]=xl.groupby("mq").ex.apply(tt).unstack()
    # longer horizons, long side wide, non-overlapping per grid
    res={}
    for h in (1,2,3,5):
        col="nxt" if h==1 else f"f{h}"
        g=x[(x.i%h==0)]
        gl=g[g.wide&(g.cl<0)][col]-g[g.wide&(g.cl<0)].drift*h
        res[h]=tt(gl.dropna())
    out["long_wide_horizons_ex"]=pd.DataFrame(res).T
    # book-level counterfactual daily: posret variants per coin-day averaged over coins
    d["long_only"]=np.where(d.pos>0,d.pos,0)*d.nxt
    d["short_down"]=np.where((d.pos<0)&(d.r20<0),d.pos,np.where(d.pos>0,d.pos,0))*d.nxt
    # fee approx: 0.19% x |allocation change|
    def book(col,poscol):
        p=poscol.fillna(0)
        ch=p.groupby([d.coin,d.w]).diff().abs().fillna(p.abs())
        r=d[col].fillna(0)-0.0019*ch
        day=pd.DataFrame({"w":d.w,"day":d.day,"r":r,"inpos":(p!=0)})
        dd=day.groupby(["w","day"]).agg(r=("r","mean"),inpos=("inpos","mean")).reset_index()
        rr=dd.r
        val=(1+rr).cumprod(); mdd=(val/val.cummax()-1).min()
        yrs=len(rr)/365; yr=val.iloc[-1]**(1/yrs)-1
        return pd.Series({"sharpe":rr.mean()/rr.std()*np.sqrt(365),"yearly_%":yr*100,"maxdd_%":mdd*100,
                          "calmar":yr/abs(mdd),"mean_inpos_bp":rr.mean()/dd.inpos.mean()*1e4,"inpos_share":dd.inpos.mean()})
    out["book_variants"]=pd.DataFrame({
        "as_tested":book("posret",d.pos),
        "long_only":book("long_only",pd.Series(np.where(d.pos>0,d.pos,0),index=d.index)),
        "short_only_down20":book("short_down",pd.Series(np.where((d.pos<0)&(d.r20<0),d.pos,np.where(d.pos>0,d.pos,0)),index=d.index)),
    }).T
    hd=d.dropna(subset=["nxt"]).groupby(["w","day"]).nxt.mean()
    v=(1+hd).cumprod()
    out["hold_sharpe_calmar"]=pd.Series({"sharpe":hd.mean()/hd.std()*np.sqrt(365),"maxdd_%":(v/v.cummax()-1).min()*100})
    # shorts in up20: by strength
    xs=x[x.wide&(x.cl>0)].copy()
    out["short_ex_by_trend_r20q"]=xs.groupby(pd.qcut(xs.r20,4,labels=False)).ex.apply(lambda s:tt(-s)).unstack()
    return out
