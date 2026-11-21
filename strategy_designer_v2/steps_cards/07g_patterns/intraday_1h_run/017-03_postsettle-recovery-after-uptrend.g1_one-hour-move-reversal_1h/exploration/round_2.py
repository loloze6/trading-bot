def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[];bk=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.sort_values("timestamp").reset_index(drop=True)
            c=b["close"].astype(float); r=c.pct_change()
            a=b["postRebalance_current_allocation"].astype(float)
            f1=c.shift(-1)/c-1
            gross=a*f1
            fee=(b["total_portfolio_value"].astype(float)-b["postRebalance_total_value"].astype(float))/b["total_portfolio_value"].astype(float)
            ts=pd.to_datetime(b["timestamp"])
            bk.append(pd.DataFrame({"coin":coin,"w":w,"day":ts.dt.floor("D"),"gross":gross,"fee":fee,"turn":(a-b["previous_allocation"].astype(float)).abs()}))
            d=pd.DataFrame({"coin":coin,"w":w,"pos":np.arange(len(b)),
                "vol720":r.rolling(720,min_periods=720).std(),"sd1":r.rolling(168,min_periods=100).std()})
            for h in [4,12,24,72]:
                d[f"r{h}"]=c/c.shift(h)-1; d[f"f{h}"]=c.shift(-h)/c-1
            rows.append(d)
    D=pd.concat(rows,ignore_index=True); B=pd.concat(bk,ignore_index=True)
    out={}
    def ts_(x):
        x=x.dropna(); n=len(x); return pd.Series({"n":n,"mean_bp":x.mean()*1e4,"t":x.mean()/(x.std()/np.sqrt(n))})
    dd=B.groupby(["coin","w","day"]).agg(gross=("gross","sum"),fee=("fee","sum"),turn=("turn","sum"))
    out["book_daily_gross_fee_turnover_bp"]=pd.DataFrame({"gross":ts_(dd.gross),"fee":ts_(dd.fee),"turn_x100":ts_(dd.turn/100)})
    res={}
    for h in [4,12,24,72]:
        g=D[D.pos%h==0].copy()
        g["z"]=g[f"r{h}"]/(g.sd1*np.sqrt(h))
        g["ex"]=g[f"f{h}"]-g.groupby("coin")[f"f{h}"].transform("mean")
        g["rev"]=-g.z.clip(-4,4)*g.ex
        res[f"h{h}_graded_all"]=ts_(g.rev)
        g["vq"]=g.groupby("coin")["vol720"].transform(lambda s:pd.qcut(s,2,labels=False,duplicates="drop"))
        for v in [0,1]:
            res[f"h{h}_vol720_half{v}"]=ts_(g[g.vq==v].rev)
        if h in (4,24):
            g["q"]=pd.qcut(g.z,5,labels=False)
            out[f"next{h}h_ex_by_z_quintile"]=g.groupby("q")["ex"].apply(ts_).unstack()
            out[f"h{h}_graded_by_coin"]=g.groupby("coin")["rev"].apply(ts_).unstack()
            wm=g.groupby(["coin","w"])["rev"].mean()
            res[f"h{h}_share_coin_windows_pos"]=pd.Series({"n":len(wm),"mean_bp":(wm>0).mean(),"t":np.nan})
    out["graded_reversal_by_horizon"]=pd.DataFrame(res).T
    return out
