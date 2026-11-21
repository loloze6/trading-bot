def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    res={}
    allrows={}
    for H in [12,24,48]:
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
                d=pd.DataFrame({"z":z,"r720":r720,"f":f,"year":ts.dt.year,"wd":ts.dt.weekday,"hour":ts.dt.hour})
                g.append(d.iloc[::H].assign(win=w))
            a=pd.concat(g).dropna(subset=["f"])
            a["drift"]=a.f.mean(); a["sd"]=a.f.std()
            a["ex"]=a.f-a.drift; a["u"]=a.ex/a.sd; a["coin"]=coin
            rows.append(a)
        A=pd.concat(rows).dropna(subset=["z","r720"])
        A["zb"]=pd.cut(A.z,[-99,-3,-2,-1,1,2,3,99])
        A["reg"]=np.where(A.r720<0,"down30","up30")
        A["era"]=np.where(A.year<=2021,"2018-21","2022-25")
        allrows[H]=A
        def summ(df,keys):
            g=df.groupby(keys,observed=True)
            o=g.agg(n=("u","size"),strength=("u","mean"),ex_pct=("ex",lambda x:100*x.mean()),
                    tot_pct=("f",lambda x:100*x.mean()),sdu=("u","std"))
            o["t"]=o.strength/(o.sdu/np.sqrt(o.n)); return o.drop(columns="sdu").round(3)
        res[f"h{H}_by_z"]=summ(A,["zb"])
        if H==24:
            res["h24_by_z_reg_era"]=summ(A,["era","reg","zb"])
            # graded slopes per coin: u on z within falls (z<0) and rises (z>0)
            sl=[]
            for coin,df in A.groupby("coin"):
                for side,dd in [("falls",df[df.z<0]),("rises",df[df.z>0])]:
                    r=stats.linregress(dd.z.clip(-5,5),dd.u)
                    sl.append({"coin":coin,"side":side,"slope":r.slope,"t":r.slope/r.stderr,"n":len(dd)})
            res["h24_slope_u_on_z_by_coin"]=pd.DataFrame(sl).set_index(["coin","side"]).round(3)
            ext=A[A.z.abs()>=2].copy(); ext["side"]=np.where(ext.z<0,"fall","rise")
            res["h24_extreme_by_coin_side"]=summ(ext,["coin","side"])
            res["h24_weekday_by_era"]=summ(A,["era","wd"])
            res["h24_friday_by_coin"]=summ(A[A.wd==4],["coin"])
    return res
