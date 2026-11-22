def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            cl=b["close"]; r=cl.pct_change()
            sd=r.rolling(20).std().shift(1)
            z=r/sd
            ret90=cl/cl.shift(90)-1
            ret30=cl/cl.shift(30)-1
            low90=cl.rolling(90,min_periods=30).min()
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(len(b)),"z":z,"ret90":ret90,"ret30":ret30,
                            "dist":cl/low90-1,"f5":cl.shift(-5)/cl-1,"f10":cl.shift(-10)/cl-1,
                            "f1":cl.shift(-1)/cl-1,"reg":b["regime"],"fc":b["forecast"],
                            "alloc":b["postRebalance_current_allocation"],
                            "prev":b["previous_allocation"]})
            rows.append(d)
    D=pd.concat(rows)
    out={}
    drift1=D.groupby("coin").f1.mean()
    # entries: alloc goes from >=0 to <0
    E=D[(D.alloc<0)&(D.prev>=0)].dropna(subset=["z","f5"])
    def summ(x,col="f5"):
        n=len(x); m=x[col].mean()
        return pd.Series({"n":n,"mean":m,"t":m/(x[col].std()/np.sqrt(n)) if n>2 else np.nan})
    out["entry_by_z"]=E.groupby(pd.cut(E.z,[-99,0,1,2,3,99])).apply(summ)
    out["entry_by_fc"]=E.groupby(pd.cut(E.fc,[-21,-15,-10,-5,-2,0.1])).apply(summ)
    # held-short bars: gain decomposition
    H=D.dropna(subset=["f1","alloc"])
    H=H.assign(g=H.alloc*H.f1, gd=H.alloc*H.coin.map(drift1))
    out["held_gain_total_vs_drift"]=pd.Series({"mean_gain_per_bar":H.g.mean(),"drift_part":H.gd.mean(),"timing_part":(H.g-H.gd).mean(),"mean_abs_alloc_short":H.alloc[H.alloc<0].mean()})
    # MR, big bounce, 5d and 10d on grid
    G=D[D.pos%5==0]
    M=G[(G.reg=="mean_reversion")].dropna(subset=["z","f5"])
    for lo,hi in [(1,2),(2,99),(1.5,99)]:
        S=M[(M.z>lo)&(M.z<=hi)]
        out[f"MR_z{lo}-{hi}_f5_f10"]=pd.DataFrame({"f5":summ(S,"f5"),"f10":summ(S.dropna(subset=["f10"]),"f10")})
    # all bars (not grid) MR z>2 by ret30 sign, f5 (overlapping-free enough: rare)
    A=D[(D.reg=="mean_reversion")&(D.z>2)].dropna(subset=["f5","ret30"])
    out["MR_z>2_allbars_by_ret30sign"]=A.groupby(A.ret30>0).apply(summ)
    out["MR_z>2_allbars_by_dist_median"]=A.groupby(A.dist>A.dist.median()).apply(summ)
    A2=D[(D.reg!="mean_reversion")&(D.z>2)].dropna(subset=["f5"])
    out["nonMR_z>2_allbars"]=summ(A2)
    # grid all MR: f5 by ret30 quartile (overall regime state)
    M2=M.dropna(subset=["ret30"])
    out["MR_grid_by_ret30q"]=M2.groupby(pd.qcut(M2.ret30,4)).apply(summ)
    # share of held short bars by z of the latest entry: fraction of short bars where today's z<1
    out["share_shortbars_entered_z_lt1"]=float((E.z<1).mean())
    return out
