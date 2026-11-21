def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    res={}
    out=[]; wins_tab=[]; coin_tab=[]; grade=[]
    for H in [12,24,48,72,96]:
        rows=[]
        for coin, wins in data["bars"].items():
            g=[]
            for w,b in wins.items():
                c=b["close"].astype(float).reset_index(drop=True)
                ts=pd.to_datetime(b["timestamp"]).reset_index(drop=True)
                r24=c/c.shift(24)-1
                z=r24/r24.abs().rolling(720,min_periods=360).mean()
                r720=c/c.shift(720)-1
                f=c.shift(-H)/c-1
                d=pd.DataFrame({"z":z,"r720":r720,"f":f,"hour":ts.dt.hour,"year":ts.dt.year})
                g.append(d.iloc[::H].assign(win=w))
            a=pd.concat(g).dropna(subset=["f"])
            a["ex"]=a.f-a.f.mean(); a["u"]=a.ex/a.f.std(); a["coin"]=coin
            rows.append(a)
        A=pd.concat(rows).dropna(subset=["z","r720"])
        A["reg"]=np.where(A.r720<0,"down30","up30")
        P=A[A.z<=-2.5]
        for reg,dd in [("all",P)]+list(P.groupby("reg")):
            u=dd.u; ex=dd.ex
            lo,hi=u.quantile([.05,.95])
            tr=u[(u>=lo)&(u<=hi)]
            out.append({"H":H,"reg":reg,"n":len(u),"strength":u.mean(),"t":u.mean()/(u.std()/np.sqrt(len(u))),
                        "median_u":u.median(),"trim90_u":tr.mean(),"trim_t":tr.mean()/(tr.std()/np.sqrt(len(tr))),
                        "ex_pct":100*ex.mean(),"tot_pct":100*dd.f.mean(),"share_pos":(ex>0).mean()})
        if H in (24,48):
            wm=P.groupby("win").u.mean()
            wins_tab.append({"H":H,"n_windows":len(wm),"windows_pos":(wm>0).sum(),
                             "loo_min_strength":min(P[P.win!=w].u.mean() for w in wm.index),
                             "loo_max_strength":max(P[P.win!=w].u.mean() for w in wm.index)})
            for coin,dd in P.groupby("coin"):
                coin_tab.append({"H":H,"coin":coin,"n":len(dd),"strength":dd.u.mean(),
                                 "t":dd.u.mean()/(dd.u.std()/np.sqrt(len(dd))),"median_u":dd.u.median()})
            F=A[A.z<0]
            r=stats.linregress(F.z.clip(-6,0),F.u)
            F2=A[A.z<=-1]
            r2=stats.linregress(F2.z.clip(-6,0),F2.u)
            grade.append({"H":H,"slope_falls":r.slope,"t":r.slope/r.stderr,"n":len(F),
                          "slope_z_le_-1":r2.slope,"t2":r2.slope/r2.stderr,"n2":len(F2)})
            if H==24:
                P2=P.copy(); P2["yr"]=P2.year
                res["h24_plunge_by_year"]=P2.groupby("yr").u.agg(["mean","count"]).round(3)
    res["plunge_by_horizon"]=pd.DataFrame(out).round(3)
    res["plunge_windows"]=pd.DataFrame(wins_tab).round(3)
    res["plunge_by_coin"]=pd.DataFrame(coin_tab).set_index(["H","coin"]).round(3)
    res["grading"]=pd.DataFrame(grade).round(3)
    return res
