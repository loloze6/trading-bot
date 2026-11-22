import pandas as pd, numpy as np

def explore(data):
    rows=[]
    for coin in data["bars"]:
        for w,b in data["bars"][coin].items():
            b=b.reset_index(drop=True)
            c=b["close"]; r1=c.pct_change(); vol=r1.rolling(20).std(); z=r1/vol
            r90=c/c.shift(90)-1
            f1=c.shift(-1)/c-1
            a=b["postRebalance_current_allocation"]
            fee=(b["total_portfolio_value"]-b["postRebalance_total_value"])/b["total_portfolio_value"]
            # bars since last bar with z>1 while r90<0
            sig=((z>1)&(r90<0)).astype(int)
            last=pd.Series(np.where(sig==1,np.arange(len(b)),np.nan)).ffill()
            since=np.arange(len(b))-last
            d=pd.DataFrame({"coin":coin,"w":w,"z":z,"r90":r90,"f1":f1,"a":a,"pnl":a*f1,"fee":fee,
                            "since":since,"turn":(a-b["previous_allocation"]).abs(),"vol":vol})
            rows.append(d)
    D=pd.concat(rows)
    out={}
    A=D[D.a<0].copy()
    A["zb"]=pd.cut(A.z,[-50,0,0.5,1,1.5,2,50])
    g=A.groupby("zb",observed=True)
    out["active short bars by today's z"]=pd.DataFrame({"n":g.size(),"mean a":g.a.mean(),"sum pnl":g.pnl.sum(),
        "mean pnl":g.pnl.mean(),"sum fee":g.fee.sum(),"t":g.pnl.apply(lambda x:x.mean()/x.std()*np.sqrt(len(x)))})
    A["sb"]=pd.cut(A.since,[-1,0,1,2,4,10,1000])
    g=A.groupby("sb",observed=True)
    out["active short bars by days since z>1 bounce"]=pd.DataFrame({"n":g.size(),"mean a":g.a.mean(),
        "sum pnl":g.pnl.sum(),"mean pnl":g.pnl.mean(),"sum fee":g.fee.sum()})
    out["totals"]=pd.Series({"sum pnl all":D.pnl.sum(),"sum fee all":D.fee.sum(),
        "sum turnover":D.turn.sum(),"fee per turnover":D.fee.sum()/D.turn.sum()})
    # next-day ex move after z>1 bounce by z of next day (does second day continue?)
    S=D[(D.since==1)&(D.r90<0)]
    S=S.copy(); S["zb"]=pd.cut(S.z,[-50,-1,0,1,50])
    g=S.groupby("zb",observed=True)
    out["day after bounce: next-day -f1 by that day's z"]=pd.DataFrame({"n":g.size(),"-f1":-g.f1.mean(),"mean a":g.a.mean()})
    return out
