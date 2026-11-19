def explore(data):
    import pandas as pd, numpy as np
    out = {}
    rows=[]
    for c, ws in data["bars"].items():
        for w, b in ws.items():
            b=b.reset_index(drop=True)
            cl=b.close.values; pos=b.postRebalance_current_allocation.fillna(0).values
            r1=np.r_[cl[1:]/cl[:-1]-1, np.nan]
            fee=((b.total_portfolio_value-b.postRebalance_total_value)/b.total_portfolio_value).fillna(0).values
            ret30=pd.Series(cl).pct_change(720).values
            ret3=pd.Series(cl).pct_change(72).values
            hi=pd.Series(b.high.values).rolling(720,min_periods=200).max().values
            vol=pd.Series(r1).shift(1).rolling(168,min_periods=50).std().values
            vol30=pd.Series(r1).shift(1).rolling(720,min_periods=200).std().values
            day=pd.to_datetime(b.timestamp).dt.floor("D").values
            rows.append(pd.DataFrame({"coin":c,"w":w,"day":day,"pos":pos,"r1":r1,"g":pos*r1,"fee":fee,
              "turn":np.abs(b.allocation_change.fillna(0).values) if "allocation_change" in b else 0,
              "ret30":ret30,"ret3":ret3,"near":cl/hi-1,"vr":vol/vol30,"fc":b.forecast.values}))
    X=pd.concat(rows)
    X["net"]=X.g-X.fee
    inpos=X[X.pos>0].copy()
    out["totals"]=pd.Series({"gross":X.g.sum(),"fee":X.fee.sum(),"turn":X.turn.sum(),"inpos_share":(X.pos>0).mean(),
        "fc_changes_per_day":(X.groupby(["coin","w"]).fc.diff().abs()>0).sum()/ (len(X)/24)})
    def tab(col,q=4):
        d=inpos.dropna(subset=[col]).copy()
        d["b"]=pd.qcut(d[col],q,labels=False,duplicates="drop")
        g=d.groupby("b").agg(lo=(col,"min"),hi=(col,"max"),n=("g","size"),pos=("pos","mean"),gross=("g","sum"),fee=("fee","sum"),
            r1bp=("r1",lambda x:x.mean()*1e4))
        g["net"]=g.gross-g.fee
        return g.round(4)
    out["inpos_by_ret30"]=tab("ret30")
    out["inpos_by_ret3"]=tab("ret3")
    out["inpos_by_near"]=tab("near")
    out["inpos_by_volratio"]=tab("vr")
    # daily book per coin, drawdown periods
    Dd=X.groupby(["w","day"]).agg(g=("g","sum"),fee=("fee","sum")).reset_index()
    Dd["g"]/=6; Dd["fee"]/=6
    Dd["wn"]=Dd.w.str[1:].astype(int); Dd=Dd.sort_values(["wn","day"])
    Dd["net"]=Dd.g-Dd.fee
    eq=(1+Dd.net).cumprod().values; dd=eq/np.maximum.accumulate(eq)-1
    Dd["dd"]=dd
    Dd["indd"]=dd<-0.10
    out["dd_vs_not"]=Dd.groupby("indd").agg(n=("net","size"),gross=("g","mean"),fee=("fee","mean"),net=("net","mean")).round(6)
    # state on days: mean ret30/vr across coins, link to daily net
    S=X.groupby(["w","day"]).agg(ret30=("ret30","last"),vr=("vr","mean"),pos=("pos","mean")).reset_index()
    M=Dd.merge(S,on=["w","day"])
    M["vrq"]=pd.qcut(M.vr,4,labels=False,duplicates="drop")
    out["day_by_volratio"]=M.groupby("vrq").agg(vr=("vr","mean"),n=("net","size"),pos=("pos","mean"),g=("g","mean"),fee=("fee","mean"),net=("net","mean"),dd=("indd","mean")).round(6)
    # daily-sampled forecast (slow part): gain if position updated once per day
    return out
