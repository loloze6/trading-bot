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
            low90=cl.rolling(90,min_periods=30).min()
            dist=cl/low90-1
            f5=cl.shift(-5)/cl-1
            ret30=cl/cl.shift(30)-1
            d=pd.DataFrame({"coin":c,"win":w,"pos":np.arange(len(b)),"z":z,"ret90":ret90,"ret30":ret30,
                            "dist":dist,"f5":f5,"reg":b["regime"],"fc":b["forecast"],
                            "alloc":b["postRebalance_current_allocation"],"yr":pd.to_datetime(b["timestamp"]).dt.year})
            rows.append(d)
    D=pd.concat(rows)
    G=D[D.pos%5==0].dropna(subset=["f5"])
    drift=G.groupby("coin").f5.mean()
    G=G.assign(u=G.f5-G.coin.map(drift))
    out={}
    out["drift5_by_coin"]=drift
    M=G[G.reg=="mean_reversion"]
    def summ(x):
        return pd.Series({"n":len(x),"mean_f5":x.f5.mean(),"mean_u":x.u.mean(),"t_f5":x.f5.mean()/(x.f5.std()/np.sqrt(len(x))) if len(x)>2 else np.nan})
    out["regime_all_grid"]=G.groupby("reg").apply(summ)
    Mz=M.dropna(subset=["z"])
    out["MR_by_z"]=Mz.groupby(pd.cut(Mz.z,[-99,-2,-1,0,1,2,3,99])).apply(summ)
    Up=G[(G.reg!="mean_reversion")].dropna(subset=["z"])
    out["nonMR_by_z"]=Up.groupby(pd.cut(Up.z,[-99,-2,-1,0,1,2,3,99])).apply(summ)
    B=Mz[Mz.z>1].dropna(subset=["dist"])
    out["MR_bounce_by_dist"]=B.groupby(pd.qcut(B.dist,4)).apply(summ)
    B2=Mz[Mz.z>1].dropna(subset=["ret90"])
    out["MR_bounce_by_ret90"]=B2.groupby(pd.qcut(B2.ret90,4)).apply(summ)
    B3=Mz[Mz.z>1].dropna(subset=["ret30"])
    out["MR_bounce_by_ret30"]=B3.groupby(pd.qcut(B3.ret30,4)).apply(summ)
    out["MR_by_ret90_all"]=M.dropna(subset=["ret90"]).groupby(pd.qcut(M.dropna(subset=["ret90"]).ret90,4)).apply(summ)
    # book
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items():
            dd.append(x.assign(coin=c,win=w,yr=pd.to_datetime(x["day"]).dt.year))
    DD=pd.concat(dd).dropna(subset=["book_return"])
    out["book_by_year"]=DD.groupby("yr").agg(book=("book_return","mean"),coin=("coin_return","mean"),n=("book_return","size"))
    out["book_by_coin"]=DD.groupby("coin").agg(book=("book_return","mean"),coin=("coin_return","mean"))
    T=pd.concat([t.assign(coin=c) for c,ws in data["trades"].items() for w,t in ws.items() if len(t)])
    out["trades"]=T.groupby("side").agg(n=("side","size"),gross=("profit_loss_percent","mean"),net=("net_profit_loss_percent","mean"),win=("profit_loss_percent",lambda s:(s>0).mean()))
    out["fc_dist_active"]=D[D.reg=="mean_reversion"].fc.describe()
    out["share_shortheld"]=float((D.alloc<0).mean())
    return out
