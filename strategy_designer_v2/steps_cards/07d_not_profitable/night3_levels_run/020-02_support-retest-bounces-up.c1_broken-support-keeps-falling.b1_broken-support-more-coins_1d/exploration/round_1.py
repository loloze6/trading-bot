import pandas as pd, numpy as np
from scipy import stats

def explore(data):
    bars=data["bars"]; days=data["days"]
    # coin mean daily return over all windows
    rows=[]; grid=[]
    for c in bars:
        allret=pd.concat([days[c][w]["coin_return"] for w in days[c]]).dropna()
        mu=allret.mean()
        for w in bars[c]:
            b=bars[c][w].reset_index(drop=True)
            d=days[c][w]
            pos=b["postRebalance_current_allocation"]
            nxt=b["close"].shift(-1)/b["close"]-1
            gain=(pos*nxt)
            rows.append(dict(coin=c,win=w,n=len(b),short_share=(pos<-1e-6).mean(),
                             mean_pos=pos.mean(),gain=gain.mean(),drift_part=(pos*mu).mean(),
                             book=d["book_return"].mean()))
            # grid 5 bars with situation measures
            cl=b["close"]
            r90=cl/cl.shift(90)-1
            r20=cl/cl.shift(20)-1
            fwd=cl.shift(-5)/cl-1
            for i in range(0,len(b)-5,5):
                grid.append(dict(coin=c,win=w,f=b["forecast"].iloc[i],fwd=fwd.iloc[i],
                                 r20=r20.iloc[i],pos=pos.iloc[i]))
    R=pd.DataFrame(rows); G=pd.DataFrame(grid)
    G["mu5"]=G.groupby("coin")["fwd"].transform("mean")
    G["ex"]=G["fwd"]-G["mu5"]
    out={}
    out["book_overall"]=pd.Series(dict(short_share=(R.short_share*R.n).sum()/R.n.sum(),
        mean_pos=(R.mean_pos*R.n).sum()/R.n.sum(),gain=(R.gain*R.n).sum()/R.n.sum(),
        drift_part=(R.drift_part*R.n).sum()/R.n.sum(),book=(R.book*R.n).sum()/R.n.sum()))
    R["wn"]=R.win.str[1:].astype(int)
    out["by_window"]=R.groupby("wn").apply(lambda x: pd.Series(dict(book=(x.book*x.n).sum()/x.n.sum(),drift=(x.drift_part*x.n).sum()/x.n.sum(),short=(x.short_share*x.n).sum()/x.n.sum()))).round(5)
    act=G[G.f<0].copy()
    act["fq"]=pd.qcut(act.f.rank(method="first"),5,labels=False)
    out["by_forecast_q"]=act.groupby("fq").agg(n=("ex","size"),f=("f","mean"),ex=("ex","mean"),fwd=("fwd","mean"))
    act=act.dropna(subset=["r20"])
    act["tq"]=pd.qcut(act.r20.rank(method="first"),5,labels=False)
    out["by_r20_q_active"]=act.groupby("tq").agg(n=("ex","size"),r20=("r20","mean"),ex=("ex","mean"),fwd=("fwd","mean"))
    flat=G[G.f==0].dropna(subset=["r20"]).copy()
    flat["tq"]=pd.qcut(flat.r20.rank(method="first"),5,labels=False)
    out["by_r20_q_flat"]=flat.groupby("tq").agg(n=("ex","size"),r20=("r20","mean"),ex=("ex","mean"))
    # within downtrend: slope of ex on f
    res={}
    for name,sub in [("r20<0",act[act.r20<0]),("r20>=0",act[act.r20>=0])]:
        s=stats.linregress(sub.f,sub.ex); res[name]=pd.Series(dict(n=len(sub),slope=s.slope,t=s.slope/s.stderr,meanex=sub.ex.mean(),meanfwd=sub.fwd.mean()))
    out["slope_by_trend"]=pd.DataFrame(res)
    out["by_coin"]=R.groupby("coin").apply(lambda x: pd.Series(dict(book=(x.book*x.n).sum()/x.n.sum(),drift=(x.drift_part*x.n).sum()/x.n.sum()))).round(5)
    return out
