def explore(data):
    import numpy as np, pandas as pd
    rows=[]; book=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True)
            c=b["close"]; r=c.pct_change()
            sd=r.rolling(720,min_periods=240).std()
            vr=b["volume"]/b["volume"].rolling(720,min_periods=240).mean()
            z=r/sd
            f6=c.shift(-6)/c-1
            f2=c.shift(-2)/c-1
            alloc=b["postRebalance_current_allocation"]
            gross=alloc*(c.shift(-1)/c-1)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            book.append(pd.DataFrame({"coin":coin,"w":w,"gross":gross,"fee":fee,"alloc":alloc,"fc":b["forecast"]}))
            idx=np.arange(0,len(b),6)
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"vr":vr,"f6":f6,"f2":f2,"fc":b["forecast"],"lhv":b["debug_info.components.vol_surge_up.last_history_value"]}).iloc[idx]
            rows.append(d)
    d=pd.concat(rows).dropna(subset=["z","vr","f6"])
    d["drift"]=d.groupby("coin")["f6"].transform("mean")
    d["u6"]=d["f6"]-d["drift"]
    d["sz"]=d["z"]*d["vr"]
    def agg(g):
        return pd.Series({"n":len(g),"u6_bp":g.u6.mean()*1e4,"t":g.u6.mean()/(g.u6.std()/np.sqrt(len(g))),"f2_bp":g.f2.mean()*1e4})
    out={}
    d["zbin"]=pd.cut(d.z,[-99,-4,-2.5,-1.5,-0.5,0.5,1.5,2.5,4,99])
    d["vbin"]=pd.cut(d.vr,[0,1,2,3,99])
    out["by_z"]=d.groupby("zbin").apply(agg)
    big=d[d.z.abs()>2.5].copy(); big["dir"]=np.sign(big.z)
    big["su6"]=big.u6*big.dir
    out["big_move_by_vol_signed"]=big.groupby(["dir","vbin"]).apply(lambda g: pd.Series({"n":len(g),"signed_u6_bp":g.su6.mean()*1e4,"t":g.su6.mean()/(g.su6.std()/np.sqrt(len(g)))}))
    d["fcpos"]=pd.cut(d.fc,[-1,0,0.5,2,5,20.1])
    out["by_forecast"]=d.groupby("fcpos").apply(agg)
    out["sz_quint_pos"]=d[d.sz>0].groupby(pd.qcut(d[d.sz>0].sz,5)).apply(agg)
    bk=pd.concat(book)
    out["book"]=bk.groupby("coin").agg(gross_bp=("gross",lambda x:x.mean()*1e4),fee_bp=("fee",lambda x:x.mean()*1e4),mean_alloc=("alloc","mean"),share_long=("alloc",lambda x:(x>0).mean()),share_fc_pos=("fc",lambda x:(x>0).mean()))
    out["by_window_gross_fee"]=bk.groupby("w").agg(gross=("gross","sum"),fee=("fee","sum"))
    return out
