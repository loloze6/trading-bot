def explore(data):
    import numpy as np, pandas as pd
    out = {}
    # book & trades
    tr = []
    for c in data["trades"]:
        for w, t in data["trades"][c].items():
            if len(t): tt = t.copy(); tt["coin"]=c; tr.append(tt)
    tr = pd.concat(tr)
    out["trades"] = pd.DataFrame({
        "n":[len(tr)],
        "mean_gross_pct":[tr.profit_loss_percent.mean()],
        "mean_net_pct":[tr.net_profit_loss_percent.mean()],
        "median_dur_min":[tr.duration_minutes.median()],
        "mean_dur_min":[tr.duration_minutes.mean()],
        "t_gross":[tr.profit_loss_percent.mean()/(tr.profit_loss_percent.std()/np.sqrt(len(tr)))],
    })
    out["trades_by_side"] = tr.groupby("side").agg(n=("profit_loss_percent","size"),
        gross=("profit_loss_percent","mean"), net=("net_profit_loss_percent","mean"))
    # recompute features per window
    H = [1,2,4,6,12,24]
    rows = []
    drift = {}
    for c in data["bars"]:
        for h in H:
            rs=[]
            for w,b in data["bars"][c].items():
                cl=b.close.values
                idx=np.arange(0,len(cl)-h,h)
                rs.append(cl[idx+h]/cl[idx]-1)
            rs=np.concatenate(rs); drift[(c,h)]=(rs.mean(), rs.std())
    for c in data["bars"]:
        for w,b in data["bars"][c].items():
            b=b.reset_index(drop=True)
            cl=b.close
            r1=cl.pct_change()
            scale=r1.abs().rolling(720,min_periods=200).mean()
            z=r1/scale
            vr=b.volume/b.volume.rolling(720,min_periods=200).mean()
            df=pd.DataFrame({"z":z,"vr":vr,"fc":b.forecast,"alloc":b.postRebalance_current_allocation,"coin":c,"pos":np.arange(len(b))})
            for h in H:
                df[f"f{h}"]=cl.shift(-h)/cl-1 - drift[(c,h)][0]
            rows.append(df)
    d=pd.concat(rows).dropna(subset=["z","vr"])
    big=d[d.z>2].copy()
    big["zb"]=pd.cut(big.z,[2,3,4,6,100])
    big["vb"]=pd.cut(big.vr,[0,0.67,1.5,3,1000])
    def summ(g,h):
        x=-g[f"f{h}"].dropna()
        return pd.Series({"n":len(x),"mean_short_pct":x.mean()*100,"t":x.mean()/(x.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    for h in [2,6,24]:
        out[f"rise_z>2_by_vol_h{h}"]=big.groupby("vb",observed=True).apply(lambda g: summ(g,h))
    q=big[(big.vr>0.67)&(big.vr<1.5)]
    for h in [1,2,4,6,12,24]:
        pass
    out["quiet_rise_by_z_h2"]=q.groupby("zb",observed=True).apply(lambda g: summ(g,2))
    out["quiet_rise_by_z_h6"]=q.groupby("zb",observed=True).apply(lambda g: summ(g,6))
    out["quiet_rise_by_z_h24"]=q.groupby("zb",observed=True).apply(lambda g: summ(g,24))
    # falls too, all volume, z<-2 for symmetry
    dn=d[d.z<-2].copy(); dn["vb"]=pd.cut(dn.vr,[0,0.67,1.5,3,1000])
    out["drop_z<-2_by_vol_h6_longdir"]=dn.groupby("vb",observed=True).apply(lambda g: summ(g.assign(**{"f6":-g.f6}),6))
    # active bars share & size of forecast
    act=d[d.fc<0]
    out["active"]=pd.DataFrame({"share_bars_short":[len(act)/len(d)],"mean_z_active":[act.z.mean()],"median_fc":[act.fc.median()],"share_fc_below_-2":[(act.fc<-2).mean()],"mean_abs_alloc":[act.alloc.abs().mean()]})
    out["active_by_z"]=act.assign(zb=pd.cut(act.z,[-100,0.5,1,2,3,100])).groupby("zb",observed=True).apply(lambda g: pd.concat([summ(g,2),pd.Series({"fc":g.fc.mean()})]))
    out["usual_move"]=pd.DataFrame({f"{k[0]}_{k[1]}h":[v[0]*100,v[1]*100] for k,v in drift.items()},index=["mean%","sd%"]).T
    return out
