def explore(data):
    import numpy as np, pandas as pd
    from scipy import stats
    rows=[]
    for coin,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.reset_index(drop=True).copy()
            c=b["close"]
            r=c.pct_change()
            sd=r.rolling(30).std()
            vsr=r/sd
            nxt=c.shift(-1)/c-1
            tr60=c/c.shift(60)-1
            pos=b["postRebalance_current_allocation"]
            pv=b["postRebalance_total_value"]; tv=b["total_portfolio_value"]
            # fee on bar: tv - pv
            fee=(tv-pv)/tv
            gain=pos*nxt
            d=pd.DataFrame({"coin":coin,"w":w,"regime":b["regime"],"vsr":vsr,"nxt":nxt,"tr60":tr60,
                            "pos":pos,"gain":gain,"fee":fee,"fc":b["forecast"],"sd":sd,
                            "year":pd.to_datetime(b["timestamp"]).dt.year,"i":np.arange(len(b)),
                            "chg":(pos-b["previous_allocation"]).abs()})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    drift=D.groupby("coin")["nxt"].mean()
    D["ex"]=D["nxt"]-D["coin"].map(drift)
    out={}
    D["agit"]=np.where(D["regime"]=="chop","calm","agit")
    D["vb"]=pd.cut(D["vsr"],[-10,-1,-0.5,0,0.25,0.5,0.75,1,1.5,2,10])
    g=D.dropna(subset=["vb","nxt"]).groupby(["agit","vb"],observed=True)["ex"]
    out["ex by agit x vsr bucket"]=pd.DataFrame({"n":g.size(),"mean":g.mean(),"t":g.mean()/(g.std()/np.sqrt(g.size()))})
    A=D[D.pos.abs()>1e-9].dropna(subset=["nxt"])
    out["in position: n, mean gain, mean fee, mean |pos|, share short"]=pd.Series({"n":len(A),"gain":A.gain.mean(),"fee_all_bars":D.fee.mean(),"abspos":A.pos.abs().mean(),"short":(A.pos<0).mean()})
    A=A.copy(); A["tb"]=pd.cut(A.tr60,[-5,-0.1,0.1,50])
    g=A.groupby("tb",observed=True)
    out["pos gain by trend"]=pd.DataFrame({"n":g.size(),"gain":g.gain.mean(),"ex_short":-g.ex.mean(),"fee":g.fee.mean()})
    g=A.groupby("vb",observed=True)
    out["pos gain by vsr bucket"]=pd.DataFrame({"n":g.size(),"gain":g.gain.mean(),"ex_short":-g.ex.mean(),"abspos":g.pos.apply(lambda x:x.abs().mean())})
    g=A.groupby("year")
    out["pos gain by year"]=pd.DataFrame({"n":g.size(),"gain":g.gain.mean(),"raw_short":-g.nxt.mean()})
    # holding duration: consecutive in-position bars
    D["inpos"]=D.pos.abs()>1e-9
    out["share of position bars where regime is mean_reversion"]=float((D[D.inpos].regime=="mean_reversion").mean())
    g=D[D.inpos].groupby("regime")
    out["pos bars by regime"]=pd.DataFrame({"n":g.size(),"gain":g.gain.mean()})
    out["fee per unit change"]=float(D.fee.sum()/ (D.chg.sum()+1e-12))
    # mean_reversion bars: next day short excess by trend
    M=D[(D.regime=="mean_reversion")].dropna(subset=["nxt","tr60"]).copy()
    M["tb"]=pd.cut(M.tr60,[-5,-0.1,0.1,50])
    g=M.groupby("tb",observed=True)
    out["MR bars short ex by trend"]=pd.DataFrame({"n":g.size(),"ex_short":-g.ex.mean(),"t":-g.ex.mean()/(g.ex.std()/np.sqrt(g.size()))})
    return out
