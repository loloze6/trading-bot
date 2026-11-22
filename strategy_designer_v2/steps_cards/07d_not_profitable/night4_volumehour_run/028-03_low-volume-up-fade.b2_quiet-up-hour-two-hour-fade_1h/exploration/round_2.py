def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book daily decomposition and fees
    dd=[]
    for c in data["days"]:
        for w,t in data["days"][c].items():
            x=t.copy(); x["coin"]=c; x["w"]=w; dd.append(x)
    dd=pd.concat(dd)
    daily=dd.groupby(["w","day"]).agg(b=("book_return","mean"),h=("coin_return","mean")).dropna()
    out["book_daily"]=pd.DataFrame({"mean_book":[daily.b.mean()],"sd_book":[daily.b.std()],"mean_hold":[daily.h.mean()],"n_days":[len(daily)]})
    # gross bar gains vs fees, per bar
    g=[]
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            r=b.close.shift(-1)/b.close-1
            gain=(b.postRebalance_current_allocation*r).sum()
            fee=(b.total_portfolio_value-b.postRebalance_total_value).sum()/b.total_portfolio_value.mean()
            turn=(b.postRebalance_current_allocation-b.previous_allocation).abs().sum()
            g.append((c,w,gain,fee,turn,len(b)))
    g=pd.DataFrame(g,columns=["coin","w","gross","fee","turnover","bars"])
    s=g.groupby("coin")[["gross","fee","turnover","bars"]].sum()
    s["gross_per_day"]=s.gross/(s.bars/24); s["fee_per_day"]=s.fee/(s.bars/24); s["turn_per_day"]=s.turnover/(s.bars/24)
    out["gross_vs_fee"]=s
    # high-volume large rises / drops at 24h on non-overlapping 24h grid, graded
    H=[6,12,24,48]
    drift={}
    for c in data["bars"]:
        for h in H:
            rs=[]
            for w,b in data["bars"][c].items():
                cl=b.close.values; idx=np.arange(0,len(cl)-h,h); rs.append(cl[idx+h]/cl[idx]-1)
            rs=np.concatenate(rs); drift[(c,h)]=(rs.mean(),rs.std())
    rows=[]
    for c in data["bars"]:
        for wi,(w,b) in enumerate(data["bars"][c].items()):
            b=b.reset_index(drop=True); cl=b.close; r1=cl.pct_change()
            z=r1/r1.abs().rolling(720,min_periods=200).mean()
            vr=b.volume/b.volume.rolling(720,min_periods=200).mean()
            df=pd.DataFrame({"z":z,"vr":vr,"coin":c,"wi":wi,"pos":np.arange(len(b))})
            for h in H: df[f"f{h}"]=(cl.shift(-h)/cl-1-drift[(c,h)][0])/drift[(c,h)][1]; df[f"t{h}"]=cl.shift(-h)/cl-1
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["z","vr"])
    def one_per_cell(x,h):
        x=x.assign(cell=x.pos//h); return x.sort_values("pos").groupby(["coin","wi","cell"]).head(1)
    res={}
    for name,cond,sign in [("rise_hv",(d.z>2)&(d.vr>3),1),("rise_mv",(d.z>2)&(d.vr>1.5)&(d.vr<=3),1),("rise_q",(d.z>2)&(d.vr<=1.5),1),("drop_hv",(d.z<-2)&(d.vr>3),-1),("drop_q",(d.z<-2)&(d.vr<=1.5),-1)]:
        for h in H:
            x=one_per_cell(d[cond],h); u=sign*x[f"f{h}"].dropna(); tot=sign*x[f"t{h}"].dropna()
            res[(name,h)]={"n":len(u),"strength":u.mean(),"t":u.mean()/(u.std()/np.sqrt(len(u))),"total_pct":tot.mean()*100}
    out["events_cont_dir"]=pd.DataFrame(res).T
    x=one_per_cell(d[(d.z>2)&(d.vr>3)],24)
    x=x.assign(zb=pd.cut(x.z,[2,3,4,6,100]),vb=pd.cut(x.vr,[3,5,8,1000]))
    f=lambda g: pd.Series({"n":len(g),"total_pct":g.t24.mean()*100,"t":g.f24.mean()/(g.f24.std()/np.sqrt(len(g)))})
    out["rise_hv_by_z_24h"]=x.groupby("zb",observed=True).apply(f)
    out["rise_hv_by_vr_24h"]=x.groupby("vb",observed=True).apply(f)
    out["rise_hv_by_coin_24h"]=x.groupby("coin").apply(f)
    out["rise_hv_by_windowthird_24h"]=x.assign(p=pd.cut(x.wi,[-1,7,15,24])).groupby("p",observed=True).apply(f)
    # graded score z*log(vr) on all rises with vr>1
    y=one_per_cell(d[(d.z>1)&(d.vr>1)],24); y=y.assign(s=y.z*np.log(y.vr)).dropna(subset=["f24"])
    y["sq"]=pd.qcut(y.s,5)
    out["rise_score_quintile_24h"]=y.groupby("sq",observed=True).apply(f)
    return out
