import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    rows=[]
    for c,ws in data["bars"].items():
        for w,b in ws.items():
            b=b.copy()
            cl=b["close"].astype(float)
            r=cl.pct_change()
            nxt=cl.shift(-1)/cl-1
            a=b["postRebalance_current_allocation"].astype(float)
            pa=b["previous_allocation"].astype(float)
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            z=r/r.rolling(20).std()
            vol720=r.rolling(720).std()
            hr=pd.to_datetime(b["timestamp"]).dt.hour
            d=pd.DataFrame({"coin":c,"win":w,"gross":a*nxt,"fee":fee,"turn":(a-pa).abs(),
                            "absz":z.abs(),"r":r,"nxt":nxt,"vol720":vol720,"hour":hr,"absa":a.abs()})
            rows.append(d)
    D=pd.concat(rows,ignore_index=True)
    D["net"]=D["gross"]-D["fee"]
    out={}
    out["per_bar_totals"]=pd.Series({"gross_mean":D.gross.mean(),"fee_mean":D.fee.mean(),"net_mean":D.net.mean(),
        "turn_mean":D.turn.mean(),"absalloc_mean":D.absa.mean(),
        "fee_per_turn":D.fee.sum()/D.turn.sum(),"gross_per_turn":D.gross.sum()/D.turn.sum()})
    D["zb"]=pd.qcut(D.absz,5,labels=False,duplicates="drop")
    g=D.groupby("zb")
    out["by_absz_quintile"]=pd.DataFrame({"n":g.size(),"gross":g.gross.mean(),"fee":g.fee.mean(),"net":g.net.mean(),
        "turn":g.turn.mean(),"t_gross":g.gross.mean()/(g.gross.std()/np.sqrt(g.size()))})
    # reversal at longer horizons, non-overlapping grids
    res=[]
    for h in [1,2,4,8,24]:
        xs=[];ys=[]
        for c,ws in data["bars"].items():
            for w,b in ws.items():
                cl=b["close"].astype(float).values
                idx=np.arange(h,len(cl)-h,h)
                past=cl[idx]/cl[idx-h]-1; fut=cl[idx+h]/cl[idx]-1
                sd=np.nanstd(np.diff(np.log(cl)))*np.sqrt(h)
                xs.append(past/sd); ys.append(fut/sd)
        x=np.concatenate(xs);y=np.concatenate(ys)
        m=np.isfinite(x)&np.isfinite(y)
        rr,p=stats.pearsonr(x[m],y[m])
        gain=-np.sign(x[m])*y[m]
        res.append({"h_hours":h,"n":m.sum(),"corr":rr,"fade_mean_sdunits":gain.mean(),"t":gain.mean()/(gain.std()/np.sqrt(m.sum()))})
    out["reversal_by_horizon"]=pd.DataFrame(res)
    gc=D.groupby("coin")
    out["by_coin"]=pd.DataFrame({"gross":gc.gross.mean(),"fee":gc.fee.mean(),"turn":gc.turn.mean()})
    D["vb"]=D.groupby("coin").vol720.transform(lambda s: s>s.median())
    gv=D[D.vol720.notna()].groupby("vb")
    out["by_vol"]=pd.DataFrame({"gross":gv.gross.mean(),"fee":gv.fee.mean(),"net":gv.net.mean()})
    dd=[]
    for c,ws in data["days"].items():
        for w,x in ws.items(): dd.append(x["book_return"])
    dr=pd.concat(dd).dropna()
    out["daily"]=pd.Series({"mean":dr.mean(),"n":len(dr)})
    return out
