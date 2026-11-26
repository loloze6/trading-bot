def explore(data):
    import numpy as np, pandas as pd
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]; r=c.pct_change()
            nxt=c.shift(-1)/c-1
            hh20=b["high"].rolling(20).max()
            sd20=r.rolling(20).std()
            depth=(c-hh20)/hh20/sd20
            tr60=c/c.shift(60)-1
            vol30=r.rolling(30).std()
            pct=vol30.rolling(365,min_periods=30).apply(lambda x:(x<=x[-1]).mean(),raw=True)
            alloc=b["postRebalance_current_allocation"]
            pv=b["postRebalance_total_value"]; tv=b["total_portfolio_value"]
            d=pd.DataFrame({"coin":coin,"w":w,"day":pd.to_datetime(b["timestamp"]).dt.floor("D"),
                "r":r,"nxt":nxt,"depth":depth,"tr60":tr60,"pct":pct,"fc":b["forecast"],
                "alloc":alloc,"gain":alloc*nxt,"fee":(tv-pv)/tv})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["r"].mean()
    D["ex"]=-(D["nxt"]-D["coin"].map(drift))
    D["agit"]=D["pct"]>0.5
    D["fall"]=D["tr60"]<-0.1
    D["sig"]=D["fc"]<0
    def summ(g):
        g=g.dropna(subset=["nxt"])
        n=len(g); 
        if n<2: return pd.Series({"n":n})
        dd=g.groupby("day")["ex"].sum(); nd=len(dd)
        tday=g["ex"].mean()/ (dd.std()*np.sqrt(nd)/n) if nd>1 else np.nan
        return pd.Series({"n":n,"days":nd,"short_ex":g["ex"].mean(),"t_day":tday,"gain":g["gain"].mean(),"fee":g["fee"].mean(),"absalloc":g["alloc"].abs().mean()})
    out={}
    F=D[D["fall"]&D["pct"].notna()].copy()
    F["grp"]=np.where(F["sig"],"signal",np.where(F["r"]>0,"up_nosig","down"))
    out["falling_by_agit_grp"]=F.groupby(["agit","grp"]).apply(summ)
    S=F[F["sig"]].copy()
    S["fcq"]=pd.qcut(S["fc"].rank(method="first"),3,labels=["deep","mid","shallow"])
    out["signal_agit_by_depth"]=S.groupby(["agit","fcq"]).apply(summ)
    # all falling agitated bars regardless of signal
    out["falling_all_by_agit"]=F.groupby("agit").apply(summ)
    # non-falling agitated up days by depth (does agitation alone carry it)
    N=D[(~D["fall"])&D["pct"].notna()&(D["r"]>0)].dropna(subset=["depth"]).copy()
    N["dq"]=pd.qcut(N["depth"].rank(method="first"),3,labels=["deep","mid","shallow"])
    out["notfall_up_agit_by_depth"]=N.groupby(["agit","dq"]).apply(summ)
    # book: gain split by agitation (bar level, summed share)
    H=D[D["alloc"].abs()>0].dropna(subset=["nxt"])
    out["held_gain_by_agit"]=H.groupby(H["agit"]).agg(n=("gain","size"),gain_sum=("gain","sum"),fee_sum=("fee","sum"),gain_mean=("gain","mean"))
    out["held_gain_by_agit_window"]=H.groupby(["w","agit"])["gain"].sum().unstack()
    return out
